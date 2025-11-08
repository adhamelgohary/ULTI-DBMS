# main_window.py

import sys
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QSplitter,
    QApplication,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QTreeWidget,
    QTreeWidgetItem,
    QStackedWidget,
    QTextEdit,
    QTableWidget,
    QLabel,
    QToolBar,
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon


class MainWindow(QMainWindow):
    """
    The main application window with a three-column layout.
    """

    def __init__(self):
        """Initializer."""
        super().__init__()
        self.setWindowTitle("SQL Client")
        self.setGeometry(100, 100, 1200, 800)

        # --- Load Icons ---
        self.db_icon = QIcon("icons/database.svg")
        self.table_icon = QIcon("icons/table.svg")

        # --- Create UI Components for each Column ---
        self.col1_widget = self._create_col1_ui()
        self.col2_widget = self._create_col2_ui()
        self.col3_widget = self._create_col3_ui()  # This is now the real QStackedWidget
        self.top_bar = self._create_top_bar()
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.top_bar)

        # --- Assemble the Layout using Splitters ---
        self.content_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.content_splitter.addWidget(self.col2_widget)
        self.content_splitter.addWidget(self.col3_widget)

        self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.main_splitter.addWidget(self.col1_widget)
        self.main_splitter.addWidget(self.content_splitter)

        # --- Set Initial Sizes and Constraints ---
        self.main_splitter.setSizes([80, 1120])
        self.content_splitter.setSizes([250, 870])
        self.col1_widget.setMinimumWidth(60)
        self.col1_widget.setMaximumWidth(100)
        self.col2_widget.setMinimumWidth(200)

        self.setCentralWidget(self.main_splitter)
        self._apply_styles()

        ## ----------------------------------------------------------------
        ## Connect Signals to Slots (The "Wiring")
        ## ----------------------------------------------------------------
        self.queries_btn.clicked.connect(self._activate_query_view)
        self.tables_btn.clicked.connect(self._activate_table_view)
        self.history_btn.clicked.connect(self._activate_history_view)
        # We can also connect the tree click for a better user experience
        self.object_tree.itemClicked.connect(self._activate_table_view)

    ## ----------------------------------------------------------------
    ## UI Builder Methods
    ## ----------------------------------------------------------------

    def _create_col1_ui(self):
        """Creates the UI for the connection switcher (Column 1)."""
        list_widget = QListWidget()
        list_widget.setViewMode(QListWidget.ViewMode.IconMode)
        list_widget.setIconSize(QSize(48, 48))
        list_widget.setMovement(QListWidget.Movement.Static)
        list_widget.setResizeMode(QListWidget.ResizeMode.Adjust)

        item = QListWidgetItem("MySQL")
        item.setIcon(self.db_icon)
        item.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
        list_widget.addItem(item)

        return list_widget

    def _create_col2_ui(self):
        """Creates the UI for the object explorer (Column 2)."""
        self.tables_btn = QPushButton("Tables")
        self.queries_btn = QPushButton("Queries")
        self.history_btn = QPushButton("History")

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.tables_btn)
        button_layout.addWidget(self.queries_btn)
        button_layout.addWidget(self.history_btn)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search for tables...")

        self.object_tree = QTreeWidget()
        self.object_tree.setHeaderHidden(True)

        table_names = ["comments", "component", "db", "default_roles", "engine_cost"]
        for name in table_names:
            item = QTreeWidgetItem(self.object_tree)
            item.setText(0, name)
            item.setIcon(0, self.table_icon)

        main_layout = QVBoxLayout()
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.search_bar)
        main_layout.addWidget(self.object_tree)

        container = QWidget()
        container.setLayout(main_layout)
        return container

    ## NEW METHOD: Builds the Content Viewer for Column 3
    def _create_col3_ui(self):
        """Creates the UI for the content viewer (Column 3) using a QStackedWidget."""
        # Create the individual "pages" that will live in the stack

        # Page 1: Table View
        self.table_view_page = QTableWidget()
        self.table_view_page.setColumnCount(4)
        self.table_view_page.setHorizontalHeaderLabels(
            ["ID", "Name", "Created At", "Value"]
        )

        # Page 2: Query View
        self.query_view_page = QTextEdit()
        self.query_view_page.setPlaceholderText("SELECT * FROM your_table;")

        # Page 3: History View
        self.history_view_page = QListWidget()
        self.history_view_page.addItem("SELECT * FROM users;")  # Placeholder history

        # Create the stacked widget and add the pages
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.table_view_page)
        self.stacked_widget.addWidget(self.query_view_page)
        self.stacked_widget.addWidget(self.history_view_page)

        return self.stacked_widget

    def _apply_styles(self):
        # The stylesheet remains the same for now
        self.setStyleSheet(
            """
            /* Main window background */
            QMainWindow {
                background-color: #FFFFFF;
            }
            QWidget {
                color: #333; /* Dark grey text */
            }
            /* Column 1: Connection Switcher */
            QListWidget#ConnectionList { /* Use object name for specificity */
                background-color: #ECECEC;
                border: none;
            }
            QListWidget#ConnectionList::item {
                padding: 8px;
                color: #555;
            }
            QListWidget#ConnectionList::item:selected {
                background-color: #D5E3F2;
                color: #000;
            }
            /* Column 2 styling */
            QPushButton {
                background-color: #f0f0f0; border: 1px solid #dcdcdc;
                padding: 5px; border-radius: 3px;
            }
            QPushButton:hover { background-color: #e8e8e8; }
            QPushButton:pressed { background-color: #d8d8d8; }
            QLineEdit { padding: 5px; border: 1px solid #dcdcdc; border-radius: 3px; }
            QTreeWidget { border: none; background-color: #F5F5F5; }
            QTreeWidget::item:hover { background-color: #E8E8E8; }
            QTreeWidget::item:selected { background-color: #D5E3F2; }
            
            /* Splitter Handle */
            QSplitter::handle { background-color: #E0E0E0; }
            QSplitter::handle:horizontal { width: 1px; }

            /* Top Toolbar */
        QToolBar {
            background-color: #ECECEC;
            border-bottom: 1px solid #D0D0D0;
            padding: 2px;
        }
        /* Style for buttons specifically on the toolbar */
        QToolBar QPushButton {
            background-color: transparent;
            border: none;
            padding: 4px;
        }
        QToolBar QPushButton:hover {
            background-color: #DCDCDC;
            border-radius: 3px;
        }
        /* Connection Status Label */
        QLabel#ConnectionLabel {
            background-color: #C5E1A5; /* A light green color */
            color: #33691E; /* Dark green text */
            padding: 3px 10px 3px 10px;
            border-radius: 10px;
            font-weight: bold;
        }
        """
        )
        # Set object names so the stylesheet can target them
        self.col1_widget.setObjectName("ConnectionList")
        self.col2_widget.setObjectName("ObjectExplorer")

    ## ----------------------------------------------------------------
    ## Slot Methods (The actions that happen on clicks)
    ## ----------------------------------------------------------------

    def _activate_table_view(self):
        """Switches the stacked widget to show the table view page."""
        print("Activating Table View...")
        self.stacked_widget.setCurrentWidget(self.table_view_page)

    def _activate_query_view(self):
        """Switches the stacked widget to show the query editor page."""
        print("Activating Query View...")
        self.stacked_widget.setCurrentWidget(self.query_view_page)

    def _activate_history_view(self):
        """Switches the stacked widget to show the history view page."""
        print("Activating History View...")
        self.stacked_widget.setCurrentWidget(self.history_view_page)

    # In main_window.py, inside the MainWindow class

    ## NEW METHOD: Builds the Top Toolbar
    def _create_top_bar(self):
        """Creates the main top toolbar for the application."""
        # Create a QToolBar instance
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(18, 18))  # Set a consistent icon size
        toolbar.setMovable(False)  # Make the toolbar non-movable

        # --- Create a container widget and a horizontal layout ---
        # This is the key to the left-center-right alignment
        container = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 0, 10, 0)  # Add some horizontal padding
        layout.setSpacing(10)  # Spacing between widgets
        container.setLayout(layout)

        # --- Left-aligned Widgets ---
        self.close_conn_btn = QPushButton(QIcon("icons/x-circle.svg"), "")
        self.eye_btn = QPushButton(QIcon("icons/eye.svg"), "")
        self.lock_btn = QPushButton(QIcon("icons/lock.svg"), "")
        self.db_icon_label = QLabel()
        self.db_icon_label.setPixmap(QIcon("icons/database.svg").pixmap(QSize(18, 18)))

        layout.addWidget(self.close_conn_btn)
        layout.addWidget(self.eye_btn)
        layout.addWidget(self.lock_btn)
        layout.addWidget(self.db_icon_label)

        # --- Center-aligned Widget (with Stretch) ---
        layout.addStretch()  # This pushes everything apart

        self.connection_label = QLabel("MySQL Brew : mysql : comments")
        self.connection_label.setObjectName("ConnectionLabel")  # For styling
        layout.addWidget(self.connection_label)

        layout.addStretch()  # This pushes everything apart

        # --- Right-aligned Widgets ---
        self.refresh_btn = QPushButton(QIcon("icons/refresh-cw.svg"), "")
        self.stats_btn = QPushButton(QIcon("icons/bar-chart-2.svg"), "")
        self.search_btn = QPushButton(QIcon("icons/search.svg"), "")
        self.left_panel_btn = QPushButton(QIcon("icons/sidebar.svg"), "")
        self.right_panel_btn = QPushButton(
            QIcon("icons/sidebar.svg"), ""
        )  # Using same icon for demo
        self.bottom_panel_btn = QPushButton(
            QIcon("icons/sidebar.svg"), ""
        )  # Using same icon for demo

        layout.addWidget(self.refresh_btn)
        layout.addWidget(self.stats_btn)
        layout.addWidget(self.search_btn)
        layout.addWidget(self.left_panel_btn)
        layout.addWidget(self.right_panel_btn)
        layout.addWidget(self.bottom_panel_btn)

        # Add the container widget to the toolbar
        toolbar.addWidget(container)
        return toolbar


# This part is just for running this file directly for testing
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
