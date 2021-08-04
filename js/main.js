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

    // hack below to stop mobile hover

    const parent = bellButton.parentNode;
    const next = bellButton.nextSibling;

    parent.removeChild(bellButton);
    setTimeout(() => parent.insertBefore(bellButton, next), 0);

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
    fetch("/php/doorbell.php");
    ringAnimation();
};

bellButton.addEventListener("click", ringBell);