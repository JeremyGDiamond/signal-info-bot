import signalpy
import subprocess
import json
import time

signal = signalpy.SignalObj("testConfig.json")

def passedTestPrint(name):
    print(f"TEST:{name} PASSED")

def failedTestPrint(name, msg):
    print(f"TEST:{name} FAILED, {msg}")

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
    message0 = "ThisMessageShouldBeTheSame1234567890" #alpha num
    message1 = "ThisMessageShouldEndWithAConfused." #test .
    message2 = "ThisMessageShouldEndWithAConfusedSpace " #test space
    message3 = "ThisMessageShouldEndWithAConfused:" #test :
    message4 = "ThisMessageShouldEndWithAConfused," #test ,

    sanitizedMessage, changes = signal.sanitizeMessage(message0)
    if not (sanitizedMessage == message0):
        failedTestPrint("passSan", "ERROR message0 mismatch")
        return
    
    sanitizedMessage, changes = signal.sanitizeMessage(message1)
    if (sanitizedMessage == message1 or ord(sanitizedMessage[-1]) != 42232):
        failedTestPrint("passSan", "ERROR message1 mismatch")
        return
        
    sanitizedMessage, changes = signal.sanitizeMessage(message2)
    if (sanitizedMessage == message2 or ord(sanitizedMessage[-1]) != 8200):
        failedTestPrint("passSan", "ERROR message2 mismatch")
        return
    
    sanitizedMessage, changes = signal.sanitizeMessage(message3)
    if (sanitizedMessage == message3 or ord(sanitizedMessage[-1]) != 760):
        failedTestPrint("passSan", "ERROR message3 mismatch")
        return
    
    sanitizedMessage, changes = signal.sanitizeMessage(message4)
    if (sanitizedMessage == message4 or ord(sanitizedMessage[-1]) != 8218):
        failedTestPrint("passSan", "ERROR message4 mismatch")
        return

    passedTestPrint("passSan")


def failEachBlockedChar(): #TODO alpha
    message = "~!@#$%^&*())))))_+`-=\u0009\\{\\}|[]\\;'\"<>?/"
    sanitizedMessage, changes = signal.sanitizeMessage(message)
    if changes != len(message) and len(sanitizedMessage) != 0:
        print(changes, len(message), len(sanitizedMessage))
        failedTestPrint("failEachBlockedChar", "blocked char mismatch")
        return
    
    passedTestPrint("failEachBlockedChar")

    

def failEachBlockedStrings(): #TODO beta
    pass

def failEachTestCommand(): #TODO beta
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
    
    print("signalpi Tests")

    # san tests
    passSan()
    failEachBlockedChar()


    # print(signal.helps)

    # testSend()
    # testSendGroup()
    # testAdminAlert()
    # testParseReceive()
    # testGetGroupInfo()
    
    
    # todo



if __name__ == "__main__":
    main()
