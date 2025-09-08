
Context
I am building a small Book + Review CLI in VS Code. I am not an avid coder, so I describe what I want and let Copilot draft it. The assignment already provides sample data and I saved it as data_file_assgt-01.json so the app can preload it.

Working style
I type short prompts like “make a function to do X” and then I read what Copilot produces. If something feels off, I ask a follow‑up, or I edit the code in small ways. I’m trying to keep the code simple enough that I can read every line and explain it.

Problem 1: Data Persistence (Load / Save) using the provided sample file
Me: The sample data is already provided. I saved it to data_file_assgt-01.json with top-level keys books and reviews. Please write load_data(filename='data_file_assgt-01.json') that reads those lists into global books and reviews on startup and prints how many records it loaded. Also write save_data(...) that writes back to the same file. If the file is missing or has invalid JSON, don’t crash—just start with empty lists and show a friendly message.
Copilot: Drafted both functions with try/except and messages.
Me: Looks good. I asked for slightly clearer messages (show counts after load; confirmation after save). I kept auto-save after adding a book or a review so I don’t forget to save, and still left Save in the menu for manual control.

Problem 2: Creating Data (Add Book / Add Review)
Me: Make add_book() that prompts for title, aiMetric (0–100), releaseYear, author, genres (comma‑separated), publisherName, publisherLocation, pages (int), sales (comma‑separated ints). Use numeric bookId by taking the current max id and adding 1. After adding, call save_data(). Keep field names exactly the same as the sample schema.
Copilot: Wrote the function. It splits genres and sales. bookId is string, computed with max+1.
Me: This matches the sample. I noted that pages or sales could throw ValueError if I type letters. For now I kept it simple and plan to add input validation later.

Me: Now add_review(). First print the list of existing books (id + title) so I know what to pick. Ask for a bookId and validate it exists. Then ask for reviewAuthor and reviewText. Use today’s date in YYYY‑MM‑DD for reviewDate. reviewId should use max+1 as well. Save after adding.
Copilot: Implemented it. If bookId is invalid, it prints a message and returns.
Me: This is exactly what I needed.

Problem 3: Display functions
Me: I need display_books() to show each book in a readable block (including nested publisher) and display_reviews() to show each review along with the resolved book title. If a review references an unknown bookId, print “Unknown Book” and continue.
Copilot: Implemented both. It loops over reviews and for each one scans books to find the title. If it doesn’t find it, it uses “Unknown Book”.
Me: I added a short comment to explain that loop so it’s clear how the title is resolved.

Problem 4: Query helpers (Part‑2)
Me: books_by_year(): Ask for a year and print all titles released that year. releaseYear might be saved as int or string, so compare using strings.
Copilot: Did it and added a numeric input check.
Me: Works. If I type spaces around the year, it still handles it after strip() which is nice.

Me: books_by_ai_metric(): Ask for a numeric threshold and list titles where aiMetric < threshold. If aiMetric is missing or not numeric, skip that book and don’t crash.
Copilot: Added a small helper that converts to int with try/except; invalid values return a sentinel so they don’t match.
Me: I added a clear error message if I type a non‑number at the prompt.

Me: books_with_reviews(): List every book that has at least one review and show the count per title.
Copilot: Built a bookId→count map and printed “Title — N review(s)”. Handles the empty case.
Me: No changes needed.

Problem 5: Menu and main loop
Me: Create display_menu() and main() so I can pick actions. The menu should include 1 Load, 2 Save, 3 Add Book, 4 Add Review, 5 Books by Year, 6 Books by AI Metric, 7 Books With Reviews, 8 Display All Books, 9 Display All Reviews, 0 Exit.
Copilot: First draft only printed 1..6 in the menu even though main() handled 1..9. I noticed this while testing and asked it to fix the menu text so the UI matches the logic.
Me: After the fix, the menu and main() routes are consistent and testing is easier.

Quick checks I ran
• Start with the sample file present and run Load → it prints how many records were loaded.
• Display All Books → I can see the sample books including nested publisher and genres.
• Display All Reviews → I can see the review list with the right book titles resolved.
• books_by_year → returns expected titles for 2023 and 2024; if I enter 1999 it shows “No books found”.
• books_by_ai_metric with a number → filters properly; with a word it shows a helpful error.
• books_with_reviews → shows all titles that have at least one review with the correct counts.
• Add Book / Add Review → new ids use max+1; auto‑save writes back to data_file_assgt-01.json.

Where AI was helpful
• The load/save skeleton with try/except and friendly messages (I kept this with minor tweaks).
• The review display logic that resolves bookId to a title while avoiding crashes on missing matches.

Where AI needed adjustments
• The menu text was incomplete at first (it didn’t list items 7..9). I asked it to update the printed menu so it matches main().
• Input parsing for numbers can still be improved. I plan to add retry loops for pages, sales, and aiMetric.

What I understand about the loops
• In display_reviews(), for each review the code scans the books list to find the book with the same bookId and reads its title. If no match is found, we print “Unknown Book”. This keeps the output readable without risking a crash.
• In books_by_ai_metric(), a small helper safely converts aiMetric to int. If conversion fails, we return a sentinel (bigger than any real threshold) so that entry won’t be listed by mistake.

Backlog if I iterate again
• Add input validation loops for pages, sales, and aiMetric.
• Add a “reset to original sample” option that re-seeds the JSON if I mess it up while testing.
• Add non‑interactive helper functions that return lists instead of printing, so I can unit‑test the logic more easily.
