import mysql.connector

# Connect to the Database
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Biswajit@03",
        database="library"
    )
    cursor = conn.cursor()

    # Create Tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            author VARCHAR(255) NOT NULL,
            quantity INT NOT NULL
        )
    ''')
    conn.commit()

    # Function to Add a Book
    def add_book(title, author, quantity):
        cursor.execute('INSERT INTO books (title, author, quantity) VALUES (%s, %s, %s)', (title, author, quantity))
        conn.commit()
        print(f'Book "{title}" by {author} added successfully.')

    # Function to Display All Books
    def display_books():
        cursor.execute('SELECT * FROM books')  # Fix: Provide a valid SQL query
        books = cursor.fetchall()
        if books:
            print("Books in the Library:")
            for book in books:
                print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Quantity: {book[3]}")
        else:
            print("No books in the library.")

    # Function to Borrow a Book
    def borrow_book(book_id):
        cursor.execute('SELECT * FROM books WHERE id = %s', (book_id,))
        book = cursor.fetchone()

        if book:
            if book[3] > 0:
                cursor.execute('UPDATE books SET quantity = %s WHERE id = %s', (book[3] - 1, book_id))
                conn.commit()
                print(f'You have borrowed the book "{book[1]}" by {book[2]}.')
            else:
                print('Sorry, the book is out of stock.')
        else:
            print('Book not found.')

    # Function to Return a Book
    def return_book(book_id):
        cursor.execute('SELECT * FROM books WHERE id = %s', (book_id,))
        book = cursor.fetchone()

        if book:
            cursor.execute('UPDATE books SET quantity = %s WHERE id = %s', (book[3] + 1, book_id))
            conn.commit()
            print(f'You have returned the book "{book[1]}" by {book[2]}.')
        else:
            print('Book not found.')

    # Main Program
    if __name__ == "__main__":
        try:
            while True:
                print("\nLibrary Management System")
                print("1. Add Book")
                print("2. Display Books")
                print("3. Borrow Book")
                print("4. Return Book")
                print("5. Exit")

                choice = input("Enter your choice: ")

                if choice == '1':
                    title = input("Enter the title of the book: ")
                    author = input("Enter the author of the book: ")
                    quantity = int(input("Enter the quantity of the book: "))
                    add_book(title, author, quantity)
                elif choice == '2':
                    display_books()
                elif choice == '3':
                    book_id = int(input("Enter the ID of the book you want to borrow: "))
                    borrow_book(book_id)
                elif choice == '4':
                    book_id = int(input("Enter the ID of the book you want to return: "))
                    return_book(book_id)
                elif choice == '5':
                    print("Exiting the Library Management System.")
                    break
                else:
                    print("Invalid choice. Please enter a valid option.")

        finally:
            # Close cursor and connection in the finally block
            cursor.close()
            conn.close()

except mysql.connector.Error as err:
    print(f"Error: {err}")
