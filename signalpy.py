import subprocess
import json
import re
import time
import logging


ACTIVE_REFRESH = 60 * 5  # Max sec between active refresh (with interaction) TODO discuss: placeholder
PASSIVE_REFRESH = 60 * 60  # Max sec between passive refresh (without any interaction) TODO discuss: placeholder
assert ACTIVE_REFRESH < PASSIVE_REFRESH

baseHelpMessage = "\
To use this bot send a command followed by a group name\n\
\n\
example: help group I am in\n\
\n\
If no group is given the default group is used\n\
\n\
---Command List---\n\
help: show this message for the group\n\
welcome: show welcome message again\n\
default: show the default group name"

def loggerConfig(logFileName):
    #configure logger to write to console and file
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(logFileName),
            logging.StreamHandler()
        ]
    )


# signal class
class SignalObj:

    def __init__(self, configFileName, logFileName):
        loggerConfig(logFileName)

        self.config = {}
        self.configFileName = configFileName
        self.readconfig()

        self.groups = {}  # grId: { "name": str, "members": list[str], "admins": list[str] }
        self.groupsTimeStamp = 0
        self.genGroups()
        self.validateConfigGroups()

        self.helps = {}  # { grId: helpText }
        self.genHelps()

        self.commandInjectionBlockChars = []
        self.commandInjectionBlockStrings = []
    
    # needed becuse of shell injections
    def sanitizeMessage(self, message):
        
        # remove offending chars
        changes = 0
        newMessage = ""

        for c in message: 
            if c.isalnum():
                newMessage += c
            elif c == ".":
                newMessage += "\uA4F8"
            elif c == " ":
                newMessage += "\u2008"
            elif c == ":":
                newMessage += " \u02F8"
            elif c == ",":
                newMessage += "\u201A"
            elif c == "\"":
                newMessage += "\uFF02"
            elif c == "-":
                newMessage += "\u2013"
            elif c == "\n":
                newMessage += "\n"
            else:
                changes = changes+1
            
        
        
        # send an error if there were any changes
        if changes != 0:
            
            errorMessage = f"Error: sanitizer caught {changes} changes see log"
            logging.error(f"sanitizer caught {changes} msg: {message}")
            
            self.adminAlert(errorMessage)
        
        return newMessage, changes
    
    def send(self, userId, message):
        if self.authenticate(userId):
            sanitizedMessage, changes = self.sanitizeMessage(message)
            if len(sanitizedMessage) != 0:
                subprocess.run(["signal-cli", "send", userId, "-m", sanitizedMessage], shell=False)
        
    def sendGroup(self, userId, grId, message):
        # TODO alpha authenticate group?

        if self.authenticateGroup(userId, grId):
            sanitizedMessage, changes = self.sanitizeMessage(message)
            if len(sanitizedMessage) != 0:
                subprocess.run(["signal-cli", "send", "-g", grId, "-m", sanitizedMessage], shell=False)
        
    def sendNTS(self, message):
        sanitizedMessage, changes = self.sanitizeMessage(message)
        if len(sanitizedMessage) != 0:
                subprocess.run(["signal-cli", "send", "--note-to-self", "-m", sanitizedMessage], shell=False)

    def receive(self):
        output = subprocess.run(["signal-cli", "receive"],
        capture_output=True, text=True, shell=False)
        return (output)

    def listGroups(self):
        output = subprocess.run(["signal-cli", "listGroups", "-d"],
        capture_output=True, text=True, shell=False)
        self.groupsTimeStamp = time.time()

        return (output)

    # Init functions
    def readconfig(self):
        with open(self.configFileName) as configFile:
            self.config = json.load(configFile)

            # Check default
            if "default" not in self.config.keys():
                logging.warning("no default set in config")
            grIdDefault = self.config["default"]
            if grIdDefault not in self.config["groups"]:
                logging.error(f"default group with id={grIdDefault} not in config[\"groups\"]")
                self.config["groups"][grIdDefault] = {}
                self.config["groups"][grIdDefault]["welcomeMessage"] = ""
                self.config["groups"][grIdDefault]["commands"] = {}

            

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
        configGroups = self.config["groups"]
        for grId in configGroups:
            if grId not in self.groups.keys():
                logging.warning(f"bot does not have access to group with id={grId} from config, skipping")  # TODO discuss: how to handle groups in config bot does not have access to
                continue
            grName = self.groups[grId]["name"]
            if "welcomeMessage" not in configGroups[grId].keys():
                configGroups[grId]["welcomeMessage"] = ""
                logging.warning(f"no Welcome Message set for group {grName} id={grId}")
            if "commands" not in configGroups[grId].keys() or len(configGroups[grId]["commands"]) == 0:
                configGroups[grId]["commands"] = {}
                logging.warning(f"no commands set for group \"{grName}\" id={grId}")

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
        welcomes = {}
        for res_group in res_groups:
            
            if res_group.strip() == "": continue

            re_res = re.search(group_re, res_group)
            if re_res is None:
                logging.warning(f"could not parse group \"{res_group}\"")
                continue
            grId, name, _, active, members, admins = re_res.groups()
            # Only process groups that are in config
            if grId not in self.config["groups"].keys():
                continue

            # Deal with inactive groups
            if active == "false":
                # TODO COMMMENT OUT THE FOLLOWING LINE WHEN TESTING WITH PERSONAL ACCOUNT
                self.activateGroup(userid, grId) #TODO uncomment when running for real
                continue

            # Skip invalid groups
            if members == "[]": continue
            if name == "null": continue

            name = name.lower().strip()
            members = members[1:-1].split(", ")
            admins = admins[1:-1].split(", ")

            if name in new_groups.keys():
                logging.error(f"bot has access to multiple groups with name={name}")
                continue
                # TODO: how to handle this, now only the first group is handled.
            new_members = {}
            if grId in self.groups.keys():
                # Send welcome message to new members
                new_members = set(members) - set(self.groups[grId]["members"])
                welcomes[grId] = new_members
                
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

        for grId, new_members in welcomes.items():
            if self.config["groups"][grId]["welcomeMessage"] != "":
                for new_member in new_members:
                    self.sendWelcome(new_member, grId)
            else:
                logging.info(f"did not send {len(new_members)} welcome message for group {name} with id={grId} because welcome message is empty")

    
    def genHelps(self):
        """Generates the help text for each group based on its commands."""
        configGroups = self.config["groups"]

        for grId, value in configGroups.items():
            try:
                grName = self.groups[grId]["name"]
            except KeyError:
                continue  # Bot does not have access to group with given id.

            grHelp = baseHelpMessage + "\n--\"" + grName + "\" Commands--"
            for commKey, commValue in value["commands"].items():
                cutOff = "..."
                if len(commValue) > 50:
                    cutOff = "..."
                grHelp = grHelp + "\n  " + commKey + ": " + commValue[:50] + cutOff

            self.helps[grId] = grHelp

    # bot behaviors
    def adminAlert(self, adminAlertMessage):
        # self.receive()
        if self.config["noteToSelfMode"]:
            self.sendNTS(adminAlertMessage)
        else:
            self.send(self.config["admin"], adminAlertMessage)

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
        Check whether user has access to bot, i.e. is a member if the default
        group.

        NOTE: this bakes if the user is in your contact list and you use ACIin the config file
        """
        configGrId = self.config["default"]
        membersDefault = self.groups[configGrId]["members"]

        

        if userId in membersDefault:
            return True

        logging.info(f"could not authenticate user with id={userId}")
        return False
    
    def authenticateGroup(self, userId, grId) -> bool:
        """
        Check whether user has access to the group bot.
        
        """
        membersDefault = self.groups[grId]["members"]

        if userId in membersDefault:
            return True

        logging.error(f"could not authenticate user with id={userId} for group id={grId}")
        logging.error(f"membersDefault {membersDefault}")
        return False
    
    def sendError(self, userId, msg):
       self.send(userId, f"ERROR: {msg}")
    
    def sendWelcome(self, userId, grId):
        members = self.getGroupMembers(grId)
        if userId in members:
            self.send(userId, self.config["groups"][grId]["welcomeMessage"])

    def activateGroup(self, userId, grId):
        """
        Sends a message to the given group to make it active again.
        Groups become inactive when there has been no activity for a certain period of time.
        """
        activationMsg = "bot: This is an activation message, you can ignore it."

        self.sendGroup(userId, grId, activationMsg)

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
                self.sendError(userId, "sorry I'm having some problems, please specify a group name.")
                logging.error(f"bot does not have access to default group with id={grId}")
                # TODO: alert admin?
        else:
            grName = " ".join(msg[1:]).lower().strip()
            configGroups = self.config["groups"]
            grId = None
            for id in configGroups.keys():
                if self.groups[id]["name"] == grName:
                    grId = id

            if grId is None:
                self.sendError(userId, f"cannot find group with that name.")
                return

        members = self.getGroupMembers(grId)
        if members is None or userId not in members:
            self.sendError(userId, f"cannot find group with name name.")
            return

        cmd = msg[0].lower().strip()
        if cmd == "help":
            self.sendHelp(userId, grId)
        elif cmd == "default":
            self.sendDefault(userId)
        elif cmd == "welcome":
            self.sendWelcome(userId, grId)
        elif cmd not in self.config["groups"][grId]["commands"]:
            self.sendError(userId, f"do not know that command for this group. Try help \"group name\" to get all possible commands.")
        else:
            res = self.config["groups"][grId]["commands"][cmd]
            self.send(userId, res)

    def processMsg(self, msg: str):
        if msg == "": return None
        # Skip group messages
        if "Group info:\n" in msg: return None

        try:
            # Extracts user ID from message, searches for a space, then the username
            # (“.+” in the regex) followed by a space and the user ID (which can
            # be a user's phone number) of the sender made up of numbers, 
            # lowercase letters, - and + ([0-9a-z\-\+]+ in the regex), followed by
            # (device:.
            # Example: " “user123 (some info)” x1z345a6-789b-1234-c56d-7891e2fg345h (device: "
            senderId = re.search(r' “.+” ([0-9a-z\-\+]+) \(device: ', msg)[1]
        except TypeError:
            logging.error(f"could not parse message, could not find sender ID, message=\"{msg}\"")
            return None

        if not self.authenticate(senderId):
            return None

        # TODO: messages containing these words are skipped now, change this
        ignoreTypes = ["Group call update", "Reaction"]
        for ignoreType in ignoreTypes:
            if f"{ignoreType}:\n" in msg:
                logging.info(f"received {ignoreType} from {senderId}, skipping")
                return None
        cannotHandleTypes = ["Attachment", "Contacts", "Sticker", "Story reply"] # Story reply seems to be picture, location, audio?
        for cannotHandleType in cannotHandleTypes:
            if f"{cannotHandleType}:\n" in msg:
                self.sendError(senderId, "I cannot handle this message type") # TODO uncomment
                return None

        if "Body: " not in msg:
            return None

        # TODO: multi-line messages (see ReceiveMesageHandler.printDataMessage)
        body = msg.split("Body: ")[1].split("\n")[0]
        logging.debug(f"received msg from {senderId}: {body}")

        self.handleCmd(senderId, body)
    
    

    def parseReceive(self):
        rcv_stdout = self.receive().stdout
        if rcv_stdout.strip() == "":
            return
        # TODO: uncomment. When you receive after a long time of not receiving, I'm pretty sure you'll receive everything since the last time, so don't uncomment following two lines before running once without them
        for msg in rcv_stdout.split("Envelope from:"):
            self.processMsg(msg)

        # Passive refresh
        if self.groupsTimeStamp - time.time() > PASSIVE_REFRESH:
            self.genGroups()

        return
