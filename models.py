from datetime import datetime
import time

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

    def __str__(self):
        status = "Deactivated" if self.is_deactivated else "Active"
        return f"{self.name} (Tag: {self.tag_id}, {status})"

    def deactivate(self):
        """Deactivate the item's RFID tag."""
        self.is_deactivated = True
        return f"Tag {self.tag_id} deactivated"

    def get_details(self):
        """Return detailed item information."""
        return {
            "name": self.name,
            "tag_id": self.tag_id,
            "status": "Deactivated" if self.is_deactivated else "Active",
            "price": self.price,
            "category": self.category,
            "timestamp": self.timestamp
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

    def add_item(self, item):
        """Add an item to the person's possession."""
        self.items.append(item)
        return f"Added {item.name} to {self.name}'s basket"

    def remove_item(self, item):
        """Remove an item from the person's possession."""
        if item in self.items:
            self.items.remove(item)
            return f"Removed {item.name} from {self.name}'s basket"
        return f"{item.name} not found in {self.name}'s basket"

    def get_total_items(self):
        """Get the total number of items."""
        return len(self.items)

    def calculate_total(self):
        """Calculate total price of all items."""
        self.total_spent = sum(item.price for item in self.items)
        return self.total_spent

    def __str__(self):
        return f"{self.name} is carrying {len(self.items)} item(s)."


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

    def scan_and_deactivate(self, person, callback=None):
        """
        Scan and deactivate items one by one.
        
        Args:
            person (Person): The customer being served
            callback (function): Optional callback for GUI updates
        """
        result = f"\n🧾 {self.name} is scanning {person.name}'s items at the checkout...\n"
        
        for item in person.items:
            scan_msg = f" - Scanning {item.name}... ✅ Tag deactivated.\n"
            result += scan_msg
            item.deactivate()
            self.items_processed += 1
            self.total_sales += item.price
            
            if callback:
                callback(scan_msg)
                time.sleep(0.5)
        
        return result

    def get_stats(self):
        """Get cashier's performance statistics."""
        return {
            "name": self.name,
            "items_processed": self.items_processed,
            "total_sales": self.total_sales
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

    def scan(self, person):
        """
        Scan a person for active RFID tags.
        
        Args:
            person (Person): The person to scan
            
        Returns:
            tuple: (scan result message, alert triggered flag)
        """
        self.total_scans += 1
        result = f"\n🚪 Scanning {person.name} at the exit gate...\n"
        alert_triggered = False
        
        for item in person.items:
            result += f" - Checking item: {item}\n"
            if not item.is_deactivated:
                result += "   🔴 ALERT: Active tag detected! Possible theft!\n"
                alert_triggered = True
        
        if alert_triggered:
            self.alerts_triggered += 1
        else:
            result += "✅ All items are safe. No alert.\n"
        
        return result, alert_triggered

    def get_stats(self):
        """Get gate statistics."""
        return {
            "total_scans": self.total_scans,
            "alerts_triggered": self.alerts_triggered,
            "alert_rate": (self.alerts_triggered / self.total_scans * 100) if self.total_scans > 0 else 0
        }