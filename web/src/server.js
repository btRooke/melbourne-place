const express = require("express");

const port = process.argv[2] ? process.argv[2] : 3000;
const app = express();

// middleware

app.use((req, res) => {
    console.log(`Request for ${req.url} from ${req.hostname}.`);
});

// endpoints

app.post("/doorbell", ((req, res) => {}));

app.post("/lights",  (req, res) => {});

// starting the server

app.listen(port, () => {
    console.log(`Listening on ${port}...`);
});