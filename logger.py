import csv
from datetime import datetime
import os
from tkinter import messagebox
import json

class SystemLogger:
    """
    Handles system logging, reporting, and analytics.
    
    Attributes:
        log_file (str): Path to the CSV log file
        json_log_file (str): Path to the JSON log file
        log_entries (list): In-memory log entries
    """
    
    def __init__(self, log_file="alerts.csv", json_log_file="alerts.json"):
        self.log_file = log_file
        self.json_log_file = json_log_file
        self.log_entries = []
        self.initialize_log_files()
        
    def initialize_log_files(self):
        """Initialize log files with headers."""
        # Initialize CSV log
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    'Timestamp',
                    'Person',
                    'Items',
                    'Alert',
                    'Details',
                    'Total Value',
                    'Duration'
                ])
        
        # Initialize JSON log
        if not os.path.exists(self.json_log_file):
            with open(self.json_log_file, 'w') as file:
                json.dump([], file)

    def log_gate_scan(self, person, alert_triggered):
        """
        Log a gate scanning event.
        
        Args:
            person (Person): The person being scanned
            alert_triggered (bool): Whether an alert was triggered
        """
        timestamp = datetime.now()
        items_list = ', '.join([item.name for item in person.items])
        total_value = sum(item.price for item in person.items)
        duration = (timestamp - person.entry_time).total_seconds()
        
        # Create log entry
        entry = {
            'timestamp': timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            'person': person.name,
            'items': items_list,
            'alert': "Yes" if alert_triggered else "No",
            'details': "Undeactivated tags detected" if alert_triggered else "All tags deactivated",
            'total_value': f"${total_value:.2f}",
            'duration': f"{duration:.1f}s"
        }
        