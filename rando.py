class Test:
    def __init__(self, name):
        self.name = name

    def __hash__(self):
        return hash(str(self.name))

    def __eq__(self, other):
        return str(self.name) == str(other.name)