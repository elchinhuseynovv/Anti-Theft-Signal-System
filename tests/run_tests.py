import unittest
from models import Item, Person, Cashier, Gate

class TestItem(unittest.TestCase):
    def setUp(self):
        self.item = Item("Test Item", "TEST001")
    
    def test_item_creation(self):
        self.assertEqual(self.item.name, "Test Item")
        self.assertEqual(self.item.tag_id, "TEST001")
        self.assertFalse(self.item.is_deactivated)
    
    def test_item_string_representation(self):
        expected = "Test Item (Tag: TEST001, Active)"
        self.assertEqual(str(self.item), expected)
        
        self.item.is_deactivated = True
        expected = "Test Item (Tag: TEST001, Deactivated)"
        self.assertEqual(str(self.item), expected)


class TestPerson(unittest.TestCase):
    def setUp(self):
        self.person = Person("Test Person")
        self.item = Item("Test Item", "TEST001")
    
    def test_person_creation(self):
        self.assertEqual(self.person.name, "Test Person")
        self.assertEqual(len(self.person.items), 0)
    
    def test_add_item(self):
        self.person.add_item(self.item)
        self.assertEqual(len(self.person.items), 1)
        self.assertEqual(self.person.items[0], self.item)
    
    def test_person_string_representation(self):
        expected = "Test Person is carrying 0 item(s)."
        self.assertEqual(str(self.person), expected)
        
        self.person.add_item(self.item)
        expected = "Test Person is carrying 1 item(s)."
        self.assertEqual(str(self.person), expected)


class TestCashier(unittest.TestCase):
    def setUp(self):
        self.cashier = Cashier("Test Cashier")
        self.person = Person("Test Person")
        self.item = Item("Test Item", "TEST001")
        self.person.add_item(self.item)
    
    def test_scan_and_deactivate(self):
        result = self.cashier.scan_and_deactivate(self.person)
        self.assertIn("Test Cashier is scanning Test Person's items", result)
        self.assertIn("Scanning Test Item", result)
        self.assertTrue(self.item.is_deactivated)


class TestGate(unittest.TestCase):
    def setUp(self):
        self.gate = Gate()
        self.person = Person("Test Person")
        self.item = Item("Test Item", "TEST001")
        self.person.add_item(self.item)
    
    def test_gate_scan_with_active_tag(self):
        result, alert = self.gate.scan(self.person)
        self.assertIn("Scanning Test Person at the exit gate", result)
        self.assertIn("ALERT: Active tag detected!", result)
        self.assertTrue(alert)
    
    def test_gate_scan_with_deactivated_tag(self):
        self.item.is_deactivated = True
        result, alert = self.gate.scan(self.person)
        self.assertIn("All items are safe", result)
        self.assertFalse(alert)