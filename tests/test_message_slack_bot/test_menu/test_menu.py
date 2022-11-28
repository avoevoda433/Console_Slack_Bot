import unittest
from message_slack_bot.menu.menu import Menu


def _test_function1():
    return 'Some text'


def _test_function2():
    return '25'


class TestMenuMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.test_menu = Menu((lambda x: str(x),
                              _test_function1,
                              _test_function2))

    def test_run(self):
        self.assertMultiLineEqual(self.test_menu.run(('some string', False, False)), 'some string')
        self.assertMultiLineEqual(self.test_menu.run((False, True, False)), 'Some text')
        self.assertMultiLineEqual(self.test_menu.run((False, False, True)), '25')
        self.assertMultiLineEqual(self.test_menu.run((False, False, True, False)), '25')


if __name__ == '__main__':
    unittest.main()
