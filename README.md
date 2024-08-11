# signal-info-bot

Welcome and info bot for signal groups based on [signal cli](https://github.com/AsamK/signal-cli)

## TODO
- [ ] MVP
  - [ ] parse commands
  - [x] Welcome message & command
  - [x] default command (shows the default group name to members)
  - [x] pulls command list and resps from json config file
  - [-] help command
    - [x] basic help
  - [-] dockerize
    - [x] ubuntu image
    - [x] installs all deps
    - [x] copy files
    - [x] login to account if logged out
    - [x] run bot
    - [ ] persistent volume
  - [ ] multi groups
  
- [ ] beta
  - [ ] update command
  - [-] admin, logging and alerts
  - [-] how to and readme
  - [ ] group admin help
  - [ ] bot admin help
  

- [ ] release
  - [ ] secure remote config
  - [ ] backup command and changes group chat
  - [ ] cron
  - [ ] group admins mass send
  
## Setup

### Local
This project can be installed locally on any Linux distro with the [signal cli](https://github.com/AsamK/signal-cli). 
tested on ubuntu 22.04 and nixos.
It is recommended that you use a dedicated account for this bot.

1. Install dependencies
   - Install signal-cli: https://packaging.gitlab.io/signal-cli/installation/standalone/
   - Install qrencode: `sudo apt install qrencode`
2. Connect signal
   - Run `./linkAccount.sh` (and scan the QR code that is generated).
3. Setup your config file
   - make a copy of exampleConfig.json and rename it to config.json
   - modify config.json to meet the needs of your group (use signal-cli commands to get group id numbers)
   - repeat the above with testConfig.py
4. Run Tests
   - `python3 tests.py` and check the output and signal behaviors
4. Run Bot
   - `python3 main.py`

### Docker
 Todo

## Command Convention
All commands must be one word all lower case. The bot will have a default group if you want to use a differant group follow the command with the group name. update is more complicated see below for details.

## Welcome
Every group has a welcome message that will be sent to all new members and can be called with the welcome command

todo example

## Help
Every group has a help message that will be sent to all new members and can be called with the help command

todo example

## Update
Every command's output can be updated by group admins with the update command followed by the command to be updated. This will be followed by an ack of update mode. the contents of the follwoing message will overwrite the old respose. it is reccomened to call the command first so you have a copy of the command test.

todo example

## config files
todo
