import unittest
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import all test modules
from tests.test_models import TestItem, TestPerson, TestCashier, TestGate
from tests.test_logger import TestSystemLogger

def run_tests():
    # Create a test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestItem))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestPerson))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCashier))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestGate))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestSystemLogger))
    
    # Run the test suite
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)