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


class Cashier:
    def __init__(self, name):
        self.name = name

    def scan_and_deactivate(self, person):
        print(f"\n🧾 {self.name} is scanning {person.name}'s items at the checkout...")
        for item in person.items:
            print(f" - Scanning {item.name}... ✅ Tag deactivated.")
            item.is_deactivated = True


class Gate:
    def __init__(self):
        pass

    def scan(self, person):
        print(f"\n🚪 Scanning {person.name} at the exit gate...")
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
milk = Item("Milk", "RFID001")
bread = Item("Bread", "RFID002")

# Create a person
alice = Person("Alice")
alice.add_item(milk)
alice.add_item(bread)

# Create a cashier and deactivate tags
cashier = Cashier("Sarah")
cashier.scan_and_deactivate(alice)

# Create a gate and scan the person
exit_gate = Gate()
exit_gate.scan(alice)
