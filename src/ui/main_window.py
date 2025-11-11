# src/ui/main_window.py

import sys
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QSplitter,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QToolBar,
    QMessageBox,
    QSizePolicy,
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon

from src.ui.object_explorer import ObjectExplorer
from src.ui.content_viewer import ContentViewer
from src.ui.database_selector_dialog import DatabaseSelectorDialog


class MainWindow(QMainWindow):
    def __init__(self, adapter, conn_details, parent=None):
        super().__init__(parent)

        # --- THE DEFINITIVE FIX FOR MACOS UNIFIED TITLE BAR ---
        # 1. We keep the unified toolbar flag.
        if sys.platform == "darwin":
            self.setUnifiedTitleAndToolBarOnMac(True)

        # 2. We explicitly set the title to an empty string to remove the text.
        self.setWindowTitle(" ")  # A space is often more reliable than fully empty ""

        self.setGeometry(100, 100, 1200, 800)

        self.active_adapter = adapter
        self.connection_details = conn_details

        self.db_icon = QIcon("src/resources/icons/database.svg")

        # --- Create UI Components ---
        self.sidebar = ObjectExplorer()
        self.content_area = ContentViewer()
        self.top_bar = self._create_top_bar()
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.top_bar)

        # --- Assemble Layout ---
        self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.main_splitter.addWidget(self.sidebar)
        self.main_splitter.addWidget(self.content_area)
        self.main_splitter.setSizes([250, 950])
        self.sidebar.setMinimumWidth(200)
        self.setCentralWidget(self.main_splitter)

        # --- Apply Styling and Object Names ---
        self._apply_styles()
        self.sidebar.setObjectName("ObjectExplorer")
        self.sidebar.tables_btn.setProperty("pos", "left")
        self.sidebar.queries_btn.setProperty("pos", "mid")
        self.sidebar.history_btn.setProperty("pos", "right")
        self.sidebar.tables_btn.setObjectName("SegmentedButton")
        self.sidebar.queries_btn.setObjectName("SegmentedButton")
        self.sidebar.history_btn.setObjectName("SegmentedButton")
        self.sidebar.tables_btn.setCheckable(True)
        self.sidebar.queries_btn.setCheckable(True)
        self.sidebar.history_btn.setCheckable(True)
        self.sidebar.tables_btn.setChecked(True)

        # --- Connect Signals ---
        self.db_selector_btn.clicked.connect(self._on_show_database_selector)
        self.sidebar.table_selected.connect(self._on_table_selected)
        self.sidebar.queries_btn.clicked.connect(self.content_area.show_query_editor)
        self.sidebar.tables_btn.clicked.connect(self.content_area.show_data_grid)
        self.sidebar.history_btn.clicked.connect(self.content_area.show_history)

        # --- Initial Population ---
        self._load_initial_state()

    def _load_initial_state(self):
        """Initial state when MainWindow opens."""
        if not self.active_adapter:
            return
        conn_name = f"{self.connection_details.get('user')}@{self.connection_details.get('host')}"
        db_name = self.connection_details.get("database")
        self.sidebar.populate_tables(self.active_adapter, db_name)
        self.connection_label.setText(f"{conn_name} : {db_name}")

    def _on_show_database_selector(self):
        """Launches the dialog to select a new database."""
        if not self.active_adapter:
            return
        databases = self.active_adapter.list_databases()
        dialog = DatabaseSelectorDialog(databases, self)
        if dialog.exec():
            selected_db = dialog.get_selected_database()
            if selected_db:
                self.connection_details["database"] = selected_db
                self.sidebar.populate_tables(self.active_adapter, selected_db)
                conn_name = f"{self.connection_details.get('user')}@{self.connection_details.get('host')}"
                self.connection_label.setText(f"{conn_name} : {selected_db}")

    def _on_table_selected(self, table_name):
        """Handles viewing a table's content."""
        if not self.active_adapter:
            return
        headers, data = self.active_adapter.get_table_content(table_name)
        if headers is not None and data is not None:
            self.content_area.show_data_grid()
            self.content_area.data_grid_page.populate_data(headers, data)
            conn_name = f"{self.connection_details.get('user')}@{self.connection_details.get('host')}"
            current_db = self.connection_details.get("database")
            self.connection_label.setText(f"{conn_name} : {current_db} : {table_name}")
        else:
            QMessageBox.warning(
                self, "Error", f"Could not retrieve data for '{table_name}'."
            )

    def _create_top_bar(self):
        """Builds the main top toolbar using the direct-addition/spacer method."""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(16, 16))
        toolbar.setMovable(False)
        toolbar.setStyleSheet("QToolBar { border: none; }")

        self.db_selector_btn = QPushButton(
            QIcon("src/resources/icons/database.svg"), ""
        )
        toolbar.addWidget(self.db_selector_btn)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        toolbar.addWidget(spacer)

        self.connection_label = QLabel("Not Connected")
        self.connection_label.setObjectName("ConnectionLabel")
        self.connection_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        toolbar.addWidget(self.connection_label)

        spacer2 = QWidget()
        spacer2.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        toolbar.addWidget(spacer2)

        self.refresh_btn = QPushButton(QIcon("src/resources/icons/refresh-cw.svg"), "")
        toolbar.addWidget(self.refresh_btn)

        return toolbar

    def _apply_styles(self):
        """Loads and applies the main stylesheet."""
        try:
            with open("src/resources/styles/macos_light.qss", "r") as f:
                style = f.read()
                self.setStyleSheet(style)
        except FileNotFoundError:
            print("Stylesheet not found.")
