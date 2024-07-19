import subprocess
import json
import time
import pprint

# signal class
class SignalObj:

    def __init__(self, configFileName):
        self.config = {}
        self.configFileName = configFileName

        self.readconfig()
        self.helps = {}
        self.genHelps()

    # needed becuse of shell injections
    def sanitizeMessage(message):

        # TODO`HOLY SHIT DO THIS BEFORE GOING PUBLIC !!!!!`

        return message

    def send(self, id, message):
        subprocess.run(["signal-cli", "send", id, "-m", sanitizeMessage(message)])


    def sendGroup(self, id, message):
        subprocess.run(["signal-cli", "send", "-g", id, "-m", sanitizeMessage(message)])

    def sendNTS(self, message):
        subprocess.run(["signal-cli", "send", "--note-to-self", "-m", sanitizeMessage(message)])

    def receive(self):
        output = subprocess.run(["signal-cli", "receive"],
        capture_output=True, text=True)
        print(output)
        return (output)

    def getGroupInfo(self):
        pass


    # bot behaviors
    def readconfig(self):

        with open(self.configFileName) as configFile:
            self.config = json.load(configFile)
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

    def welcome(self, userId, groupId):
        members = getGroupMembers(groupId)

        if userId in members:
            send(userId, config[groupId][welcomeMessage])

    def genHelps(self):

        baseMessage = ''' To use this bot send a command follwoed by a group name

                        example: help group i'm in

                        If no group is given the default group is used

                        Command List -
                        help: show this message for the group
                        welcome: show welcome message again
                        default: show the default group name
                        '''
        for key, value in self.config["groups"].items():
            grHelp = baseMessage + "\n" + value["grName"] + " Commands - "
            for commKey,commValue in value["commands"].items():
                grHelp + "\n" + commKey + ": " + commValue

            self.helps[key] = grHelp
            print(self.helps[key])



    def parseReceive(self):
        output = self.receive()
        directMessages = []

        # list of touples command and groups
        commandList = []
        groupJoins = []
        # pp = pprint.PrettyPrinter()
        print(output)

        # todo dms to command list

        return commandList, groupJoins
