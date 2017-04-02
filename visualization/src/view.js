import $ from "jquery";
import md5 from "md5";
import * as THREE from "three";
import * as THREE_particle from "./particle";
import Stats from "stats.js";


export default class View {

	constructor(controller) {
		this.controller = controller;
		this.model = null;

		controller.on('start', m => {
			this.model = m;
			this.init();
		});
		controller.on('showArrow', arrowData => {
			this.showArrow(arrowData);
		});
		controller.on('score', () => {
			// NONE
		});
		controller.on('servicesStatuses', () => {
			this.drawServicesStatusesAndStat();
		});
		controller.on('flagStat', () => {
			$("#attacks").find(".value").text(this.model.flagsCount);
		});
	}

	init() {
		this.createFilterPanel();

		this.initThree();
	}

	drawServicesStatusesAndStat() {
		const _this = this;
		let teamsWithAliveService = 0; // количество команд с хотя бы 1 сервисом
		this.model.teams.forEach(function (nData) {
			let hasUp = false;
			for (let i = 0; i < _this.model.services.length; i++) {
				const isUp = _this.model.services[i].visible && nData.servicesStatuses[i];
				hasUp = hasUp || isUp;
			}
			if (hasUp)
				teamsWithAliveService++;
		});
		$("#alive").find(".value").text(teamsWithAliveService);
	}

	static getLogo(nodeData) {
		return "<img src='https://ructfe.org/logos/" + md5(nodeData.name ) + ".png'/>";
	}

	createFilterPanel() {
		const _this = this;
		const deselectionFlag = "deselected";
		const $fc = $("#filters-container");

		for (let i=0; i<this.model.services.length; i++) {
			const service = this.model.services[i];
			const $filter = $(`<div class="filter"><span class="bullet">&#9679;&ensp;&thinsp;</span><span class="service-name">${service.name}</span></div>`);
			$filter.css("color", "#B7E99B");
			$filter.find(".bullet").css("color", service.color);
			$filter.click( function(index) { return function () {
				if ($(this).hasClass(deselectionFlag)) {
					$(this).removeClass(deselectionFlag);
					_this.model.services[index].visible = true;
				} else {
					$(this).addClass(deselectionFlag);
					_this.model.services[index].visible = false;
				}
				_this.drawServicesStatusesAndStat();
				_this.controller.emit('calcFlagStat');
			};
			}(i));
			$fc.append($filter);
		}
	}

	showArrow(arrowData) {
		if(!arrowData.svc.visible)
			return;
		const posFrom = arrowData.from.pos.clone();
		const posTo = arrowData.to.pos.clone();
		const spline_points = View.getSplinePoints(posFrom.normalize().multiplyScalar(44), posTo.normalize().multiplyScalar(44));
		this.createArrow(spline_points, arrowData.svc.color);
	}

	createArrow(points, color) {
		const particleSystem = new THREE_particle.GPUParticleSystem({
			maxParticles: 10000,
			particleSpriteTex: this.particleSpriteTex
		});
		const spline = new THREE.CatmullRomCurve3(points);
		this.planetGroup.add(particleSystem);
		const arrow = {
			particleSystem,
			spline,
			timer: 0,
			color: new THREE.Color(color)
		};
		this.arrows.push(arrow);
	}

	static getSplinePoints(pos0, pos1) {
		const result = [pos0];
		result.push(pos0.clone().normalize().multiplyScalar(46).add(pos1.clone().normalize()));
		result.push(new THREE.Vector3(0.01, 0, 0).add(pos0).add(pos1).normalize().multiplyScalar(46));
		result.push(pos1.clone().normalize().multiplyScalar(46).add(pos0.clone().normalize()));
		result.push(pos1);
		return result;
	}

