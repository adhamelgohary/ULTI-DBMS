# main_window.py

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,  # QPushButton is new
    QSplitter,
    QListWidget,
    QTextEdit,
    QTableWidget,
    QDialog,
)
from PyQt6.QtCore import Qt
from database_manager import DatabaseManager  # NEW: Import our manager
from connection_dialog import ConnectionDialog


class MainWindow(QMainWindow):
    """Our main application window."""

    def __init__(self):
        """Initializer."""
        super().__init__()

        self.setWindowTitle("SQL Client MVP")
        self.setGeometry(100, 100, 1200, 800)

        # NEW: Instantiate our database manager
        self.db_manager = DatabaseManager()

        # --- Create Widgets ---
        self.sidebar = QListWidget()

        # NEW: Add a connect button to the top of the sidebar
        self.connect_button = QPushButton("Connect to DB")
        self.connect_button.clicked.connect(self.on_connect_clicked)
        
        self.query_editor = QTextEdit()
        self.query_editor.setPlaceholderText("SELECT * FROM your_table;")

        self.results_table = QTableWidget()
        self.results_table.setColumnCount(3)
        self.results_table.setHorizontalHeaderLabels(["ID", "Name", "Value"])

        # --- Create Layouts ---

        # NEW: Create a layout for the sidebar to hold the button and the list
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(0, 0, 0, 0)  # Use all available space
        sidebar_layout.addWidget(self.connect_button)
        sidebar_layout.addWidget(self.sidebar)

        # NEW: Put the sidebar layout into a generic QWidget to add to the splitter
        sidebar_container = QWidget()
        sidebar_container.setLayout(sidebar_layout)

        content_splitter = QSplitter(Qt.Orientation.Horizontal)
        content_splitter.addWidget(sidebar_container)  # NEW: Add the container
        content_splitter.addWidget(self.query_editor)
        content_splitter.setSizes([200, 800])

        main_splitter = QSplitter(Qt.Orientation.Vertical)
        main_splitter.addWidget(content_splitter)
        main_splitter.addWidget(self.results_table)
        main_splitter.setSizes([600, 200])

        self.setCentralWidget(main_splitter)

    def on_connect_clicked(self):
        """Handles the connect button click event by opening the connection dialog."""
        dialog = ConnectionDialog(self)  # Pass 'self' to make it a child of MainWindow

        # .exec() shows the dialog and blocks until the user closes it.
        # It returns QDialog.DialogCode.Accepted if the user clicked OK.
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # If the user clicked OK, get the details from our custom method
            db_config = dialog.get_connection_details()

            if self.db_manager.connect(db_config):
                tables = self.db_manager.list_tables()
                self._update_sidebar_tables(tables)
            else:
                # We could show an error message dialog here
                print("Connection failed. Check console for details.")
                self.sidebar.clear()
        else:
            print("Connection cancelled by user.")

    # NEW: Helper method to update the UI
    def _update_sidebar_tables(self, tables):
        """Populates the sidebar list widget with table names."""
        self.sidebar.clear()
        for table_name in tables:
            self.sidebar.addItem(table_name)
