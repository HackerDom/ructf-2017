import EventEmitter from "event-emitter-es6";
import {GameModel} from "./model";

const INVISIBLE_TEAM = "Invisible";
let Invisible_team_id;
const INVISIBLE_SERVICE = "pool";
let Invisible_service_id;

export default class Controller extends EventEmitter {
	constructor() {
		super({emitDelay: 1});
		this.model = null;

		this.on('calcFlagStat', () => {
			this.model.updateFlagsStat();
			this.emit('flagStat');
		});

		fetch("/api/info")
			.then(response => {
				if (response.ok)
					return response.json();
			}).then(info => {
				for (const fieldName in info.teams) {
					if (info.teams.hasOwnProperty(fieldName)) {
						const name = info.teams[fieldName];
						if (name === INVISIBLE_TEAM) {
							delete info.teams[fieldName];
							Invisible_team_id = fieldName;
							break;
						}
					}
				}
				for (const fieldName in info.services) {
					if (info.services.hasOwnProperty(fieldName)) {
						const name = info.services[fieldName];
						if (name === INVISIBLE_SERVICE) {
							delete info.services[fieldName];
							Invisible_service_id = fieldName;
							break;
						}
					}
				}
				this.model = new GameModel(info);
				this.emitSync('start', this.model);
				this.connectWebSocket();
			});
	}

	connectWebSocket() {
		const ws = new WebSocket("ws://" + window.location.hostname + (PRODUCTION ? "" : ":8080") + "/api/events");
		ws.onopen = (e) => {
			console.log('WebSocket opened.');
		};
		ws.onmessage = (e) => {
			let event = JSON.parse(e.data);
			if (event.type === "attack")
				this.processAttack(event.value);
			else if (event.type === "state")
				this.processState(event.value);
		};
		ws.onerror = (e) => {
			console.error('WebSocket encountered error. Closing websocket.');
			ws.close();
		};
		ws.onclose = (e) => {
			console.log('WebSocket is closed. Reconnect will be attempted in 1 second.');
			setTimeout(() => {
				this.connectWebSocket();
			}, 1000);
		};
	}

	processAttack(attack) {
		if (attack.service_id === Invisible_service_id || attack.attacker_id === Invisible_team_id || attack.victim_id === Invisible_team_id)
			return;
		const arrow = {
			from: this.model.getTeamById(attack.attacker_id),
			to: this.model.getTeamById(attack.victim_id),
			svc: this.model.getServiceById(attack.service_id)
		};
		this.emit('showArrow', arrow);
	}

	processState(state) {
		let invisibleTeamPos;
		for (let i = 0; i < state.scoreboard.length; i++) {
			const teamData = state.scoreboard[i];
			if (teamData.name === INVISIBLE_TEAM) {
				invisibleTeamPos = i;
				break;
			}
		}
		state.scoreboard.splice(invisibleTeamPos, 1);
		for (let i = 0; i < state.scoreboard.length; i++) {
			const teamData = state.scoreboard[i];
			for (let j = 0; j < teamData.services.length; j++) {
				const serviceData = teamData.services[j];
				if (serviceData.id === Invisible_service_id) {
					teamData.services.splice(j, 1);
					break;
				}
			}
		}
		this.model.setScoreboard(state.scoreboard);
		this.model.updateServicesStatuses();
		this.emit('servicesStatuses');
		this.model.updateFlagsStat();
		this.emit('flagStat');
		this.model.updateScore();
		this.emit('score');
	}
}
