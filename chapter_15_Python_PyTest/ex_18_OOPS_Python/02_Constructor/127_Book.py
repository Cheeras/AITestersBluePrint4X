# 3. Create a Book class where the constructor prints "Book added!" every time
class Book:
    def __init__(self,title, author):
        self.title = title
        self.author = author
        print(f"Book added: {self.title} by {self.author}")

book1 = Book("The Alchemist","Paulo Coelho")
book2 = Book("1984","George Orwell")

