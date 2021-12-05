callBellAPI = (request) => {

    fetch("/doorbell/morse", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(request)

    })
    .then(res => {

        if (!res.ok) {
            alert("The doorbell couldn't be bonged at this time...");
        }
        
    });

}

morseRing = (message) => {

    callBellAPI({
        morseMessage: message
    });

}

