import subprocess
import json
import time

# signal class
class SignalObj:

    def __init__(self, configFileName):
        self.config = {}
        self.configFileName = configFileName

        self.readconfig()

    def send(self, id, message):
        subprocess.run(["signal-cli", "send", id, "-m", message])
        

    def sendGroup(self, id, message):
        subprocess.run(["signal-cli", "send", "-g", id, "-m", message])
        
    def sendNTS(self, message):
        subprocess.run(["signal-cli", "send", "--note-to-self", "-m", message])

    def receive(self):
        output = subprocess.run(["signal-cli", "receive"], capture_output=True)
        # print(output)
        return (output)
    
    def getGroupInfo(self):
        pass


    # bot behaviors
    def readconfig(self):
        # todo not working cus of scope i don't care enough right now
        with open(self.configFileName) as configFile:
            self.config = json.load(configFile)
            # print(self.config)

    def adminAlert(self, adminAlertMessage):
        self.receive()
        if self.config["noteToSelfMode"]:
            self.sendNTS(adminAlertMessage)
        else:
            self.send(self.config["testDmId"], adminAlertMessage)


    def getGroupMembers():
        pass

    def verfiyPrivs():
        pass

    def welcome():
        pass

    def parseReceive():
        pass

    def sanitizeMessage():
        pass