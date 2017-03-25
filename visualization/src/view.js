import $ from "jquery";
import md5 from "md5";
import * as THREE from "three";
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
			//this.showArrow(arrowData);
		});
		controller.on('score', () => {
			//this.updateOpenedTooltip();
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

		$("#find-team-wrapper").find("input").on("keyup paste", function () {
			const text = $(this).val().toLowerCase();
		});

		this.initThree(this.model.teams);
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

	initThree(teams) {
		const $container = $("#container");
		let SCREEN_WIDTH = $container.width();
		let SCREEN_HEIGHT = $container.height();
		let aspect = SCREEN_WIDTH / SCREEN_HEIGHT;

		let camera, scene;
		let renderer;
		let planetGroup;

		const clock = new THREE.Clock();
		let lon = 0, lat = 0;
		let phi = 0, theta = 0;

		let onPointerDownPointerX, onPointerDownPointerY, onPointerDownLon, onPointerDownLat;

		init();
		animate();

		function init() {
			camera = new THREE.PerspectiveCamera(60, aspect, 1, 1000);
			camera.position.set(0, 0, 100);

			scene = new THREE.Scene();

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

			planetGroup = new THREE.Object3D();

			const sphere = new THREE.Mesh(new THREE.IcosahedronBufferGeometry(40, 5), new THREE.MeshLambertMaterial({color: 0xFF0000}));
			sphere.castShadow = true;
			sphere.position.set(0, 0, 0);
			sphere.receiveShadow = true;
			planetGroup.add(sphere);

			let nodes_points = [];
			let samplesCount = teams.length;
			while (nodes_points.length < teams.length) {
				nodes_points = fibonacci_sphere(samplesCount);
				nodes_points = nodes_points.filter(p => p[1] >= -0.5 && p[1] <= 0.5);
				samplesCount++;
			}
			if (nodes_points.length > teams.length)
				nodes_points = nodes_points.slice(0, teams.length);

			const nodes = [];
			for(let i=0; i<nodes_points.length; i++) {
				const node = genNode();
				node.castShadow = true;
				node.receiveShadow = true;
				node.position.set(nodes_points[i][0] * 43, nodes_points[i][1] * 43, nodes_points[i][2] * 43);
				let myDirectionVector = new THREE.Vector3(nodes_points[i][0], nodes_points[i][1], nodes_points[i][2]);
				let mx = new THREE.Matrix4().lookAt(new THREE.Vector3(0,0,0), myDirectionVector, new THREE.Vector3(0,1,0));
				let qt = new THREE.Quaternion().setFromRotationMatrix(mx);
				node.quaternion.copy(qt);
				nodes.push(node);
				planetGroup.add(node);

				const spritey = makeTextSprite( " c00kies@venice ",
					{ fontsize: 24, borderColor: {r:255, g:0, b:0, a:1.0}, backgroundColor: {r:255, g:100, b:100, a:0.8} } );
				spritey.position.set(nodes_points[i][0] * 50, nodes_points[i][1] * 50, nodes_points[i][2] * 50);
				planetGroup.add(spritey);
			}

			scene.add(planetGroup);

			scene.updateMatrixWorld(true); // Координаты вершин должны рассчитаться для рассчета координат стрелок
			const pos0 = new THREE.Vector3();
			pos0.setFromMatrixPosition(nodes[0].matrixWorld);
			const pos1 = new THREE.Vector3();
			pos1.setFromMatrixPosition(nodes[1].matrixWorld);
			const spline_points = getSplinePoints(pos0.normalize().multiplyScalar(44), pos1.normalize().multiplyScalar(44));
			getLine(spline_points);

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

		function getLine(points) {
			const spline = new THREE.CatmullRomCurve3(points);
			const geometry = new THREE.Geometry();
			const colors = [];
			const stepsCount = 100;
			for (let i = 0; i < stepsCount; i++) {
				const index = i / stepsCount;
				const position = spline.getPoint(index);
				geometry.vertices[i] = new THREE.Vector3(position.x, position.y, position.z);
				colors[i] = new THREE.Color(0xffffff);
				colors[i].setHSL(1.0, 1.0, index);
			}
			geometry.colors = colors;

			const customMaterial = new THREE.ShaderMaterial(
				{
					uniforms:
						{
							"c":   { type: "f", value: 0 },
							"p":   { type: "f", value: 0.2 },
							glowColor: { type: "c", value: new THREE.Color(0x78782f) },
							viewVector: { type: "v3", value: camera.position }
						},
					vertexShader:   document.getElementById( 'vertexShader'   ).textContent,
					fragmentShader: document.getElementById( 'fragmentShader' ).textContent,
					side: THREE.FrontSide,
					blending: THREE.AdditiveBlending,
					transparent: true
				});

			const lineGlow = new THREE.Mesh(new THREE.TubeBufferGeometry(spline, 200, 0.4, 5, false), customMaterial.clone() );
			planetGroup.add(lineGlow);

			window.lineGlow = lineGlow;
		}

		function getSplinePoints(pos0, pos1) {
			const result = [pos0];
			result.push(pos0.clone().normalize().multiplyScalar(46).add(pos1.clone().normalize()));
			result.push(new THREE.Vector3(0.01, 0, 0).add(pos0).add(pos1).normalize().multiplyScalar(46));
			result.push(pos1.clone().normalize().multiplyScalar(46).add(pos0.clone().normalize()));
			result.push(pos1);
			return result;
		}

		function makeTextSprite( message, parameters )
		{
			if ( parameters === undefined ) parameters = {};

			var fontface = parameters.hasOwnProperty("fontface") ?
				parameters["fontface"] : "Arial";

			var fontsize = parameters.hasOwnProperty("fontsize") ?
				parameters["fontsize"] : 18;

			var borderThickness = parameters.hasOwnProperty("borderThickness") ?
				parameters["borderThickness"] : 4;

			var borderColor = parameters.hasOwnProperty("borderColor") ?
				parameters["borderColor"] : { r:0, g:0, b:0, a:1.0 };

			var backgroundColor = parameters.hasOwnProperty("backgroundColor") ?
				parameters["backgroundColor"] : { r:255, g:255, b:255, a:1.0 };


			var canvas = document.createElement('canvas');
			var context = canvas.getContext('2d');
			context.font = "Bold " + fontsize + "px " + fontface;

			// get size data (height depends only on font size)
			var metrics = context.measureText( message );
			var textWidth = metrics.width;

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
			var texture = new THREE.Texture(canvas);
			texture.needsUpdate = true;

			var spriteMaterial = new THREE.SpriteMaterial(
				{ map: texture } );
			var sprite = new THREE.Sprite( spriteMaterial );
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
			requestAnimationFrame(animate);
			render();
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
			planetGroup.rotateY(delta / 3);
			renderer.render(scene, camera);
		}
	}
}