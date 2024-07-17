# signal-info-bot

Welcome and info bot for signal groups based on [signal cli](https://github.com/AsamK/signal-cli)

## TODO
- [ ] MVP
  - [ ] parse commands
  - [ ] welcome message & command
  - [ ] default command (shows the default group name to members)
  - [ ] pulls command list and resps from json config file
  - [ ] help command 
    - [ ] basic help
    - [ ] group admin help
    - [ ] bot admin help
  - [ ] update command
  - [ ] admin, logging and alerts
  - [ ] dockerize
  - [ ] backup command and changes group chat
  - [ ] how to and readme
- [ ] everything else
  - [ ] secure remote config
  - [ ] multi groups
  - [ ] cron
  - [ ] group admins mass send
  
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