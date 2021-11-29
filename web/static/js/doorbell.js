callBellAPI = (request) => {

    fetch("/doorbell/morse", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(request)

    })
    .then(res => res.json())
    .then(res => {

        if (res.status != 0) {
            alert("The doorbell couldn't be bonged at this time...");
        }
        
    });

}

morseRing = (message) => {

    callBellAPI({
        morseMessage: message
    });

}

