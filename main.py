import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialogButtonBox
from PyQt5.QtCore import Qt
from PyQt5 import uic
import os

import tempfile
import shutil

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

# Define paths
# Use temp directory for the patched UI file as _MEIPASS is read-only
UI_FILE_NAME = 'main.ui'
UI_FILE_ORIG = get_resource_path(os.path.join('GUI', UI_FILE_NAME))
# Use standard temp dir for the patch to ensure writability
UI_FILE_PATCHED = os.path.join(tempfile.gettempdir(), 'main_patched.ui')

def patch_ui_file():
    """Reads main.ui, fixes PyQt5 incompatible enums, saves to main_patched.ui in tmp"""
    try:
        if not os.path.exists(UI_FILE_ORIG):
             print(f"Warning: Original UI file not found at {UI_FILE_ORIG}")
             return UI_FILE_ORIG # Fatal, but let loader handle

        with open(UI_FILE_ORIG, 'r') as f:
            content = f.read()
        
        # Replace C++ style scoped enums with PyQt5 friendly ones
        new_content = content.replace('QDialogButtonBox::StandardButton::', 'QDialogButtonBox::')
        new_content = new_content.replace('Qt::Orientation::', 'Qt::')
        
        with open(UI_FILE_PATCHED, 'w') as f:
            f.write(new_content)
            
        return UI_FILE_PATCHED
    except Exception as e:
        print(f"Warning: Failed to patch UI file: {e}")
        return UI_FILE_ORIG

class CalculatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Patch and load the UI file
        ui_path = patch_ui_file()
        try:
            uic.loadUi(ui_path, self)
        except FileNotFoundError:
            print(f"Error: UI file not found at {ui_path}")
            sys.exit(1)

        # Initialize state variables
        self.total_marks = 0.0
        self.correct_count = 0
        self.incorrect_count = 0
        self.total_questions = 0

        # Specific counters for each button type
        self.count_pos_1 = 0
        self.count_pos_2 = 0
        self.count_neg_1_3 = 0
        self.count_neg_2_3 = 0
        self.count_pos_0 = 0

        # Set specific line edits to read-only and center align
        self.lineEdit_mark_pos_1.setReadOnly(True)
        self.lineEdit_mark_pos_1.setAlignment(Qt.AlignCenter)
        
        self.lineEdit_mark_pos_2.setReadOnly(True)
        self.lineEdit_mark_pos_2.setAlignment(Qt.AlignCenter)
        
        self.lineEdit_mark_neg_onethird.setReadOnly(True)
        self.lineEdit_mark_neg_onethird.setAlignment(Qt.AlignCenter)
        
        self.lineEdit_mark_neg_twothird.setReadOnly(True)
        self.lineEdit_mark_neg_twothird.setAlignment(Qt.AlignCenter)
        
        self.lineEdit_mark_pos_0.setReadOnly(True)
        self.lineEdit_mark_pos_0.setAlignment(Qt.AlignCenter)

        # Set display LineEdits to read-only and center align
        self.lineEdit_total_marks.setReadOnly(True)
        self.lineEdit_total_marks.setAlignment(Qt.AlignCenter)
        
        self.lineEdit_correct_ans.setReadOnly(True)
        self.lineEdit_correct_ans.setAlignment(Qt.AlignCenter)
        
        self.lineEdit_incorrect.setReadOnly(True)
        self.lineEdit_incorrect.setAlignment(Qt.AlignCenter)
        
        self.lineEdit_total.setReadOnly(True)
        self.lineEdit_total.setAlignment(Qt.AlignCenter)

        # Connect buttons to functions
        self.mark_pos_1_pushButt.clicked.connect(self.add_1_mark)
        self.mark_pos_2_pushButt.clicked.connect(self.add_2_marks)
        self.mark_neg_onethird_pushButt.clicked.connect(self.sub_1_3_mark)
        self.mark_neg_twothird_pushButt.clicked.connect(self.sub_2_3_mark)
        self.mark_pos_0_pushButt.clicked.connect(self.add_0_mark)
        
        # Set window title
        self.setWindowTitle("MRKCalc")
        
        # Connect ButtonBox / Close Button
        # User reported issues with closeButton presence. 
        # Checking if it exists before connecting to avoid crashes.
        if hasattr(self, 'closeButton'):
             self.closeButton.clicked.connect(self.close)
        elif hasattr(self, 'buttonBox'):
             self.buttonBox.accepted.connect(self.close)
             self.buttonBox.rejected.connect(self.close)

        # Initial display update
        self.update_display()

    def add_1_mark(self):
        self.total_marks += 1.0
        self.correct_count += 1
        self.total_questions += 1
        self.count_pos_1 += 1
        self.update_display()

    def add_2_marks(self):
        self.total_marks += 2.0
        self.correct_count += 1
        self.total_questions += 1
        self.count_pos_2 += 1
        self.update_display()

    def sub_1_3_mark(self):
        self.total_marks -= (1/3)
        self.incorrect_count += 1
        self.total_questions += 1
        self.count_neg_1_3 += 1
        self.update_display()

    def sub_2_3_mark(self):
        self.total_marks -= (2/3)
        self.incorrect_count += 1
        self.total_questions += 1
        self.count_neg_2_3 += 1
        self.update_display()

    def add_0_mark(self):
        # 0 marks added
        self.total_marks += 0.0
        self.total_questions += 1
        self.count_pos_0 += 1
        self.update_display()

    def update_display(self):
        # Main displays
        self.lineEdit_total_marks.setText(f"{self.total_marks:.2f}")
        self.lineEdit_correct_ans.setText(str(self.correct_count))
        self.lineEdit_incorrect.setText(str(self.incorrect_count))
        self.lineEdit_total.setText(str(self.total_questions))

        # Individual mark displays
        # "if mark 1 is clicked 5 times it show 5 marks" -> count * value
        self.lineEdit_mark_pos_1.setText(f"{self.count_pos_1 * 1}")
        self.lineEdit_mark_pos_2.setText(f"{self.count_pos_2 * 2}")
        
        # Negative marks logic - accumulated value
        # Using .2f for cleaner display of floats
        self.lineEdit_mark_neg_onethird.setText(f"{self.count_neg_1_3 * (-1/3):.2f}")
        self.lineEdit_mark_neg_twothird.setText(f"{self.count_neg_2_3 * (-2/3):.2f}")
        
        # Zero mark logic: "0 x _times_the button_clicked_"
        self.lineEdit_mark_pos_0.setText(f"0 x {self.count_pos_0}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalculatorApp()
    window.show()
    sys.exit(app.exec_())