	initThree() {
		const teams = this.model.teams;
		const $container = $("#container");
		let SCREEN_WIDTH = $container.width();
		let SCREEN_HEIGHT = $container.height();
		let aspect = SCREEN_WIDTH / SCREEN_HEIGHT;

		let camera;
		let renderer;
		const planetGroup = new THREE.Object3D();
		this.planetGroup = planetGroup;
		const scene = new THREE.Scene();
		this.scene = scene;

		const clock = new THREE.Clock();
		let lon = 0, lat = 0;
		let phi = 0, theta = 0;

		let onPointerDownPointerX, onPointerDownPointerY, onPointerDownLon, onPointerDownLat;

		const textureLoader = new THREE.TextureLoader();
		this.particleSpriteTex = textureLoader.load("static/img/particle2.png");
		const planetTex = textureLoader.load("static/img/planet.jpg");

		const options = {
			position: new THREE.Vector3(),
			positionRandomness: 1.2,
			velocityRandomness: 0.43,
			colorRandomness: 0,
			turbulence: 0.5,
			lifetime: 0.5,
			size: 6,
			sizeRandomness: 3
		};

		const spawnerOptions = {
			spawnRate: 4000
		};

		this.arrows = [];
		const _this = this;

		const stats = new Stats();
		stats.showPanel( 0 ); // 0: fps, 1: ms, 2: mb, 3+: custom
		$("#stats-container").append(stats.dom);

		init();
		animate();

		function init() {
			camera = new THREE.PerspectiveCamera(60, aspect, 1, 1000);
			camera.position.set(0, 0, 100);

			const light = new THREE.DirectionalLight(0xdfebff, 1);
			light.position.set(75, 20, 60);
			light.shadow.mapSize.width = 2048; // default is 512
			light.shadow.mapSize.height = 2048; // default is 512
			light.castShadow = true;
			light.shadow.camera.left = -80;
			light.shadow.camera.right = 80;
			light.shadow.camera.top = 80;
			light.shadow.camera.bottom = -80;
			light.shadowCameraHelper = new THREE.CameraHelper(light.shadow.camera);
			scene.add(light);
			scene.add(light.shadowCameraHelper);

			scene.add(new THREE.AmbientLight(0x666666));

			const sphere = new THREE.Mesh(new THREE.IcosahedronBufferGeometry(40, 3), new THREE.MeshLambertMaterial({map: planetTex}));
			sphere.castShadow = true;
			sphere.position.set(0, 0, 0);
			sphere.receiveShadow = true;
			planetGroup.add(sphere);

			calculateNodesPositions();

			for(let i=0; i<teams.length; i++) {
				const team = teams[i];
				const node = genNode();
				node.castShadow = true;
				node.receiveShadow = true;
				const myDirectionVector = new THREE.Vector3(team.point[0], team.point[1], team.point[2]);
				const nodePosition = myDirectionVector.clone().multiplyScalar(43);
				node.position.set(nodePosition.x, nodePosition.y, nodePosition.z);
				let mx = new THREE.Matrix4().lookAt(new THREE.Vector3(0,0,0), myDirectionVector, new THREE.Vector3(0,1,0));
				let qt = new THREE.Quaternion().setFromRotationMatrix(mx);
				node.quaternion.copy(qt);
				team.node = node;
				team.pos = nodePosition;
				planetGroup.add(node);

				const spritey = makeTextSprite( " " + team.name + " ",
					{ fontsize: 24, borderColor: {r:255, g:0, b:0, a:1.0}, backgroundColor: {r:255, g:100, b:100, a:0.8} } );
				const spriteyPosition = myDirectionVector.clone().multiplyScalar(50);
				spritey.position.set(spriteyPosition.x, spriteyPosition.y, spriteyPosition.z);
				planetGroup.add(spritey);
			}

			scene.add(planetGroup);

			const axes = new THREE.AxisHelper(100);
			scene.add(axes);

			renderer = new THREE.WebGLRenderer({alpha: true, antialias: true});
			renderer.setSize(SCREEN_WIDTH, SCREEN_HEIGHT);
			renderer.shadowMap.enabled = true;

			$container.append(renderer.domElement);
			window.addEventListener('resize', onWindowResized, false);
			document.addEventListener('mousedown', onDocumentMouseDown, false);
			document.addEventListener('wheel', onDocumentMouseWheel, false);
		}

		function calculateNodesPositions() {
			let nodes_points = [];
			let samplesCount = teams.length;
			while (nodes_points.length < teams.length) {
				nodes_points = fibonacci_sphere(samplesCount);
				nodes_points = nodes_points.filter(p => p[1] >= -0.5 && p[1] <= 0.5);
				samplesCount++;
			}
			if (nodes_points.length > teams.length)
				nodes_points = nodes_points.slice(0, teams.length);
			for(let i=0; i<nodes_points.length; i++)
				teams[i].point = nodes_points[i];
		}

		function genNode() {
			const geometry = new THREE.Geometry();
			const ISLAND_WIDTH = 8;
			const ISLAND_HEIGHT = ISLAND_WIDTH * 0.866; // sqrt(3)/2
			const fig = [{x: ISLAND_WIDTH / 4 , y: 0},
				{x: ISLAND_WIDTH * 3 / 4, y: 0},
				{x: ISLAND_WIDTH, y: ISLAND_HEIGHT / 2},
				{x: ISLAND_WIDTH * 3 / 4, y: ISLAND_HEIGHT},
				{x: ISLAND_WIDTH / 4 , y: ISLAND_HEIGHT},
				{x: 0, y: ISLAND_HEIGHT / 2}];
			for (let i=0; i<fig.length; i++)
				geometry.vertices.push(new THREE.Vector3(fig[i].x - ISLAND_WIDTH / 2, fig[i].y - ISLAND_HEIGHT / 2, -1));
			for (let i=0; i<fig.length; i++)
				geometry.vertices.push(new THREE.Vector3(fig[i].x  - ISLAND_WIDTH / 2, fig[i].y - ISLAND_HEIGHT / 2, 1));
			const faces1 = [[0,5,1],[1,3,2],[3,5,4],[1,5,3]];
			const faces2 = [[0,1,5],[1,2,3],[3,4,5],[1,3,5]];
			for (let i=0; i<faces1.length; i++)
				geometry.faces.push(new THREE.Face3(faces1[i][0], faces1[i][1], faces1[i][2]));
			for (let i=0; i<faces2.length; i++)
				geometry.faces.push(new THREE.Face3(faces2[i][0] + 6, faces2[i][1] + 6, faces2[i][2] + 6));
			const borders = [[0,7,6],[1,8,7],[2,9,8],[3,10,9],[4,11,10],[5,6,11],
				[0,1,7],[1,2,8],[2,3,9],[3,4,10],[4,5,11],[5,0,6]];
			for (let i=0; i<borders.length; i++)
				geometry.faces.push(new THREE.Face3(borders[i][0], borders[i][1], borders[i][2]));
			geometry.computeVertexNormals();
			return new THREE.Mesh(geometry, new THREE.MeshLambertMaterial({color: 0x0000ff}));
		}

		function fibonacci_sphere(samples) { // http://stackoverflow.com/questions/9600801/evenly-distributing-n-points-on-a-sphere
			const rnd = 1;
			const points = [];
			const offset = 2. / samples;
			const increment = Math.PI * (3. - Math.sqrt(5.));

			for (let i = 0; i<samples; i++) {
				let y = ((i * offset) - 1) + (offset / 2);
				let r = Math.sqrt(1 - Math.pow(y, 2));

				let phi = ((i + rnd) % samples) * increment;

				let x = Math.cos(phi) * r;
				let z = Math.sin(phi) * r;

				points.push([x, y, z]);
			}
			return points;
		}


		function makeTextSprite( message, parameters )
		{
			if ( parameters === undefined ) parameters = {};

			const fontface = parameters.hasOwnProperty("fontface") ?
				parameters["fontface"] : "Arial";

			const fontsize = parameters.hasOwnProperty("fontsize") ?
				parameters["fontsize"] : 18;

			const borderThickness = parameters.hasOwnProperty("borderThickness") ?
				parameters["borderThickness"] : 4;

			const borderColor = parameters.hasOwnProperty("borderColor") ?
				parameters["borderColor"] : { r:0, g:0, b:0, a:1.0 };

			const backgroundColor = parameters.hasOwnProperty("backgroundColor") ?
				parameters["backgroundColor"] : { r:255, g:255, b:255, a:1.0 };


			const canvas = document.createElement('canvas');
			const context = canvas.getContext('2d');
			context.font = "Bold " + fontsize + "px " + fontface;

			// get size data (height depends only on font size)
			const metrics = context.measureText( message );
			const textWidth = metrics.width;

			// background color
			context.fillStyle   = "rgba(" + backgroundColor.r + "," + backgroundColor.g + ","
				+ backgroundColor.b + "," + backgroundColor.a + ")";
			// border color
			context.strokeStyle = "rgba(" + borderColor.r + "," + borderColor.g + ","
				+ borderColor.b + "," + borderColor.a + ")";

			context.lineWidth = borderThickness;
			roundRect(context, borderThickness/2, borderThickness/2, textWidth + borderThickness, fontsize * 1.4 + borderThickness, 6);
			// 1.4 is extra height factor for text below baseline: g,j,p,q.

			// text color
			context.fillStyle = "rgba(0, 0, 0, 1.0)";

			context.fillText( message, borderThickness, fontsize + borderThickness);

			// canvas contents will be used for a texture
			const texture = new THREE.Texture(canvas);
			texture.needsUpdate = true;

			const spriteMaterial = new THREE.SpriteMaterial(
				{ map: texture } );
			const sprite = new THREE.Sprite( spriteMaterial );
			sprite.scale.set(15,8,1.0);
			return sprite;
		}

		function roundRect(ctx, x, y, w, h, r)
		{
			ctx.beginPath();
			ctx.moveTo(x+r, y);
			ctx.lineTo(x+w-r, y);
			ctx.quadraticCurveTo(x+w, y, x+w, y+r);
			ctx.lineTo(x+w, y+h-r);
			ctx.quadraticCurveTo(x+w, y+h, x+w-r, y+h);
			ctx.lineTo(x+r, y+h);
			ctx.quadraticCurveTo(x, y+h, x, y+h-r);
			ctx.lineTo(x, y+r);
			ctx.quadraticCurveTo(x, y, x+r, y);
			ctx.closePath();
			ctx.fill();
			ctx.stroke();
		}

		function onWindowResized() {
			SCREEN_WIDTH = $container.width();
			SCREEN_HEIGHT = $container.height();
			renderer.setSize(SCREEN_WIDTH, SCREEN_HEIGHT);
			aspect = SCREEN_WIDTH / SCREEN_HEIGHT;
			camera.aspect = aspect;
			camera.updateProjectionMatrix();
		}

		function onDocumentMouseDown(event) {
			event.preventDefault();
			onPointerDownPointerX = event.clientX;
			onPointerDownPointerY = event.clientY;
			onPointerDownLon = lon;
			onPointerDownLat = lat;
			document.addEventListener('mousemove', onDocumentMouseMove, false);
			document.addEventListener('mouseup', onDocumentMouseUp, false);
		}

		function onDocumentMouseMove(event) {
			lon = (event.clientX - onPointerDownPointerX) * 0.1 + onPointerDownLon;
			lat = (event.clientY - onPointerDownPointerY) * 0.1 + onPointerDownLat;
		}

		function onDocumentMouseUp() {
			document.removeEventListener('mousemove', onDocumentMouseMove, false);
			document.removeEventListener('mouseup', onDocumentMouseUp, false);
		}

		function onDocumentMouseWheel(event) {
			const newFov = camera.fov + (event.deltaY * 0.05);
			if(newFov > 60 && newFov < 100)
				camera.fov = newFov;
			camera.updateProjectionMatrix();
		}

		function animate() {
			stats.begin();
			render();
			stats.end();
			requestAnimationFrame(animate);
		}

		function render() {
			lat = Math.max(-89, Math.min(89, lat));
			phi = THREE.Math.degToRad(lat - 90);
			theta = THREE.Math.degToRad(lon - 90);
			camera.position.x = 100 * Math.sin(phi) * Math.cos(theta);
			camera.position.y = 100 * Math.cos(phi);
			camera.position.z = 100 * Math.sin(phi) * Math.sin(theta);
			camera.lookAt(scene.position);
			const delta = clock.getDelta();
			planetGroup.rotateY(delta / 10);

			_this.arrows = _this.arrows.filter(function(a) {
				if(a.timer <= 1)
					return true;
				planetGroup.remove(a.particleSystem);
				return false;
			});
			for (let i = 0; i < _this.arrows.length; i++) {
				const arrow = _this.arrows[i];
				arrow.timer += delta / 3;
				if (delta > 0) {
					options.position = arrow.spline.getPoint(arrow.timer);
					options.color = arrow.color.getHex();
					for (let x = 0; x < spawnerOptions.spawnRate * delta; x++) {
						arrow.particleSystem.spawnParticle(options);
					}
				}
				arrow.particleSystem.update(arrow.timer);
			}

			renderer.render(scene, camera);
		}
	}
}