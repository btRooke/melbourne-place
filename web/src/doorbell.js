const net = require("net");

const realtimeHandler = (socket) => {

    socket.on("on", () => {

        console.log(`${socket.id} bell on!`);

        const doorbell = new net.Socket();

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

        console.log(`${socket.id} bell off!`);

        const doorbell = new net.Socket();

        doorbell.connect({
            host: "192.168.1.194",
            port: 42069
        });

        doorbell.on("connect", () => {
            doorbell.write("off");
            doorbell.destroy();
        });

        doorbell.on("error", () => {
            socket.emit("error", "Failed to connect to doorbell; it's probably off.")
            doorbell.destroy();
        });

    });

}

const morseHandler = (req, res) => {

    let message = res.body["morseMessage"];

    if (message) {

        console.log(`Morsing ${message}!`);

        const doorbell = new net.Socket();

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
            res.write("Failed to connect to doorbell; it's probably off.");

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