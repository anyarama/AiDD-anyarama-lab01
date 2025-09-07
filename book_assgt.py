# Explanation of imports
# Import json for reading and writing data in JSON format
# Import os for file path operations (not used directly in this code, but useful for file management)
# Import datetime for handling and formatting dates (used for review dates)
import json
import os
from datetime import datetime

# Global variables to store our data
books = []
reviews = []

# Function to load data from a JSON file
def load_data(filename="data_file_assgt-01.json"):
    """
    Load books and reviews data from a JSON file.
    This function reads the JSON file and populates the global books and reviews lists.
    """
#To modify the global variables books and reviews inside this function
    global books, reviews
    try:
        with open(filename, 'r') as file:  # Open the file for reading
            data = json.load(file)  # Load JSON data from the file
            books = data.get('books', [])  # Get books list or empty list if not found
            reviews = data.get('reviews', [])  # Get reviews list or empty list if not found
            print(f"Data loaded successfully from {filename}")  # Success message
            print(f"Loaded {len(books)} books and {len(reviews)} reviews")  # Loaded books and reviews count
    except FileNotFoundError:  # Handle file not found error
        print(f"File {filename} not found. Starting with empty data.")  # File not found message
        books = []
        reviews = []
    except json.JSONDecodeError: # Handle JSON decode error
        print("Error reading JSON file. Starting with empty data.")
        books = []
        reviews = []
# Function to save data to a JSON file
def save_data(filename="data_file_assgt-01.json"):  # Specify default filename
    """
    Save books and reviews data to a JSON file.
    This function creates a dictionary with books and reviews and writes it to JSON.
    """
    data = {  # Create a dictionary to hold the data
        "books": books,
        "reviews": reviews
    }
    try:  # Attempt to save data
        with open(filename, 'w') as file:  # Open the file for writing
            json.dump(data, file, indent=2)  # indent=2 makes the JSON readable
        print(f"Data saved successfully to {filename}")
    except Exception as e:  # Catch any exceptions
        print(f"Error saving data: {e}")

# Function to add a new book
def add_book():
    """
    Prompt user to create a new book and add it to the books list.
    This function collects all required book information from the user.
    """
    print("\n--- Add New Book ---")
    
    # Generate a new book ID (find the highest existing ID and add 1)
    if books:
        max_id = max(int(book['bookId']) for book in books)  # Find the highest book ID
        book_id = str(max_id + 1)  # Generate new book ID
    else:
        book_id = "1"  # Start with ID 1 if no books exist

    # Collect book information from user
    title = input("Enter book title: ")
    ai_metric = input("Enter AI metric (0-100): ")
    release_year = input("Enter release year: ")
    author = input("Enter author name: ")
    
    # Handle genres (multiple genres separated by commas)
    genres_input = input("Enter genres (separated by commas): ")
    genres = [genre.strip() for genre in genres_input.split(',')]
    
    # Publisher information
    publisher_name = input("Enter publisher name: ")
    publisher_location = input("Enter publisher location: ")
    
    pages = int(input("Enter number of pages: "))
    
    # Handle sales data (multiple years separated by commas)
    sales_input = input("Enter yearly sales figures (separated by commas): ")
    sales = [int(sale.strip()) for sale in sales_input.split(',')]
    
    # Create the new book dictionary
    new_book = {  # Create a dictionary for the new book
        "bookId": book_id,
        "title": title,
        "aiMetric": ai_metric,
        "releaseYear": release_year,
        "author": author,
        "genres": genres,
        "publisher": {
            "publisherName": publisher_name,
            "location": publisher_location
        },
        "pages": pages,
        "sales": sales
    }
    
    books.append(new_book)  # Add the new book to our books list
    print(f"Added book: {title}")
    
    # Automatically save after adding a book
    save_data()
# Function to add a new review
def add_review():
    """
    Prompt user to create a new review and add it to the reviews list.
    This function shows available books and lets user select one to review.
    """
    print("\n--- Add New Review ---")
    
    # Show available books
    if not books:  # Check if there are no books
        print("No books available to review. Please add a book first.")
        return
    
    print("Available books:")
    for book in books:  # List all available books
        print(f"ID {book['bookId']}: {book['title']} by {book['author']}")  # Show book details

    # Get book ID to review
    book_id = input("Enter the book ID to review: ")
    
    # Check if book exists
    book_exists = any(book['bookId'] == book_id for book in books)
    if not book_exists:
        print("Invalid book ID. Please try again.")
        return
    
    # Generate a new review ID
    if reviews:  # Check if there are existing reviews
        max_id = max(int(review['reviewId']) for review in reviews)  # Find the highest review ID
        review_id = str(max_id + 1)  # Generate new review ID
    else:
        review_id = "1"
    
    # Collect review information
    review_author = input("Enter your name (review author): ")
    review_text = input("Enter your review: ")  # Get the review text

    # Use current date
    review_date = datetime.now().strftime("%Y-%m-%d")
    
    # Create the new review dictionary
    new_review = {
        "reviewId": review_id,
        "reviewAuthor": review_author,
        "reviewDate": review_date,
        "reviewText": review_text,
        "bookId": book_id
    }
    
    reviews.append(new_review)  # Add the new review to our reviews list
    print(f"Added review by {review_author}")  # Confirm review addition

    # Automatically save after adding a review
    save_data()
# Function to display all books
def display_books():
    """
    Display all books in a readable format.
    """
    print("\n--- All Books ---")
    if not books:
        print("No books available.")
        return

    for book in books:  # Iterate through all books
        print(f"ID: {book['bookId']}")
        print(f"Title: {book['title']}")
        print(f"Author: {book['author']}")
        print(f"Release Year: {book['releaseYear']}")
        print(f"AI Metric: {book['aiMetric']}")
        print(f"Genres: {', '.join(book['genres'])}")
        print(f"Publisher: {book['publisher']['publisherName']} ({book['publisher']['location']})")
        print(f"Pages: {book['pages']}")
        print(f"Sales: {book['sales']}")
        print("-" * 40)

