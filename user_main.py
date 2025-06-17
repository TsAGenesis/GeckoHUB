#!/usr/bin/env python3
"""
GeckosHUB - User Version (Auto-Generated)
Gaming Tools & Bots Launcher ohne Login
"""

import sys
import json
import os
from datetime import datetime
from PySide6.QtWidgets import (QApplication, QMainWindow, QTabWidget, QVBoxLayout, 
                               QWidget, QDialog, QLineEdit, QPushButton, QLabel, 
                               QHBoxLayout, QMessageBox, QFrame, QListWidget,
                               QListWidgetItem, QProgressBar)
from PySide6.QtCore import Qt, QThread, Signal, QTimer
from PySide6.QtGui import QFont
import subprocess
import urllib.request
import webbrowser

class UpdateChecker(QThread):
    """Thread für Update-Überprüfung"""
    update_available = Signal(dict)
    
    def __init__(self):
        super().__init__()
        # Korrekte GitHub URL für TsAGenesis/GeckoHUB
        self.github_url = "https://raw.githubusercontent.com/TsAGenesis/GeckoHUB/main"
        
    def run(self):
        try:
            # Version von GitHub abrufen
            version_url = f"{self.github_url}/version.json"
            response = urllib.request.urlopen(version_url, timeout=10)
            remote_version = json.loads(response.read().decode())
            
            # Lokale Version laden
            local_version = {"version": "0.0.0", "build": 0}
            if os.path.exists("version.json"):
                with open("version.json", 'r') as f:
                    local_version = json.load(f)
                    
            # Vergleichen
            if remote_version["build"] > local_version["build"]:
                self.update_available.emit(remote_version)
                
        except Exception as e:
            print(f"Update check failed: {e}")

class LicenseKeyDialog(QDialog):
    """Dialog für License Key Eingabe"""
    
    def __init__(self, tab_name, parent=None):
        super().__init__(parent)
        self.tab_name = tab_name
        self.license_key = ""
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle(f"🦎 {self.tab_name} - License Required")
        self.setFixedSize(600, 400)
        self.setStyleSheet("""
            QDialog {
                background-color: rgb(17, 17, 17);
                color: white;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(25)
        
        # Header
        title = QLabel(f"🔐 {self.tab_name}")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: rgb(34, 197, 94);")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtitle = QLabel("License Key Required")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setStyleSheet("color: rgb(156, 163, 175);")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # License Input
        instruction = QLabel(f"Enter your {self.tab_name} license key:")
        instruction.setFont(QFont("Segoe UI", 11))
        instruction.setStyleSheet("color: rgb(34, 197, 94);")
        
        self.license_input = QLineEdit()
        self.license_input.setFont(QFont("Segoe UI", 12))
        self.license_input.setMinimumHeight(40)
        self.license_input.setPlaceholderText(f"{self.tab_name.upper().replace(' ', '_')}-XXXXXXXX-XXXXXXXX")
        self.license_input.setStyleSheet("""
            QLineEdit {
                background-color: rgb(45, 45, 45);
                color: white;
                border: 2px solid rgb(60, 60, 60);
                border-radius: 8px;
                padding: 12px 15px;
            }
            QLineEdit:focus {
                border: 2px solid rgb(34, 197, 94);
            }
        """)
        
        # Status
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.validate_btn = QPushButton("🔓 Validate License")
        self.validate_btn.setMinimumHeight(45)
        self.validate_btn.setStyleSheet("""
            QPushButton {
                background-color: rgb(34, 197, 94);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgb(22, 163, 74);
            }
        """)
        self.validate_btn.clicked.connect(self.validate_license)
        
        self.cancel_btn = QPushButton("❌ Cancel")
        self.cancel_btn.setMinimumHeight(45)
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: rgb(75, 85, 99);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                font-weight: bold;
            }
        """)
        self.cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(self.validate_btn)
        button_layout.addWidget(self.cancel_btn)
        
        # Add to layout
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(instruction)
        layout.addWidget(self.license_input)
        layout.addWidget(self.status_label)
        layout.addLayout(button_layout)
        
        # Enter key binding
        self.license_input.returnPressed.connect(self.validate_license)
        
    def validate_license(self):
        """License validieren"""
        license_key = self.license_input.text().strip()
        
        if not license_key:
            self.status_label.setText("❌ Please enter a license key")
            self.status_label.setStyleSheet("color: rgb(239, 68, 68);")
            return
            
        # Einfache Client-seitige Validierung
        tab_prefix = self.tab_name.upper().replace(' ', '_')
        if license_key.startswith(f"{tab_prefix}-") or license_key.startswith("GECKO-"):
            # Hier würde normalerweise eine Server-Validierung stattfinden
            self.license_key = license_key
            self.status_label.setText("✅ License valid!")
            self.status_label.setStyleSheet("color: rgb(34, 197, 94);")
            QTimer.singleShot(1000, self.accept)
        else:
            self.status_label.setText("❌ Invalid license key format")
            self.status_label.setStyleSheet("color: rgb(239, 68, 68);")

