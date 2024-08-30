import signalpy
import subprocess
import json
import time
import logging


#configure logger to write to console and file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)

signal = signalpy.SignalObj("config.json", "debug.log")

def main():
    print("Bot alive")
    
    while True:
        # signal.receive()
        signal.parseReceive()
        logging.info("receieve run")

if __name__ == "__main__":
    main()
