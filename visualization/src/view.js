import $ from "jquery";
import md5 from "md5";
require('jquery-ui/ui/widgets/tooltip');
const d3 = Object.assign(require("d3-selection"), require("d3-zoom"), require("d3-shape"));

const DOWN_SERVICE_COLOR = "#1D3542";
const ISLAND_WIDTH = 60;
const ISLAND_HEIGHT = ISLAND_WIDTH * 0.866; // sqrt(3)/2

const svgWrapperId = "svg-wrapper";
const svgId = "svg-viz";
const tooltipContentWrapperClass = "team-tooltip";
const timeForArrowAnimation = 0.8;
const tracePortion = 0.4;
const whitePortion = 0.1;

const allCoords = [[19,20],[19,18],[18,19],[18,21],[19,22],[20,21],[21,20],[22,21],[21,22],[20,23],[21,24],[22,25],[21,26],[20,25],[6,11],[6,13],[7,12],[8,13],[9,12],[8,11],[8,9],[7,10],[7,14],[8,15],[7,16],[8,17],[9,16],[9,14],[10,15],[10,17],[9,18],[7,18],[8,19],[9,20],[10,19],[11,18],[12,17],[12,15],[11,16],[11,14],[8,23],[8,25],[8,21],[9,22],[22,19],[23,20],[22,17],[21,16],[23,18],[24,19],[25,18],[24,17],[25,16],[24,15],[23,16],[23,14],[22,15],[21,14],[20,13],[21,12],[22,13],[25,20],[26,21],[27,22],[28,23],[29,24],[30,23],[29,22],[28,21],[27,20],[26,19],[27,18],[26,17],[26,15],[27,16],[13,24],[13,26],[13,28],[14,27],[15,28],[15,26],[14,25],[12,27],[11,28],[13,32],[13,30],[14,33],[14,31],[14,29],[15,30],[16,31],[17,30],[18,31],[18,33],[17,32],[16,33],[17,34],[15,32],[12,33],[13,34],[12,31],[11,32],[10,33],[28,17],[29,16],[30,17],[29,18],[28,19],[29,20],[24,21],[6,9],[5,10],[5,12],[5,14],[4,13],[3,14],[3,12],[9,8],[9,6],[8,7],[12,9],[13,8],[14,7],[13,6],[17,10],[16,11],[15,12],[16,13],[17,12],[16,15],[21,10],[22,11],[23,12],[23,10],[23,8],[24,9],[24,11],[24,13],[25,12],[25,14],[6,19],[5,20],[4,21],[4,19],[3,18],[3,20],[4,23],[5,22],[6,21],[7,20],[7,22],[14,23],[15,24],[16,25],[27,10],[27,8],[27,6],[28,7],[29,6],[29,4],[31,8],[30,9],[29,10],[28,9],[29,8],[30,7],[30,11],[31,10],[31,12],[32,11],[6,27],[5,28],[4,27],[4,29],[3,28],[3,30],[3,32],[4,31],[5,30],[6,29],[7,30],[7,32],[6,31],[7,34],[6,33],[5,32],[22,31],[23,30],[24,29],[25,28],[23,32],[22,33],[22,35],[23,34],[24,33],[25,32],[25,30],[24,31],[26,29],[27,30],[26,31],[27,28],[26,33],[27,34],[28,35],[29,34],[29,32],[29,30],[5,8],[4,7],[5,6],[6,7],[3,6],[4,5],[18,9],[12,5],[13,4],[31,26],[32,25],[33,24],[33,22],[33,20],[33,18],[32,19],[34,21],[35,22],[34,23],[34,25],[35,24],[35,26],[34,27],[34,29],[33,26],[33,28],[36,29],[35,28],[36,27],[36,25],[34,33],[33,34],[32,35],[32,33],[33,8],[34,7],[35,8],[34,9],[35,10],[36,11],[37,12],[36,13],[36,15],[37,16],[37,18],[36,17],[37,20],[36,9],[37,10],[34,15],[34,13],[35,12],[35,14],[38,15],[3,4],[2,5],[2,13],[1,14],[0,15],[1,16],[2,15],[2,31],[1,32],[3,34],[4,37],[3,36],[2,37],[2,35],[5,38],[4,39],[10,35],[11,34],[11,36],[10,37],[11,38],[12,39],[12,37],[12,35],[13,36],[14,35],[26,39],[27,38],[28,39],[29,38],[29,40],[28,41],[27,40],[26,41],[28,37],[29,36],[27,36],[26,35],[35,36],[34,35],[34,37],[35,38],[34,39],[35,34],[33,36],[10,21],[11,20],[25,22],[2,7],[1,6],[17,20],[2,27],[36,35],[37,34],[37,26],[19,30],[18,29],[30,5],[36,7],[37,8],[36,39],[32,39],[31,38],[31,36],[32,37],[33,38],[8,41],[8,39],[7,40],[6,39],[5,40],[4,41],[13,18],[13,16],[0,31],[0,33],[1,26],[2,3],[38,27],[37,40],[37,38],[33,40],[32,41],[38,25],[39,26],[39,14],[39,12],[38,13],[37,14],[36,5],[37,6],[38,5],[33,6],[21,8],[8,5],[5,4],[9,4],[12,29],[11,30],[9,32],[10,31],[10,29],[0,17],[1,18],[1,8],[8,3],[15,14],[30,3],[31,4],[18,7],[21,6],[22,7],[22,9],[23,6],[16,7],[17,6],[17,8],[11,4],[10,5],[10,3],[9,2],[10,7],[11,6],[1,38],[2,39],[26,5],[27,4],[27,2],[32,3],[36,3],[37,4],[34,3],[34,1],[38,35],[11,40],[11,26],[12,25],[2,19],[2,21],[1,20],[12,7],[28,5],[36,37],[37,36],[38,41],[38,1],[4,3],[10,1],[8,1],[2,29],[1,28],[2,25],[1,40],[32,9],[33,10],[34,11],[33,4],[32,1],[33,2],[30,31],[1,4],[1,2],[0,1],[2,1],[39,28],[25,40],[-1,16],[-1,18],[39,34],[40,33],[41,34],[39,20],[40,21],[40,23],[41,20],[41,22],[40,35],[41,26],[41,18],[42,19],[3,38],[1,10],[0,9],[-1,8],[0,7],[-2,9],[-2,23],[-3,24],[-3,26],[-2,25],[-1,26],[-2,29],[-4,20]];


