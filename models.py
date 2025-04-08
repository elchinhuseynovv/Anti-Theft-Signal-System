from datetime import datetime

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

    def scan_and_deactivate(self, person, callback=None):
        result = f"\n🧾 {self.name} is scanning {person.name}'s items at the checkout...\n"
        for item in person.items:
            scan_msg = f" - Scanning {item.name}... ✅ Tag deactivated.\n"
            result += scan_msg
            item.is_deactivated = True
            if callback:
                callback(scan_msg)
                time.sleep(0.5)
        return result


class Gate:
    def __init__(self):
        pass

    def scan(self, person):
        result = f"\n🚪 Scanning {person.name} at the exit gate...\n"
        alert_triggered = False
        for item in person.items:
            result += f" - Checking item: {item}\n"
            if not item.is_deactivated:
                result += "   🔴 ALERT: Active tag detected! Possible theft!\n"
                alert_triggered = True
        if not alert_triggered:
            result += "✅ All items are safe. No alert.\n"
        return result, alert_triggered