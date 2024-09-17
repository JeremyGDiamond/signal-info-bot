import signalpy
import subprocess
import json
import time
import datetime
import logging
import shutil


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
# currentTime = datetime.datetime.now()
tom = currentTime + datetime.timedelta(days=1)

def main():
    logging.info("Bot alive")
    
    while True:
        # signal.receive()
        signal.parseReceive()
        logging.info("receieve run")

        if datetime.datetime.now() >= tom:
            yest = "yest.log"
            current = "debug.log"
            if os.path.isfile(yest):
                os.remove(yest)

            if os.path.isfile(current):
                shutil.copy(current, yest)

                os.remove(current)
            
                with open(path, 'a'):
                    os.utime(path, None)
                    
            tom = currentTime + datetime.timedelta(days=1)


if __name__ == "__main__":
    main()
