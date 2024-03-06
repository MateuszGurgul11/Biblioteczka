import json

class Liblary():
    def __init__(self):
        try:
            with open('liblary.json', 'r') as f:
                self.liblary = json.load(f)
        except FileNotFoundError:
            self.liblary = []
    
    def all(self):
        return self.liblary

    def get(self, id):
        for book in self.all():
            if 'id' in book and book['id'] == id:
                return book
        return None
    
    def create(self, data):
        self.liblary.append(data)
        self.save_all()

    def save_all(self):
        with open('liblary.json', 'w') as f:
            json.dump(self.liblary, f)

    def update(self, data, id):
        book = self.get(id)
        if book:
            index = self.liblary.index(book)
            self.liblary[index] = data
            self.save_all()
            return True
        return False

    def delete(self, id):
        book = self.get(id)
        if book:
            self.liblary.remove(book)
            self.save_all()
            return True
        return False

liblary = Liblary()