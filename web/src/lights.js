const fs = require("fs");
const config = require("../config");

function setStaticHandler() {

};

function setPresetHandler() {

};

function getPresetsHandler(req, res) {

    fs.readdir(testFolder, (err, files) => {

        if (err) {
            res.status(500);
            res.send("Failed to read light presets.");
        }

        else {
            res.json(files);
        }

        res.end();

    });

};

module.exports = {
    setStaticHandler,
    setPresetHandler,
    getPresetsHandler
}