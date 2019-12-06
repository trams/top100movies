import parser

try:
    import readline
    no_readline = False
except ImportError:
    no_readline = True


class State:
    def __init__(self, path):
        with open(path) as f:
            self.db = parser.json_to_db(f)

        self.index = dict()

        for movie, people in self.db.items():
            for person in people:
                for word in person.name.lower().split():
                    if word != "":
                        self.index.setdefault(word, set()).add(movie)

    def get(self, raw_query):
        query = [item.lower() for item in raw_query.split(" ") if item != ""]
        if len(query) == 0:
            return []
        result = None

        for word in query:
            word_result = self.index.get(word, set())
            if result is None:
                result = word_result
            else:
                result = result.intersection(word_result)

        return list(result)

    def naive_get(self, raw_query):
        query = [item for item in raw_query.split(" ") if item != ""]
        if len(query) == 0:
            return []
        result = []
        for movie, people in self.db.items():
            full_query_match = True
            for query_part in query:
                match = False
                for person in people:
                    if person.name.lower().find(query_part) != -1:
                        match = True
                        break

                if not match:
                    full_query_match = False
                    break
            if full_query_match:
                result.append(movie)

        return result


class Application:
    def __init__(self, folder):
        print("Loading from {} ...".format(folder))
        self.db = State(folder)

    def run(self):
        while True:
            command = input("> ")
            if command == "quit":
                return

            for movie in self.db.get(command):
                print(movie)


if __name__ == "__main__":
    if not no_readline:
        readline.parse_and_bind("tab: complete")
        histfile = ".history"
        if hasattr(readline, "read_history_file"):
            try:
                readline.read_history_file(histfile)
            except FileNotFoundError:
                pass

            def save_history(histfile_path):
                readline.set_history_length(1000)
                readline.write_history_file(histfile_path)

            import atexit

            atexit.register(save_history, histfile)

    import sys
    path = sys.argv[1]
    app = Application(path)
    app.run()
