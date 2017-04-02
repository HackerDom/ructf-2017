import EventEmitter from "event-emitter-es6";
import {GameModel} from "./model";

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
				this.model = new GameModel(info);
				this.emitSync('start', this.model);
				this.connectWebSocket();
			});
	}

	connectWebSocket() {
		const ws = new WebSocket("ws://127.0.0.1:8080//apiws/events");
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
		const arrow = {
			from: this.model.getTeamById(attack.attacker_id),
			to: this.model.getTeamById(attack.victim_id),
			svc: this.model.getServiceById(attack.service_id)
		};
		this.emit('showArrow', arrow);
	}

	processState(state) {
		this.model.setScoreboard(state.scoreboard);
		this.model.updateServicesStatuses();
		this.emit('servicesStatuses');
		this.model.updateFlagsStat();
		this.emit('flagStat');
		this.model.updateScore();
		this.emit('score');
	}
}
