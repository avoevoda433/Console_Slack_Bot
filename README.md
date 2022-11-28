# Slack-App
Slack-App is a bot that uses the Slack API and can send and delete messages in a channel.

## Table of contents
* [Installation](#installation)
* [Usage](#usage)
* [Uninstallation](#uninstallation)
### Author
[Alexey Voevoda](https://github.com/avoevoda433)

## Installation
[Download](https://github.com/iba-gomel-students/avayavoda-python-be/archive/refs/heads/task_2.zip)
archive. Unpack app following commands.
```bash
sudo unzip avayavoda-python-be-task_2.zip
cd avayavoda-python-be-task_2/task_2
sudo python3 setup.py build 
sudo python3 setup.py install --record files.txt
```


## Usage
Use follow command and run app:
```bash
sudo message_slack_bot -some_flag
```
List of available flags:

``` -n, --new ['your_bot_token'] ['your_bot_name'] ['your_channel_id'] [your_channel_name'] ``` - set needed credential for app work (use quotes ' ' for data input)

```-s, --send [some message]``` - send message in channel

```-d, --delete``` - delete last message

```-da, --delete_all``` - delete all messages

```-h, --help``` - info about flags

You may receive the following messages after executing the command:
* *SUCCESS* - your command successfully executed
* *WARNING* - your command isn't executed in a specific case 
* *FAILED* - your command failed due to a technical error 

## Uninstallation
You can uninstall app following command:
```bash
# Open app directory 
cd avayavoda-python-be-task_2/task_2
sudo pip3 uninstall Slack-App
sudo bash -c "cat files.txt | xargs rm -rf"
```
