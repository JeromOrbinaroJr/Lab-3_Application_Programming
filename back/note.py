import datetime

class Note:
    def __init__(self, id, title: str, content: str, category, date=None):
        self.id = id
        self.title = title
        self.content = content
        self.date = date if date else datetime.datetime.now()
        self.category = category
