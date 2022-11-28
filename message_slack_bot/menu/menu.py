
class Menu:
    def __init__(self, commands: tuple):
        self.__commands = commands

    def run(self, selected_commands: tuple) -> str:
        """ Get and run the command which a user choose """
        for command, selections in zip(self.__commands, selected_commands):
            if selections:
                return command(selections) if isinstance(selections, str) else command()
