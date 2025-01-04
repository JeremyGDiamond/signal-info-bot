# signal-info-bot

Welcome and info bot for signal groups based on [signal cli](https://github.com/AsamK/signal-cli)
 
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
Run `make run` to build the conatiner and run it

Each make run will need to be linked to the singal account and the old one should be removed before a new one is made

Run `make restart` to restart an exiting containter and not need to relink everything



## Command Convention
All commands must be one word all lower case. The bot will have a default group if you want to use a differant group follow the command with the group name. update is more complicated see below for details.

## Welcome
Every group has a welcome message that will be sent to all new members and can be called with the welcome command

todo example

## Help
Every group has a help message that will be sent to all new members and can be called with the help command

todo example

## config files
todo
