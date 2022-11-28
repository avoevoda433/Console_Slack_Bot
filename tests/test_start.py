import unittest
from message_slack_bot.app.app import Events
from message_slack_bot.start import _set_creds
from message_slack_bot.start import _parse_args
from message_slack_bot.start import command_parser


class FileObject:
    def __init__(self, data):
        self.data = data

    def read(self, *args, **kwargs):
        return self.data

    def write(self, data, *args, **kwargs):
        self.data = data


class TestStartMethods(unittest.TestCase):

    def test_set_creds(self):
        self.assertMultiLineEqual(_set_creds(['1', '2', '3']),
                                  "".join([Events.SUCCESS.value, Events.SET_CREDS.value]))

    def test_parse_args(self):
        self.assertEqual(_parse_args(), command_parser.parse_args())


if __name__ == '__main__':
    unittest.main()
