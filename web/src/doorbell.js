const net = require("net");
const localSocketTimeout = 250;

const realtimeHandler = (socket) => {

    socket.on("on", () => {

        const doorbell = new net.Socket();
        doorbell.setTimeout(localSocketTimeout);

        doorbell.connect({
            host: "192.168.1.194",
            port: 42069
        });

        doorbell.on("connect", () => {
            doorbell.write("on");
            doorbell.destroy();
        });

        doorbell.on("error", () => {
            socket.emit("error", "Failed to connect to doorbell; it's probably off.")
            doorbell.destroy();
        });

    });

    socket.on("off", () => {

        const doorbell = new net.Socket()
        doorbell.setTimeout(localSocketTimeout);

        doorbell.connect({
            host: "192.168.1.194",
            port: 42069
        });

        doorbell.on("connect", () => {
            doorbell.write("off");
            doorbell.destroy();
        });

        doorbell.on("error", () => {
            socket.emit("error", "Something went wrong whilst connecting to the bell.")
            doorbell.destroy();
        });

        doorbell.on("timeout", () => {
            socket.emit("error", "Doorbell connect timed out - it's probably off.")
            doorbell.destroy();
        });

    });

}

const morseHandler = (req, res) => {

    let message = req.body["morseMessage"];

    if (message) {

        const doorbell = new net.Socket();
        doorbell.setTimeout(localSocketTimeout);

        doorbell.connect({
            host: "192.168.1.194",
            port: 42069
        });

        doorbell.on("connect", () => {
            doorbell.write(message);
        });

        doorbell.on("data", ringMessage => {

            res.json({
                message: ringMessage
            });

            doorbell.destroy();

        })

        doorbell.on("error", () => {

            res.status(500);
            res.write("Something went wrong whilst connecting to the doorbell - let us know if this happens.");

            doorbell.destroy();

        });

        doorbell.on("timeout", () => {

            res.status(500);
            res.send("Failed to connect to the doorbell - it's probably off.")

            doorbell.destroy();

        });

    }

    else {

        res.status(400);
        res.write("Missing morse message.");

    }

}

module.exports = {
    realtimeHandler,
    morseHandler
}