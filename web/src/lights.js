const fs = require("fs");
const net = require("net");
const sanitize = require("sanitize-filename");
const localSocketTimeout = 250;

// Sets the lights to a static colour or preset
// Uses req's type value to determine which
const lightHandler = io => (req, res) => {
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

            let colourMatches = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(payload);

            let colours = colourMatches.slice(1);
            colours = colours.map(hex => parseInt(hex, 16));

            script =  `r = ${colours[0]}\n`;
            script += `g = ${colours[1]}\n`;
            script += `b = ${colours[2]}\n`;
            script += "save";
            break;

        // Load from the given file
        case "preset":
            let filename = sanitize(payload);

            try {
                script = fs.readFileSync(`light-scripts/${filename}`, 'utf-8');
                break;
            }
            catch {
                res.status(404);
                res.send("Couldn't open the given file");
                return;
            }

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
    const lights = new net.Socket();
    lights.setTimeout(localSocketTimeout);

    lights.connect({
        host: "192.168.1.179",
        port: 8080
    });

    lights.on("connect", () => {
        lights.write(script);
        lights.destroy();

        res.status(200);
        res.json({
            message: "Success!"
        });

        io.emit("lights", payload);

    });

    lights.on("error", () => {
        lights.destroy();
        res.status(500);
        res.send("Something went wrong whilst connecting to the lights - let us know if this happens.");
    });

    lights.on("timeout", () => {
        lights.destroy();
        res.status(500);
        res.send("Connection to lights timed out - they're probably off.")
    });

}

// Returns the names of all available preset files
const presetHandler = (req, res) => {
    fs.readdir("light-scripts", (err, files) => {
        if (err) {
            res.status(500);
            res.send("Failed to read light presets.");
        }
        else {
            res.status(200);
            res.json(files);
        }
    });
}

module.exports = {
    lightHandler,
    presetHandler
}