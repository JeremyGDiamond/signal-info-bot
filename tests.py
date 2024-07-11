import signalpy
import subprocess
import json
import time

signal = signalpy.SignalObj()

# test signal funcs
def testSend():
    receive()
    send(config["testDmId"], "#bot hardcoded test send function")

def testSendGroup():
    receive()
    sendGroup(config["testGrId"], "#bot hardcoded test group send function")

# test bot behaviors
def testAdminAlert():
    signal.receive()
    signal.adminAlert("#bot test admin alert")



def main():
    
    print("tests")

    # testSend()
    # testSendGroup()
    testAdminAlert()
    
    
    # todo



if __name__ == "__main__":
    main()
