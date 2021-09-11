setStaticColour = (colourCode) => {

    fetch("api/lights.php", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            requestType: "static",
            colourCode: colourCode
        })

    });

    
}

setPreset = (presetName) => {

    fetch("api/lights.php", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            requestType: "preset",
            name: presetName
        })

    });

}