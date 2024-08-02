import subprocess
import json
import re
import time
import pprint

# TODO: keys in config.groups group ID instead of group names

ACTIVE_REFRESH = 60 * 5  # Max sec between active refresh (with interaction) TODO placeholder
PASSIVE_REFRESH = 60 * 60  # Max sec between passive refresh (without any interaction) TODO placeholder
assert ACTIVE_REFRESH < PASSIVE_REFRESH

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

        self.groups = {} # <GroupID>: { name: str, members: list[str], admins: list[str] }
        self.groupsTimeStamp = time.time()
        self.genGroups()

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
        output = self.listGroups()
        # output = subprocess.run(["signal-cli", "receive"], # TODO
        # capture_output=True, text=True) # TODO
        # print(output)
        return (output)

    def listGroups(self):
        output = subprocess.run(["signal-cli", "listGroups", "-d"],
        capture_output=True, text=True)
        self.groupsTimeStamp = time.time()

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

            # Check validity of config.
            if "default" not in self.config.keys():
                print("WARNING: no default set")
            groups = self.config["groups"]
            invalid_groups = []
            for group in groups:
                if "grId" not in groups[group].keys() or groups[group]["grId"].strip() == "":
                    print(f"WARNING: no ID set for group {group}, removing group")
                    invalid_groups.append(group)
                    continue
                if "welcomeMessage" not in groups[group].keys():
                    groups[group]["welcomeMessage"] = ""
                    print(f"WARNING: no Welcome Message set for group {group}")
                if "commands" not in groups[group].keys() or len(groups[group]["commands"]) == 0:
                    groups[group]["commands"] = {}
                    print(f"WARNING: no commands set for group {group}")

            # Remove invalid groups
            for invalid_group in invalid_groups:
                del groups[invalid_group]

            # print(self.config)

    def adminAlert(self, adminAlertMessage):
        # self.receive()
        if self.config["noteToSelfMode"]:
            self.sendNTS(adminAlertMessage)
        else:
            self.send(self.config["testDmId"], adminAlertMessage)

    def getGroupMembers(self, groupId):
        self.genGroups()

        try:
            return self.groups[groupId]["members"]
        except KeyError:
            return None

    def getGroupAdmins(self, groupId):
        self.genGroups()

        try:
            return self.groups[groupId]["admins"]
        except KeyError:
            return None

    def error(self, userId, msg):
        self.send(userId, f"ERROR: {msg}")

    def welcome(self, userId, groupId):
        members = self.getGroupMembers(groupId)

        if userId in members:
            self.send(userId, self.config[groupId]["welcomeMessage"])

    def genHelps(self):

        configGroups = self.config["groups"]
        
        for grName, value in configGroups.items():
            
            grHelp = baseHelpMessage + "\n" + grName + " Commands - "
            for commKey,commValue in value["commands"].items():
                grHelp = grHelp + "\n" + commKey + ": " + commValue[1]
            
            self.helps[grName] = grHelp

    def genGroups(self):
        # Return if not time for active refresh.
        if time.time() - self.groupsTimeStamp < ACTIVE_REFRESH:
            return

        res = self.listGroups().stdout
        res_groups = res.split("Id: ")

        group_re = r"(.+) Name: (.+) Description: (.|\n)* Active: (true|false) .+ Members: (\[.*\]) Pending members: .+ Admins: (\[.*\]) Banned: "
        for res_group in res_groups:
            if res_group.strip() == "": continue

            re_res = re.search(group_re, res_group)
            if re_res is None:
                print(f"WARNING: could not parse group {res_group}")
                continue
            groupId, name, _, active, members, admins = re_res.groups()

            # Skip inactive groups
            if active == "false": continue
            if members == "[]": continue
            if name == "null": continue

            members = members[1:-1].split(", ")
            admins = admins[1:-1].split(", ")

            if groupId in self.groups.keys():
                # Send welcome message to new members
                new_members = set(members) - set(self.groups[groupId]["members"])
                for new_member in new_members:
                    self.welcome(new_member, groupId)

                self.groups[groupId]["name"] = name
                self.groups[groupId]["members"] = members
                self.groups[groupId]["admins"] = admins
            else:
                self.groups[groupId] = {
                    "name": name,
                    "members": members,
                    "admins": admins,
                }

    def sendHelp(self, userId, groupId):
        members = getGroupMembers(groupId)

        if userId in members:
            send(userId, config[groupId][welcomeMessage])

    def handleCmd(self, userId, msg):
        msg = msg.lower().strip().split()  # TODO: save group names in lower case in config
        if len(msg) == 1:  # TODO: assuming one-word commands!
            groupName = self.config["default"]
            groupId = self.config["groups"][groupName]["grId"]
        else:
            groupName = " ".join(msg[1:])
            try:
                groupId = self.config["groups"][groupName]["grId"]
            except KeyError:
                self.error(userId, f"cannot find group with name '{groupName}'.")
                return

        members = self.getGroupMembers(groupId)
        if members is None or userId not in members:
            self.error(userId, f"cannot find group with name '{groupName}'.")
            return

        cmd = msg[0]
        if cmd == "help":
            self.send(userId, self.helps[groupId])
        elif cmd not in self.config["groups"][groupName]["commands"]:
            self.error(userId, f"do not know command '{cmd}' for group '{groupName}'. Try help to get all possible commands.")
        else:
            res = self.config["groups"][groupName]["commands"][cmd]
            self.send(userId, self.sanitizeMessage(res))

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

        # Passive refresh
        if self.groupsTimeStamp - time.time() > PASSIVE_REFRESH:
            self.genGroups()

        return commandList, groupJoins
