# main.py

import sys
from PyQt6.QtWidgets import QApplication
from main_window import MainWindow

if __name__ == '__main__':
    # An application instance is required for any PyQt GUI.
    app = QApplication(sys.argv)

    # Create an instance of our main window.
    window = MainWindow()
    
    # Show the window.
    window.show()

    # Start the application's event loop.
    sys.exit(app.exec())