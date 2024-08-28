import signalpy
import subprocess
import json
import time

signal = signalpy.SignalObj("testConfig.json")

# test init

def testReadConfig(): #TODO alpha
    pass

def testGenGroups(): #TODO alpha
    pass

def testValidateConfigGroups(): #TODO alpha
    pass

def testGenHelps(): #TODO alpha
    pass

# test message sanitizer

def passSan(): #TODO alpha
    signal.sanitizeMessage("This message should be the same")

def failEachBlockedChar(): #TODO alpha
    pass

def failEachBlockedStrings(): #TODO alpha
    pass

def failEachTestCommand(): #TODO alpha
    pass

# test signal funcs
def testSend():
    # signal.receive()
    signal.send(signal.config["testDmId"], "#bot hardcoded test send function")

def testSendGroup():
    # signal.receive()
    signal.sendGroup(signal.config["testGrId"], "#bot hardcoded test group send function")

def testSendNTS():
    # signal.receive()
    signal.sendNTS(signal.config["testDmId"], "#bot hardcoded test sendNTS function")

def testListGroups(): #TODO alpha
    pass


# test bot behaviors
def testAdminAlert():
    # signal.receive()
    signal.adminAlert("#bot test admin alert")

def testGetGroupMembers(): #TODO alpha
    pass

def testGetGroupAdmins(): #TODO alpha
    pass

def testError(): #TODO alpha
    pass

def testAuth(): #TODO alpha
    pass

def testAuthGroup(): #TODO alpha
    pass

def testSendWelcome(): #TODO alpha
    pass

def testActivateGroup(): #TODO alpha
    pass

def testSendHelp(): #TODO alpha
    pass

def testSendDefault(): #TODO alpha
    pass

def testHandleCmd(): #TODO alpha
    pass

def testProcessMsg(): #TODO alpha
    pass

def testParseReceive():
    signal.parseReceive()





def main():
    
    print("tests")
    # print(signal.helps)

    # testSend()
    # testSendGroup()
    # testAdminAlert()
    # testParseReceive()
    testGetGroupInfo()
    
    
    # todo



if __name__ == "__main__":
    main()
