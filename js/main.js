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

bellButton = document.querySelector("#bell");

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

ringBell = () => {
    simpleRing();
    ringAnimation();
};

bellButton.addEventListener("click", ringBell);

morseButton = document.querySelector("#sendMorse");
morseButton.addEventListener("click", () => {

    morseBox = document.querySelector("#morseMessage");

    if (morseBox.value.length > 0) {
        morseRing(morseBox.value);
    }

});