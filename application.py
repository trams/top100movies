import parser

try:
    import readline
except ImportError:
    pass


class State:
    def __init__(self, folder):
        self.db = dict()
        for movie, people in parser.load_all_data(folder):
            print("Loaded {}".format(movie))
            self.db[movie] = [person.name.lower() for person in people]

    def get(self, raw_query):
        query = [item for item in raw_query.split(" ") if item != ""]
        if len(query) == 0:
            return []
        result = []
        for movie, people in self.db.items():
            full_query_match = True
            for query_part in query:
                match = False
                for person in people:
                    if person.find(query_part) != -1:
                        match = True
                        break

                if not match:
                    full_query_match = False
                    break
            if full_query_match:
                result.append(movie.name)

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
    import sys
    data_folder = sys.argv[1]
    app = Application(data_folder)
    app.run()
