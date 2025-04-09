# Author

Elchin Huseynov

# Anti-Theft-Signal-System

A comprehensive supermarket anti-theft simulation system built with Python and Tkinter.

## Features

- 🛍️ **Item Management**
  - RFID tag simulation
  - Real-time tag status tracking
  - Item-by-item scanning

- 👥 **Customer Flow**
  - Multi-person simulation
  - Automatic customer generation
  - Theft simulation options

- 💳 **Checkout Process**
  - Smart cashier simulation
  - Item-by-item deactivation
  - Real-time scanning feedback

- 🚨 **Security Features**
  - Exit gate scanning
  - Active tag detection
  - Alert system

- 📊 **Analytics**
  - Real-time statistics
  - Safe vs. Alert scan visualization
  - CSV logging
  - Summary report generation

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```bash
python main.py
```

Run tests:
```bash
python tests/run_tests.py
```

## Testing

The project includes comprehensive unit tests covering:
- Item management
- Customer interactions
- Cashier operations
- Gate scanning
- Logging system

## Project Structure

```
├── main.py              # Application entry point
├── models.py            # Core business logic classes
├── gui.py              # GUI implementation
├── logger.py           # Logging and reporting
├── requirements.txt    # Project dependencies
└── tests/              # Test suite
    ├── __init__.py
    ├── test_models.py
    ├── test_logger.py
    └── run_tests.py
```