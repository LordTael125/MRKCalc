import sys
from PyQt5.QtWidgets import QApplication
from main import CalculatorApp
import unittest

class TestCalculatorLogic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create the app instance once
        cls.app = QApplication(sys.argv)
        cls.window = CalculatorApp()

    def setUp(self):
        # Reset state before each test
        self.window.total_marks = 0.0
        self.window.correct_count = 0
        self.window.incorrect_count = 0
        self.window.total_questions = 0
        
        self.window.count_pos_1 = 0
        self.window.count_pos_2 = 0
        self.window.count_neg_1_3 = 0
        self.window.count_neg_2_3 = 0
        self.window.count_pos_0 = 0
        
        self.window.update_display()

    def test_add_1_mark(self):
        self.window.mark_pos_1_pushButt.click()
        self.assertEqual(self.window.total_marks, 1.0)
        self.assertEqual(self.window.correct_count, 1)
        self.assertEqual(self.window.total_questions, 1)
        self.assertEqual(self.window.lineEdit_total_marks.text(), "1.00")
        self.assertEqual(self.window.lineEdit_mark_pos_1.text(), "1")

    def test_add_2_marks(self):
        self.window.mark_pos_2_pushButt.click()
        self.assertEqual(self.window.total_marks, 2.0)
        self.assertEqual(self.window.correct_count, 1)
        self.assertEqual(self.window.total_questions, 1)
        self.assertEqual(self.window.lineEdit_total_marks.text(), "2.00")
        self.assertEqual(self.window.lineEdit_mark_pos_2.text(), "2")

    def test_sub_1_3_mark(self):
        self.window.mark_neg_onethird_pushButt.click()
        self.assertAlmostEqual(self.window.total_marks, -1/3, places=2)
        self.assertEqual(self.window.incorrect_count, 1)
        self.assertEqual(self.window.total_questions, 1)
        self.assertEqual(self.window.lineEdit_total_marks.text(), "-0.33")
        self.assertEqual(self.window.lineEdit_mark_neg_onethird.text(), "-0.33")

    def test_sub_2_3_mark(self):
        self.window.mark_neg_twothird_pushButt.click()
        self.assertAlmostEqual(self.window.total_marks, -2/3, places=2)
        self.assertEqual(self.window.incorrect_count, 1)
        self.assertEqual(self.window.total_questions, 1)
        self.assertEqual(self.window.lineEdit_total_marks.text(), "-0.67")
        self.assertEqual(self.window.lineEdit_mark_neg_twothird.text(), "-0.67")
        
    def test_add_0_mark(self):
        self.window.mark_pos_0_pushButt.click()
        self.assertEqual(self.window.total_marks, 0.0)
        self.assertEqual(self.window.correct_count, 0)
        self.assertEqual(self.window.incorrect_count, 0)
        self.assertEqual(self.window.total_questions, 1)
        self.assertEqual(self.window.lineEdit_total_marks.text(), "0.00")
        self.assertEqual(self.window.lineEdit_mark_pos_0.text(), "0 x 1")

    def test_mixed_sequence(self):
        # +1 (5 times), +2 (8 times), 0 (3 times) to test user request specifically
        for _ in range(5):
             self.window.mark_pos_1_pushButt.click()
        
        self.assertEqual(self.window.lineEdit_mark_pos_1.text(), "5") # 5 * 1
             
        for _ in range(8):
             self.window.mark_pos_2_pushButt.click()
             
        self.assertEqual(self.window.lineEdit_mark_pos_2.text(), "16") # 8 * 2
        
        for _ in range(3):
            self.window.mark_pos_0_pushButt.click()
            
        self.assertEqual(self.window.lineEdit_mark_pos_0.text(), "0 x 3") # 0 x count

        # Check legacy mixed totals logic briefly
        # Total = 5*1 + 8*2 + 0 = 21
        self.assertEqual(self.window.lineEdit_total_marks.text(), "21.00")

if __name__ == '__main__':
    unittest.main()
