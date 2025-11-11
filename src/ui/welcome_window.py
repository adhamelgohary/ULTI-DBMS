# src/ui/welcome_window.py

from PyQt6.QtWidgets import (
    QDialog,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QListWidget,
    QMessageBox,
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

# Import the necessary components
from src.ui.connection_dialog import ConnectionDialog
from src.database.adapters.mysql_adapter import MySQLAdapter

# The Adapter Factory
DB_ADAPTERS = {
    "MySQL": MySQLAdapter,
}


class WelcomeWindow(QDialog):
    """The initial window for creating or selecting a connection."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Connect to Database")
        self.setMinimumSize(800, 500)

        # This will hold the successfully created adapter to pass to MainWindow
        self.successful_adapter = None
        self.connection_details = None
        self.selected_database = None

        # --- Create Main Layout ---
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- Create Widgets for each Column ---
        left_column = self._create_left_column()
        right_column = self._create_right_column()

        main_layout.addWidget(left_column, 1)
        main_layout.addWidget(right_column, 2)

        self._apply_styles()

        # --- Connect Signals ---
        self.create_conn_btn.clicked.connect(self._on_create_connection)
        self.db_list_widget.itemDoubleClicked.connect(self._on_database_selected)

    def _on_create_connection(self):
        """Opens and manages the connection dialog."""
        dialog = ConnectionDialog(self)
        dialog.test_connection_requested.connect(self._on_test_connection)

        # We reset the state each time we open the dialog
        self.successful_adapter = None
        self.connection_details = None

        if dialog.exec():
            # If the user clicked "Continue", the test must have succeeded.
            # self.successful_adapter and self.connection_details are now set.
            if self.successful_adapter:
                databases = self.successful_adapter.list_databases()
                self._populate_database_list(databases)
            else:
                # This case shouldn't happen if the logic is correct, but it's good practice
                QMessageBox.critical(self, "Error", "Connection was not established.")

    def _on_test_connection(self, details):
        """Slot that receives the test request from the ConnectionDialog."""
        print(f"[DEBUG] Test requested with details: {details}")
        # The sender() is the dialog that emitted the signal
        dialog = self.sender()

        db_type = details.get("db_type", "").split(" ")[0]
        adapter_class = DB_ADAPTERS.get(db_type)
        if not adapter_class:
            QMessageBox.critical(
                dialog, "Error", f"Database type '{db_type}' not supported."
            )
            return

        try:
            adapter = adapter_class()
            # We need to remove db_type before passing details to the adapter's connect method
            connect_details = details.copy()
            connect_details.pop("db_type", None)

            if adapter.connect(connect_details):
                QMessageBox.information(dialog, "Success", "Connection successful!")
                # On success, enable the continue button and store the state
                dialog.on_test_success()
                self.successful_adapter = adapter
                self.connection_details = (
                    details  # Store the full details, including db_type
                )
            else:
                QMessageBox.critical(
                    dialog, "Failed", "Connection failed. Please check credentials."
                )
                self.successful_adapter = None
                self.connection_details = None
        except Exception as e:
            QMessageBox.critical(dialog, "Error", f"An unexpected error occurred: {e}")
            self.successful_adapter = None
            self.connection_details = None

    def _populate_database_list(self, databases):
        """Shows and populates the list of databases in the right column."""
        self.prompt_label.setVisible(False)
        self.db_list_widget.clear()
        self.db_list_widget.addItems(databases)
        self.db_list_widget.setVisible(True)

    def _on_database_selected(self, item):
        """When a database is chosen, finalize and close the welcome window."""
        print("[DEBUG] Database double-clicked:", item.text())

        # THE FIX: We check that the connection details exist before proceeding.
        if not self.connection_details:
            print("[DEBUG] ERROR: Cannot proceed, connection_details is not set.")
            return

        self.selected_database = item.text()
        # We now safely add the selected database to our stored details
        self.connection_details["database"] = self.selected_database

        print("[DEBUG] Final connection details:", self.connection_details)
        print("[DEBUG] Closing WelcomeWindow with 'Accepted' result.")

        # This signals to main.py that we're ready to launch the MainWindow
        self.accept()

    # --- UI Builder and Styling Methods (unchanged) ---
    def _create_left_column(self):
        container = QWidget()
        container.setObjectName("LeftColumn")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        app_name_label = QLabel("ULTI DMBS")
        app_name_label.setObjectName("AppNameLabel")
        version_label = QLabel("Version: 0.1.0")
        version_label.setObjectName("VersionLabel")
        self.create_conn_btn = QPushButton(
            QIcon("src/resources/icons/plus.svg"), " Create Connection"
        )
        self.restore_db_btn = QPushButton(
            QIcon("src/resources/icons/eye.svg"), " Restore Database"
        )
        self.restore_db_btn.setEnabled(False)
        self.backup_db_btn = QPushButton(
            QIcon("src/resources/icons/eye.svg"), " Backup Database"
        )
        self.backup_db_btn.setEnabled(False)
        layout.addWidget(app_name_label)
        layout.addWidget(version_label)
        layout.addStretch(1)
        layout.addWidget(self.create_conn_btn)
        layout.addWidget(self.restore_db_btn)
        layout.addWidget(self.backup_db_btn)
        layout.addStretch(2)
        return container

    def _create_right_column(self):
        container = QWidget()
        container.setObjectName("RightColumn")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(20, 20, 20, 20)
        self.prompt_label = QLabel("Connect to a server to see its databases.")
        self.prompt_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.db_list_widget = QListWidget()
        self.db_list_widget.setVisible(False)
        layout.addWidget(self.prompt_label)
        layout.addWidget(self.db_list_widget)
        return container

    def _apply_styles(self):
        self.setStyleSheet(
            """#LeftColumn{background-color:#F0F0F0;border-right:1px solid #D0D0D0;}#AppNameLabel{font-size:24px;font-weight:bold;}#VersionLabel{color:#888;}#LeftColumn QPushButton{padding:8px;text-align:left;background-color:transparent;border:none;font-size:14px;}#LeftColumn QPushButton:hover{background-color:#DCDCDC;border-radius:4px;}#RightColumn{background-color:#FFFFFF;}#RightColumn QLabel{font-size:16px;color:#AAA;}QListWidget{border:1px solid #D0D0D0;border-radius:4px;}"""
        )
