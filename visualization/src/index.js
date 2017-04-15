import "whatwg-fetch";
import Controller from "./controller";
import View from "./view";


const controller = new Controller();
new View(controller);