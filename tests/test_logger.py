import unittest
import os
import csv
from datetime import datetime
from models import Item, Person
from logger import SystemLogger

class TestSystemLogger(unittest.TestCase):
    def setUp(self):
        self.test_log_file = "test_alerts.csv"
        self.logger = SystemLogger(self.test_log_file)
        self.person = Person("Test Person")
        self.item = Item("Test Item", "TEST001")
        self.person.add_item(self.item)
    
    def tearDown(self):
        # Clean up test files after each test
        if os.path.exists(self.test_log_file):
            os.remove(self.test_log_file)
        if os.path.exists("summary_report.txt"):
            os.remove("summary_report.txt")
    
    def test_initialize_log_file(self):
        self.assertTrue(os.path.exists(self.test_log_file))
        with open(self.test_log_file, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            expected_header = ['Timestamp', 'Person', 'Items', 'Alert', 'Details']
            self.assertEqual(header, expected_header)
    
    def test_log_gate_scan(self):
        self.logger.log_gate_scan(self.person, True)
        
        with open(self.test_log_file, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            row = next(reader)
            
            # Check timestamp format
            datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
            
            self.assertEqual(row[1], "Test Person")
            self.assertEqual(row[2], "Test Item")
            self.assertEqual(row[3], "Yes")
            self.assertEqual(row[4], "Undeactivated tags detected")
    
    def test_generate_report(self):
        # Test report generation with some sample data
        self.logger.generate_report(
            person_counter=5,
            alert_counter=2,
            safe_scan_counter=3,
            alert_history=["Person 1", "Person 3"]
        )
        
        self.assertTrue(os.path.exists("summary_report.txt"))
        with open("summary_report.txt", 'r') as f:
            content = f.read()
            self.assertIn("Total People Scanned: 5", content)
            self.assertIn("Total Alerts: 2", content)
            self.assertIn("Total Safe Scans: 3", content)
            self.assertIn("Person 1", content)
            self.assertIn("Person 3", content)