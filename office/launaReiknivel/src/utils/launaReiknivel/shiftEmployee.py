class Employee:
    def __init__(self, name, id=None):
        self.name = name
        self.id = id

    def getEmployeeName(self):
        return self.name

    def getEmployeeId(self):
        return self.id
        
    def mapName(self):
        return self.name.replace(" ", "_")
    
    def __str__(self):
        if self.id is not None:
            return self.mapName() + "_" + self.id
        return self.mapName()


