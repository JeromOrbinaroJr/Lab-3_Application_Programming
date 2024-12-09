import datetime
class Note:
    def __init__(self, id, title: str, content: str, category):
        self.id = id
        self.title = title
        self.content = content
        self.date = datetime.datetime.now()
        self.category = category


