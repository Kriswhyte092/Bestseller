class Employee:
    def __init__(self, name, id=None):
        self.name = name
        self.id = id

        return f"Name: {self.name}, ID: {self.get_id()}"


