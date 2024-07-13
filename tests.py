import signalpy
import subprocess
import json
import time

signal = signalpy.SignalObj("testConfig.json")

# test signal funcs
def testSend():
    # signal.receive()
    signal.send(signal.config["testDmId"], "#bot hardcoded test send function")

def testSendGroup():
    # signal.receive()
    signal.sendGroup(signal.config["testGrId"], "#bot hardcoded test group send function")

# test bot behaviors
def testAdminAlert():
    # signal.receive()
    signal.adminAlert("#bot test admin alert")

def testParseReceive():
    signal.parseReceive()



def main():
    
    print("tests")

    # testSend()
    # testSendGroup()
    testAdminAlert()
    testParseReceive()
    
    
    # todo



if __name__ == "__main__":
    main()
