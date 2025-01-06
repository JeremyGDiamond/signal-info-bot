import signalpy
# import subprocess
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

signal = signalpy.SignalObj("config.json5", "debug.log")

def main():
    logging.info("Bot alive")

    waitFor10min = 0
    
    while True:
        # signal.receive()
        signal.parseReceive()
        logging.info("receieve run")

        waitFor10min += 1

        if waitFor10min == 61: #this is a hack
            signal.genGroups()
            logging.info("groups gen, welcomes sent")
            waitFor10min = 0

        

        # try:
        #     if datetime.datetime.now() >= tom:
        #         yest = "yest.log"
        #         current = "debug.log"
        #         if os.path.isfile(yest):
        #             os.remove(yest)

        #         if os.path.isfile(current):
        #             shutil.copy(current, yest)

        #             os.remove(current)
                
        #             with open(path, 'a'):
        #                 os.utime(path, None)
                        
        #         tom = tom + datetime.timedelta(days=1)
        #         logging.info(f"tom set for {tom}")
        # except:
        #     tom = datetime.datetime.now() + datetime.timedelta(days=1)
        #     logging.info(f"tom set for {tom}")


if __name__ == "__main__":
    main()