export default class View {

	constructor(controller) {
		this.controller = controller;
		this.model = null;

		controller.on('start', m => {
			this.model = m;
			this.init();
		});
		controller.on('score', () => {
			this.updateOpenedTooltip();
			this.draw_services_statuses();
		});
		controller.on('showArrow', arrowData => {
			this.showArrow(arrowData);
		});
		controller.on('flagStat', flags_count => {
			$("#attacks").find(".value").text(flags_count);
		});

		this.nodes = null;
		this.lastGradientId = 0;
		this.lastArrowId = 0;
		this.openedTooltipTeamId = null;

		this.svg = d3.select("#" + svgId);
		this.container = this.svg.append("g").classed("container", true);
		this.defs = this.svg.append("defs");
		this.zoom = d3.zoom().scaleExtent([0.25, 3]).on("zoom", () => {
			this.container.attr("transform", `translate(${d3.event.transform.x},${d3.event.transform.y})scale(${d3.event.transform.k})`);
		});
		this.svg.call(this.zoom);
	}

	init() {
		this.drawTeams();
		this.setResizeEvent();
		this.initTooltips();
		this.createFilterPanel();
	}

	draw_services_statuses() {
		const _this = this;
		let teams_with_alive = 0; // количество команд с хотя бы 1 сервисом
		d3.selectAll(".node").each(function () {
			const n = d3.select(this);
			const nData = n.data()[0];
			let hasUp = false;
			for (let i=0; i<_this.model.services.length; i++) {
				const isUp = _this.model.services[i].visible && nData.servicesStatuses[i];
				hasUp = hasUp || isUp;
				n.select(".service_" + i).attr("fill", isUp ? _this.model.services[i].color : DOWN_SERVICE_COLOR);
			}
			if (hasUp)
				teams_with_alive++;
		});
		$("#alive").find(".value").text(teams_with_alive);
	}

	updateOpenedTooltip() {
		if (this.openedTooltipTeamId == null)
			return;
		const team = this.model.teams[this.openedTooltipTeamId];
		const html = View.createTooltipHtml(team);
		$("." + tooltipContentWrapperClass).empty().append(html);
	}

	setOptimalZoom() {
		const $svg = $("#" + svgId);
		const realHeight = $svg.height();
		const realWidth = $svg.width();
		const cad = this.getCetnerAndDelta(this.model.teams);
		const size = ISLAND_WIDTH;
		cad.dx += size * 2;
		cad.dy += size * 5;
		cad.x += size * 0.5;
		cad.y += size * 0.5;
		const scale = Math.min(realWidth / cad.dx, realHeight / cad.dy);
		const translate = [realWidth / 2 - scale * cad.x, realHeight / 2 - scale * cad.y];
		this.zoom.transform(this.svg, d3.zoomIdentity.translate(...translate).scale(scale));
	}