class ProgramTab(QWidget):
    """Dynamischer Tab für Programme"""
    
    def __init__(self, tab_data, parent=None):
        super().__init__(parent)
        self.tab_data = tab_data
        self.validated = not tab_data.get('requires_license', False)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background-color: rgb(25, 25, 25);
                border: 2px solid rgb(34, 197, 94);
                border-radius: 10px;
                padding: 20px;
            }
        """)
        
        header_layout = QVBoxLayout(header_frame)
        header_layout.setSpacing(10)
        
        title = QLabel(f"{self.tab_data['icon']} {self.tab_data['name']}")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setStyleSheet("color: rgb(34, 197, 94);")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        if self.tab_data.get('description'):
            desc = QLabel(self.tab_data['description'])
            desc.setFont(QFont("Segoe UI", 12))
            desc.setStyleSheet("color: rgb(156, 163, 175);")
            desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
            desc.setWordWrap(True)
            header_layout.addWidget(desc)
            
        header_layout.addWidget(title)
        
        # License Status
        if self.tab_data.get('requires_license', False):
            self.license_status = QLabel("🔐 License Required")
            self.license_status.setFont(QFont("Segoe UI", 11))
            self.license_status.setStyleSheet("color: rgb(239, 68, 68);")
            self.license_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
            header_layout.addWidget(self.license_status)
        
        # Program List
        self.program_list = QListWidget()
        self.program_list.setStyleSheet("""
            QListWidget {
                background-color: rgb(30, 30, 30);
                border: 1px solid rgb(60, 60, 60);
                border-radius: 8px;
                padding: 15px;
            }
            QListWidget::item {
                padding: 15px;
                margin: 5px;
                border-radius: 8px;
                background-color: rgb(40, 40, 40);
                border: 1px solid rgb(60, 60, 60);
            }
            QListWidget::item:hover {
                background-color: rgb(50, 50, 50);
                border: 1px solid rgb(34, 197, 94);
            }
            QListWidget::item:selected {
                background-color: rgb(34, 197, 94);
                color: black;
            }
        """)
        self.program_list.itemDoubleClicked.connect(self.launch_program)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.launch_btn = QPushButton("🚀 Launch Selected")
        self.launch_btn.setStyleSheet("""
            QPushButton {
                background-color: rgb(34, 197, 94);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 25px;
                font-weight: bold;
                min-height: 35px;
            }
            QPushButton:hover {
                background-color: rgb(22, 163, 74);
            }
            QPushButton:disabled {
                background-color: rgb(60, 60, 60);
                color: rgb(120, 120, 120);
            }
        """)
        self.launch_btn.clicked.connect(self.launch_program)
        
        if self.tab_data.get('requires_license', False):
            self.validate_license_btn = QPushButton("🔐 Validate License")
            self.validate_license_btn.setStyleSheet("""
                QPushButton {
                    background-color: rgb(168, 85, 247);
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 12px 25px;
                    font-weight: bold;
                    min-height: 35px;
                }
                QPushButton:hover {
                    background-color: rgb(147, 51, 234);
                }
            """)
            self.validate_license_btn.clicked.connect(self.validate_license)
            button_layout.addWidget(self.validate_license_btn)
            
        button_layout.addWidget(self.launch_btn)
        button_layout.addStretch()
        
        layout.addWidget(header_frame)
        layout.addWidget(self.program_list)
        layout.addLayout(button_layout)
        
        self.load_programs()
        self.update_ui_state()
        
    def load_programs(self):
        """Programme laden"""
        self.program_list.clear()
        
        programs = self.tab_data.get('programs', [])
        if not programs:
            item = QListWidgetItem("ℹ️ No programs configured for this tab")
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            self.program_list.addItem(item)
            return
        
        for program in programs:
            license_text = " 🔐" if program.get('requires_license', False) else ""
            type_text = "📁" if program.get('type') == 'file' else "🌐"
            
            item_text = f"{type_text} {program['name']}{license_text}\n{program.get('description', '')}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, program)
            self.program_list.addItem(item)
            
    def update_ui_state(self):
        """UI-Status aktualisieren"""
        if self.tab_data.get('requires_license', False) and not self.validated:
            self.program_list.setEnabled(False)
            self.launch_btn.setEnabled(False)
        else:
            self.program_list.setEnabled(True)
            self.launch_btn.setEnabled(True)
            
    def validate_license(self):
        """Lizenz validieren"""
        dialog = LicenseKeyDialog(self.tab_data['name'], self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.validated = True
            self.program_list.setEnabled(True)
            self.launch_btn.setEnabled(True)
            if hasattr(self, 'validate_license_btn'):
                self.validate_license_btn.setText("✅ Licensed")
                self.validate_license_btn.setStyleSheet("""
                    QPushButton {
                        background-color: rgb(34, 197, 94);
                        color: white;
                        border: none;
                        border-radius: 8px;
                        padding: 12px 25px;
                        font-weight: bold;
                        min-height: 35px;
                    }
                """)
                self.validate_license_btn.setEnabled(False)
            if hasattr(self, 'license_status'):
                self.license_status.setText("✅ Licensed")
                self.license_status.setStyleSheet("color: rgb(34, 197, 94);")
            
    def launch_program(self, item=None):
        """Programm starten"""
        if not self.validated and self.tab_data.get('requires_license', False):
            self.validate_license()
            return
            
        if item is None:
            item = self.program_list.currentItem()
            
        if item is None:
            QMessageBox.warning(self, "No Selection", "Please select a program to launch.")
            return
            
        program = item.data(Qt.ItemDataRole.UserRole)
        if program is None:
            return
        
        if program.get('requires_license', False) and not self.validated:
            QMessageBox.warning(self, "License Required", "This program requires a valid license.")
            return
            
        try:
            if program.get('type') == 'file':
                file_path = program.get('path', '')
                if os.path.exists(file_path):
                    subprocess.Popen([file_path])
                    QMessageBox.information(self, "Launched", f"{program['name']} started successfully!")
                else:
                    QMessageBox.critical(self, "File Not Found", f"Program file not found:\n{file_path}")
            else:
                url = program.get('path', '')
                if url:
                    webbrowser.open(url)
                    QMessageBox.information(self, "Opened", f"Download link opened in browser.")
                else:
                    QMessageBox.critical(self, "No URL", "No download URL configured.")
                
        except Exception as e:
            QMessageBox.critical(self, "Launch Error", f"Failed to launch {program['name']}:\n{str(e)}")

class GeckosHUB(QMainWindow):
    """User Hauptfenster ohne Login"""
    
    def __init__(self):
        super().__init__()
        self.tabs_config = {}
        self.load_tabs_config()
        self.setup_ui()
        self.check_for_updates()
        
    def load_tabs_config(self):
        """Tab-Konfiguration laden"""
        try:
            if os.path.exists("tabs_config.json"):
                with open("tabs_config.json", 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tabs_config = data
            else:
                self.tabs_config = {
                    "tabs": [
                        {
                            "name": "Welcome",
                            "icon": "🦎",
                            "description": "No configuration found. Please ensure tabs_config.json exists.",
                            "requires_license": False,
                            "programs": []
                        }
                    ],
                    "version": "1.0.0"
                }
                
        except Exception as e:
            print(f"Error loading tabs config: {e}")
            self.tabs_config = {
                "tabs": [
                    {
                        "name": "Configuration Error",
                        "icon": "❌",
                        "description": f"Error loading configuration: {e}",
                        "requires_license": False,
                        "programs": []
                    }
                ]
            }
            
    def setup_ui(self):
        self.setWindowTitle("🦎 GeckosHUB - Gaming Tools & Bots Launcher")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(1000, 700)
        
        # Styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: rgb(17, 17, 17);
                color: rgb(34, 197, 94);
            }
            QTabWidget::pane {
                border: 2px solid rgb(34, 197, 94);
                background-color: rgb(25, 25, 25);
                border-radius: 8px;
            }
            QTabBar::tab {
                background-color: rgb(30, 30, 30);
                color: rgb(156, 163, 175);
                padding: 12px 20px;
                margin-right: 3px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: bold;
                min-width: 120px;
            }
            QTabBar::tab:selected {
                background-color: rgb(34, 197, 94);
                color: rgb(17, 17, 17);
            }
            QTabBar::tab:hover:!selected {
                background-color: rgb(45, 45, 45);
                color: rgb(34, 197, 94);
            }
        """)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Header
        self.create_header(layout)
        
        # Tab Widget
        self.tab_widget = QTabWidget()
        self.setup_tabs()
        
        layout.addWidget(self.tab_widget)
        
    def create_header(self, parent_layout):
        """Header erstellen"""
        header_frame = QFrame()
        header_frame.setFixedHeight(120)
        header_frame.setStyleSheet("""
            QFrame {
                background-color: rgb(25, 25, 25);
                border: 2px solid rgb(34, 197, 94);
                border-radius: 10px;
            }
        """)

        layout = QHBoxLayout(header_frame)
        layout.setContentsMargins(25, 20, 25, 20)

        # Title Section
        title_layout = QVBoxLayout()
        title_layout.setSpacing(5)

        title = QLabel("🦎 GECKOSHUB")
        title.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        title.setStyleSheet("color: rgb(34, 197, 94);")

        subtitle = QLabel("Gaming Tools & Bots Launcher")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setStyleSheet("color: rgb(156, 163, 175);")

        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        title_layout.addStretch()

        # Version & Update Section
        version_layout = QVBoxLayout()
        version_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        version_layout.setSpacing(8)

        self.version_label = QLabel("Version: Loading...")
        self.version_label.setFont(QFont("Segoe UI", 11))
        self.version_label.setStyleSheet("color: rgb(156, 163, 175);")
        self.version_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.version_label.setMinimumWidth(250)   # Mehr Platz!

        self.update_status_label = QLabel("")
        self.update_status_label.setFont(QFont("Segoe UI", 10))
        self.update_status_label.setStyleSheet("color: rgb(34, 197, 94);")
        self.update_status_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.update_status_label.setMinimumWidth(250)

        self.manual_update_btn = QPushButton("🔄 Check Updates")
        self.manual_update_btn.setFixedHeight(35)
        self.manual_update_btn.setMinimumWidth(160)  # Mehr Breite
        self.manual_update_btn.setStyleSheet("""
            QPushButton {
                background-color: rgb(59, 130, 246);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 15px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgb(37, 99, 235);
            }
        """)
        self.manual_update_btn.clicked.connect(self.manual_check_updates)

        version_layout.addWidget(self.version_label)
        version_layout.addWidget(self.update_status_label)
        version_layout.addWidget(self.manual_update_btn)

        layout.addLayout(title_layout, 3)
        layout.addStretch(1)
        layout.addLayout(version_layout, 2)

        parent_layout.addWidget(header_frame)

        
    def setup_tabs(self):
        """Tabs einrichten"""
        tabs = self.tabs_config.get('tabs', [])
        
        if not tabs:
            no_config_widget = QWidget()
            layout = QVBoxLayout(no_config_widget)
            layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            message = QLabel("❌ No tabs configured\n\nPlease ensure tabs_config.json exists and contains valid tab configuration.")
            message.setFont(QFont("Segoe UI", 14))
            message.setStyleSheet("color: rgb(239, 68, 68);")
            message.setAlignment(Qt.AlignmentFlag.AlignCenter)
            message.setWordWrap(True)
            
            layout.addWidget(message)
            self.tab_widget.addTab(no_config_widget, "❌ No Config")
            return
        
        for tab_data in tabs:
            tab_widget = ProgramTab(tab_data)
            tab_icon = tab_data.get('icon', '🎮')
            tab_name = tab_data.get('name', 'Unknown')
            self.tab_widget.addTab(tab_widget, f"{tab_icon} {tab_name}")
            
    def check_for_updates(self):
        """Nach Updates suchen"""
        self.update_checker = UpdateChecker()
        self.update_checker.update_available.connect(self.on_update_available)
        self.update_checker.start()
        
        # Lokale Version anzeigen
        try:
            if os.path.exists("version.json"):
                with open("version.json", 'r') as f:
                    version_data = json.load(f)
                    self.version_label.setText(f"Version: {version_data.get('version', 'Unknown')}")
            else:
                self.version_label.setText("Version: No version file")
        except Exception as e:
            self.version_label.setText("Version: Error reading")
            
    def manual_check_updates(self):
        """Manuell nach Updates suchen"""
        self.update_status_label.setText("🔄 Checking...")
        self.update_status_label.setStyleSheet("color: rgb(251, 191, 36);")
        
        self.manual_update_checker = UpdateChecker()
        self.manual_update_checker.update_available.connect(self.on_update_available)
        self.manual_update_checker.finished.connect(self.on_manual_check_finished)
        self.manual_update_checker.start()
        
    def on_manual_check_finished(self):
        """Manuelle Update-Prüfung beendet"""
        if not hasattr(self, '_update_found'):
            self.update_status_label.setText("✅ Up to date")
            self.update_status_label.setStyleSheet("color: rgb(34, 197, 94);")
            QTimer.singleShot(3000, lambda: self.update_status_label.setText(""))
            
    def on_update_available(self, version_data):
        """Update verfügbar"""
        self._update_found = True
        self.update_status_label.setText("🔄 Update available!")
        self.update_status_label.setStyleSheet("color: rgb(251, 191, 36);")
        
        current_version = "Unknown"
        try:
            if os.path.exists("version.json"):
                with open("version.json", 'r') as f:
                    local_version = json.load(f)
                    current_version = local_version.get('version', 'Unknown')
        except:
            pass
        
        reply = QMessageBox.question(
            self,
            "Update Available",
            f"A new version is available!\n\n"
            f"Current: {current_version}\n"
            f"New: {version_data.get('version', 'Unknown')}\n\n"
            f"Changes: {version_data.get('changes', 'Various improvements')}\n\n"
            f"Would you like to update now?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.download_update(version_data)
            
    def download_update(self, version_data):
        """Update herunterladen"""
        try:
            # Update-Dialog
            update_dialog = QDialog(self)
            update_dialog.setWindowTitle("🦎 Updating GeckosHUB")
            update_dialog.setFixedSize(400, 200)
            update_dialog.setStyleSheet("""
                QDialog { 
                    background-color: rgb(17, 17, 17); 
                    color: white; 
                }
            """)
            
            layout = QVBoxLayout(update_dialog)
            
            status_label = QLabel("Downloading update...")
            status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            progress_bar = QProgressBar()
            progress_bar.setRange(0, 100)
            
            layout.addWidget(status_label)
            layout.addWidget(progress_bar)
            
            update_dialog.show()
            QApplication.processEvents()
            
            # Files herunterladen
            github_base = self.update_checker.github_url
            files_to_update = ["tabs_config.json", "version.json"]
            
            for i, filename in enumerate(files_to_update):
                status_label.setText(f"Downloading {filename}...")
                progress_bar.setValue(int((i / len(files_to_update)) * 100))
                QApplication.processEvents()
                
                try:
                    url = f"{github_base}/{filename}"
                    urllib.request.urlretrieve(url, filename)
                except Exception as e:
                    print(f"Failed to download {filename}: {e}")
                    continue
                
            progress_bar.setValue(100)
            status_label.setText("Update complete!")
            QApplication.processEvents()
            
            QMessageBox.information(
                self,
                "Update Complete",
                "Update downloaded successfully!\nPlease restart GeckosHUB to apply changes."
            )
            
            update_dialog.close()
            
        except Exception as e:
            QMessageBox.critical(self, "Update Error", f"Failed to download update:\n{str(e)}")

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("GeckosHUB")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("Gecko")
    
    # Dark theme
    app.setStyle('Fusion')
    
    window = GeckosHUB()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
