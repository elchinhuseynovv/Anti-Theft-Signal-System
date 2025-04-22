import time
from datetime import datetime

class Item:
    """
    Represents an item with an RFID tag in the store.
    
    Attributes:
        name (str): The name of the item
        tag_id (str): Unique RFID tag identifier
        is_deactivated (bool): Tag deactivation status
        price (float): Item price
        category (str): Item category
        timestamp (datetime): When the item was created
    """
    
    def __init__(self, name, tag_id, price=0.0, category="General", is_deactivated=False):
        self.name = name
        self.tag_id = tag_id
        self.is_deactivated = is_deactivated
        self.price = price
        self.category = category
        self.timestamp = datetime.now()
        self.scan_history = []
        self.location = "shelf"

    def __str__(self):
        status = "Deactivated" if self.is_deactivated else "Active"
        return f"{self.name} (Tag: {self.tag_id}, {status}, ${self.price:.2f})"

    def deactivate(self):
        """Deactivate the item's RFID tag."""
        self.is_deactivated = True
        self.log_scan("deactivation")
        return f"Tag {self.tag_id} deactivated"

    def log_scan(self, scan_type):
        """Log when the item is scanned."""
        self.scan_history.append({
            'timestamp': datetime.now(),
            'type': scan_type,
            'location': self.location
        })

    def update_location(self, new_location):
        """Update item's location in the store."""
        self.location = new_location
        self.log_scan("location_update")

    def get_scan_history(self):
        """Get the complete scan history of the item."""
        return self.scan_history

    def get_details(self):
        """Return detailed item information."""
        return {
            "name": self.name,
            "tag_id": self.tag_id,
            "status": "Deactivated" if self.is_deactivated else "Active",
            "price": self.price,
            "category": self.category,
            "timestamp": self.timestamp,
            "location": self.location,
            "scan_count": len(self.scan_history)
        }


class Person:
    """
    Represents a customer in the store.
    
    Attributes:
        name (str): Customer name
        items (list): Items in possession
        entry_time (datetime): When the customer entered
        total_spent (float): Total amount spent
    """
    
    def __init__(self, name):
        self.name = name
        self.items = []
        self.entry_time = datetime.now()
        self.total_spent = 0.0
        self.visit_history = []
        self.shopping_path = []

    def add_item(self, item):
        """Add an item to the person's possession."""
        self.items.append(item)
        item.update_location(f"with_{self.name}")
        self.shopping_path.append({
            'action': 'pick_up',
            'item': item.name,
            'timestamp': datetime.now()
        })
        self.calculate_total()
        return f"Added {item.name} to {self.name}'s basket"

    def remove_item(self, item):
        """Remove an item from the person's possession."""
        if item in self.items:
            self.items.remove(item)
            item.update_location('shelf')
            self.shopping_path.append({
                'action': 'return',
                'item': item.name,
                'timestamp': datetime.now()
            })
            self.calculate_total()
            return f"Removed {item.name} from {self.name}'s basket"
        return f"{item.name} not found in {self.name}'s basket"

    def get_total_items(self):
        """Get the total number of items."""
        return len(self.items)

    def calculate_total(self):
        """Calculate total price of all items."""
        self.total_spent = sum(item.price for item in self.items)
        return self.total_spent

    def log_visit(self, action, location):
        """Log customer's movement in the store."""
        self.visit_history.append({
            'timestamp': datetime.now(),
            'action': action,
            'location': location
        })

    def get_shopping_summary(self):
        """Get a summary of the shopping session."""
        return {
            'customer': self.name,
            'entry_time': self.entry_time,
            'duration': (datetime.now() - self.entry_time).total_seconds(),
            'items_picked': len(self.shopping_path),
            'final_items': len(self.items),
            'total_spent': self.total_spent,
            'shopping_path': self.shopping_path
        }

    def __str__(self):
        return f"{self.name} is carrying {len(self.items)} item(s) worth ${self.total_spent:.2f}"


