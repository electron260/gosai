let modules = {};
let canvas;

const xoffset = -260; // millimeters
const yoffset = 70;

const screenwidth = 392.85; //millimeters
const screenheight = 698.4;

let global_data = {};
let recieved = false;

function setup() {
    canvas = createCanvas(windowWidth, windowHeight);
    frameRate(120);
}

function draw() {
    background(0);
    let start = Date.now();

    for (const [name, module] of Object.entries(modules)) {
        if (module.activated) {
            module.update();
            module.show();
        }
    }

    let end = Date.now();
    // console.log(end - start);
}

function windowResized() {
    resizeCanvas(windowWidth, windowHeight);
}