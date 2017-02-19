import EventEmitter from "event-emitter-es6";
import {GameModel, NOT_STARTED} from "./model";

const LOAD_DATA_INTERVAL = 30*1000;
const EVENTS_VISUALIZATION_INTERVAL = 1000;


export default class Controller extends EventEmitter {
	constructor() {
		super({emitDelay: 1});

		this.model = null;

		this._cur_round = -1;
		this._prev_interval = -1;
		this._pending_events = [];
		this._new_events = [];

		this.emitSync = this.emitSync.bind(this);
		this.emit = this.emit.bind(this);
		this.load_services_statuses = this.load_services_statuses.bind(this);

		this.on('calcFlagStat', () => {
			this.update_flag_stat();
		});

		this.start();
	}

	start() {
		const _this = this;
		Promise.all([fetch("/api/info"), fetch("/api/scoreboard")])
			.then(response => {
				if (response[0].ok && response[1].ok)
					return Promise.all([response[0].json(), response[1].json()]);
			}).then(response => {
				const [info, scoreboard] = response;
				this.model = new GameModel(info);
				this.model.setScoreboard(scoreboard);
				this.emitSync('start', this.model);

				setTimeout(() => {
					this.load_data();
					setInterval(() => this.load_data(), LOAD_DATA_INTERVAL);
				}, 0);

				setTimeout(() => {
					//this.events_visualization_loop();
					setInterval(() => {
						//this.events_visualization_loop();
					}, EVENTS_VISUALIZATION_INTERVAL);
				}, 0);
			});

		const ws = new WebSocket("ws://127.0.0.1:8080/websocket");
		ws.onmessage = function(e) {
			let event = JSON.parse(e.data);
			let arrowData = {
				from: _this.model.getTeamById(event[3]),
				to: _this.model.getTeamById(event[4]),
				svc: _this.model.getServiceById(event[2])
			};
			_this.emit('showArrow', arrowData);
		};
		ws.onerror = function(error) {
			console.log("Ошибка " + error.message);
		};
	}

	load_data() {
		fetch("/api/scoreboard")
			.then(response => {
				if (response.ok)
					return response.json();
			}).then(scoreboardData => {
				this.model.setScoreboard(scoreboardData);
				this.load_events();
				fetch("/scoreboard.json")
					.then(response => {
						if (response.ok)
							return response.json();
					}).then(scores_json => {
						this.load_services_statuses(scores_json);
						this.model.updateScore();
						this.emit('score');
					});
			});
	}

	load_services_statuses(scores_json) {
		for (let i = 0; i < scores_json['scoreboard'].length; i++) {
			const teamData = scores_json['scoreboard'][i];
			const team = this.model.getTeamByName(teamData['name']);

			for (let j = 0; j < teamData['services'].length; j++) {
				const serviceData = teamData['services'][j];
				team.servicesStatuses[this.model._serviceIdToNum[serviceData['id']]] = (serviceData['status'] == 101);
			}
		}
	}

	// Если начался новый раунд, запрашивает данные за предыдущий и кладет события в pending_events
	// При открытии для предыдущего раунда запрашивает данные сразу.
	load_events() {
		if (this._cur_round < 0) { this._cur_round = this.model.round - 1; }
		if (this._cur_round === this.model.round) { return; }
		const next_round = this.model.round;

		fetch('/api/events?from=' + this._cur_round)
			.then(
				response => response.json()
			).then(eventsData => {
				this._new_events = [];
				for (let i = 0; i < eventsData.length; ++i) {
					if (this._cur_round <= eventsData[i][0] && eventsData[i][0] < next_round) {
						this._new_events.push(eventsData[i]);
					}
				}
				this._new_events.sort((a, b) => {
					const x = parseInt(a[1]);
					const y = parseInt(b[1]);
					if (x < y) { return -1; }
					else if (x > y) { return 1; }
					else { return 0; }
				});
				this._pending_events = this._pending_events.concat(this._new_events);
				this._cur_round = next_round;
				this.update_flag_stat();
			});
	}

	events_visualization_loop() {
		if (this.model.status == NOT_STARTED)
			return;

		if (this._prev_interval < 0) {
			if (this._pending_events.length > 0)
				this._prev_interval = this._pending_events[0][1] - EVENTS_VISUALIZATION_INTERVAL;
			else
				return;
		}

		const prev_interval_end = this._prev_interval + EVENTS_VISUALIZATION_INTERVAL;
		while (this._pending_events.length > 0 && this._pending_events[0][1] < prev_interval_end) {
			const event = this._pending_events.shift();
			const showArrowFunc = (arrowData =>
				() => this.emit('showArrow', arrowData)
			)({
				from: this.model.getTeamById(event[3]),
				to: this.model.getTeamById(event[4]),
				svc: this.model.getServiceById(event[2])
			});
			setTimeout(showArrowFunc, event[1] - this._prev_interval);
		}
		this._prev_interval = prev_interval_end;
	}

	update_flag_stat() {
		let flags_count = 0;

		for (let i = 0; i < this._new_events.length; i++) {
			const service_id = this._new_events[i][2];
			if (this.model.getServiceById(service_id).visible)
				flags_count++;
		}

		this.emit('flagStat', flags_count);
	}
}
