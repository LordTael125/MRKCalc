# MRKCalc

A specialized calculator designed to help students and exam aspirants calculate their total marks based on standard competitive exam marking schemes (e.g., GATE, IES, JEE, etc.). It handles positive marks (+1, +2) and their corresponding negative deductions (-1/3, -2/3) efficiently.

Built with **Python** and **PyQt5**.

## Features

- **Marking Scheme Support**:
  - **+1 Mark**: For correct 1-mark questions.
  - **+2 Marks**: For correct 2-mark questions.
  - **-1/3 Mark**: Deduction for incorrect 1-mark questions.
  - **-2/3 Mark**: Deduction for incorrect 2-mark questions.
  - **+0 Mark**: For numerical answer type (NAT) or unattempted questions where applicable.
- **Real-time Statistics**: Automatically updates and displays:
  - Total Marks Scored.
  - Number of Correct Attempts.
  - Number of Incorrect Attempts.
  - Total Questions Attempted.
- **Detailed Breakdown**: Shows the count of questions attempted for each category (e.g., "5 x 1 mark", "3 x -0.33").
- **Portable**: Can be built into a standalone Linux AppImage.

## Prerequisites

- Python 3.x
- PyQt5

## Installation & Running Locally

1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd GATEMCalculator
    ```

2.  **Install Dependencies**:
    ```bash
    pip install PyQt5
    ```

3.  **Run the Application**:
    ```bash
    python main.py
    ```

## Building Executable (AppImage)

The project includes a script to package the application as a standalone Linux AppImage, similar to a portable `.exe` on Windows.

1.  **Make the build script executable**:
    ```bash
    chmod +x build_package.sh
    ```

2.  **Run the build script**:
    ```bash
    ./build_package.sh
    ```

    This script will:
    - Clean previous builds.
    - Run **PyInstaller** to create a single-file executable.
    - Create the AppImage directory structure.
    - Download `appimagetool` (if not present).
    - Generate `MRKCalc.AppImage`.

3.  **Run the AppImage**:
    You can simply double-click the generated `.AppImage` file or run it from the terminal:
    ```bash
    ./MRKCalc.AppImage
    ```

## Project Structure

- **main.py**: The entry point of the application. Handles logic and UI loading.
- **GUI/**: Contains the User Interface files (`.ui`).
- **build_package.sh**: Automated script to build the AppImage.
- **test_logic.py**: Unit tests for the calculator logic.

## Troubleshooting

- **UI File Not Found**: The application dynamically patches the `.ui` file for compatibility. Ensure `GUI/main.ui` exists.
- **PyQt5 Errors**: Ensure you have a compatible version of PyQt5 installed (`pip install PyQt5`).
