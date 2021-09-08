# Local imports
import interpreter

# Library imports
import machine, socket, neopixel, uasyncio

# Constants
PORT = 8080

# Variables
r = 0
g = 0
b = 0

# Main routine
def main(socket, led):
    task = None

    while True:
        # Accept and decode request
        conn, addr = socket.accept()
        print("Accepted a connection")

        conn.setblocking(false)
        data = conn.recv(2048).decode("utf-8")
        print("Received request from", addr)
        print("Received script:\n", data)

        # Translate request into executable python
        tabs = 1
        try:
            for i, line in enumerate(data):
                data[i], tabs = interpreter.interpret(line, tabs)
        except:
            conn.close()
            continue

        script = '\n'.join(data)
        print("Script translated to:\n", script)

        # Run the code in a task
        if task is not None:
            task.cancel()
        task = uasyncio.create_task(run(conn, script))
        conn.close()

async def run(conn, script):
    try:
        exec("async def __script():\n{0}".format(script))
    except Exception as e:
        conn.send(str(e).encode("utf-8"))

if __name__ == "__main__":
    # Listen on port 8080
    addr = socket.getaddrinfo("0.0.0.0", PORT)[0][-1]
    
    s = socket.socket()
    s.bind(addr)
    s.listen(1) # Only allow 1 unaccepted connection to be queued
    print("Listening on port", PORT)

    # Get LED strip
    led = neopixel.NeoPixel(machine.Pin(4), 1)
    
    if led:
        main(s, led)
    else:
        print("Could not create a reference to the LED strip")

# The following script will cycle through the colour spectrum:
"""
set r 255
set g 0
set b 0
save

while 1
    while g < 255
        add g 1
        wait 10
        save

    then while r > 0
        sub r 1
        wait 10
        save

    then while b < 255
        add b 1
        wait 10
        save

    then while g > 0
        sub g 1
        wait 10
        save

    then while r < 255
        add g 1
        wait 10
        save

    then while b > 0
        sub b 1
        wait 10
        save
"""