	getCetnerAndDelta(nodes) {
		let miny, maxy;
		let minx = miny = Number.MAX_VALUE;
		let maxx = maxy = Number.MIN_VALUE;
		nodes.forEach(function(d) {
			if(d == undefined)
				return;
			minx = Math.min(d.x, minx);
			maxx = Math.max(d.x, maxx);
			miny = Math.min(d.y, miny);
			maxy = Math.max(d.y, maxy);
		});
		const dx = maxx - minx;
		const dy = maxy - miny;
		const x = (maxx + minx ) / 2;
		const y = (maxy + miny) / 2;
		return { x: x, y: y, dx: dx, dy: dy };
	}

	showArrow(arrow) {
		const _this = this;
		const service = arrow.svc;
		if (!service.visible)
			return;

		const links = this.container.selectAll(".arrow" + this.lastArrowId)
			.data([arrow])
			.enter()
			.append("g")
			.attr("class", ".arrow" + this.lastArrowId);
		this.lastArrowId++;

		links.each(function () {
			const link = d3.select(this);
			const linkData = link.data()[0];
			const teamFrom = linkData.from;
			const teamTo = linkData.to;
			const fromX = teamFrom.x + ISLAND_WIDTH / 2;
			const fromY = teamFrom.y + ISLAND_HEIGHT / 2;
			const toX = teamTo.x + ISLAND_WIDTH / 2;
			const toY = teamTo.y + ISLAND_HEIGHT / 2;
			const dx = toX - fromX;
			const dy = toY - fromY;
			const length = Math.sqrt(dx * dx + dy * dy);
			const angleRad = Math.atan2(dy, dx);
			const angle = angleRad * 180 / Math.PI;
			const gradientId = "grad" + _this.lastGradientId;
			const color = service.color;
			_this.lastGradientId++;
			const lineFunction = d3.line()
				.x(d => d.x)
				.y(d => d.y)
				.curve(d3.curveBasis);
			const vec_length = - length / 4; // Вектор из центра линии до кончика параболы.
			const vec_x = vec_length * Math.sin(angleRad); // Изначальный ветор меняется только по y вверх.
			const vec_y = vec_length * Math.cos(angleRad);
			const lineData = [ { "x": fromX, "y": fromY}, { "x": fromX + length / 2 + vec_x, "y": fromY + vec_y}, { "x": fromX + length,  "y": fromY + 0.01} ];
			link.append("path")
				.attr("class", "arrow-line")
				.attr("d", lineFunction(lineData))
				.attr("stroke", `url(#${gradientId})`);
			link.attr("transform", `rotate(${angle} ${fromX} ${fromY})`);
			_this.addGradient(gradientId, color);
			setTimeout(() => {
				link.remove();
				_this.defs.select("#" + gradientId).remove();
			}, timeForArrowAnimation * 1000 * (1 + tracePortion + whitePortion));
			setTimeout(() => {
				_this.addRadialGradient(gradientId + "radial", color);
				const explosion = _this.container.append("circle")
					.attr("class", "explosion")
					.attr("r", ISLAND_WIDTH / 3)
					.attr("cx", toX)
					.attr("cy", toY)
					.attr("fill", `url(#${gradientId}radial)`);
				setTimeout(() => {
					explosion.style("fill-opacity", 0);
				}, 100);
				setTimeout(() => {
					_this.defs.select(`#${gradientId}radial`).remove();
					explosion.remove();
				}, timeForArrowAnimation * 1000 * (tracePortion + whitePortion) );
			}, timeForArrowAnimation * 1000);
		});
	}

