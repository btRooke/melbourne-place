const fs = require("fs");
const net = require("net");
const sanitize = require("sanitize-filename");

// Sets the lights to a static colour or preset
// Uses req's type value to determine which
const lightHandler = (req, res) => {
    let type = req.body["type"];
    let payload = req.body["payload"];

    // Payload check
    if (!payload) {
        res.status(400);
        res.send("Missing request payload");
        return;
    }

    // Get the script to send
    let script;
    switch (type) {
        // Generate from the given colour
        case "static":
            let colour = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(payload);
            script =  `r = ${colour[1]}\n`;
            script += `g = ${colour[2]}\n`;
            script += `b = ${colour[3]}`;
            break;

        // Load from the given file
        case "preset":
            let filename = sanitize(payload);
            fs.readFileSync(`light-scripts/${filename}`, 'utf-8', (err, data) => {
                if (err) {
                    res.status(400);
                    res.send("Couldn't open the given file");
                }
                else {
                    script = data;
                }
            })
            break;

        // Type check
        default:
            res.status(400);
            res.send("Invalid request type");
            return;
    }

    // Check for null and excessive length
    if (!script) {
        return;
    }
    else if (script.length > 2048) {
        res.status(400);
        res.send("File is too large to process - cannot be larger than 2048 bytes");
        return;
    }

    // Send the script
    console.log(`Sending ${payload}`);
    const lights = new net.Socket();

    lights.connect({
        host: "192.168.1.179",
        port: 8080
    });

    lights.on("connect", () => {
        lights.write(script);
        res.status(200);
        lights.destroy();
    });

    lights.on("error", () => {
        res.status(500);
        res.send("Failed to connect to lights - they're probably off");
        lights.destroy();
    });
}

// Returns the names of all available preset files
const presetHandler = (req, res) => {
    console.log(req);

    fs.readdir("light-scripts", (err, files) => {
        if (err) {
            res.status(500);
            res.send("Failed to read light presets.");
        }
        else {
            res.json(files);
        }
    });
}

module.exports = {
    lightHandler,
    presetHandler
}