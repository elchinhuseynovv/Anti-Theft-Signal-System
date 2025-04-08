import tkinter as tk
from tkinter import ttk, messagebox, font
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import time
from models import Item, Person, Cashier, Gate
from logger import SystemLogger

class StatisticsWindow:
    def __init__(self, parent, safe_scans, alert_scans):
        self.window = tk.Toplevel(parent)
        self.window.title("Scan Statistics")
        self.window.geometry("600x400")
        
        fig, ax = plt.subplots(figsize=(6, 4))
        labels = ['Safe Scans', 'Alert Scans']
        sizes = [safe_scans, alert_scans]
        colors = ['#2ecc71', '#e74c3c']
        
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        
        canvas = FigureCanvasTkAgg(fig, master=self.window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=20)


class AntiTheftGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Supermarket Anti-Theft System")
        self.root.geometry("1000x1000")
        self.root.configure(bg='#f0f0f0')

        # Initialize fonts
        self.header_font = font.Font(size=12, weight='bold')
        self.text_font = font.Font(size=10)
        self.log_font = font.Font(size=11, family='Courier')
        self.status_font = font.Font(size=12, weight='bold')

        # Initialize counters and system components
        self.person_counter = 0
        self.alert_counter = 0
        self.safe_scan_counter = 0
        self.alert_history = []
        
        # Initialize logger
        self.logger = SystemLogger()

        # Available items in the store
        self.available_items = [
            Item("Milk", "RFID001"),
            Item("Bread", "RFID002"),
            Item("Cheese", "RFID003"),
            Item("Coffee", "RFID004"),
            Item("Chocolate", "RFID005")
        ]

        # Create first person and system components
        self.new_person()
        self.cashier = Cashier("Sarah")
        self.gate = Gate()

        self.create_widgets()
        self.update_button_states()

    # [Rest of the AntiTheftGUI class methods remain the same as in the original file]
    # Include all methods from the original AntiTheftGUI class here