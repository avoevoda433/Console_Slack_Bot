from message_slack_bot.app.app import SlackBot
from message_slack_bot.menu.menu import Menu
from message_slack_bot.app.app import CredsNames
from message_slack_bot.app.app import Events
from dotenv import load_dotenv, dotenv_values
import argparse
import os

load_dotenv('.env')
command_parser = argparse.ArgumentParser()


def _parse_args():
    command_parser.add_argument("-n", "--new", nargs=4, type=str, required=False)
    command_parser.add_argument("-s", "--send", nargs="+", type=str, required=False)
    command_parser.add_argument("-d", "--delete", action="store_true", required=False)
    command_parser.add_argument("-da", "--delete_all", action="store_true", required=False)
    return command_parser.parse_args()


def _set_creds(parameters: list):
    try:
        f = open('.env', 'w')
        for name, parameter in zip(list(e.name for e in CredsNames), parameters):
            f.write(f"{name}='{parameter}'\n")
        f.close()
        return "".join([Events.SUCCESS.value, Events.SET_CREDS.value])
    except FileNotFoundError:
        return "".join([Events.FAILED.value, Events.SET_CREDS_ERROR.value])


def main():
    args = _parse_args()
    if args.new:
        print(_set_creds(args.new))
    elif dotenv_values('.env'):
        # Create the SlackBot object with access to the Slack API
        app = SlackBot(os.environ[CredsNames.BOT_TOKEN.name],
                       os.environ[CredsNames.BOT_NAME.name],
                       os.environ[CredsNames.CHANNEL_ID.name],
                       os.environ[CredsNames.CHANNEL_NAME.name])

        # Available commands
        options = (app.send_message,
                   app.delete_message,
                   app.delete_all_messages)

        # Create Menu object
        slack_bot_menu = Menu(options)

        print(slack_bot_menu.run((' '.join(args.send) if args.send else args.send,
                                  args.delete,
                                  args.delete_all)))

    else:
        print(Events.WARNING.value, Events.NO_CREDS.value)


if __name__ == '__main__':
    main()
