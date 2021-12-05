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

// very hacky - apologies reader

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

socket.on("error", message => alert(message));

bellButton.addEventListener("pointerdown", () => {
    socket.emit("on");
    console.log("Ringing started.");
    bellBox.setAttribute("class", "sectionBox bell active");
});

function bellOff() {
    socket.emit("off");
    console.log("Ringing stopped.");
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
    if (res.status == 200) {
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
        console.warn("Failed to request light preset file list");
    }
})