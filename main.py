import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
from PIL import Image, ImageTk
from urllib.request import urlopen
from io import BytesIO

class BookDetailsWindow:
    def __init__(self, parent, book_data):
        self.top = tk.Toplevel(parent)
        self.top.title("Book Details")
        
        # Window sizing and positioning
        window_width = 800
        window_height = 600
        screen_width = self.top.winfo_screenwidth()
        screen_height = self.top.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.top.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        self.create_details_view(book_data)
        
    def create_details_view(self, book):
        main_frame = ttk.Frame(self.top, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left frame for cover art
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, padx=10)
        
        # Placeholder for book cover (you can replace this with actual cover art loading)
        cover_label = ttk.Label(left_frame, text="Cover Art\nPlaceholder", 
                              borderwidth=2, relief="solid", width=30, padding=100)
        cover_label.pack()
        
        # Right frame for book details
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        # Title
        title_label = ttk.Label(right_frame, text=book['title'], 
                               font=('Helvetica', 16, 'bold'))
        title_label.pack(anchor='w', pady=5)
        
        # Author
        author_label = ttk.Label(right_frame, text=f"By {book['author']}", 
                                font=('Helvetica', 12, 'italic'))
        author_label.pack(anchor='w', pady=5)
        
        # Genre
        genre_label = ttk.Label(right_frame, text=f"Genre: {book['genre']}")
        genre_label.pack(anchor='w', pady=5)
        
        # Release Date
        release_label = ttk.Label(right_frame, text=f"Released: {book['release_date']}")
        release_label.pack(anchor='w', pady=5)
        
        # Book Resume
        resume_frame = ttk.LabelFrame(right_frame, text="Book Summary", padding="10")
        resume_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        resume_text = tk.Text(resume_frame, wrap=tk.WORD, height=10)
        resume_text.insert(tk.END, "Book summary placeholder text. You can add the actual book summary here.")
        resume_text.config(state='disabled')
        resume_text.pack(fill=tk.BOTH, expand=True)
        
        # Close button
        close_button = ttk.Button(right_frame, text="Close", command=self.top.destroy)
        close_button.pack(pady=10)

class AddBookWindow:
    def __init__(self, parent, callback):
        self.top = tk.Toplevel(parent)
        self.top.title("Add New Book")
        self.callback = callback
        
        # Center the window
        window_width = 400
        window_height = 300
        screen_width = self.top.winfo_screenwidth()
        screen_height = self.top.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.top.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        self.create_widgets()
        
    def create_widgets(self):
        # Create and pack frames
        main_frame = ttk.Frame(self.top, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(main_frame, text="Title:").grid(row=0, column=0, sticky='w', pady=5)
        self.title_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.title_var, width=30).grid(row=0, column=1, pady=5)
        
        # Author
        ttk.Label(main_frame, text="Author:").grid(row=1, column=0, sticky='w', pady=5)
        self.author_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.author_var, width=30).grid(row=1, column=1, pady=5)
        
        # Genre
        ttk.Label(main_frame, text="Genre:").grid(row=2, column=0, sticky='w', pady=5)
        self.genre_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.genre_var, width=30).grid(row=2, column=1, pady=5)
        
        # Release Date
        ttk.Label(main_frame, text="Release Date:").grid(row=3, column=0, sticky='w', pady=5)
        self.release_date_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.release_date_var, width=30).grid(row=3, column=1, pady=5)
        
        # Copies
        ttk.Label(main_frame, text="Copies:").grid(row=4, column=0, sticky='w', pady=5)
        self.copies_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.copies_var, width=30).grid(row=4, column=1, pady=5)
        
        # Time Borrowed
        ttk.Label(main_frame, text="Time Borrowed:").grid(row=5, column=0, sticky='w', pady=5)
        self.time_borrowed_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.time_borrowed_var, width=30).grid(row=5, column=1, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Submit", command=self.submit).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.top.destroy).pack(side=tk.LEFT, padx=5)
        
    def submit(self):
        book_data = {
            'title': self.title_var.get().strip(),
            'author': self.author_var.get().strip(),
            'genre': self.genre_var.get().strip(),
            'release_date': self.release_date_var.get().strip(),
            'copies': self.copies_var.get().strip(),
            'time_borrowed': self.time_borrowed_var.get().strip()
        }
        
        if all(book_data.values()):
            self.callback(book_data)
            self.top.destroy()
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")

class LibraryUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Library Management")
        self.root.geometry("1000x600")
        
        self.json_file = "library_data.json"
        self.load_books()
        
        self.create_frames()
        self.create_book_list()
        self.create_buttons()
        
    def load_books(self):
        if os.path.exists(self.json_file):
            with open(self.json_file, 'r') as file:
                old_data = json.load(file)
                # Convert old data format to new format
                self.books = []
                for book in old_data:
                    self.books.append({
                        'title': book.get('title', ''),
                        'author': book.get('author', ''),
                        'genre': book.get('genre', ''),
                        'release_date': book.get('release_date', ''),
                        'copies': book.get('copies', ''),
                        'time_borrowed': book.get('time_borrowed', '')
                    })
        else:
            self.books = []
            
    def save_books(self):
        books_data = []
        for item in self.tree.get_children():
            values = self.tree.item(item)['values']
            books_data.append({
                'title': values[0],
                'author': values[1],
                'genre': values[2],
                'release_date': values[3],
                'copies': values[4],
                'time_borrowed': values[5]
            })
        
        with open(self.json_file, 'w') as file:
            json.dump(books_data, file, indent=4)
        
    def create_frames(self):
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
    def create_book_list(self):
        columns = ("Title", "Author", "Genre", "Release Date", "Copies", "Time Borrowed")
        self.tree = ttk.Treeview(self.main_frame, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        
        for book in self.books:
            self.tree.insert("", tk.END, values=(
                book['title'], 
                book['author'], 
                book['genre'],
                book['release_date'],
                book['copies'],
                book['time_borrowed']
            ))
        
        # Add double-click event binding
        self.tree.bind('<Double-1>', self.show_book_details)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
    def create_buttons(self):
        button_frame = ttk.Frame(self.root, padding="10")
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Add Book", command=self.show_add_book_window).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Selected", command=self.delete_book).pack(side=tk.LEFT, padx=5)
        
    def show_add_book_window(self):
        AddBookWindow(self.root, self.add_book)
            
    def add_book(self, book_data):
        self.tree.insert("", tk.END, values=(
            book_data['title'],
            book_data['author'],
            book_data['genre'],
            book_data['release_date'],
            book_data['copies'],
            book_data['time_borrowed']
        ))
        self.save_books()
            
    def delete_book(self):
        selected_item = self.tree.selection()
        if selected_item:
            self.tree.delete(selected_item)
            self.save_books()
        else:
            messagebox.showinfo("Selection", "Please select a book to delete.")
    
    def show_book_details(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item)['values']
            book_data = {
                'title': values[0],
                'author': values[1],
                'genre': values[2],
                'release_date': values[3],
                'copies': values[4],
                'time_borrowed': values[5]
            }
            BookDetailsWindow(self.root, book_data)

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryUI(root)
    root.mainloop()