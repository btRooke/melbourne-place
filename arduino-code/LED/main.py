# Local imports
import interpreter, dimming

# Library imports
import machine, socket, uasyncio, random

# Constants
PORT = 8080

task = None

led = [
    machine.PWM(x, freq=100, duty=0) for x in [
        machine.Pin(14, machine.Pin.OUT), 
        machine.Pin(12, machine.Pin.OUT),
        machine.Pin(13, machine.Pin.OUT)]
    ]

lookup = [round(dimming.cie1931(float(L) / 255) * 1023) for L in range(256)]

# Main routine
async def main(reader, writer):
    try:
        global task
        global led
        global lookup

        # Accept and decode request
        print("Accepted a connection")

        asbytes = await reader.read(2048)
        data = asbytes.decode("utf-8").split('\n')
        
        print("Received script:")
        print(data)

        # Translate request into executable python
        tabs = 1
        try:
            script = interpreter.interpret(data)
            print("Script translated to:")
            print(script)
        except Exception as e:
            fail(str(e))
            return

        # Run the code in a task, cancelling the previous task
        if task is not None:
            task.cancel()
        task = uasyncio.current_task()
        await exec_async(script, led, lookup)
        task = None

    # Catch task getting cancelled by the next request
    except uasyncio.CancelledError:
        print("Cancelling current task")

    # Close streams on completion
    finally:
        reader.close()
        writer.close()

# Asynchronously execute a string as a function
async def exec_async(func, led, lookup):
    print("Executing")
    exec(func)
    await locals()['__script'](0, 0, 0, led, lookup)

# Set LEDs to red and print error message on failure
async def fail(msg):
    print(msg)

    led[0].duty(1023)
    led[1].duty(0)
    led[2].duty(0)

# On executing, start a TCP socket
if __name__ == "__main__":
    loop = uasyncio.get_event_loop()
    loop.create_task(uasyncio.start_server(main, "0.0.0.0", 8080, backlog=1))
    print("Listening on port", PORT)
    loop.run_forever()
    loop.close()