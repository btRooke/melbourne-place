// LED

scriptUpload = document.querySelector("#ledscript");

setLedScript = () => {
    fetch("/api/led.php", {
        method: "POST",
        headers: {},
        body: scriptUpload.files[0]
    });
}

scriptUpload.addEventListener("change", setLedScript)