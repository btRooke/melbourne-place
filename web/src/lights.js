const fs = require("fs");

const setStaticHandler = (req, res) => {
    res.status(501);
}

const setPresetHandler = (req, res) => {
    res.status(501);
}

const getPresetsHandler = (req, res) => {

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
    setStaticHandler,
    setPresetHandler,
    getPresetsHandler
}