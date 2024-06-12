import asyncio
from bleak import BleakClient
import uuid
import struct
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
#import threading
from threading import Thread
import pyglet
from math import sqrt, pow
import socket

# UUID of the characteristic you want to read from
CHARACTERISTIC_UUID = uuid.UUID("430A5B62-C01A-4DB5-8347-0565C672C459")

# Initialize the data lists
xs = []
ys1 = []
ys2 = []
ys3 = []

async def sound_alarm():
    # play an alarm sound
    music = pyglet.resource.media('alarm.wav')
    music.play()
    pyglet.app.run()
    await asyncio.sleep(2)
    pyglet.app.exit()

async def update_data(client, t):
    while True:
        try:
            y = await client.read_gatt_char(CHARACTERISTIC_UUID)
            y = struct.unpack('9f', y)
            y = np.asarray(y)
            x = time.time() - t
            
            clientsocket.send(bytes(f"{(np.pi*y[2]/180.0)},{(np.pi*y[0]/180.0)}", "utf-8")) # send to game
            y1, y2, y3 = y[0], y[1], y[2]
            xs.append(x)
            ys1.append(y1)
            ys2.append(y2)
            ys3.append(y3)
            print(y1, y2, y3)
        except Exception as e:
            print(f"Error: {e}")
        await asyncio.sleep(0.05)
        
async def check_condition():
    if sqrt(pow(ys1[1,-1], 2) + pow(ys2[1,-1], 2) + pow(ys3[1,-1], 2)) > 3:
            await sound_alarm()
            print("Careful!")

def plot_data(i, xs, ys1, ys2, ys3):
    ax.clear()
    ax.plot(xs, ys1, color='r')
    ax.plot(xs, ys2, color='g') #we don't want this in the game
    ax.plot(xs, ys3, color='b')

async def main():
    async with BleakClient('0F:A9:4D:AD:9E:83') as client:
        await update_data(client, t)
        


if __name__ == "__main__":
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), 1234))
    s.listen(5)
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")
    ## Code above is added for the game
    t = time.time()
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    
    ani = animation.FuncAnimation(fig, plot_data, fargs=(xs, ys1, ys2, ys3), interval=50)
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    thread = Thread(target=lambda: loop.run_forever())
    thread.start()
    
    asyncio.run_coroutine_threadsafe(main(), loop)
    
    loop1 = asyncio.new_event_loop()
    asyncio.set_event_loop(loop1)
    
    thread1 = Thread(target=lambda: loop1.run_forever())
    thread1.start()
    
    asyncio.run_coroutine_threadsafe(check_condition(), loop1)
    
    plt.show()
    
    loop.call_soon_threadsafe(loop.stop)
    loop1.call_soon_threadsafe(loop1.stop)
    thread.join()
    thread1.join()
    
