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
        self.total_revenue = 0.0
        self.total_prevented_theft = 0.0
        
        # Initialize logger
        self.logger = SystemLogger()

        # Available items in the store with prices
        self.available_items = [
            Item("Milk", "RFID001", price=3.99, category="Dairy"),
            Item("Bread", "RFID002", price=2.49, category="Bakery"),
            Item("Cheese", "RFID003", price=4.99, category="Dairy"),
            Item("Coffee", "RFID004", price=7.99, category="Beverages"),
            Item("Chocolate", "RFID005", price=1.99, category="Snacks"),
            # Add more items
            Item("Apple", "RFID006", price=0.99, category="Produce"),
            Item("Cereal", "RFID007", price=5.99, category="Breakfast"),
            Item("Chips", "RFID008", price=3.49, category="Snacks"),
            Item("Soda", "RFID009", price=2.99, category="Beverages"),
            Item("Eggs", "RFID010", price=4.49, category="Dairy")
        ]

        # Create first person and system components
        self.new_person()
        self.cashier = Cashier("Sarah")
        self.gate = Gate()

        self.create_widgets()
        self.update_button_states()
        
        # Set up keyboard shortcuts
        self.setup_shortcuts()

    def setup_shortcuts(self):
        """Set up keyboard shortcuts for common actions."""
        self.root.bind('<Control-n>', lambda e: self.new_person())
        self.root.bind('<Control-a>', lambda e: self.add_item())
        self.root.bind('<Control-c>', lambda e: self.clear_basket())
        self.root.bind('<Control-g>', lambda e: self.go_to_cashier())
        self.root.bind('<Control-p>', lambda e: self.pass_through_gate())

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

        # Revenue Display
        revenue_frame = ttk.Frame(self.root, padding="20 10")
        revenue_frame.grid(row=1, column=1, sticky="ew", padx=20)
        
        self.revenue_label = ttk.Label(
            revenue_frame,
            text="Total Revenue: $0.00",
            font=self.header_font,
            foreground='green'
        )
        self.revenue_label.pack(side="left")
        
        self.prevented_theft_label = ttk.Label(
            revenue_frame,
            text="Prevented Theft: $0.00",
            font=self.header_font,
            foreground='blue'
        )
        self.prevented_theft_label.pack(side="right")

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

        # Search Bar
        search_frame = ttk.Frame(self.root, padding="20 10")
        search_frame.grid(row=2, column=1, sticky="ew", padx=20)
        
        ttk.Label(
            search_frame,
            text="Search Items:",
            font=self.text_font
        ).pack(side="left")
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.update_item_list())
        
        search_entry = ttk.Entry(
            search_frame,
            textvariable=self.search_var
        )
        search_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        # Add Shortcuts Help Button
        ttk.Button(
            search_frame,
            text="Keyboard Shortcuts",
            command=self.show_shortcuts
        ).pack(side="right")

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

        # Category Filter
        filter_frame = ttk.LabelFrame(
            self.root,
            text="Filter by Category",
            padding="20 10 20 20"
        )
        filter_frame.grid(row=3, column=1, padx=20, pady=10, sticky="ew")
        
        categories = sorted(set(item.category for item in self.available_items))
        self.category_var = tk.StringVar(value="All")
        
        ttk.Radiobutton(
            filter_frame,
            text="All",
            variable=self.category_var,
            value="All",
            command=self.update_item_list
        ).pack(anchor="w")
        
        for category in categories:
            ttk.Radiobutton(
                filter_frame,
                text=category,
                variable=self.category_var,
                value=category,
                command=self.update_item_list
            ).pack(anchor="w")

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
            command=self.go_to_cashier,
            state=tk.DISABLED
        )
        self.cashier_button.pack(side="left", padx=10)

        self.skip_cashier_button = ttk.Button(
            self.action_frame,
            text="Skip Cashier",
            style='Alert.TButton',
            command=self.skip_cashier,
            state=tk.DISABLED
        )
        self.skip_cashier_button.pack(side="left", padx=10)

        self.gate_button = ttk.Button(
            self.action_frame, 
            text="Pass Through Gate",
            style='Action.TButton',
            command=self.pass_through_gate,
            state=tk.DISABLED
        )
        self.gate_button.pack(side="left", padx=10)

        self.clear_button = ttk.Button(
            self.action_frame, 
            text="Clear Basket",
            style='Action.TButton',
            command=self.clear_basket,
            state=tk.DISABLED
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

    def show_shortcuts(self):
        """Display keyboard shortcuts help window."""
        shortcuts = """
        Keyboard Shortcuts:
        ------------------
        Ctrl + N: New Person
        Ctrl + A: Add Item
        Ctrl + C: Clear Basket
        Ctrl + G: Go to Cashier
        Ctrl + P: Pass Through Gate
        """
        messagebox.showinfo("Keyboard Shortcuts", shortcuts)

    def update_item_list(self):
        """Update the item dropdown based on category filter and search."""
        selected_category = self.category_var.get()
        search_text = self.search_var.get().lower()
        
        filtered_items = [
            item.name for item in self.available_items
            if (selected_category == "All" or item.category == selected_category)
            and (search_text == "" or search_text in item.name.lower())
        ]
        
        self.item_dropdown['values'] = filtered_items
        if filtered_items and not self.item_var.get() in filtered_items:
            self.item_var.set(filtered_items[0])

    def update_revenue_display(self):
        """Update the revenue and prevented theft displays."""
        self.revenue_label.configure(text=f"Total Revenue: ${self.total_revenue:.2f}")
        self.prevented_theft_label.configure(text=f"Prevented Theft: ${self.total_prevented_theft:.2f}")

    def update_button_states(self):
        """Update the state of all buttons based on current conditions."""
        state = tk.NORMAL if self.current_person.items else tk.DISABLED
        self.cashier_button.configure(state=state)
        self.gate_button.configure(state=state)
        self.clear_button.configure(state=state)
        self.skip_cashier_button.configure(state=state)

    def update_basket_display(self):
        """Update the basket display with current items."""
        self.basket_display.config(state=tk.NORMAL)
        self.basket_display.delete(1.0, tk.END)
        if self.current_person.items:
            total = 0.0
            for item in self.current_person.items:
                status = "✅ Deactivated" if item.is_deactivated else "🔴 Active"
                self.basket_display.insert(tk.END, 
                    f"• {item.name} (${item.price:.2f}) - {status}\n")
                total += item.price
            self.basket_display.insert(tk.END, f"\nTotal: ${total:.2f}")
        else:
            self.basket_display.insert(tk.END, "Basket is empty")
        self.basket_display.config(state=tk.DISABLED)

    def update_status(self, message, is_alert=False):
        """Update the status message."""
        color = '#ff0000' if is_alert else '#008000'
        self.status_label.configure(text=message, foreground=color)

    def new_person(self):
        """Create a new person."""
        self.person_counter += 1
        self.current_person = Person(f"Person {self.person_counter}")
        if hasattr(self, 'person_label'):
            self.person_label.configure(text=f"Current Customer: {self.current_person.name}")
            self.clear_basket()
            self.update_status(f"New customer: {self.current_person.name}")

    def add_item(self):
        """Add an item to the current person's basket."""
        selected_item_name = self.item_var.get()
        if selected_item_name:
            for item in self.available_items:
                if item.name == selected_item_name:
                    new_item = Item(item.name, item.tag_id, 
                                  price=item.price, category=item.category)
                    self.current_person.add_item(new_item)
                    self.log_text.insert("end", 
                        f"➕ Added {new_item.name} (${new_item.price:.2f}) to basket\n")
                    self.log_text.see("end")
                    self.update_basket_display()
                    self.update_button_states()
                    self.update_status(f"Added {new_item.name} to basket")
                    break

    def clear_basket(self):
        """Clear all items from the current basket."""
        self.current_person.items = []
        self.log_text.insert("end", "🗑️ Basket cleared\n")
        self.log_text.see("end")
        self.update_basket_display()
        self.update_button_states()
        self.update_status("Basket has been cleared")

    def go_to_cashier(self):
        """Process items through the cashier."""
        if not self.current_person.items:
            messagebox.showwarning("Empty Basket", "No items in the basket!")
            return
        
        try:
            result = self.cashier.scan_and_deactivate(self.current_person, 
                lambda msg: self.update_log_with_delay(msg))
            self.total_revenue += self.current_person.calculate_total()
            self.update_revenue_display()
            self.update_basket_display()
            self.update_status("All items have been scanned and deactivated")
        except Exception as e:
            messagebox.showerror("Cashier Error", f"Error during checkout: {str(e)}")

    def skip_cashier(self):
        """Skip the cashier (simulating potential theft)."""
        if not self.current_person.items:
            messagebox.showwarning("Empty Basket", "No items in the basket!")
            return
        
        self.log_text.insert("end", f"\n⚠️ {self.current_person.name} is skipping the cashier!\n")
        self.log_text.see("end")
        self.update_status("⚠️ Skipping cashier!", True)
        self.pass_through_gate()

    def pass_through_gate(self):
        """Process the current person through the security gate."""
        if not self.current_person.items:
            messagebox.showwarning("Empty Basket", "No items to scan!")
            return
        
        try:
            result, alert_triggered = self.gate.scan(self.current_person)
            self.log_text.insert("end", result)
            self.log_text.see("end")
            
            if alert_triggered:
                self.alert_counter += 1
                self.alert_history.append(self.current_person.name)
                self.alert_label.configure(text=f"Total Alerts: {self.alert_counter}")
                self.total_prevented_theft += self.current_person.calculate_total()
                self.update_revenue_display()
                self.update_status("🚨 ALERT: Active tag detected!", True)
            else:
                self.safe_scan_counter += 1
                self.update_status("✅ All items are safe. No alert.")
            
            self.logger.log_gate_scan(self.current_person, alert_triggered)
            
        except Exception as e:
            messagebox.showerror("Gate Error", f"Error during gate scan: {str(e)}")

    def update_log_with_delay(self, message):
        """Update the log with a delay for visual effect."""
        self.log_text.insert("end", message)
        self.log_text.see("end")
        self.root.update_idletasks()
        time.sleep(0.5)

    def simulate_random_customers(self):
        """Simulate multiple customers with random behaviors."""
        try:
            for _ in range(10):
                self.new_person()
                # Add 1-5 random items
                num_items = random.randint(1, 5)
                for _ in range(num_items):
                    item = random.choice(self.available_items)
                    new_item = Item(item.name, item.tag_id, 
                                  price=item.price, category=item.category)
                    self.current_person.add_item(new_item)
                    self.update_basket_display()
                    self.update_button_states()
                    self.root.update_idletasks()
                    time.sleep(0.2)
                
                # 30% chance to skip cashier
                if random.random() < 0.3:
                    self.skip_cashier()
                else:
                    self.go_to_cashier()
                
                self.pass_through_gate()
                time.sleep(0.5)
        except Exception as e:
            messagebox.showerror("Simulation Error", f"Error during simulation: {str(e)}")