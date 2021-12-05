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
            alert(res.body["message"]);
        }
    });
}

setStaticColour = (colourCode) => {
    callLightAPI({
        type: "static",
        payload: colourCode
    });
}

setPreset = (presetName) => {
    callLightAPI({
        type: "preset",
        payload: presetName
    });
}