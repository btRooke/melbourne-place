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
const server = http.createServer(app);
const io = new Server(server);

// ======== sockets IO ========

io.on("connection", socket => {

    doorbell.realtimeHandler(socket);

    console.log(`SocketIO connection from ${socket.handshake.headers.host}: ${socket.id}`);

    socket.on("disconnect", () => {
        console.log(`SocketIO ${socket.id} disconnected!`);
    })

});

// ======== expess configuration ========

// cross origin requests

app.use(cors());

// logging

app.use((req, res, next) => { // log requests
    console.log(`${req.method} for ${req.url} from ${req.hostname}.`);
    next();
});

// parse body to JSON

app.use(express.json());

app.post("/doorbell/morse", doorbell.morseHandler);

app.post("/lights/static", lights.lightHandler(io));

app.post("/lights/preset", lights.lightHandler(io));

app.get("/lights/presets", lights.presetHandler);

// serve static files

app.use(express.static(staticDirectory));

// ======== 404 ========

app.use((req, res, next) => {
    console.log(`Couldn't find ${req.url}...`);
    res.status(404);
    res.send(`Couldn't find ${req.url}.`);
    res.end();
    next();
});

// ======== start the server ========

server.listen(port, () => {
    console.log(`Listening on ${port}...`);
});