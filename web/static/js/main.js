// doorbell animation

const bellAnimation = bodymovin.loadAnimation({

    container: document.querySelector(".bellIconContainer"),
    path: "media/bell.json",
    renderer: "svg",
    autoplay: false,
    loop: false,

    rendererSettings: {
        preserverAspectRatio: "xMinYMin",
    }

});

const bellButton = document.querySelector("#bell");

ringAnimation = () => {

    bellButton.disabled = true;
    document.querySelector(".overlay").setAttribute("class", "fullScreen centreContent noselect overlay");

    bellAnimation.play();

    setTimeout(() => {

        document.querySelector(".overlay").setAttribute("class", "fullScreen centreContent noselect overlay hidden");
        bellAnimation.stop();
        bellButton.disabled = false;

    }, 1500);

}

// bell stuff

const bellBox = document.querySelector("#bellBox");

const socket = io();

socket.on("error", message => console.error(message));

bellButton.addEventListener("pointerdown", () => {
    socket.emit("on");
    bellBox.setAttribute("class", "sectionBox bell active");
});

function bellOff() {
    socket.emit("off");
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

// Light presets

let presetList = document.querySelector("#preset");

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
        console.warn("Failed to request light preset file list!");
    }
})

presetList.addEventListener("change", e => setPreset(e.target.value));