# Local imports
from led import led, lookup, rng
from parser import generate_tokens, parse
from setup_net import PORT

# Library imports
from uasyncio import get_event_loop, start_server, current_task, CancelledError

# Main routine
async def main(task, reader, writer):
    try:
        # Accept and decode request
        print("Accepted a connection")

        asbytes = await reader.read(2048)
        data = asbytes.decode("utf-8")
        
        print("Received script:")
        print(data)

        # Translate request into executable python
        script = ""
        
        try:
            tokens = generate_tokens(data)
            script = parse(tokens)
            print("Script translated to:")
            print(script)

        except Exception as e:
            fail(str(e))
            return

        # Run the code in a task, cancelling the previous task
        if task is not None:
            task.cancel()

        task = current_task()
        await exec_async(script, led, lookup)
        task = None

    # Catch task getting cancelled by the next request
    except CancelledError:
        print("Cancelling current task")

    # Close streams on completion
    finally:
        reader.close()
        writer.close()


# Asynchronously execute a string as a function
async def exec_async(func: str, led: list, lookup: list):
    print("Executing")
    exec(func)
    await locals()['__script']({ "r" : 0, "g" : 0, "b" : 0 }, led, lookup, rng)


# Set LEDs to red and print error message on failure
async def fail(msg: str):
    print(msg)

    led[0].duty(1023)
    led[1].duty(0)
    led[2].duty(0)


# On executing, start a TCP socket
if __name__ == "__main__":
    task = None

    loop = get_event_loop()
    loop.create_task(start_server(lambda reader, writer: main(task, reader, writer), "0.0.0.0", PORT, backlog=1))
    print("Listening on port", PORT)
    loop.run_forever()
    loop.close()