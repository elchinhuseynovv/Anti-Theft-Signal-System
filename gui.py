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
        
        # Create figure and plot
        fig, ax = plt.subplots(figsize=(6, 4))
        labels = ['Safe Scans', 'Alert Scans']
        sizes = [safe_scans, alert_scans]
        colors = ['#2ecc71', '#e74c3c']
        
        if sum(sizes) > 0:  # Only create pie chart if there's data
            ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
        else:
            ax.text(0.5, 0.5, 'No scan data available', 
                   horizontalalignment='center',
                   verticalalignment='center')
            ax.axis('off')
        
        # Embed plot in Tkinter window
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

        # Available items in the store with prices
        self.available_items = [
            Item("Milk", "RFID001", price=3.99, category="Dairy"),
            Item("Bread", "RFID002", price=2.49, category="Bakery"),
            Item("Cheese", "RFID003", price=4.99, category="Dairy"),
            Item("Coffee", "RFID004", price=7.99, category="Beverages"),
            Item("Chocolate", "RFID005", price=1.99, category="Snacks")
        ]

        # Create first person and system components
        self.new_person()
        self.cashier = Cashier("Sarah")
        self.gate = Gate()

        self.create_widgets()
        self.update_button_states()

    def create_widgets(self):
        """Create all GUI widgets."""
        # Title and Person Info Frame
        title_frame = ttk.Frame(self.root, padding="20 20 20 10")
        title_frame.grid(row=0, column=0, sticky="ew")
        
        title_label = ttk.Label(
            title_frame, 
            text="Supermarket Anti-Theft System", 
            font=('Helvetica', 16, 'bold')
        )
        title_label.pack(side="left", padx=10)

        self.person_label = ttk.Label(
            title_frame,
            text=f"Current Customer: {self.current_person.name}",
            font=self.header_font
        )
        self.person_label.pack(side="right", padx=10)

        # Stats Frame
        stats_frame = ttk.Frame(self.root, padding="20 10")
        stats_frame.grid(row=1, column=0, sticky="ew", padx=20)
        
        self.alert_label = ttk.Label(
            stats_frame,
            text="Total Alerts: 0",
            font=self.header_font,
            foreground='red'
        )
        self.alert_label.pack(side="left")

        new_person_btn = ttk.Button(
            stats_frame,
            text="New Person",
            command=self.new_person
        )
        new_person_btn.pack(side="right")

        # Analysis Frame
        analysis_frame = ttk.LabelFrame(
            self.root,
            text="Analysis Tools",
            padding="20 10 20 20"
        )
        analysis_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        ttk.Button(
            analysis_frame,
            text="Show Statistics",
            command=lambda: StatisticsWindow(self.root, self.safe_scan_counter, self.alert_counter)
        ).pack(side="left", padx=5)

        ttk.Button(
            analysis_frame,
            text="Simulate Random Customers",
            command=self.simulate_random_customers
        ).pack(side="left", padx=5)

        ttk.Button(
            analysis_frame,
            text="Generate Report",
            command=lambda: self.logger.generate_report(
                self.person_counter,
                self.alert_counter,
                self.safe_scan_counter,
                self.alert_history
            )
        ).pack(side="left", padx=5)

        # Item Selection Frame
        self.item_frame = ttk.LabelFrame(
            self.root, 
            text="Add Items to Basket", 
            padding="20 10 20 20"
        )
        self.item_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        # Configure item frame grid
        self.item_frame.columnconfigure(1, weight=1)
        
        # Item selection widgets
        ttk.Label(
            self.item_frame, 
            text="Select Item:", 
            font=self.header_font
        ).grid(row=0, column=0, padx=5, pady=5)
        
        self.item_var = tk.StringVar()
        item_names = [item.name for item in self.available_items]
        self.item_dropdown = ttk.Combobox(
            self.item_frame, 
            textvariable=self.item_var, 
            values=item_names,
            width=30
        )
        self.item_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        self.add_button = ttk.Button(
            self.item_frame, 
            text="Add to Basket",
            command=self.add_item
        )
        self.add_button.grid(row=0, column=2, padx=5, pady=5)

        # Current Basket Frame
        self.basket_frame = ttk.LabelFrame(
            self.root,
            text="Current Basket",
            padding="20 10 20 20"
        )
        self.basket_frame.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        
        # Basket display
        self.basket_display = tk.Text(
            self.basket_frame,
            height=5,
            width=70,
            font=self.text_font,
            wrap=tk.WORD,
            bg='#ffffff',
            fg='#000000'
        )
        self.basket_display.pack(fill=tk.BOTH, expand=True)
        self.basket_display.config(state=tk.DISABLED)

        # Actions Frame
        self.action_frame = ttk.LabelFrame(
            self.root, 
            text="Actions", 
            padding="20 10 20 20"
        )
        self.action_frame.grid(row=5, column=0, padx=20, pady=10, sticky="ew")

        # Action buttons with improved styling
        style = ttk.Style()
        style.configure('Action.TButton', font=self.text_font)
        style.configure('Alert.TButton', foreground='red')

        self.cashier_button = ttk.Button(
            self.action_frame, 
            text="Go to Cashier",
            style='Action.TButton',
            command=self.go_to_cashier
        )
        self.cashier_button.pack(side="left", padx=10)

        self.skip_cashier_button = ttk.Button(
            self.action_frame,
            text="Skip Cashier",
            style='Alert.TButton',
            command=self.skip_cashier
        )
        self.skip_cashier_button.pack(side="left", padx=10)

        self.gate_button = ttk.Button(
            self.action_frame, 
            text="Pass Through Gate",
            style='Action.TButton',
            command=self.pass_through_gate
        )
        self.gate_button.pack(side="left", padx=10)

        self.clear_button = ttk.Button(
            self.action_frame, 
            text="Clear Basket",
            style='Action.TButton',
            command=self.clear_basket
        )
        self.clear_button.pack(side="left", padx=10)

        # Status Label Frame
        self.status_frame = ttk.Frame(self.root, padding="20 10 20 10")
        self.status_frame.grid(row=6, column=0, sticky="ew", padx=20)
        
        self.status_label = ttk.Label(
            self.status_frame,
            text="Ready to scan items",
            font=self.status_font,
            foreground='#666666'
        )
        self.status_label.pack()

        # System Log Frame
        self.log_frame = ttk.LabelFrame(
            self.root, 
            text="System Log", 
            padding="20 10 20 20"
        )
        self.log_frame.grid(row=7, column=0, padx=20, pady=10, sticky="nsew")
        self.log_frame.columnconfigure(0, weight=1)
        self.log_frame.rowconfigure(0, weight=1)

        # Log display with custom font and colors
        self.log_text = tk.Text(
            self.log_frame,
            height=15,
            width=70,
            font=self.log_font,
            wrap=tk.WORD,
            bg='#ffffff',
            fg='#000000'
        )
        self.log_text.grid(row=0, column=0, sticky="nsew")

        # Add scrollbar to log
        scrollbar = ttk.Scrollbar(
            self.log_frame,
            orient="vertical",
            command=self.log_text.yview
        )
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.log_text.configure(yscrollcommand=scrollbar.set)

        # Configure grid weights
        self.root.grid_rowconfigure(7, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def simulate_random_customers(self):
        """Simulate multiple customers with random behaviors."""
        try:
            for _ in range(10):
                self.new_person()
                # Add 1-5 random items
                num_items = random.randint(1, 5)
                for _ in range(num_items):
                    item = random.choice(self.available_items)
                    new_item = Item(item.name, item.tag_id, price=item.price, category=item.category)
                    self.current_person.add_item(new_item)
                    self.update_basket_display()
                    self.update_button_states()
                    self.root.update_idletasks()
                    time.sleep(0.2)