	drawTeams() {
		const _this = this;
		const coordsForTeams = View.getCoordsForTeams(this.model.teams.length);

		this.nodes = this.container.selectAll(".node")
			.data(this.model.teams)
			.enter()
			.append("g")
			.attr("class", "node");

		this.nodes.each(function () {
			const node = d3.select(this);
			const nodeData = node.data()[0];
			const coords = coordsForTeams.shift();
			nodeData.x = coords.x;
			nodeData.y = coords.y;
			const poly =
				[{"x": ISLAND_WIDTH / 4 , "y": 0},
					{"x": ISLAND_WIDTH * 3 / 4, "y": 0},
					{"x": ISLAND_WIDTH, "y": ISLAND_HEIGHT / 2},
					{"x": ISLAND_WIDTH * 3 / 4, "y": ISLAND_HEIGHT},
					{"x": ISLAND_WIDTH / 4 , "y": ISLAND_HEIGHT},
					{"x": 0, "y": ISLAND_HEIGHT / 2}];
			const polygon = node.append("polygon")
				.classed("island", true)
				.attr("points", poly.map(function(d) { return [d.x, d.y].join(","); }).join(" "))
				.attr("transform", `translate(${nodeData.x},${nodeData.y})`)
				.attr("fill-opacity", 0);

			const center = {"x": ISLAND_WIDTH / 2, "y": ISLAND_HEIGHT / 2};
			const shift = 0.55;
			for (let i=0; i<_this.model.services.length; i++) {
				const sphere_num = _this.model.services[i].sphere_num;
				const cx = center.x + (center.x - poly[sphere_num].x) * shift;
				const cy = center.y + (center.y - poly[sphere_num].y) * shift;
				node.append("circle")
					.classed("service", true)
					.classed("service_" + _this.model.services[i].id, true)
					.attr("r", ISLAND_WIDTH / 12)
					.attr("cx", cx)
					.attr("cy", cy)
					.attr("fill", DOWN_SERVICE_COLOR)
					.attr("transform", `translate(${nodeData.x},${nodeData.y})`);
			}
		});

		this.setOptimalZoom();

		$("#find-team-wrapper").find("input").on("keyup paste", function () {
			const text = $(this).val().toLowerCase();
			_this.nodes.each(function (){
				const n = d3.select(this);
				const nData = n.data()[0];
				const isFiltered = !text.length ? false : nData.name.toLowerCase().indexOf(text) === 0;
				n.select(".island").attr("fill-opacity", isFiltered ? 1 : 0);
			});
		});
	}

	static getCoordsForTeams(count) {
		const coords = [];
		for (let i=0; i<count; i++) {
			coords.push({"x": allCoords[i][0] * 45, "y":  allCoords[i][1] * 26});
		}
		return coords;
	}

	setResizeEvent() {
		$(window).resize(() => {
			this.setOptimalZoom();
		});
	}

	initTooltips() {
		const _this = this;
		$("#" + svgWrapperId).tooltip({
			items: ".node",
			track: true,
			show: {effect: "fadeIn", delay: 100, duration: 80},
			hide: {effect: "fadeOut", delay: 50, duration: 40},
			content: function () {
				const node = d3.select(this);
				const nodeData = node.data()[0];
				const html = View.createTooltipHtml(nodeData);
				_this.openedTooltipTeamId = nodeData.id;
				return "<div class='" + tooltipContentWrapperClass + "'>" + html + "</div>";
			},
			close: function () {
				_this.penedTooltipTeamId = null;
			}
		});
		$(".ui-helper-hidden-accessible").remove();
	}

	static createTooltipHtml(nodeData) {
		return "<table><td><img src='https://ructfe.org/logos/" + md5(nodeData.name ) + ".png'/></td>"
			+ "<td><div class='header-wrapper'><span class='value team-name'>" + View.htmlEncode(nodeData.name) + "</span></div>"
			+ "<div><span class='header'>Place:</span> <span class='value'>" + nodeData.place + "</span></div>"
			+ "<div><span class='header'>Score:</span> <span class='value'>" + nodeData.score + "</span></div></td></tr></table>";
	}

