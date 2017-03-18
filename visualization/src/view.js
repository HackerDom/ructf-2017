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

	initThree() {
		var SCREEN_WIDTH = window.innerWidth - 100;
		var SCREEN_HEIGHT = window.innerHeight - 100;

		var camera, scene;
		var canvasRenderer, webglRenderer;

		var container, mesh, geometry, plane;

		var windowHalfX = window.innerWidth / 2;
		var windowHalfY = window.innerHeight / 2;
		var lon = 0, lat = 0;
		var phi = 0, theta = 0;

		var aspect = SCREEN_WIDTH / SCREEN_HEIGHT;
		var onPointerDownPointerX, onPointerDownPointerY, onPointerDownLon, onPointerDownLat;

		init();
		animate();

		function init() {

			container = document.createElement('div');
			document.body.appendChild(container);

			camera = new THREE.PerspectiveCamera( 60, aspect, 1, 1000 );

			scene = new THREE.Scene();


			var ambient = 0xf4f4f4;
			var groundMaterial = new THREE.MeshLambertMaterial({
				color: 0xFF0000,
				// map: texture
				// ambient: ambient
			});
			// LIGHTS
			scene.add(new THREE.AmbientLight(0x666666));

			var light;

			light = new THREE.SpotLight(0xdfebff, 1);
			light.position.set(50, 0, 0);


			light.castShadow = true;
			light.shadowCameraVisible = true;

// ------------------------------------------------------------------------------------

// custom shadow frustum
			light.shadow = new THREE.LightShadow( new THREE.PerspectiveCamera( 50, aspect, 1, 20 ) );

// shadow camera helper
			light.shadowCameraHelper = new THREE.CameraHelper( light.shadow.camera );
			scene.add( light.shadowCameraHelper );

// ------------------------------------------------------------------------------------



			const group = new THREE.Object3D();

			var sphere = new THREE.Mesh( new THREE.IcosahedronBufferGeometry( 40, 3 ), new THREE.MeshLambertMaterial( { color: 0xFF0000 } ) );
			sphere.castShadow = false;
			sphere.position.set(0, 0, 0);
			sphere.receiveShadow = true;
			group.add(sphere);

			var cube = genNode();
			cube.castShadow = true;
			cube.position.set( 42, 0, 0 );

			group.add(cube);
			group.add(light);
			scene.add(group);

			// RENDERER
			webglRenderer = new THREE.WebGLRenderer({ alpha: true });
			webglRenderer.setSize(SCREEN_WIDTH, SCREEN_HEIGHT);
			webglRenderer.domElement.style.position = "relative";
			webglRenderer.shadowMapEnabled = true;
			webglRenderer.shadowMapSoft = true;

			container.appendChild(webglRenderer.domElement);
			window.addEventListener( 'resize', onWindowResized, false );
			document.addEventListener( 'mousedown', onDocumentMouseDown, false );
			document.addEventListener( 'wheel', onDocumentMouseWheel, false );

		}

		function genNode() {
			const geometry = new THREE.Geometry();
			const ISLAND_WIDTH = 5;
			const ISLAND_HEIGHT = ISLAND_WIDTH * 0.866; // sqrt(3)/2
			const fig = [{x: ISLAND_WIDTH / 4 , y: 0},
				{x: ISLAND_WIDTH * 3 / 4, y: 0},
				{x: ISLAND_WIDTH, y: ISLAND_HEIGHT / 2},
				{x: ISLAND_WIDTH * 3 / 4, y: ISLAND_HEIGHT},
				{x: ISLAND_WIDTH / 4 , y: ISLAND_HEIGHT},
				{x: 0, y: ISLAND_HEIGHT / 2}];
			for (let i=0; i<fig.length; i++)
				geometry.vertices.push(new THREE.Vector3(-1, fig[i].x - ISLAND_WIDTH / 2, fig[i].y - ISLAND_HEIGHT / 2 ));
			for (let i=0; i<fig.length; i++)
				geometry.vertices.push(new THREE.Vector3(1, fig[i].x  - ISLAND_WIDTH / 2, fig[i].y - ISLAND_HEIGHT / 2 ));
			const faces1 = [[0,5,1],[1,3,2],[3,5,4],[1,5,3]];
			const faces2 = [[0,1,5],[1,2,3],[3,4,5],[1,3,5]];
			for (let i=0; i<faces1.length; i++)
				geometry.faces.push( new THREE.Face3(faces1[i][0], faces1[i][1], faces1[i][2] ) );
			for (let i=0; i<faces2.length; i++)
				geometry.faces.push( new THREE.Face3(faces2[i][0] + 6, faces2[i][1] + 6, faces2[i][2] + 6 ) );
			const borders = [[0,7,6],[1,8,7],[2,9,8],[3,10,9],[4,11,10],[5,6,11],
				[0,1,7],[1,2,8],[2,3,9],[3,4,10],[4,5,11],[5,0,6]];
			for (let i=0; i<borders.length; i++)
				geometry.faces.push( new THREE.Face3(borders[i][0], borders[i][1], borders[i][2] ) );
			geometry.computeVertexNormals();
			return new THREE.Mesh(geometry, new THREE.MeshLambertMaterial( { color: 0xff0000 } ) );
		}

		function onWindowResized() {
			renderer.setSize(window.innerWidth - 1, window.innerHeight - 1 );
			camera.aspect = (window.innerWidth - 1) / (window.innerHeight - 1);
			camera.updateProjectionMatrix();
		}
		function onDocumentMouseDown( event ) {
			event.preventDefault();
			onPointerDownPointerX = event.clientX;
			onPointerDownPointerY = event.clientY;
			onPointerDownLon = lon;
			onPointerDownLat = lat;
			document.addEventListener( 'mousemove', onDocumentMouseMove, false );
			document.addEventListener( 'mouseup', onDocumentMouseUp, false );
		}
		function onDocumentMouseMove( event ) {
			lon = ( event.clientX - onPointerDownPointerX ) * 0.1 + onPointerDownLon;
			lat = ( event.clientY - onPointerDownPointerY ) * 0.1 + onPointerDownLat;
		}
		function onDocumentMouseUp( event ) {
			document.removeEventListener( 'mousemove', onDocumentMouseMove, false );
			document.removeEventListener( 'mouseup', onDocumentMouseUp, false );
		}
		function onDocumentMouseWheel( event ) {
			camera.fov += ( event.deltaY * 0.05 );
			camera.updateProjectionMatrix();
		}

		function animate() {
			requestAnimationFrame( animate );
			render();
		}
		function render() {
			//var time = Date.now();
			//lon = 20;
			lat = Math.max( - 85, Math.min( 85, lat ) );
			phi = THREE.Math.degToRad( 90 - lat );
			theta = THREE.Math.degToRad( lon );
			camera.position.x = 100 * Math.sin( phi ) * Math.cos( theta );
			camera.position.y = 100 * Math.cos( phi );
			camera.position.z = 100 * Math.sin( phi ) * Math.sin( theta );
			camera.lookAt( scene.position );
			webglRenderer.render( scene, camera );
		}

	}
}