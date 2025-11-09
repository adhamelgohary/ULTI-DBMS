# main.py

import sys
from PyQt6.QtWidgets import QApplication, QDialog

# MODIFIED: Import QDialog to access its result codes
from src.ui.welcome_window import WelcomeWindow
from src.ui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    welcome_win = WelcomeWindow()
    result = welcome_win.exec()

    # CORRECTED: Use the full, correct PyQt6 enum 'QDialog.DialogCode.Accepted'
    if result == QDialog.DialogCode.Accepted:
        # Launch the MainWindow, passing the fully configured adapter and details
        # The welcome_win object still exists and holds the data we need
        main_win = MainWindow(
            adapter=welcome_win.successful_adapter,
            conn_details=welcome_win.connection_details,
        )
        main_win.show()
        sys.exit(app.exec())
    else:
        # If user cancelled the WelcomeWindow, exit the application
        sys.exit(0)
