from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from enum import Enum


class Events(Enum):
    SUCCESS = f"\n\033[32;3m{'success'.upper()}\033[0m"
    WARNING = f"\n\033[33;3m{'warning'.upper()}\033[0m"
    FAILED = f"\n\033[31;3m{'failed'.upper()}\033[0m"
    ERROR = "\n\033[3mGot an error:\033[0m"
    NO_MESSAGES = "\n\033[3mIn the channel there aren't messages that you sent\033[0m\n"
    NO_CREDS = "\n\033[3mCheck your input credentials\033[0m\n"
    SET_CREDS = "\n\033[3mYour credentials set\033[0m\n"
    SET_CREDS_ERROR = "\n\033[3mSome error. Your credentials can't set\033[0m\n"
    SEND_INFO = "\n\033[3mYour message sending\033[0m\n"
    DELETE_INFO = "\n\033[3mYour last message deleted\033[0m\n"
    DELETE_ALL_INFO = "\n\033[3mYour all message deleted\033[0m\n"


# Names of all credentials
class CredsNames(Enum):
    BOT_TOKEN = 0
    BOT_NAME = 1
    CHANNEL_ID = 2
    CHANNEL_NAME = 3


def _error(e) -> str:
    return "".join([Events.FAILED.value,
                    f"{Events.ERROR.value} {e}\n"])


def _warning() -> str:
    return "".join([Events.WARNING.value,
                    Events.NO_MESSAGES.value])


class SlackBot:
    def __init__(self,
                 bot_token: str,
                 bot_name: str,
                 channel_id: str,
                 channel_name: str):
        # Set the required parameters
        self.__bot_token = bot_token
        self.__bot_name = bot_name
        self.__channel_id = channel_id
        self.__channel_name = channel_name

    def send_message(self, text_msg: str) -> str:
        """ This function uses API methods and send a message in the channel """
        try:
            # Call the chat_postMessage method and send message
            response = WebClient(token=self.__bot_token).chat_postMessage(channel=self.__channel_name,
                                                                          text=text_msg)
            if response['ok']:
                # Print the result if the message was successfully sent
                return "".join((Events.SUCCESS.value,
                                Events.SEND_INFO.value))
            else:
                return _error(response['error'])

        except SlackApiError as e:
            # Print the error if the message wasn't sent
            return _error(e)

    def delete_message(self) -> str:
        """ This function uses API methods and delete the last message """
        try:
            # Call the conversation_history method and get info about messages in the channel
            response = WebClient(token=self.__bot_token).conversations_history(channel=self.__channel_id)
            conversation_history = list(msg_info for msg_info in response["messages"]
                                        if msg_info.get('bot_profile', {}).get('name', None) == self.__bot_name)
            # Check messages in the channel
            if not conversation_history:
                return _warning()
            else:
                # Call the chat_delete method and delete last message
                result = WebClient(token=self.__bot_token).chat_delete(channel=self.__channel_id,
                                                                       ts=conversation_history[0]['ts'])

                # Print the result if the message was successfully deleted
                if result['ok']:
                    return "".join([Events.SUCCESS.value,
                                    Events.DELETE_INFO.value])
                else:
                    return _error(result['error'])

        except SlackApiError as e:
            return _error(e)

    def delete_all_messages(self) -> str:
        """ This function uses API methods and delete all messages in the channel """
        try:
            # Call the conversation_history method and get info about messages in the channel
            result = WebClient(token=self.__bot_token).conversations_history(channel=self.__channel_id)
            conversation_history = list(msg_info for msg_info in result["messages"]
                                        if msg_info.get('bot_profile', {}).get('name', None) == self.__bot_name)

            # Check messages in the channel
            if not conversation_history:
                return _warning()
            else:
                # Call the chat_delete method and delete every message in the list
                for msg in conversation_history:
                    result = WebClient(token=self.__bot_token).chat_delete(channel=self.__channel_id, ts=msg['ts'])
                    if not result['ok']:
                        return _error(result['error'])

                # Print the result if messages were successfully deleted
                return "".join([Events.SUCCESS.value,
                                Events.DELETE_ALL_INFO.value])

        except SlackApiError as e:
            return _error(e)
