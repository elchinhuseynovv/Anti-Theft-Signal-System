class Item:
    def __init__(self, name, tag_id, is_deactivated=False):
        self.name = name
        self.tag_id = tag_id
        self.is_deactivated = is_deactivated

    def __str__(self):
        status = "Deactivated" if self.is_deactivated else "Active"
        return f"{self.name} (Tag: {self.tag_id}, {status})"

class Person:
    def __init__(self, name):
        self.name = name
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def __str__(self):
        return f"{self.name} is carrying {len(self.items)} item(s)."

class Gate:
    def __init__(self):
        pass

    def scan(self, person):
        print(f"\nScanning {person.name} at the gate...")
        alert_triggered = False
        for item in person.items:
            print(f" - Checking item: {item}")
            if not item.is_deactivated:
                print("   🔴 ALERT: Active tag detected! Possible theft!")
                alert_triggered = True
        if not alert_triggered:
            print("✅ All items are safe. No alert.")

# --- Simulation ---

# Create items
apple = Item("Apple", "RFID123", is_deactivated=True)  # Legit
cheese = Item("Cheese", "RFID456")                    # Stolen (tag not deactivated)

# Create a person and add items
john = Person("John")
john.add_item(apple)
john.add_item(cheese)

# Create a gate and scan
exit_gate = Gate()
exit_gate.scan(john)
