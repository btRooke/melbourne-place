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

    document.querySelector(".overlay").setAttribute("class", "fullScreen centreContent noselect overlay");

    bellAnimation.play();

    setTimeout(() => {
        document.querySelector(".overlay").setAttribute("class", "fullScreen centreContent noselect overlay hidden");
        bellAnimation.stop();
    }, 1500);

}

ringBell = () => {
    fetch("/php/doorbell.php");
    ringAnimation();
};

bellButton.addEventListener("click", ringBell);