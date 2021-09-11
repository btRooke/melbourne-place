# Local imports
import interpreter

# Library imports
import machine, socket, uasyncio

# Constants
PORT = 8080

# Main routine
def main(socket):
    task = None

    led = [
        machine.PWM(x, freq=100, duty=0) for x in [
            machine.Pin(14, machine.Pin.OUT), 
            machine.Pin(12, machine.Pin.OUT),
            machine.Pin(13, machine.Pin.OUT)]
        ]

    while True:
        # Accept and decode request
        conn, addr = socket.accept()
        print("Accepted a connection")

        data = conn.recv(2048).decode("utf-8").split('\n')
        print("Received request from", addr)
        print("Received script:")
        print(data)

        # Translate request into executable python
        tabs = 1
        try:
            for i, line in enumerate(data):
                data[i], tabs = interpreter.interpret(line, tabs)
        except Exception as e:
            conn.close()
            fail(str(e))
            continue

        script = '\n'.join(data)
        print("Script translated to:")
        print(script)

        # Run the code in a task
        if task is not None:
            task.cancel()
        
        loop = uasyncio.new_event_loop()
        task = loop.create_task(exec_async(script, led))
        loop.run_forever()
        conn.close()
        print("Checkpoint")

# Asynchronously execute a string as a function
async def exec_async(func, led):
    print("Executing")
    exec("async def __script(r, g, b, led):\n{0}".format(func))
    await locals()['__script'](0, 0, 0, led)

# Set LEDs to red and print error message on failure
async def fail(msg):
    print(msg)

    led[0].duty(1023)
    led[1].duty(0)
    led[2].duty(0)

# On executing, start a TCP socket
if __name__ == "__main__":
    # Listen on port 8080
    addr = socket.getaddrinfo("0.0.0.0", PORT)[0][-1]
    
    s = socket.socket()
    s.bind(addr)
    s.listen(1) # Only allow 1 unaccepted connection to be queued
    print("Listening on port", PORT)
  
    main(s)