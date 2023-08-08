# File Content Searcher

## Description
File Content Searcher is a simple GUI application built using Python and Tkinter. It allows users to search for a specified keyword within all files in a selected directory and its subdirectories. After completing the search, the application prompts the user to save a log file containing details about the search, including the time the search was run, the total number of files scanned, and the list of matching files.

## Prerequisites

Ensure you have the following installed
- Python (3.x recommended)
- Tkinter (usually comes bundled with Python)

## How to Run

1. Clone the repository or download the script.
2. Navigate to the script's directory via your terminal or command prompt.
3. Run the script using the command `python file_content_searcher.py` (or `python3` depending on your setup).

## Features

### User-Friendly GUI
- **Intuitive Design:** The graphical interface is simple and intuitive, requiring minimal instructions for use. 
- **Input Flexibility:** Users can manually type in or use a "Browse" button to select the directory for searching.

### Advanced Search Capabilities
- **Recursive Searching:** The application recursively searches through all files in the selected directory, including nested subdirectories.
- **Keyword Search:** Users can specify any keyword, and the program will hunt for files containing that keyword.

### Multi-Threading for Performance
- **Responsive UI:** By leveraging multi-threading, the application remains responsive, allowing users to see real-time search progress without freezing.
- **Concurrent Processing:** The search operation runs on a separate thread, ensuring the UI is free to update and show progress.

### Real-Time Feedback
- **Progress Bar:** As the application sifts through files, a progress bar visually represents how much of the search operation is complete.
- **Detailed Results Display:** Matching file paths are shown in a scrollable text area, providing users with clickable links to open the files directly.

### Comprehensive Logging
- **Save Search Results:** After the search completes, users are prompted to save a detailed log of the operation.
- **Log Details:** Each log file encapsulates key information including:
  - The exact date and time of the search.
  - The specified search keyword.
  - Total number of files scanned.
  - Number of files matching the search criteria.
  - Paths to the matching files.

## Contribution

Contributions are welcome! Please ensure that any changes do not break the existing functionalities and that the code is properly commented.

## License

This project is open source (use it as you please)
