import json


class GhStorage:

    # init from json file
    def __init__(self, json_file, content=None ):
        if content is None :
            self.json_file = json_file
            self.content = {}
            try:
                self.open()
            except FileNotFoundError:
                try:
                    self.create()
                except Exception as e:
                    print("Failed to initialize storage on file {} : {}".format(self.json_file, e))
        else:
            # init from direct json content
            self.json_file = None
            self.content = content
            print("GhStorage: transient usage")

    def open(self):
        if self.json_file is not None:
            with open(self.json_file) as file:
                self.content = json.load(file)
            print("GhStorage loaded")
        else:
            print("GhStorage : open ignored, not open from file")

    def create(self):
        if self.json_file is not None:
            print("Creating local storage")
            with open(self.json_file, "w") as file:
                file.write("{}")
            self.open()
        else:
            print("GhStorage : create ignored, not open from file")

    def reset(self, content):
        self.content = content
        if self.json_file is not None:
            self.save()

    def save(self):
        if self.json_file is not None:
            with open(self.json_file, "w", encoding='utf-8') as file:
                json.dump(self.content, file, ensure_ascii=False, indent=4)
                print("GhStorage : {} saved".format(self.json_file))
        else:
            print("GhStorage : save ignored, not open from file")

    def data(self):
        return self.content

    def getOrCreate(self, data, key, default):
        try:
            return self.content[key]
        except KeyError:
            self.content[key] = default
            self.save()
            return self.content[key]

    @staticmethod
    def getValue(data, key):
        try:
            return data[key]
        except:
            return None


