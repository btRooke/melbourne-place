# Local imports
import interpreter

# Library imports
import machine, socket, uasyncio

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

        data = conn.recv(2048).decode("utf-8")
        print("Received request from", addr)
        print("Received script:")
        print(data)

        # Translate request into executable python
        tabs = 1
        try:
            for i, line in enumerate(data):
                data[i], tabs = interpreter.interpret(line, tabs)
        except:
            conn.close()
            fail(led)
            continue

        script = '\n'.join(data)
        print("Script translated to:\n", script)

        # Run the code in a task
        if task is not None:
            task.cancel()
        task = uasyncio.create_task(run(conn, script))
        conn.close()

def fail(led):
    led[0].duty(1023)
    led[1].duty(0)
    led[2].duty(0)

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
    pins = [
        machine.Pin(14, machine.Pin.OUT), 
        machine.Pin(12, machine.Pin.OUT),
        machine.Pin(13, machine.Pin.OUT)]

    pwm = [machine.PWM(x, freq=50, duty=0) for x in pins]   
    main(s, pwm)
