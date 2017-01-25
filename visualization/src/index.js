import "whatwg-fetch";
import Controller from "./controller";
import View from "./view";


const controller = new Controller();
controller.on('start', (infoData, startScoreboard) => {
	new View(infoData, startScoreboard, controller);
});
