callBellAPI = (request) => {

    fetch("/api/doorbell.php", {

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

simpleRing = () => {
    callBellAPI({});
}

morseRing = (message) => {

    alert(message);

    // callBellAPI({
    //     morseMessage: message
    // });

}

