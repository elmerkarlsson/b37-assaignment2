# necessary imports
import json
import tkinter as tk
from tkinter import messagebox


# creating the Book class
class Book:
    def __init__(self, ID, Title, Genre, Author, Price):
        self.ID = ID
        self.Title = Title
        self.Genre = Genre
        self.Author = Author
        self.Price = Price


# creating the BookManager class
# this class handles loading saving searching ading updating and deleting books
class BookManager:
    def __init__(self, filename):
        self.filename = filename
        self.books = []
        self.load_books()

    # loads books from the JSON file
    def load_books(self):
        with open(self.filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.books = []

        for item in data:
            book = Book(
                item["ID"],
                item["Title"],
                item["Genre"],
                item["Author"],
                item["Price"]
            )
            self.books.append(book)

    # saves all books to the JSON file
    def save_books(self):
        data = []

        for book in self.books:
            data.append({
                "ID": book.ID,
                "Title": book.Title,
                "Genre": book.Genre,
                "Author": book.Author,
                "Price": book.Price
            })

        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    # searches books by chosen field
    def search_books(self, field, query):
        results = []

        for book in self.books:
            value = str(getattr(book, field))

            if query.lower() in value.lower():
                results.append(book)

        return results

    # adds a new book and saves it to the JSON file
    def add_book(self, book):
        self.books.append(book)
        self.save_books()

    # updates a book by ID and saves the change
    def update_book(self, book_id, title, genre, author, price):
        for book in self.books:
            if book.ID == book_id:
                book.Title = title
                book.Genre = genre
                book.Author = author
                book.Price = price
                self.save_books()
                return True

        return False

    # deletes a book by id and saves the change
    def delete_book(self, book_id):
        for book in self.books:
            if book.ID == book_id:
                self.books.remove(book)
                self.save_books()
                return True

        return False

    # checks if a book id already exists
    def book_id_exists(self, book_id):
        for book in self.books:
            if book.ID == book_id:
                return True

        return False


# creating the GUI class
# This class handles everything the user sees and klicks on
class BookGUI:
    def __init__(self, window, manager):
        self.window = window
        self.manager = manager

        self.window.title("Book Manager")
        self.window.geometry("850x650")

        # Search section
        self.search_label = tk.Label(window, text="Search:")
        self.search_label.pack()

        self.search_entry = tk.Entry(window, width=40)
        self.search_entry.pack()

        self.search_field = tk.StringVar()
        self.search_field.set("Title")

        self.field_menu = tk.OptionMenu(window, self.search_field, "Title", "Genre", "Author", "Price")
        self.field_menu.pack()

        self.search_button = tk.Button(window, text="Search", command=self.search_button_clicked)
        self.search_button.pack()

        # result list
        self.result_list = tk.Listbox(window, width=120, height=12)
        self.result_list.pack(pady=10)

        # When the user selects a book in the list the input fields are filled
        self.result_list.bind("<<ListboxSelect>>", self.select_book)

        # Input fields 
        self.id_label = tk.Label(window, text="ID:")
        self.id_label.pack()
        self.id_entry = tk.Entry(window, width=40)
        self.id_entry.pack()

        self.title_label = tk.Label(window, text="Title:")
        self.title_label.pack()
        self.title_entry = tk.Entry(window, width=40)
        self.title_entry.pack()

        self.genre_label = tk.Label(window, text="Genre:")
        self.genre_label.pack()
        self.genre_entry = tk.Entry(window, width=40)
        self.genre_entry.pack()

        self.author_label = tk.Label(window, text="Author:")
        self.author_label.pack()
        self.author_entry = tk.Entry(window, width=40)
        self.author_entry.pack()

        self.price_label = tk.Label(window, text="Price:")
        self.price_label.pack()
        self.price_entry = tk.Entry(window, width=40)
        self.price_entry.pack()

        # Buttons 
        self.add_button = tk.Button(window, text="Add Book", command=self.add_button_clicked)
        self.add_button.pack(pady=5)

        self.update_button = tk.Button(window, text="Update Book", command=self.update_button_clicked)
        self.update_button.pack(pady=5)

        self.delete_button = tk.Button(window, text="Delete Book", command=self.delete_button_clicked)
        self.delete_button.pack(pady=5)

        self.clear_button = tk.Button(window, text="Clear Fields", command=self.clear_fields)
        self.clear_button.pack(pady=5)

        # Show all books when the program starts
        self.show_all_books()

    # Checks that the input fields are valid
    def validate_inputs(self):
        book_id = self.id_entry.get().strip()
        title = self.title_entry.get().strip()
        genre = self.genre_entry.get().strip()
        author = self.author_entry.get().strip()
        price = self.price_entry.get().strip()

        if book_id == "" or title == "" or genre == "" or author == "" or price == "":
            messagebox.showerror("Error", "All fields must be filled in.")
            return None

        try:
            price = int(price)
        except ValueError:
            messagebox.showerror("Error", "Price must be a number.")
            return None

        return book_id, title, genre, author, price

    # Shows all books in the result list
    def show_all_books(self):
        self.result_list.delete(0, tk.END)

        for book in self.manager.books:
            self.result_list.insert(
                tk.END,
                f"{book.ID} | {book.Title} | {book.Genre} | {book.Author} | {book.Price}"
            )

    # Handles the search button
    def search_button_clicked(self):
        self.result_list.delete(0, tk.END)

        query = self.search_entry.get()
        field = self.search_field.get()

        results = self.manager.search_books(field, query)

        for book in results:
            self.result_list.insert(
                tk.END,
                f"{book.ID} | {book.Title} | {book.Genre} | {book.Author} | {book.Price}"
            )

    # Adds a new book
    def add_button_clicked(self):
        values = self.validate_inputs()

        if values is None:
            return

        book_id, title, genre, author, price = values

        if self.manager.book_id_exists(book_id):
            messagebox.showerror("Error", "A book with this ID already exists.")
            return

        new_book = Book(book_id, title, genre, author, price)
        self.manager.add_book(new_book)

        messagebox.showinfo("Success", "Book added successfully.")
        self.clear_fields()
        self.show_all_books()

    # Updates an existing book
    def update_button_clicked(self):
        values = self.validate_inputs()

        if values is None:
            return

        book_id, title, genre, author, price = values

        updated = self.manager.update_book(book_id, title, genre, author, price)

        if updated:
            messagebox.showinfo("Success", "Book updated successfully.")
            self.clear_fields()
            self.show_all_books()
        else:
            messagebox.showerror("Error", "No book with this ID was found.")

    # Deletes an existing book
    def delete_button_clicked(self):
        book_id = self.id_entry.get().strip()

        if book_id == "":
            messagebox.showerror("Error", "Enter the ID of the book you want to delete.")
            return

        deleted = self.manager.delete_book(book_id)

        if deleted:
            messagebox.showinfo("Success", "Book deleted successfully.")
            self.clear_fields()
            self.show_all_books()
        else:
            messagebox.showerror("Error", "No book with this ID was found.")

    # Fills the input fields when a book is selected in the list
    def select_book(self, event):
        try:
            selected = self.result_list.get(self.result_list.curselection())
        except:
            return

        parts = selected.split(" | ")

        self.clear_fields()

        self.id_entry.insert(0, parts[0])
        self.title_entry.insert(0, parts[1])
        self.genre_entry.insert(0, parts[2])
        self.author_entry.insert(0, parts[3])
        self.price_entry.insert(0, parts[4])

    # Clears all input fields
    def clear_fields(self):
        self.id_entry.delete(0, tk.END)
        self.title_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)


# Starts the program
manager = BookManager("books.json")

window = tk.Tk()
app = BookGUI(window, manager)
window.mainloop()