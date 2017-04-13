/*
 * GPU Particle System
 * @author flimshaw - Charlie Hoey - http://charliehoey.com
 *
 * A simple to use, general purpose GPU system. Particles are spawn-and-forget with
 * several options available, and do not require monitoring or cleanup after spawning.
 * Because the paths of all particles are completely deterministic once spawned, the scale
 * and direction of time is also variable.
 *
 * Currently uses a static wrapping perlin noise texture for turbulence, and a small png texture for
 * particles, but adding support for a particle texture atlas or changing to a different type of turbulence
 * would be a fairly light day's work.
 *
 * Shader and javascript packing code derrived from several Stack Overflow examples.
 *
 */

import * as THREE from "three";

export const GPUParticleSystem = function(options) {

	var self = this;
	options = options || {};

	// parse options and use defaults
	self.PARTICLE_COUNT = options.maxParticles || 1000000;
	self.PARTICLE_CONTAINERS = options.containerCount || 1;

	self.PARTICLE_SPRITE_TEXTURE = options.particleSpriteTex || null;

	self.PARTICLES_PER_CONTAINER = Math.ceil(self.PARTICLE_COUNT / self.PARTICLE_CONTAINERS);
	self.PARTICLE_CURSOR = 0;
	self.time = 0;


	// Custom vertex and fragement shader
	var GPUParticleShader = {

		vertexShader: [

			'uniform float uTime;',
			'uniform float uScale;',

			'attribute vec4 particlePositionsStartTime;',
			'attribute vec4 particleVelColSizeLife;',
			'attribute vec4 particleColor;',

			'varying vec4 vColor;',
			'varying float lifeLeft;',

			'void main() {',
				'vColor = particleColor / 255.0;',
				'float timeElapsed = uTime - particlePositionsStartTime.a;',
				'lifeLeft = 1. - (timeElapsed / particleVelColSizeLife.w);',
				'gl_PointSize = ( uScale * particleVelColSizeLife.z ) * lifeLeft;',
				'gl_Position = projectionMatrix * modelViewMatrix * vec4( particlePositionsStartTime.xyz, 1.0 );',
			'}'

		].join("\n"),

		fragmentShader: [

			'float scaleLinear(float value, vec2 valueDomain) {',
				'return (value - valueDomain.x) / (valueDomain.y - valueDomain.x);',
			'}',

			'float scaleLinear(float value, vec2 valueDomain, vec2 valueRange) {',
				'return mix(valueRange.x, valueRange.y, scaleLinear(value, valueDomain));',
			'}',

			'varying vec4 vColor;',
			'varying float lifeLeft;',
			'uniform sampler2D tSprite;',
			'void main() {',
				'float alpha = 0.;',
				'if( lifeLeft > .995 ) {',
					'alpha = scaleLinear( lifeLeft, vec2(1., .995), vec2(0., 1.));',
				'} else {',
					'alpha = lifeLeft * .75;',
				'}',
				'vec4 tex = texture2D( tSprite, gl_PointCoord );',
				'gl_FragColor = vec4( vColor.rgb * tex.a, alpha * tex.a );',
			'}'

		].join("\n")

	};

	// preload a million random numbers
	self.rand = [];

	for (var i = 1e5; i > 0; i--) {
		self.rand.push(Math.random() - .5);
	}

	self.random = function() {
		return ++i >= self.rand.length ? self.rand[i = 1] : self.rand[i];
	};

	self.particleSpriteTex = self.PARTICLE_SPRITE_TEXTURE;
	self.particleSpriteTex.wrapS = self.particleSpriteTex.wrapT = THREE.RepeatWrapping;

	self.particleShaderMat = new THREE.ShaderMaterial({
		transparent: true,
		depthWrite: false,
		uniforms: {
			"uTime": {
				value: 0.0
			},
			"uScale": {
				value: 1.0
			},
			"tSprite": {
				value: self.particleSpriteTex
			}
		},
		blending: THREE.AdditiveBlending,
		vertexShader: GPUParticleShader.vertexShader,
		fragmentShader: GPUParticleShader.fragmentShader
	});

	// define defaults for all values
	self.particleShaderMat.defaultAttributeValues.particlePositionsStartTime = [0, 0, 0, 0];
	self.particleShaderMat.defaultAttributeValues.particleVelColSizeLife = [0, 0, 0, 0];
	self.particleShaderMat.defaultAttributeValues.particleColor = [0, 0, 0, 0];

	self.particleContainers = [];


	// extend Object3D
	THREE.Object3D.apply(this, arguments);

	this.init = function() {

		for (var i = 0; i < self.PARTICLE_CONTAINERS; i++) {

			var c = new GPUParticleContainer(self.PARTICLES_PER_CONTAINER, self);
			self.particleContainers.push(c);
			self.add(c);

		}

	};

	this.spawnParticle = function(options) {

		self.PARTICLE_CURSOR++;
		if (self.PARTICLE_CURSOR >= self.PARTICLE_COUNT) {
			self.PARTICLE_CURSOR = 1;
		}

		var currentContainer = self.particleContainers[Math.floor(self.PARTICLE_CURSOR / self.PARTICLES_PER_CONTAINER)];

		currentContainer.spawnParticle(options);

	};

	this.update = function(time) {
		for (var i = 0; i < self.PARTICLE_CONTAINERS; i++) {

			self.particleContainers[i].update(time);

		}
	};

	this.dispose = function() {
		this.particleShaderMat.dispose();
		this.particleSpriteTex.dispose();

		for (let i = 0; i < this.PARTICLE_CONTAINERS; i++)
			this.particleContainers[ i ].dispose();
	};

	this.init();

};