	static htmlEncode(value){
		return $('<div/>').text(value).html();
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
				_this.draw_services_statuses();
				_this.controller.emit('calcFlagStat');
			};
			}(i));
			$fc.append($filter);
		}
	}

	addRadialGradient(id, color) {
		const gradient = this.defs.append("radialGradient").attr("id", id);
		gradient.append("stop")
			.attr("offset", 0.02)
			.attr("stop-color", "white")
			.attr("stop-opacity", 1);
		gradient.append("stop")
			.attr("offset", 0.37)
			.attr("stop-color", color)
			.attr("stop-opacity", 1);
		gradient.append("stop")
			.attr("offset", 1)
			.attr("stop-color", color)
			.attr("stop-opacity", 0);
	}

	addGradient(id, color) {
		const startTime = this.svg.node().getCurrentTime();
		const gradient = this.defs.append("linearGradient").attr("id", id);
		const traceTime = timeForArrowAnimation * tracePortion;
		const whiteTime = timeForArrowAnimation * whitePortion;
		const allTime = timeForArrowAnimation + traceTime + whiteTime;

		gradient.append("stop")
			.attr("offset", 0)
			.attr("stop-color", "white")
			.attr("stop-opacity", 0);
		const stop2 = gradient.append("stop")
			.attr("offset", 0)
			.attr("stop-color", color)
			.attr("stop-opacity", 1);
		stop2.append("animate")
			.attr("attributeName", "stop-opacity")
			.attr("begin", startTime + whiteTime)
			.attr("dur", traceTime)
			.attr("values", "1;0")
			.attr("repeatCount", 1)
			.attr("fill", "freeze");
		stop2.append("animate")
			.attr("attributeName", "offset")
			.attr("begin", startTime + traceTime)
			.attr("dur", timeForArrowAnimation)
			.attr("values", "0;1")
			.attr("repeatCount", 1)
			.attr("fill", "freeze");
		stop2.append("animate")
			.attr("attributeName", "stop-opacity")
			.attr("begin", startTime + allTime)
			.attr("dur", "0.001s")
			.attr("values", "0;1")
			.attr("repeatCount", 1)
			.attr("fill", "freeze");
		stop2.append("animate")
			.attr("attributeName", "offset")
			.attr("begin", startTime + allTime)
			.attr("dur", "0.001s")
			.attr("values", "1;0")
			.attr("repeatCount", 1)
			.attr("fill", "freeze");
		const stop3 = gradient.append("stop")
			.attr("offset", 0)
			.attr("stop-color", "white")
			.attr("stop-opacity", 1);
		stop3.append("animate")
			.attr("attributeName", "stop-color")
			.attr("begin", startTime)
			.attr("dur", whiteTime)
			.attr("values", "white;" + color)
			.attr("repeatCount", 1)
			.attr("fill", "freeze");
		stop3.append("animate")
			.attr("attributeName", "offset")
			.attr("begin", startTime + whiteTime)
			.attr("dur", timeForArrowAnimation)
			.attr("values", "0;1")
			.attr("repeatCount", 1)
			.attr("fill", "freeze");
		stop3.append("animate")
			.attr("attributeName", "stop-opacity")
			.attr("begin", startTime + timeForArrowAnimation + whiteTime)
			.attr("dur", traceTime)
			.attr("values", "1;0")
			.attr("repeatCount", 1)
			.attr("fill", "freeze");
		stop3.append("animate")
			.attr("attributeName", "stop-color")
			.attr("begin", startTime + allTime)
			.attr("dur", "0.001s")
			.attr("values", color + ";white")
			.attr("repeatCount", 1)
			.attr("fill", "freeze");
		stop3.append("animate")
			.attr("attributeName", "offset")
			.attr("begin", startTime + allTime)
			.attr("dur", "0.001s")
			.attr("values", "1;0")
			.attr("repeatCount", 1)
			.attr("fill", "freeze");
		stop3.append("animate")
			.attr("attributeName", "stop-opacity")
			.attr("begin", startTime + allTime)
			.attr("dur", "0.001s")
			.attr("values", "0;1")
			.attr("repeatCount", 1)
			.attr("fill", "freeze");
		const stop4 = gradient.append("stop")
			.attr("offset", 0)
			.attr("stop-color", "white")
			.attr("stop-opacity", 1);
		stop4.append("animate")
			.attr("attributeName", "offset")
			.attr("begin", startTime)
			.attr("dur", timeForArrowAnimation)
			.attr("values", "0;1")
			.attr("repeatCount", 1)
			.attr("fill", "freeze");
		stop4.append("animate")
			.attr("attributeName", "stop-color")
			.attr("begin", startTime + timeForArrowAnimation)
			.attr("dur", whiteTime)
			.attr("values", "white;" + color)
			.attr("repeatCount", 1)
			.attr("fill", "freeze");
		stop4.append("animate")
			.attr("attributeName", "offset")
			.attr("begin", startTime + allTime)
			.attr("dur", "0.001s")
			.attr("values", "1;0")
			.attr("repeatCount", 1)
			.attr("fill", "freeze");
		stop4.append("animate")
			.attr("attributeName", "stop-color")
			.attr("begin", startTime + allTime)
			.attr("dur", "0.001s")
			.attr("values", color + ";white")
			.attr("repeatCount", 1)
			.attr("fill", "freeze");
		const stop5 = gradient.append("stop")
			.attr("offset", 0)
			.attr("stop-color", "white")
			.attr("stop-opacity", 0);
		stop5.append("animate")
			.attr("attributeName", "offset")
			.attr("begin", startTime)
			.attr("dur", timeForArrowAnimation)
			.attr("values", "0;1")
			.attr("repeatCount", 1)
			.attr("fill", "freeze");
		stop5.append("animate")
			.attr("attributeName", "offset")
			.attr("begin", startTime + allTime)
			.attr("dur", "0.001s")
			.attr("values", "1;0")
			.attr("repeatCount", 1)
			.attr("fill", "freeze");
		gradient.append("stop")
			.attr("offset", 1)
			.attr("stop-color", "white")
			.attr("stop-opacity", 0);
	}
}