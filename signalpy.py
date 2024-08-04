import subprocess
import json
import re
import time
import logging
import pprint

ACTIVE_REFRESH = 60 * 5  # Max sec between active refresh (with interaction) TODO discuss: placeholder
PASSIVE_REFRESH = 60 * 60  # Max sec between passive refresh (without any interaction) TODO discuss: placeholder
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

        self.groups = {}  # grId: { "name": str, "members": list[str], "admins": list[str] }
        self.groupsTimeStamp = 0
        self.genGroups()
        self.validateConfigGroups()

        self.readconfig()
        self.helps = {}  # { grId: helpText }
        self.genHelps()

    # needed becuse of shell injections
    def sanitizeMessage(self, message):
        
        # TODO`HOLY SHIT DO THIS BEFORE GOING PUBLIC !!!!!`

        return message
    
    def send(self, userId, message):
        # TODO: check if sanitized message is empty?
        if self.authenticate(userId):
            subprocess.run(["signal-cli", "send", userId, "-m", self.sanitizeMessage(message)])
        
    def sendGroup(self, grId, message):
        # TODO: check if sanitized message is empty?
        # TODO authenticate group?
        subprocess.run(["signal-cli", "send", "-g", grId, "-m", self.sanitizeMessage(message)])
        
    def sendNTS(self, message):
        # TODO: check if sanitized message is empty?
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

            # Check default
            if "default" not in self.config.keys():
                logging.warning("no default set in config")
            grIdDefault = self.config["default"]
            if grIdDefault not in self.config["groups"]:
                logging.error(f"default group with id={grIdDefault} not in config[\"groups\"]")
                self.config["groups"][grIdDefault]["welcomeMessage"] = ""
                self.config["groups"][grIdDefault]["commands"] = {}

            # print(self.config)

    def validateConfigGroups(self):
        """
        Validate config["groups"].
        NOTE: does not check whether bot has access to all groups in the config.
        """
        # Check default
        grIdDefault = self.config["default"]
        if grIdDefault not in self.groups.keys():
            logging.error(f"bot does not have access to default group with id={grIdDefault}")

        # Check groups
        groups = self.config["groups"]
        invalid_groups = []
        for grId in groups:
            if grId not in self.groups.keys():
                logging.warning(f"bot does not have access to group with id={grId} from config, skipping")  # TODO discuss: how to handle groups in config bot does not have access to
                continue
            grName = groups[grId]["name"]
            if "welcomeMessage" not in groups[grId].keys():
                groups[grId]["welcomeMessage"] = ""
                logging.warning(f"no Welcome Message set for group {grName} id={grId}")
            if "commands" not in groups[grId].keys() or len(groups[grId]["commands"]) == 0:
                groups[grId]["commands"] = {}
                logging.warning(f"no commands set for group {grName} id={grId}")

        # Remove invalid groups
        for invalid_group in invalid_groups:
            del groups[invalid_group]

    def adminAlert(self, adminAlertMessage):
        # self.receive()
        if self.config["noteToSelfMode"]:
            self.sendNTS(adminAlertMessage)
        else:
            self.send(self.config["testDmId"], adminAlertMessage)

    def getGroupMembers(self, grId):
        self.genGroups()

        try:
            return self.groups[grId]["members"]
        except KeyError:
            return None

    def getGroupAdmins(self, grId):
        self.genGroups()

        try:
            return self.groups[grId]["admins"]
        except KeyError:
            return None

    def authenticate(self, userId) -> bool:
        """
        Check whether user has access to bot.
        TODO discuss: when does a user have access to the bot?
                        For now: has to be member of the default group.
        """
        configGrId = self.config["default"]
        membersDefault = self.groups[configGrId]["members"]

        logging.info(f"could not authenticate user with id={userId}")

        return (userId in membersDefault)

    def error(self, userId, msg):
        self.send(userId, f"ERROR: {msg}")

    def sendWelcome(self, userId, grId):
        members = self.getGroupMembers(grId)

        if userId in members:
            self.send(userId, self.config[grId]["welcomeMessage"])

    def genHelps(self):
        """Generates the help text for each group based on its commands."""
        configGroups = self.config["groups"]

        for grId, value in configGroups.items():
            try:
                grName = self.groups[grId]["name"]
            except KeyError:
                continue  # Bot does not have access to group with given id.

            grHelp = baseHelpMessage + "\n" + grName + " Commands - "
            for commKey,commValue in value["commands"].items():
                grHelp = grHelp + "\n" + commKey + ": " + commValue[1]

            self.helps[grId] = grHelp

    def genGroups(self):
        """
        Retrieves name, members and admins for each group the bot has access to.
        NOTE: group names are stored lower case.
        TODO discuss: how to deal with duplicate group names
        TODO discuss: how to deal with groups bot has lost access to
        """
        # Return if not time for active refresh.
        if time.time() - self.groupsTimeStamp < ACTIVE_REFRESH:
            return

        res = self.listGroups().stdout
        res_groups = res.split("Id: ")

        group_re = r"(.+) Name: (.+) Description: (.|\n)* Active: (true|false) .+ Members: (\[.*\]) Pending members: .+ Admins: (\[.*\]) Banned: "
        new_groups = {}
        for res_group in res_groups:
            if res_group.strip() == "": continue

            re_res = re.search(group_re, res_group)
            if re_res is None:
                logging.warning(f"could not parse group \"{res_group}\"")
                continue
            grId, name, _, active, members, admins = re_res.groups()

            # Only process groups that are in config
            if grId not in self.config["groups"].keys(): continue

            # Skip inactive groups
            if active == "false": continue
            if members == "[]": continue
            if name == "null": continue

            name = name.lower().strip()
            members = members[1:-1].split(", ")
            admins = admins[1:-1].split(", ")

            if name in new_groups.keys():
                logging.error(f"bot has access to multiple groups with name={name}")
                continue
                # TODO: how to handle this, now only the first group is handled.

            if grId in self.groups.keys():
                # Send welcome message to new members
                new_members = set(members) - set(self.groups[grId]["members"])
                if self.config["groups"][grId]["welcomeMessage"] != "":
                    for new_member in new_members:
                        self.sendWelcome(new_member, grId)
                else:
                    logging.info(f"did not send {len(new_members)} welcome message for group {name} with id={grId} because welcome message is empty")

            new_groups[grId] = {
                "name": name,
                "members": members,
                "admins": admins,
            }

        # Check if bot has lost access to groups.
        accessLostGrIds = set(self.groups.keys()) - set(new_groups.keys())
        for grId in accessLostGrIds:
            grName = self.groups[grId]["name"]
            logging.info(f"bot has lost access to group {grName} with id={grId}")

        self.groups = new_groups

    def sendHelp(self, userId, grId):
        members = self.getGroupMembers(grId)

        if userId in members:
            self.send(userId, self.helps[grId])

    def sendDefault(self, userId):
        defaultGrId = self.config["default"]
        members = self.getGroupMembers(defaultGrId)

        if userId in members:
            grName = self.groups[defaultGrId]["name"]
            self.send(userId, f"\"{grName}\" is the default group.")

    def handleCmd(self, userId, msg):
        msg = msg.lower().strip().split()
        if len(msg) == 1:  # TODO: assuming one-word commands!
            grId = self.config["default"]
            try:
                grName = self.groups[grId]["name"]
            except KeyError:  # Bot does not have access to group
                self.error(userId, "sorry I'm having some problems, please specify a group name.")
                logging.error(f"bot does not have access to default group with id={grId}")
                # TODO: alert admin?
        else:
            grName = " ".join(msg[1:]).lower().strip()
            configGroups = self.config["groups"]
            grId = None
            for id in configGroups.keys():
                if self.groups[grId]["name"] == grName:
                    grId = id

            if grId is None:
                self.error(userId, f"cannot find group with name '{grName}'.")
                return

        members = self.getGroupMembers(grId)
        if members is None or userId not in members:
            self.error(userId, f"cannot find group with name '{grName}'.")
            return

        cmd = msg[0]
        if cmd == "help":
            self.sendHelp(userId, grId)
        elif cmd == "default":
            self.sendDefault(userId)
        elif cmd not in self.config["groups"][grId]["commands"]:
            self.error(userId, f"do not know command '{cmd}' for group '{grName}'. Try help to get all possible commands.")
        else:
            res = self.config["groups"][grId]["commands"][cmd]
            self.send(userId, self.sanitizeMessage(res))

    def processMsg(self, msg: str):
        if msg == "": return
        if "Group info:\n" in msg: # Skip group messages
            print("skipping group message")  # TODO: remove (debug)
            return None

        try:
            senderId = re.search(r' .+ ([0-9a-z\-\+]+) \(device: ', msg)[1]
        except TypeError:
            logging.error(f"could not parse message, could not find sender ID, message=\"{msg}\"")
            return None

        if not self.authenticate(senderId):
            return

        # TODO: messages containing these words are skipped now, change this
        ignoreTypes = ["Group call update", "Reaction"]
        for ignoreType in ignoreTypes:
            if f"{ignoreType}:\n" in msg:
                logging.info(f"received {ignoreType} from {senderId}, skipping")
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
        print(f"received message from {senderId}: {body}")  # TODO: remove (debug)

        self.handleCmd(senderId, body)

    def parseReceive(self):
        output = self.receive()
        # TODO: uncomment when ready to receive (comment out above line)
        # NOTE: when you receive after a long time of not receiving, I'm pretty sure you'll receive everything since the last time, so maybe disable all parsing etc at first.
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
