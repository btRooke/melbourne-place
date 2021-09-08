// LED

scriptUpload = document.querySelector("#ledscript");

setLedScript = () => {
    alert("Sending script")
    fetch("/api/led.php", {
        method: "POST",
        headers: {},
        body: scriptUpload.files[0]
    });
}

scriptUpload.addEventListener("change", setLedScript)