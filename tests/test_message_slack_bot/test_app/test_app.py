import unittest
from message_slack_bot.app.app import _error
from message_slack_bot.app.app import _warning
from message_slack_bot.app.app import SlackBot
from message_slack_bot.app.app import Events
from unittest.mock import patch, MagicMock, sentinel


class TestAppMethods(unittest.TestCase):
    def test_error(self):
        self.assertMultiLineEqual(_error('Some error'), "".join([Events.FAILED.value,
                                                                f"{Events.ERROR.value} Some error\n"]))

    def test_warning(self):
        self.assertMultiLineEqual(_warning(), "".join([Events.WARNING.value,
                                                       Events.NO_MESSAGES.value]))

    def setUp(self) -> None:
        # Create the test object
        self.test_app = SlackBot(sentinel.token,
                                 sentinel.name,
                                 sentinel.id,
                                 sentinel.channel)

        self.test_message = 'some test message'

        # setup for good response send message
        self.good_response_send = MagicMock()
        good_response_data_send = {'ok': True,
                                   'channel': sentinel.channel,
                                   'message': {'text': self.test_message,
                                               'username': sentinel.name},
                                   'type': 'message'}
        self.good_response_send.__getitem__.side_effect = good_response_data_send.__getitem__

        # setup for bad response send message
        self.bad_response_send = MagicMock()
        bad_response_data_send = {'ok': False,
                                  'error': 'some test error'}
        self.bad_response_send.__getitem__.side_effect = bad_response_data_send.__getitem__

        # setup for good response get history
        self.good_response_history = MagicMock()
        good_response_data_history = {'ok': True,
                                      'messages': [{'type': 'message',
                                                    'bot_profile': {'name': sentinel.name},
                                                    'text': self.test_message,
                                                    'ts': sentinel.test_ts1},
                                                   {'type': 'message',
                                                    'bot_profile': {'name': sentinel.name},
                                                    'text': self.test_message,
                                                    'ts': sentinel.test_ts2}
                                                   ]}
        self.good_response_history.__getitem__.side_effect = good_response_data_history.__getitem__

        # setup for empty response get history
        self.empty_response_history = MagicMock()
        empty_response_data_history = {'ok': True,
                                       'messages': [{'type': 'message',
                                                     'user': 'test_user',
                                                     'text': self.test_message,
                                                     'ts': sentinel.test_ts}]}
        self.empty_response_history.__getitem__.side_effect = empty_response_data_history.__getitem__

        # setup for good response delete message
        self.good_response_delete = MagicMock()
        good_response_data_delete = {'ok': True,
                                     'channel': sentinel.channel,
                                     'ts': sentinel.test_ts}
        self.good_response_delete.__getitem__.side_effect = good_response_data_delete.__getitem__

        # setup for bad response delete message
        self.bad_response_delete = MagicMock()
        bad_response_data_delete = {'ok': False,
                                    'error': 'some test error'}
        self.bad_response_delete.__getitem__.side_effect = bad_response_data_delete.__getitem__

    @patch('message_slack_bot.app.app.WebClient')
    def test_send_message_success(self, mock_request):
        mock_request(sentinel.token).chat_postMessage.return_value = self.good_response_send
        self.assertEqual(self.test_app.send_message(self.test_message), "".join((Events.SUCCESS.value,
                                                                                 Events.SEND_INFO.value)))

    @patch('message_slack_bot.app.app.WebClient')
    def test_send_message_fail(self, mock_request):
        mock_request(sentinel.token).chat_postMessage.return_value = self.bad_response_send
        self.assertEqual(self.test_app.send_message(self.test_message), _error('some test error'))

    @patch('message_slack_bot.app.app.WebClient')
    def test_delete_message_success(self, mock_request):
        mock_request(sentinel.token).conversations_history.return_value = self.good_response_history
        mock_request(sentinel.token).chat_delete.return_value = self.good_response_delete
        self.assertEqual(self.test_app.delete_message(), "".join([Events.SUCCESS.value, Events.DELETE_INFO.value]))

    @patch('message_slack_bot.app.app.WebClient')
    def test_delete_message_empty(self, mock_request):
        mock_request(sentinel.token).conversations_history.return_value = self.empty_response_history
        self.assertEqual(self.test_app.delete_message(), _warning())

    @patch('message_slack_bot.app.app.WebClient')
    def test_delete_message_fail(self, mock_request):
        mock_request(sentinel.token).conversations_history.return_value = self.good_response_history
        mock_request(sentinel.token).chat_delete.return_value = self.bad_response_delete
        self.assertEqual(self.test_app.delete_message(), _error('some test error'))

    @patch('message_slack_bot.app.app.WebClient')
    def test_delete_all_messages_success(self, mock_request):
        mock_request(sentinel.token).conversations_history.return_value = self.good_response_history
        mock_request(sentinel.token).chat_delete.return_value = self.good_response_delete
        self.assertEqual(self.test_app.delete_all_messages(), "".join([Events.SUCCESS.value,
                                                                       Events.DELETE_ALL_INFO.value]))

    @patch('message_slack_bot.app.app.WebClient')
    def test_delete_all_messages_empty(self, mock_request):
        mock_request(sentinel.token).conversations_history.return_value = self.empty_response_history
        self.assertEqual(self.test_app.delete_all_messages(), _warning())

    @patch('message_slack_bot.app.app.WebClient')
    def test_delete_all_messages_fail(self, mock_request):
        mock_request(sentinel.token).conversations_history.return_value = self.good_response_history
        mock_request(sentinel.token).chat_delete.return_value = self.bad_response_delete
        self.assertEqual(self.test_app.delete_all_messages(), _error('some test error'))


if __name__ == '__main__':
    unittest.main()
