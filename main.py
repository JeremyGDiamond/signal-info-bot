import subprocess
import json
import time

signal = signalpy.SignalObj("config.json")

def main():
    print("Bot alive")
    
    # todo
    # - receive on seperate process, killed after timeout, 
    # - receive output passes as return
    # - loop receive
    # - parse new join and dm new group member welcome message
    # - command parser
    # - read commands from config
    # - commands can't be a vuln
    # - admin alerts
    # - move signal calls to lib file and tests to test file
    # - include example config file


    while True:
        # signal.receive()
        signal.parseReceive()
        print("receieve run")


        




if __name__ == "__main__":
    main()
