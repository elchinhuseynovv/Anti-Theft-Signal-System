import csv
from datetime import datetime
import os
from tkinter import messagebox

class SystemLogger:
    def __init__(self, log_file="alerts.csv"):
        self.log_file = log_file
        self.initialize_log_file()
        
    def initialize_log_file(self):
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Timestamp', 'Person', 'Items', 'Alert', 'Details'])

    def log_gate_scan(self, person, alert_triggered):
        with open(self.log_file, 'a', newline='') as file:
            writer = csv.writer(file)
            items_list = ', '.join([item.name for item in person.items])
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                person.name,
                items_list,
                "Yes" if alert_triggered else "No",
                "Undeactivated tags detected" if alert_triggered else "All tags deactivated"
            ])

    def generate_report(self, person_counter, alert_counter, safe_scan_counter, alert_history):
        with open('summary_report.txt', 'w') as f:
            f.write("=== Supermarket Anti-Theft System Report ===\n\n")
            f.write(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"Total People Scanned: {person_counter}\n")
            f.write(f"Total Alerts: {alert_counter}\n")
            f.write(f"Total Safe Scans: {safe_scan_counter}\n\n")
            
            if alert_history:
                f.write("People Who Triggered Alerts:\n")
                for person in alert_history:
                    f.write(f"- {person}\n")
            else:
                f.write("No alerts were triggered during this session.\n")
        
        messagebox.showinfo("Report Generated", 
                          "Summary report has been generated as 'summary_report.txt'")