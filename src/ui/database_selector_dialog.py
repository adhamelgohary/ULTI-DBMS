# src/ui/database_selector_dialog.py

from PyQt6.QtWidgets import (
    QDialog, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QListWidget, QDialogButtonBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

class DatabaseSelectorDialog(QDialog):
    """A dialog to list, search, and select a database from a connection."""
    def __init__(self, databases, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Database")
        self.setMinimumSize(400, 500)
        self.selected_database = None

        # --- Widgets ---
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search for a database...")
        
        self.db_list = QListWidget()
        self.db_list.addItems(databases)

        # --- Buttons ---
        self.button_box = QDialogButtonBox()
        self.cancel_btn = self.button_box.addButton(QDialogButtonBox.StandardButton.Cancel)
        # Custom buttons need to be added separately
        self.new_db_btn = QPushButton(QIcon("src/resources/icons/plus.svg"), " New")
        self.select_btn = QPushButton("Select")
        self.select_btn.setEnabled(False) # Disabled until a selection is made
        self.select_btn.setDefault(True) # Activated on Enter key press
        
        self.button_box.addButton(self.new_db_btn, QDialogButtonBox.ButtonRole.ActionRole)
        self.button_box.addButton(self.select_btn, QDialogButtonBox.ButtonRole.AcceptRole)

        # --- Layout ---
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.search_bar)
        main_layout.addWidget(self.db_list)
        main_layout.addWidget(self.button_box)

        # --- Connect Signals ---
        self.select_btn.clicked.connect(self._on_accept)
        self.cancel_btn.clicked.connect(self.reject)
        self.db_list.itemSelectionChanged.connect(self._on_selection_changed)
        self.db_list.itemDoubleClicked.connect(self._on_accept)
        # TODO: Connect search_bar and new_db_btn signals

    def _on_selection_changed(self):
        """Enable the select button only if an item is selected."""
        self.select_btn.setEnabled(len(self.db_list.selectedItems()) > 0)

    def _on_accept(self):
        """Store the selected database name and accept the dialog."""
        if self.db_list.selectedItems():
            self.selected_database = self.db_list.selectedItems()[0].text()
            self.accept()

    def get_selected_database(self):
        """Public method to retrieve the result."""
        return self.selected_database