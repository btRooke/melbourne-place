// bell stuff

const bellButton = document.querySelector("#bell");
const bellBox = document.querySelector("#bellBox");

const socket = io();

socket.on("error", message => console.error(message));

bellButton.addEventListener("pointerdown", () => {
    socket.emit("on");
    window.navigator.vibrate(60 * 1000); // non blocking
    bellBox.setAttribute("class", "sectionBox bell active");
});

function bellOff() {
    socket.emit("off");
    window.navigator.vibrate(0);
    bellBox.setAttribute("class", "sectionBox bell");
}

bellButton.addEventListener("touchend", bellOff); // for mobile
document.addEventListener("pointerup", bellOff);

// morse stuff

const morseBox = document.querySelector("#morseMessage");
const morseButton = document.querySelector("#sendMorse");

morseButton.addEventListener("click", () => {

    if (morseBox.value.length > 0) {
        morseRing(morseBox.value);
    }

});

// light stuff

const lightBox = document.querySelector(".sectionBox.lights");

socket.on("lights", code => {
    lightBox.style.borderColor = code;
    console.log(`Other user set lights to ${code}`);
});

// Light presets

let box = document.querySelector(".sectionBox.lights");
let msg = box.querySelector("p");
let presetList = document.querySelector("#preset");

if (!box) {
    console.warn("No light box found - cannot change border colour.");
}
if (!presetList) {
    console.warn("Cannot find light preset list to populate");
}

if (box) {
    fetch("lights/ping").then(res => {
        if (res.ok) {
            res.json().then(details => {

                if (details.static) {
                    if (box.classList.contains("preset")) {
                        box.classList.remove("preset");  
                    }
                    box.style.borderColor = colourCode;
                }
                else if (!box.classList.contains("preset")) {
                    box.classList.add("preset");   
                }
            })
        } else {
            box.disabled = true;

            if (msg) {
                msg.innerText = 
                    "Can't connect to the lights - try refreshing the page.\n\n" +
                    "If that doesn't work, they're probably switched off.";
            }
        }
    })
}

if (presetList) {
    fetch("lights/presets").then(res => {
        if (res.ok) {
            // Loop through each file name, adding it as an option to the preset list
            res.json().then(filenames => {
                let option;
    
                for (let i = 0; i < filenames.length; i++) {
                    option = document.createElement("option");
                    option.text = filenames[i].split('.').slice(0, -1).join('.');
                    option.value = filenames[i];
                    presetList.add(option);
                }
            })
        }
        else {
            console.warn("Failed to request light preset file list.");
        }
    })

    presetList.addEventListener("change", e => setPreset(e.target.value));
}