callLightAPI = (request) => {
    fetch(`lights/${request.type}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(request)
    })
    .then(res => res.json())
    .then(res => {
        if (res.status >= 400) {
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