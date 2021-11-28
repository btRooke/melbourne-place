const express = require("express");
const cors = require("cors")
const { Server } = require("socket.io");
const http = require("http");

const doorbell = require("./doorbell");
const lights = require("./lights");

// ======== config ========

const staticDirectory = "static"; // relative to package.json
const port = process.argv[2] ? process.argv[2] : 3000;

// ======== initialise express and socket IO ========

const app = express();
const io = new Server(http.createServer(app));

// ======== request middleware ========

app.use(cors());

app.use((req, res, next) => { // log requests
    console.log(`${req.method} for ${req.url} from ${req.hostname}.`);
    next();
});

app.use((err, req, res, next) => {
    console.error(`Error ${err.statusCode}: ${err.statusMessage}.`);
    next();
});

app.use(express.static(staticDirectory)); // server static files

app.use(express.json()); // parse body to JSON

// ======== API endpoints ========

app.post("/doorbell/ring", doorbell.ringHandler);

app.post("/doorbell/morse", doorbell.ringHandler);

app.post("/lights/setStatic", lights.setPresetsHandler);

app.post("/lights/setPreset", lights.setPresetsHandler);

app.post("/lights/presets", lights.getPresetsHandler);

// ======== socket IO ========

io.on("connection", socket => {

    doorbell.realtimeHandler(socket);

    console.log(`SocketIO connection from ${socket.handshake.headers.host}: ${socket.id}`);

    socket.on("disconnect", () => {
        console.log(`SocketIO ${socket.id} disconnected!`);
    })

});

// ======== 404 ========

app.use((req, res, next) => {
    console.log(`Couldn't find ${req.url}...`);
    res.status(404);
    res.send(`Couldn't find ${req.url}.`);
    res.end();
    next();
});

// ======== start the server ========

app.listen(port, () => {
    console.log(`Listening on ${port}...`);
});