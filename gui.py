import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFileDialog, QListWidget, QMessageBox,
    QAction, QAbstractItemView
)
from main import find_files_with_extension, move_or_copy_file, delete_file, open_file_or_folder


class FileManagementApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.folder_label = None
        self.folder_lineedit = None
        self.folder_browse_button = None

        self.extension_label = None
        self.extension_lineedit = None

        self.find_files_button = None

        self.file_listwidget = None

        self.select_all_button = None
        self.copy_button = None
        self.move_button = None
        self.delete_button = None
        self.open_folder_button = None
        self.open_file_button = None

        self.pos_x = 200
        self.pos_y = 200
        self.width = 600
        self.height = 780

        self.setWindowTitle('File Management App')
        self.setGeometry(self.pos_x, self.pos_y, self.width, self.height)

        self.central_widget = None

        self.initUI()

    def initUI(self):
        # Widgets
        self.folder_label = QLabel('Select Folder:')
        self.folder_lineedit = QLineEdit()
        self.folder_browse_button = QPushButton('Browse')

        self.extension_label = QLabel('File Extension:')
        self.extension_lineedit = QLineEdit()

        self.find_files_button = QPushButton('Find Files')

        self.file_listwidget = QListWidget()
        self.file_listwidget.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.select_all_button = QPushButton('Select All')
        self.copy_button = QPushButton('Copy Selected Files')
        self.move_button = QPushButton('Move Selected Files')
        self.delete_button = QPushButton('Delete Selected Files')
        self.open_folder_button = QPushButton('Open File Location')
        self.open_file_button = QPushButton('Open File')

        # Layout
        vbox = QVBoxLayout()

        hbox_folder = QHBoxLayout()
        hbox_folder.addWidget(self.folder_label)
        hbox_folder.addWidget(self.folder_lineedit)
        hbox_folder.addWidget(self.folder_browse_button)

        hbox_extension = QHBoxLayout()
        hbox_extension.addWidget(self.extension_label)
        hbox_extension.addWidget(self.extension_lineedit)

        vbox.addLayout(hbox_folder)
        vbox.addLayout(hbox_extension)
        vbox.addWidget(self.find_files_button)
        vbox.addWidget(self.file_listwidget)

        hbox_buttons = QHBoxLayout()
        hbox_buttons.addWidget(self.select_all_button)
        hbox_buttons.addWidget(self.copy_button)
        hbox_buttons.addWidget(self.move_button)
        vbox.addLayout(hbox_buttons)

        xbox_buttons = QHBoxLayout()
        xbox_buttons.addWidget(self.delete_button)
        xbox_buttons.addWidget(self.open_folder_button)
        xbox_buttons.addWidget(self.open_file_button)
        vbox.addLayout(xbox_buttons)

        self.central_widget = QWidget()
        self.central_widget.setLayout(vbox)
        self.setCentralWidget(self.central_widget)

        # Menu bar
        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')

        exit_action = QAction('&Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Connect signals and slots
        self.folder_browse_button.clicked.connect(self.browse_folder)
        self.find_files_button.clicked.connect(self.find_files)
        self.select_all_button.clicked.connect(self.select_all_files)
        self.copy_button.clicked.connect(self.copy_files)
        self.move_button.clicked.connect(self.move_files)
        self.delete_button.clicked.connect(self.delete_files)
        self.open_folder_button.clicked.connect(self.open_file_location)
        self.open_file_button.clicked.connect(self.open_file)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folder:
            self.folder_lineedit.setText(folder)

    def find_files(self):
        folder = self.folder_lineedit.text()
        extension = self.extension_lineedit.text()

        if not folder or not extension:
            QMessageBox.warning(self, 'Warning', 'Please select a folder and enter an extension.')
            return

        found_files = find_files_with_extension(folder, extension)

        self.file_listwidget.clear()
        for file_info in found_files:
            self.file_listwidget.addItem(file_info['Path'])

    def select_all_files(self):
        self.file_listwidget.selectAll()

    def copy_files(self):
        selected_items = self.file_listwidget.selectedItems()

        if not selected_items:
            QMessageBox.warning(self, 'Warning', 'Please select files to copy.')
            return

        destination_folder = QFileDialog.getExistingDirectory(self, 'Select Destination Folder')
        if not destination_folder:
            return

        for item in selected_items:
            file_path = item.text()
            move_or_copy_file(file_path, destination_folder, action='copy')

        QMessageBox.information(self, 'Success', 'Files copied successfully.')

    def move_files(self):
        selected_items = self.file_listwidget.selectedItems()

        if not selected_items:
            QMessageBox.warning(self, 'Warning', 'Please select files to move.')
            return

        destination_folder = QFileDialog.getExistingDirectory(self, 'Select Destination Folder')
        if not destination_folder:
            return

        for item in selected_items:
            file_path = item.text()
            move_or_copy_file(file_path, destination_folder, action='cut')

        QMessageBox.information(self, 'Success', 'Files moved successfully.')

    def delete_files(self):
        selected_items = self.file_listwidget.selectedItems()

        if not selected_items:
            QMessageBox.warning(self, 'Warning', 'Please select files to delete.')
            return

        reply = QMessageBox.question(self, 'Confirmation', 'Are you sure you want to delete selected files?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            for item in selected_items:
                file_path = item.text()
                delete_file(file_path)

            QMessageBox.information(self, 'Success', 'Files deleted successfully.')

    def open_file_location(self):
        selected_items = self.file_listwidget.selectedItems()

        if not selected_items:
            QMessageBox.warning(self, 'Warning', 'Please select a file to open its location.')
            return

        # Open file location for the first selected item
        file_path = selected_items[0].text()

        open_file_or_folder(file_path, file=False)

    def open_file(self):
        selected_items = self.file_listwidget.selectedItems()

        if not selected_items:
            QMessageBox.warning(self, 'Warning', 'Please select a file to open its location.')
            return

        # Open file location for the first selected item
        file_path = selected_items[0].text()

        open_file_or_folder(file_path, file=True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FileManagementApp()
    window.show()
    sys.exit(app.exec_())