class Cashier:
    """
    Represents a cashier who can scan and deactivate items.
    
    Attributes:
        name (str): Cashier name
        items_processed (int): Count of items processed
        total_sales (float): Total sales amount
    """
    
    def __init__(self, name):
        self.name = name
        self.items_processed = 0
        self.total_sales = 0.0
        self.transaction_history = []
        self.shift_start = datetime.now()
        self.performance_metrics = {
            'avg_scan_time': 0,
            'successful_deactivations': 0,
            'failed_deactivations': 0
        }

    def scan_and_deactivate(self, person, callback=None):
        """
        Scan and deactivate items one by one.
        
        Args:
            person (Person): The customer being served
            callback (function): Optional callback for GUI updates
        """
        transaction_start = datetime.now()
        result = f"\n🧾 {self.name} is scanning {person.name}'s items at the checkout...\n"
        
        for item in person.items:
            scan_start = time.time()
            scan_msg = f" - Scanning {item.name} (${item.price:.2f})... ✅ Tag deactivated.\n"
            result += scan_msg
            item.deactivate()
            scan_time = time.time() - scan_start
            
            self.items_processed += 1
            self.total_sales += item.price
            self.performance_metrics['avg_scan_time'] = (
                (self.performance_metrics['avg_scan_time'] * (self.items_processed - 1) + scan_time)
                / self.items_processed
            )
            self.performance_metrics['successful_deactivations'] += 1
            
            if callback:
                callback(scan_msg)
                time.sleep(0.5)
        
        # Log transaction
        self.transaction_history.append({
            'timestamp': transaction_start,
            'customer': person.name,
            'items': len(person.items),
            'total': person.total_spent,
            'duration': (datetime.now() - transaction_start).total_seconds()
        })
        
        result += f"\nTotal: ${person.total_spent:.2f}\n"
        return result

    def get_shift_summary(self):
        """Get a summary of the cashier's current shift."""
        return {
            'cashier': self.name,
            'shift_start': self.shift_start,
            'duration': (datetime.now() - self.shift_start).total_seconds(),
            'items_processed': self.items_processed,
            'total_sales': self.total_sales,
            'avg_scan_time': self.performance_metrics['avg_scan_time'],
            'successful_deactivations': self.performance_metrics['successful_deactivations'],
            'transaction_count': len(self.transaction_history)
        }

    def get_transaction_history(self):
        """Get the complete transaction history."""
        return self.transaction_history

    def get_stats(self):
        """Get cashier's performance statistics."""
        return {
            "name": self.name,
            "items_processed": self.items_processed,
            "total_sales": self.total_sales,
            "performance_metrics": self.performance_metrics
        }


class Gate:
    """
    Represents a security gate that can detect active RFID tags.
    
    Attributes:
        total_scans (int): Total number of scans performed
        alerts_triggered (int): Number of alerts triggered
    """
    
    def __init__(self):
        self.total_scans = 0
        self.alerts_triggered = 0
        self.scan_history = []
        self.peak_times = {}
        self.alert_patterns = {}

    def scan(self, person):
        """
        Scan a person for active RFID tags.
        
        Args:
            person (Person): The person to scan
            
        Returns:
            tuple: (scan result message, alert triggered flag)
        """
        scan_start = datetime.now()
        self.total_scans += 1
        result = f"\n🚪 Scanning {person.name} at the exit gate...\n"
        alert_triggered = False
        active_tags = []
        
        for item in person.items:
            result += f" - Checking item: {item}\n"
            if not item.is_deactivated:
                result += f"   🔴 ALERT: Active tag detected on {item.name} (${item.price:.2f})!\n"
                alert_triggered = True
                active_tags.append(item.tag_id)
        
        if alert_triggered:
            self.alerts_triggered += 1
            result += f"\n⚠️ Total value of items with active tags: ${person.total_spent:.2f}\n"
        else:
            result += "✅ All items are safe. No alert.\n"
        
        # Log scan details
        hour = scan_start.hour
        self.peak_times[hour] = self.peak_times.get(hour, 0) + 1
        
        scan_record = {
            'timestamp': scan_start,
            'person': person.name,
            'items': len(person.items),
            'alert_triggered': alert_triggered,
            'active_tags': active_tags,
            'duration': (datetime.now() - scan_start).total_seconds()
        }
        self.scan_history.append(scan_record)
        