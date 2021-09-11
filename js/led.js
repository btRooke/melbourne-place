callLightAPI = (request) => {

    fetch("api/lights.php", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(request)

    })
    .then(res => res.json())
    .then(res => {

        if (res.status == -2) {
            alert("The lights aren't on right now...");
        }
        
    });

}

setStaticColour = (colourCode) => {

    callLightAPI({
        requestType: "static",
        colourCode: colourCode
    });
    
}

setPreset = (presetName) => {

    callLightAPI({
        requestType: "preset",
        name: presetName
    });

}