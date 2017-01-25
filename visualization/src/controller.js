import EventEmitter from "event-emitter-es6";


export default class Controller extends EventEmitter {
	constructor() {
		super({emitDelay: 1});
		this.emitSync = this.emitSync.bind(this);
		this.start();
	}

	start() {
		Promise.all([fetch("/api/info"), fetch("/api/scoreboard")])
			.then(response => {
				if (response[0].ok && response[1].ok)
					return Promise.all([response[0].json(), response[1].json()]);
			}).then(
				response => this.emitSync('start', ...response)
			);
	}
}
