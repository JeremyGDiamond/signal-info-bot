import subprocess
import json
import re
import time
import pprint

baseHelpMessage = "\
To use this bot send a command followed by a group name\n\
\n\
example: help group I'm in\n\
\n\
If no group is given the default group is used\n\
\n\
Command List\n\
help: show this message for the group\n\
welcome: show welcome message again\n\
default: show the default group name"


# signal class
class SignalObj:

    def __init__(self, configFileName):
        self.config = {}
        self.configFileName = configFileName

        self.readconfig()
        self.helps = {}
        self.genHelps()

    # needed becuse of shell injections
    def sanitizeMessage(self, message):
        
        # TODO`HOLY SHIT DO THIS BEFORE GOING PUBLIC !!!!!`

        return message
    
    def send(self, userId, message):
        subprocess.run(["signal-cli", "send", userId, "-m", self.sanitizeMessage(message)])
        

    def sendGroup(self, groupId, message):
        subprocess.run(["signal-cli", "send", "-g", groupId, "-m", self.sanitizeMessage(message)])
        
    def sendNTS(self, message):
        subprocess.run(["signal-cli", "send", "--note-to-self", "-m", self.sanitizeMessage(message)])

    def receive(self):
        output = subprocess.run(["signal-cli", "listGroups", "-d"], 
        # output = subprocess.run(["signal-cli", "receive"], # TODO
        capture_output=True, text=True)
        # print(output)
        return (output)
    
    def getGroupInfo(self):
        # TODO add refersh message to get inactive groups

        output = subprocess.run(["signal-cli", ""], 
        capture_output=True, text=True)
        print(output)
        return (output)

    # bot behaviors
    def readconfig(self):
       
        with open(self.configFileName) as configFile:
            self.config = json.load(configFile)
            # TODO: check validity of config: default, for each group id, help and welcome. Group names lower case.
            # print(self.config)

    def adminAlert(self, adminAlertMessage):
        # self.receive()
        if self.config["noteToSelfMode"]:
            self.sendNTS(adminAlertMessage)
        else:
            self.send(self.config["testDmId"], adminAlertMessage)

    def getGroupMembers(self, groupId):
        output = getGroupInfo(groupId)
        members = {}
        # todo some stuff

        return members
    
    def getGroupAdmins():
        output = getGroupInfo(groupId)
        admins = {}
        # some stuff

        return admins

    def error(self, userId, msg):
        self.send(userId, f"ERROR: {msg}")

    def welcome(self, userId, groupId):
        members = getGroupMembers(groupId)

        if userId in members:
            send(userId, config[groupId][welcomeMessage])

    def genHelps(self):

        groups = self.config["groups"]
        
        for grName, value in groups.items():
            
            grHelp = baseHelpMessage + "\n" + grName + " Commands - "
            for commKey,commValue in value["commands"].items():
                grHelp = grHelp + "\n" + commKey + ": " + commValue[1]
            
            self.helps[grName] = grHelp
        

    def sendHelp(self, userId, groupId):
        members = getGroupMembers(groupId)

        if userId in members:
            send(userId, config[groupId][welcomeMessage])

    def handleCmd(self, userId, msg):
        msg = msg.lower().strip().split()  # TODO: save group names in lower case in config
        if len(msg) == 1:
            groupName = self.config["default"]
            groupId = self.config["groups"][groupName]["grId"]
        else:
            groupName = " ".join(msg[1:])
            try:
                groupId = self.config["groups"][groupName]["grId"]
            except KeyError:
                self.error(userId, f"cannot find group with name '{groupName}'.")
                return

        if userId not in self.getGroupMembers(groupId):
            self.error(userId, f"cannot find group with name '{groupName}'.")
            return

        cmd = msg[0]
        if cmd == "help":
            self.helps[groupId]
        elif cmd not in self.config["groups"][groupName]["commands"]:
            self.error(userId, f"do not know command '{cmd}' for group '{groupName}'. Try help to get all possible commands.")
        else:
            res = self.config["groups"][groupName]["commands"][cmd]
            self.send(userId, res)

    def processMsg(self, msg: str):
        if msg == "": return
        if "Group info:\n" in msg: # Skip group messages
            print("skipping group message")
            return None

        try:
            senderId = re.search(r' .+ ([0-9a-z\-\+]+) \(device: ', msg)[1]
        except TypeError:
            print(msg)
            print("Error parsing message, could not find sender ID")
            return None

        # TODO: messages containing these words are skipped
        ignoreTypes = ["Group call update", "Reaction"]
        for ignoreType in ignoreTypes:
            if f"{ignoreType}:\n" in msg:
                print(f"Received {ignoreType} from {senderId}, skipping")
                return None
        cannotHandleTypes = ["Attachment", "Contacts", "Sticker", "Story reply"] # Story reply seems to be picture, location, audio?
        for cannotHandleType in cannotHandleTypes:
            if f"{cannotHandleType}:\n" in msg:
                # self.error(senderId, "I cannot handle this message type") # TODO uncomment
                return None

        if "Body: " not in msg:
            return None

        # TODO: multi-line messages (see ReceiveMesageHandler.printDataMessage)
        body = self.sanitizeMessage(msg.split("Body: ")[1].split("\n")[0])
        print(f"received message from {senderId}: {body}")

        self.handleCmd(senderId, body)

    def parseReceive(self):
        output = self.receive()
        # TODO: uncomment when ready to receive (comment above)
        # stdout = self.receive().stdout
        # if stdout.strip() == "":
        #     return
        # for msg in stdout.split("Envelope from:"):
        #     self.processMsg(msg)

        directMessages = []

        #list of touples command and groups
        commandList = []
        groupJoins = []
        # pp = pprint.PrettyPrinter()
        print(output)

        # todo dms to command list

        return commandList, groupJoins
