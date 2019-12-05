import parser

try:
    import readline
except ImportError:
    pass

class State:
    def __init__(self, folder):
        self.db = dict()
        for movie, people in parser.load_all_data(folder):
            self.db[movie] = people


class Application:
    def __init__(self):
        pass

    def run(self):
        while True:
            command = input("> ")
            if command == "quit":
                return

            print(command)


if __name__ == "__main__":
    app = Application()
    app.run()