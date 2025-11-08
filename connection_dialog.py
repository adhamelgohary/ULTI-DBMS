# connection_dialog.py

from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QVBoxLayout,
    QLabel,
)


class ConnectionDialog(QDialog):
    """A dialog for getting database connection details from the user."""

    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle("Connect to Database")

        # Create the input fields
        self.host_input = QLineEdit("127.0.0.1")
        self.port_input = QLineEdit("3306")
        self.user_input = QLineEdit("root")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)  # Hide password
        self.database_input = QLineEdit()  # Optional database name

        # Create the layout and add widgets
        form_layout = QFormLayout()
        form_layout.addRow("Host:", self.host_input)
        form_layout.addRow("Port:", self.port_input)
        form_layout.addRow("User:", self.user_input)
        form_layout.addRow("Password:", self.password_input)
        form_layout.addRow("Database (Optional):", self.database_input)

        # Create the standard OK/Cancel buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(
            self.accept
        )  # The 'accept' slot closes the dialog with a 'Accepted' result
        button_box.rejected.connect(
            self.reject
        )  # The 'reject' slot closes the dialog with a 'Rejected' result

        # Set the main layout for the dialog
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(button_box)
        self.setLayout(main_layout)

    def get_connection_details(self):
        """
        A public method for the MainWindow to call to get the entered details.

        Returns:
            dict: A dictionary of the connection details, or None.
        """
        details = {
            "host": self.host_input.text(),
            "port": int(self.port_input.text()),  # Port should be an integer
            "user": self.user_input.text(),
            "password": self.password_input.text(),
            "database": self.database_input.text() or None,  # Use None if empty
        }
        # Filter out the database key if it's None or empty
        if not details["database"]:
            del details["database"]

        return details
