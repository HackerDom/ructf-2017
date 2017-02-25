import _ from "underscore";

const SERVICE_NAME_TO_NUM = {"atlablog": 4, "weather": 1, "cartographer": 3, "sapmarine": 2, "crash": 0, "thebin": 5};
const COLOR_CONSTANTS = ["#ED953A", "#E5BD1F", "#3FE1D6", "#568AFF", "#8C41DA", "#BA329E"];
const SERVICE_NAME_TO_SPHERE_NUM = {"atlablog": 3, "weather": 4, "cartographer": 5, "sapmarine": 0, "crash": 1, "thebin": 2};
const SERVICES_COUNT = 6;

export class GameModel {
	constructor(info) {
		this.teams = [];
		this._teamIdToNum = {};
		this._teamNameToNum = {};

		this.services = new Array(SERVICES_COUNT);
		this._serviceIdToNum = {};

		this.scoreboard = undefined;
		this.flagsCount = undefined;

		this.initTeams(info);
		this.initServices(info);
	}

	initTeams(info) {
		for (const fieldName in info.teams) {
			if (info.teams.hasOwnProperty(fieldName)) {
				const id = this.teams.length;
				const name = info.teams[fieldName];
				this.teams.push({
					index: id,
					id: id,
					team_id:
					fieldName,
					name: name,
					score: 0,
					place: null,
					status: 0,
					servicesStatuses: new Array(SERVICES_COUNT)
				});
				const num = this.teams.length - 1;
				this._teamIdToNum[fieldName] = num;
				this._teamNameToNum[name] = num;
			}
		}
	}

	initServices(info) {
		for (const fieldName in info.services) {
			if (info.services.hasOwnProperty(fieldName)) {
				const name = info.services[fieldName];
				const num = SERVICE_NAME_TO_NUM[name];
				this.services[num] = {
					id: num,
					service_id: fieldName,
					name: name,
					color: COLOR_CONSTANTS[num],
					visible: true,
					sphere_num: SERVICE_NAME_TO_SPHERE_NUM[name]
				};
				this._serviceIdToNum[fieldName] = num;
			}
		}
	}

	getTeamByName(name) {
		return this.teams[this._teamNameToNum[name]];
	}

	getTeamById(id) {
		return this.teams[this._teamIdToNum[id]];
	}

	getServiceById(name) {
		return this.services[this._serviceIdToNum[name]];
	}

	setScoreboard(scoreboard) {
		this.scoreboard = scoreboard;
	}

	updateFlagsStat() {
		this.flagsCount = 0;
		for (let i = 0; i < this.scoreboard.length; i++)
			for (let j = 0; j < SERVICES_COUNT; j++)
				if (this.getServiceById(this.scoreboard[i].services[j].id).visible)
					this.flagsCount += this.scoreboard[i].services[j].flags;
	}

	updateServicesStatuses() {
		for (let i = 0; i < this.scoreboard.length; i++) {
			const teamData = this.scoreboard[i];
			const team = this.getTeamByName(teamData.name);

			for (let j = 0; j < teamData.services.length; j++) {
				const serviceData = teamData.services[j];
				team.servicesStatuses[this._serviceIdToNum[serviceData.id]] = serviceData.status == 101;
			}
		}
	}

	updateScore() {
		for (let i = 0; i < this.scoreboard.length; i++)
			this.getTeamByName(this.scoreboard[i].name).score = this.scoreboard[i].score;
		this.setPlaces();
	}

	setPlaces() {
		const groupsHash = _.groupBy(this.teams, 'score');
		let groupsArray = [];
		for (const groupKey in groupsHash) {
			if (groupsHash.hasOwnProperty(groupKey)) {
				groupsArray.push({'key': parseFloat(groupKey), 'value': groupsHash[groupKey]});
			}
		}
		groupsArray = _.sortBy(groupsArray, 'key').reverse();
		let minPlace = 1;
		for (let i = 0; i < groupsArray.length; i++) {
			const teamsInGroup = groupsArray[i].value;
			const maxPlace = minPlace + teamsInGroup.length - 1;
			for (let j = 0; j < teamsInGroup.length; j++) {
				if (minPlace === maxPlace)
					teamsInGroup[j].place = minPlace + "";
				else
					teamsInGroup[j].place = minPlace + "-" + maxPlace;
			}
			minPlace = maxPlace + 1;
		}
	}
}
