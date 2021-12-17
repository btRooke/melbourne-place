let border = document.querySelector(".sectionBox.lights");

if (!border) {
    console.warn("No light box found - cannot change border colour.");
}

callLightAPI = (request) => {

    fetch(`lights/${request.type}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(request)
    })

    .then(res => {

        if (!res.ok) {
            res.text().then(text => alert(text));
        }

    });

}

setStaticColour = (colourCode) => {

    callLightAPI({
        type: "static",
        payload: colourCode
    });

    if (border) {
        if (border.classList.contains("preset")) {
            border.classList.remove("preset");  
        }
        border.style.borderColor = colourCode;
    }

}

setPreset = (presetName) => {

    callLightAPI({
        type: "preset",
        payload: presetName
    });

    if (border && !border.classList.contains("preset")) {
        border.classList.add("preset");   
    }

}