import "whatwg-fetch";
import Controller from "./controller";
import View from "./view";


const controller = new Controller();
controller.on('start', (model) => {
	new View(model, controller);
});
