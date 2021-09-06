// Doorbell

const bellAnimation = bodymovin.loadAnimation({

    container: document.querySelector(".bellIconContainer"),
    path: "media/bell.json",
    renderer: "svg",
    autoplay: false,
    loop: false,

    rendererSettings: {
        preserverAspectRatio: "xMinYMin",
    },

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
    fetch("/api/doorbell.php");
    ringAnimation();
};

bellButton.addEventListener("click", ringBell);

// LED

scriptUpload = document.querySelector("#ledscript");

setLedScript = () => {
    fetch("/api/led.php", {
        method: "POST",
        headers: {},
        body: scriptUpload.files[0]
    });
}

scriptUpload.addEventListener("change", setLedScript)