import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
import uuid 


DATA_FILE = 'books.json'


def load_data(filename):
    "Loads data from a JSON file."
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

            if not isinstance(data, list):
                 print(f"Warning: Data file '{filename}' contains invalid data. Starting fresh.")
                 return []
            return data
    except json.JSONDecodeError:
        messagebox.showerror("Error", f"Could not decode JSON from {filename}. File might be corrupted.")
        return []
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while loading data: {e}")
        return []

def save_data(data, filename):
    "Saves data to a JSON file."
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving data: {e}")


class BookFormWindow(tk.Toplevel):
    "A separate window for adding or editing book details."
    def __init__(self, parent, book_data=None):
        super().__init__(parent)
        self.parent = parent
        self.book_data = book_data
        self.result = None

        self.title(f"{'Edit' if book_data else 'Add'} Book")
        self.geometry("400x200")
        self.transient(parent)
        self.grab_set()


        self.frame = ttk.Frame(self, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1) # Make entry fields expand

        ttk.Label(self.frame, text="Title:").grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        self.title_entry = ttk.Entry(self.frame, width=40)
        self.title_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)

        ttk.Label(self.frame, text="Author:").grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        self.author_entry = ttk.Entry(self.frame, width=40)
        self.author_entry.grid(row="1", column=1, sticky=(tk.W, tk.E), pady=5, padx=5)

        ttk.Label(self.frame, text="Year:").grid(row=2, column=0, sticky=tk.W, pady=5, padx=5)
        self.year_entry = ttk.Entry(self.frame, width=40)
        self.year_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)


        button_frame = ttk.Frame(self.frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=15)

        ttk.Button(button_frame, text="Save", command=self._on_save).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self._on_cancel).pack(side=tk.LEFT, padx=5)


        if book_data:
            self.title_entry.insert(0, book_data.get('title', ''))
            self.author_entry.insert(0, book_data.get('author', ''))
            self.year_entry.insert(0, book_data.get('year', ''))


        self.bind("<Return>", lambda event=None: self._on_save())

        self.bind("<Escape>", lambda event=None: self._on_cancel())


        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{int(x)}+{int(y)}")


    def _on_save(self):
        "Handles the save button click."
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        year = self.year_entry.get().strip()

        if not title or not author or not year:
            messagebox.showwarning("Input Error", "Title, Author, and Year cannot be empty.", parent=self)
            return

        # Basic year validation
        if not year.isdigit() or int(year) <= 0:
             messagebox.showwarning("Input Error", "Year must be a positive number.", parent=self)
             return

        self.result = {
            'title': title,
            'author': author,
            'year': year
        }


        if self.book_data and 'id' in self.book_data:
            self.result['id'] = self.book_data['id']

        self.destroy()

    def _on_cancel(self):
        """Handles the cancel button click."""
        self.result = None
        self.destroy()

    def show(self):
        "Waits for the window to be closed and returns the result."
        self.parent.wait_window(self)
        return self.result


class BookCatalogApp(tk.Tk):
    "Main application window for the book catalog."
    def __init__(self):
        super().__init__()
        self.title("Book Catalog")
        self.geometry("700x500")


        self.data = load_data(DATA_FILE)


        self.main_frame = ttk.Frame(self, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)


        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=0)


        self.tree = ttk.Treeview(self.main_frame, columns=('Author', 'Year'), show='headings')
        self.tree.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))


        self.tree.heading('#0', text='Title')
        self.tree.heading('Author', text='Author')
        self.tree.heading('Year', text='Year')


        self.tree.column('#0', width=250, minwidth=150, stretch=tk.YES)
        self.tree.column('Author', width=150, minwidth=100, stretch=tk.YES)
        self.tree.column('Year', width=80, minwidth=50, stretch=tk.YES)



        scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))


        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Add Book", command=self.add_book).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Edit Book", command=self.edit_book).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Book", command=self.delete_book).pack(side=tk.LEFT, padx=5)



        self.status_label = ttk.Label(self, text="Ready.", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)


        self.display_books()
        self.update_status("Data loaded.")

    def display_books(self):
        """Clears the treeview and populates it with current data."""

        for item in self.tree.get_children():
            self.tree.delete(item)





        for book in self.data:


            self.tree.insert('', tk.END, iid=book.get('id'),
                             text=book.get('title', 'Untitled'),
                             values=(book.get('author', 'Unknown Author'),
                                     book.get('year', 'N/A')))
        self.update_status(f"Displayed {len(self.data)} books.")


    def add_book(self):
        """Opens the form to add a new book."""
        form = BookFormWindow(self)
        new_book_data = form.show()

        if new_book_data:

            new_book_data['id'] = str(uuid.uuid4()) # Use UUID

            self.data.append(new_book_data)
            save_data(self.data, DATA_FILE)
            self.display_books()
            self.update_status(f"Book '{new_book_data['title']}' added.")
            messagebox.showinfo("Success", "Book added successfully!")


    def edit_book(self):
        "Opens the form to edit the selected book."
        selected_item_id = self.tree.focus()
        if not selected_item_id:
            messagebox.showwarning("Selection Error", "Please select a book to edit.")
            return

        # Find the book in the data list using its ID (which is the item's iid)
        book_to_edit = next((book for book in self.data if book.get('id') == selected_item_id), None)

        if book_to_edit:
            form = BookFormWindow(self, book_to_edit)
            updated_book_data = form.show()

            if updated_book_data:

                try:
                    index = next(i for i, book in enumerate(self.data) if book.get('id') == updated_book_data.get('id'))

                    self.data[index].update(updated_book_data)
                    save_data(self.data, DATA_FILE)
                    self.display_books()
                    self.update_status(f"Book '{updated_book_data['title']}' updated.")
                    messagebox.showinfo("Success", "Book updated successfully!")
                except StopIteration:

                     messagebox.showerror("Error", "Could not find the book to update.")
        else:
             messagebox.showerror("Error", "Selected item data not found.")


    def delete_book(self):
        "Deletes the selected book after confirmation."
        selected_item_id = self.tree.focus()
        if not selected_item_id:
            messagebox.showwarning("Selection Error", "Please select a book to delete.")
            return


        book_item = self.tree.item(selected_item_id)
        book_title = book_item.get('text', 'Selected Book')

        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{book_title}'?",
                                      icon='warning')

        if confirm:

            initial_count = len(self.data)
            self.data = [book for book in self.data if book.get('id') != selected_item_id]

            if len(self.data) < initial_count:
                save_data(self.data, DATA_FILE)
                self.display_books()
                self.update_status(f"Book '{book_title}' deleted.")
                messagebox.showinfo("Success", "Book deleted successfully!")
            else:
                messagebox.showerror("Error", "Could not find the book to delete.")


    def update_status(self, message):
        "Updates the text in the status bar."
        self.status_label.config(text=message)



if __name__ == "__main__":
    app = BookCatalogApp()
    app.mainloop()