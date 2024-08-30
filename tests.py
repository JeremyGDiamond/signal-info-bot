import signalpy
import subprocess
import json
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("testsDebug.log"),
        logging.StreamHandler()
    ]
)

signal = signalpy.SignalObj("testConfig.json", "testsDebug.log")

def passedTestPrint(name):
    logging.info(f"TEST:{name} PASSED")

def failedTestPrint(name, msg):
    logging.info(f"TEST:{name} FAILED, {msg}")

# test init

def testReadConfig(): #TODO alpha use exmapleConfig.json
    pass

def testGenGroups(): #TODO alpha use exmapleConfig.json
    pass

def testValidateConfigGroups(): #TODO alpha use exmapleConfig.json
    pass

def testGenHelps(): #TODO alpha use exmapleConfig.json
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
        logging.error(changes, len(message), len(sanitizedMessage))
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
    signal.send(signal.config["testDmId"], "bot: hardcoded test send function")
    passedTestPrint("testSend")

def testSendGroup():
    # signal.receive()
    signal.sendGroup(signal.config["admin"], signal.config["testGrId"], "bot: hardcoded test group send function")
    passedTestPrint("testSendGroup")

def testSendNTS():
    # signal.receive()
    signal.sendNTS("bot: hardcoded test sendNTS function")
    passedTestPrint("testSendNTS")

def testReceive(): #TODO check ret codes and contents 
    output = signal.receive()
    logging.info(output)
    passedTestPrint("testReceive")

def testListGroups(): #TODO check ret codes and contents
    output = signal.listGroups()
    logging.info(output)
    passedTestPrint("testListGroups")

# test bot behaviors
def testAdminAlert():
    signal.adminAlert("bot: test admin alert")
    passedTestPrint("testAdminAlert")

def testGetGroupMembers(): #TODO alpha use exmapleConfig.json
    output = signal.getGroupMembers(signal.config["default"])

    if len(output) != 0:
        passedTestPrint("testGetGroupMembers")
        return
    failedTestPrint("testGetGroupMembers")

def testGetGroupAdmins(): #TODO alpha use exmapleConfig.json
    output = signal.getGroupAdmins(signal.config["default"])

    if len(output) != 0:
        passedTestPrint("testGetGroupAdmins")
        return
    failedTestPrint("testGetGroupAdmins")

def testError():
    signal.error(signal.config["admin"], "bot: hardcoded test of the error function")
    passedTestPrint("testError")

def testAuth():
    if signal.authenticate(signal.config["admin"]):
        passedTestPrint("testAuth")
        return
    failedTestPrint("testAuth")    

def testAuthGroup(): #TODO alpha use exmapleConfig.json
    if signal.authenticateGroup(signal.config["admin"], signal.config["testGrId"]):
        passedTestPrint("testAuthGroup")
        return
    failedTestPrint("testAutGroup")   

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
    
    logging.info("signalpi Tests")

    # san tests
    passSan()
    failEachBlockedChar()

    # send receive and list groups tests

    testSend()
    testSendGroup()
    testSendNTS()
    testAdminAlert()
    testReceive()
    testListGroups()

    # group info tests
    testGetGroupMembers()
    testGetGroupAdmins()




    #test error and auth
    testError()
    testAuth()
    testAuthGroup()


    # testParseReceive()
    # testGetGroupInfo()
    
    
    # todo



if __name__ == "__main__":
    main()
