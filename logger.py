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
        
        # Add to in-memory log
        self.log_entries.append(entry)
        
        # Write to CSV
        with open(self.log_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                entry['timestamp'],
                entry['person'],
                entry['items'],
                entry['alert'],
                entry['details'],
                entry['total_value'],
                entry['duration']
            ])
        
        # Update JSON log
        with open(self.json_log_file, 'w') as file:
            json.dump(self.log_entries, file, indent=2)

    def generate_report(self, person_counter, alert_counter, safe_scan_counter, alert_history):
        """
        Generate a detailed summary report.
        
        Args:
            person_counter (int): Total number of people scanned
            alert_counter (int): Total number of alerts
            safe_scan_counter (int): Total number of safe scans
            alert_history (list): List of people who triggered alerts
        """
        with open('summary_report.txt', 'w') as f:
            f.write("=== Supermarket Anti-Theft System Report ===\n\n")
            f.write(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Overall Statistics
            f.write("=== Overall Statistics ===\n")
            f.write(f"Total People Scanned: {person_counter}\n")
            f.write(f"Total Alerts: {alert_counter}\n")
            f.write(f"Total Safe Scans: {safe_scan_counter}\n")
            
            if person_counter > 0:
                alert_rate = (alert_counter / person_counter) * 100
                f.write(f"Alert Rate: {alert_rate:.1f}%\n\n")
            
            # Alert History
            f.write("=== Alert History ===\n")
            if alert_history:
                for person in alert_history:
                    f.write(f"- {person}\n")
            else:
                f.write("No alerts were triggered during this session.\n\n")
            
            # Value Analysis
            if self.log_entries:
                total_value = sum(float(entry['total_value'].replace('$', '')) 
                                for entry in self.log_entries)
                avg_duration = sum(float(entry['duration'].replace('s', '')) 
                                 for entry in self.log_entries) / len(self.log_entries)
                
                f.write("\n=== Value Analysis ===\n")
                f.write(f"Total Value Processed: ${total_value:.2f}\n")
                f.write(f"Average Processing Time: {avg_duration:.1f}s\n")
        
        messagebox.showinfo(
            "Report Generated", 
            "Summary report has been generated as 'summary_report.txt'"
        )

    def get_analytics(self):
        """
        Get system analytics.
        
        Returns:
            dict: Analytics data including trends and patterns
        """
        if not self.log_entries:
            return None
            
        analytics = {
            'total_entries': len(self.log_entries),
            'alert_rate': sum(1 for entry in self.log_entries if entry['alert'] == 'Yes') / len(self.log_entries),
            'avg_basket_value': sum(float(entry['total_value'].replace('$', '')) for entry in self.log_entries) / len(self.log_entries),
            'avg_processing_time': sum(float(entry['duration'].replace('s', '')) for entry in self.log_entries) / len(self.log_entries)
        }
        
        return analytics