GPUParticleSystem.prototype = Object.create(THREE.Object3D.prototype);
GPUParticleSystem.prototype.constructor = GPUParticleSystem;


// Subclass for particle containers, allows for very large arrays to be spread out
export const GPUParticleContainer = function(maxParticles, particleSystem) {

	var self = this;
	self.PARTICLE_COUNT = maxParticles || 100000;
	self.PARTICLE_CURSOR = 0;
	self.time = 0;
	self.DPR = window.devicePixelRatio;
	self.GPUParticleSystem = particleSystem;

	var particlesPerArray = Math.floor(self.PARTICLE_COUNT / self.MAX_ATTRIBUTES);

	// extend Object3D
	THREE.Object3D.apply(this, arguments);

	// construct a couple small arrays used for packing variables into floats etc
	var UINT8_VIEW = new Uint8Array(4);
	var FLOAT_VIEW = new Float32Array(UINT8_VIEW.buffer);

	function decodeFloat(x, y, z, w) {
		UINT8_VIEW[0] = Math.floor(w);
		UINT8_VIEW[1] = Math.floor(z);
		UINT8_VIEW[2] = Math.floor(y);
		UINT8_VIEW[3] = Math.floor(x);
		return FLOAT_VIEW[0];
	}

	function componentToHex(c) {
		var hex = c.toString(16);
		return hex.length == 1 ? "0" + hex : hex;
	}

	function rgbToHex(r, g, b) {
		return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
	}

	function hexToRgb(hex) {
		var r = hex >> 16;
		var g = (hex & 0x00FF00) >> 8;
		var b = hex & 0x0000FF;

		if (r > 0) r--;
		if (g > 0) g--;
		if (b > 0) b--;

		return [r, g, b];
	}

	self.particles = [];
	self.deadParticles = [];
	self.particlesAvailableSlot = [];

	// create a container for particles
	self.particleUpdate = false;

	// Shader Based Particle System
	self.particleShaderGeo = new THREE.BufferGeometry();

	// new hyper compressed attributes
	self.particleVertices = new Float32Array(self.PARTICLE_COUNT * 3); // position
	self.particlePositionsStartTime = new Float32Array(self.PARTICLE_COUNT * 4); // position
	self.particleVelColSizeLife = new Float32Array(self.PARTICLE_COUNT * 4);
	self.particleColor = new Float32Array(self.PARTICLE_COUNT * 4);

	for (var i = 0; i < self.PARTICLE_COUNT; i++) {
		self.particlePositionsStartTime[i * 4 + 0] = 100; //x

		self.particleVelColSizeLife[i * 4 + 2] = 1.0; //size
	}

	self.particleShaderGeo.addAttribute('position', new THREE.BufferAttribute(self.particleVertices, 3));
	self.particleShaderGeo.addAttribute('particlePositionsStartTime', new THREE.BufferAttribute(self.particlePositionsStartTime, 4).setDynamic(true));
	self.particleShaderGeo.addAttribute('particleVelColSizeLife', new THREE.BufferAttribute(self.particleVelColSizeLife, 4).setDynamic(true));
	self.particleShaderGeo.addAttribute('particleColor', new THREE.BufferAttribute(self.particleColor, 4).setDynamic(true));

	self.posStart = self.particleShaderGeo.getAttribute('particlePositionsStartTime');
	self.velCol = self.particleShaderGeo.getAttribute('particleVelColSizeLife');
	self.color = self.particleShaderGeo.getAttribute('particleColor');

	self.particleShaderMat = self.GPUParticleSystem.particleShaderMat;

	this.init = function() {
		self.particleSystem = new THREE.Points(self.particleShaderGeo, self.particleShaderMat);
		self.particleSystem.frustumCulled = false;
		this.add(self.particleSystem);
	};

	var options = {},
		position = new THREE.Vector3(),
		velocity = new THREE.Vector3(),
		positionRandomness = 0.,
		velocityRandomness = 0.,
		color = 0xffffff,
		colorRandomness = 0.,
		turbulence = 0.,
		lifetime = 0.,
		size = 0.,
		sizeRandomness = 0.,
		smoothPosition = false;

	var maxVel = 2;
	var maxSource = 250;
	this.offset = 0;
	this.count = 0;

	this.spawnParticle = function(options) {

		options = options || {};

		// setup reasonable default values for all arguments
		position = options.position !== undefined ? position.copy(options.position) : position.set(0., 0., 0.);
		velocity = options.velocity !== undefined ? velocity.copy(options.velocity) : velocity.set(0., 0., 0.);
		positionRandomness = options.positionRandomness !== undefined ? options.positionRandomness : 0.0;
		velocityRandomness = options.velocityRandomness !== undefined ? options.velocityRandomness : 0.0;
		color = options.color !== undefined ? options.color : 0xffffff;
		colorRandomness = options.colorRandomness !== undefined ? options.colorRandomness : 1.0;
		turbulence = options.turbulence !== undefined ? options.turbulence : 1.0;
		lifetime = options.lifetime !== undefined ? options.lifetime : 5.0;
		size = options.size !== undefined ? options.size : 10;
		sizeRandomness = options.sizeRandomness !== undefined ? options.sizeRandomness : 0.0;
		smoothPosition = options.smoothPosition !== undefined ? options.smoothPosition : false;

		if (self.DPR !== undefined) size *= self.DPR;

		i = self.PARTICLE_CURSOR;

		self.posStart.array[i * 4 + 0] = position.x + ((particleSystem.random()) * positionRandomness);
		self.posStart.array[i * 4 + 1] = position.y + ((particleSystem.random()) * positionRandomness);
		self.posStart.array[i * 4 + 2] = position.z + ((particleSystem.random()) * positionRandomness);
		self.posStart.array[i * 4 + 3] = self.time + (particleSystem.random() * 2e-2); //startTime

		const rgb = hexToRgb(color);
		self.color.array[i * 4 + 0] = rgb[0];
		self.color.array[i * 4 + 1] = rgb[1];
		self.color.array[i * 4 + 2] = rgb[2];

		self.velCol.array[i * 4 + 2] = size + (particleSystem.random()) * sizeRandomness; //size
		self.velCol.array[i * 4 + 3] = lifetime; //lifespan

		if (this.offset == 0) {
			this.offset = self.PARTICLE_CURSOR;
		}

		self.count++;

		self.PARTICLE_CURSOR++;

		if (self.PARTICLE_CURSOR >= self.PARTICLE_COUNT) {
			self.PARTICLE_CURSOR = 0;
		}

		self.particleUpdate = true;

	};

	this.update = function(time) {

		self.time = time;
		self.particleShaderMat.uniforms['uTime'].value = time;

		this.geometryUpdate();

	};

	this.dispose = function() {
		this.particleShaderGeo.dispose();
	};

	this.geometryUpdate = function() {
		if (self.particleUpdate == true) {
			self.particleUpdate = false;

			// if we can get away with a partial buffer update, do so
			if (self.offset + self.count < self.PARTICLE_COUNT) {
				self.posStart.updateRange.offset = self.velCol.updateRange.offset = self.offset * 4;
				self.posStart.updateRange.count = self.velCol.updateRange.count = self.count * 4;
			} else {
				self.posStart.updateRange.offset = 0;
				self.posStart.updateRange.count = self.velCol.updateRange.count = (self.PARTICLE_COUNT * 4);
			}

			self.posStart.needsUpdate = true;
			self.velCol.needsUpdate = true;
			self.color.needsUpdate = true;

			self.offset = 0;
			self.count = 0;
		}
	};

	this.init();

};

GPUParticleContainer.prototype = Object.create(THREE.Object3D.prototype);
GPUParticleContainer.prototype.constructor = GPUParticleContainer;