# Function to display all reviews
def display_reviews():
    """
    Display all reviews in a readable format.
    """
    print("\n--- All Reviews ---")
    if not reviews:  # Check if there are no reviews
        print("No reviews available.")
        return
    
    for review in reviews:
        # Find the book title for this review
        book_title = "Unknown Book"  # Default title if not found
        for book in books:
            if book['bookId'] == review['bookId']:  # Match book ID
                book_title = book['title']
                break
        
        print(f"Review ID: {review['reviewId']}")
        print(f"Book: {book_title} (ID: {review['bookId']})")
        print(f"Author: {review['reviewAuthor']}")
        print(f"Date: {review['reviewDate']}")
        print(f"Review: {review['reviewText']}")
        print("-" * 40)

# Function to display the main menu
def display_menu():
    """
    Display the main menu options.
    """
    print("\n=== Book Review Management System ===")
    print("1. Load Data")
    print("2. Save Data")
    print("3. Add Book")
    print("4. Add Review")
    print("5. Books by Year")
    print("6. Books by AI Metric (Lower Than Threshold)")
    print("7. Books With Reviews")
    print("8. Display All Books")
    print("9. Display All Reviews")
    print("0. Exit")

# Main program loop
def main():
    """
    Main program function that handles the menu system.
    """
    print("Welcome to the Book Review Management System!")
    
    # Automatically load data when program starts
    load_data()
    
    while True:
        display_menu()
        choice = input("Enter your choice: ")
        
        if choice == "1":
            load_data()
        elif choice == "2":
            save_data()
        elif choice == "3":
            add_book()
        elif choice == "4":
            add_review()
        elif choice == "5":
            books_by_year()
        elif choice == "6":
            books_by_ai_metric()
        elif choice == "7":
            books_with_reviews()
        elif choice == "8":
            display_books()
        elif choice == "9":
            display_reviews()
        elif choice == "0":
            print("Thank you for using the Book Review Management System!")
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the program

# Function to print titles of all books released in a user specified year
def books_by_year():
    """
    Prompt the user for a release year and print the titles of all books released in that year.
    This function reads from the global `books` list. It handles both string and integer year values.
    """
    print("\n--- Books by Release Year ---")
    if not books:
        print("No books loaded. Please add or load books first.")  # Check if there are no books
        return

    year_input = input("Enter the release year (e.g., 2023): ").strip()
    if not year_input.isdigit():  # Check if input is a valid year
        print("Invalid year. Please enter a numeric year like 2024.")
        return

    year_str = str(year_input)
    matches = [b for b in books if str(b.get("releaseYear", "")).strip() == year_str]  # Find matching books
    if not matches:
        print(f"No books found for the year {year_str}.")
        return

    print(f"Books released in {year_str}:")
    for idx, b in enumerate(matches, start=1):  # Enumerate through matching books
        print(f"{idx}. {b.get('title', 'Untitled')}")

# Function to print titles of all books with AI Metric lower than a user specified value
def books_by_ai_metric():
    """
    Prompt the user for an AI Metric threshold and print titles of books with aiMetric lower than that value.
    Converts aiMetric values to integers safely (treats missing/invalid as very high to avoid false matches).
    """
    print("\n--- Books by AI Metric (Lower Than Threshold) ---")
    if not books:  # Check if there are no books
        print("No books loaded. Please add or load books first.")
        return

    raw = input("Show books with AI Metric lower than: ").strip()  # Get user input
    try:
        threshold = int(raw)
    except ValueError:  # Handle invalid input
        print("Invalid number. Please enter an integer between 0 and 100.")
        return

    def to_int(val):  # Convert value to int, treating invalid/missing as 101
        try:
            return int(val)
        except (TypeError, ValueError):
            # If aiMetric is missing or malformed, treat it as 101 so it won't be picked up accidentally
            return 101 

    matches = [b for b in books if to_int(b.get("aiMetric")) < threshold]  # Find matching books
    if not matches:  # Check if there are no matching books
        print(f"No books found with AI Metric lower than {threshold}.")
        return

    print(f"Books with AI Metric < {threshold}:")  # Print matching books
    for idx, b in enumerate(matches, start=1):  # Enumerate through matching books
        print(f"{idx}. {b.get('title', 'Untitled')} (AI Metric: {b.get('aiMetric')})")

# Function to print all books that have at least 1 review
def books_with_reviews():
    """
    Print all books that have at least one review.
    A review is counted if `review['bookId']` matches the book's `bookId`.
    """
    print("\n--- Books With Reviews ---")
    if not books:
        print("No books loaded. Please add or load books first.")
        return

    # Build an index of review counts per bookId for O(n) pass
    counts = {}
    for r in reviews:  # Count reviews per bookId
        bid = str(r.get("bookId", "")).strip()  # Get the bookId from the review
        if bid:
            counts[bid] = counts.get(bid, 0) + 1  # Increment the count for this bookId

    matches = [(b, counts.get(str(b.get("bookId", "")).strip(), 0)) for b in books]  # Pair books with their review counts
    matches = [(b, c) for b, c in matches if c > 0]  # Filter out books without reviews

    if not matches:
        print("No books have reviews yet.")
        return

    print("Books with at least one review:")
    for idx, (b, c) in enumerate(matches, start=1):  # Enumerate through matching books
        print(f"{idx}. {b.get('title', 'Untitled')} — {c} review(s)")  # Print book title and review count

if __name__ == "__main__":
    main()