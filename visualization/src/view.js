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
}