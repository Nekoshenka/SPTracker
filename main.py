"""
Tracker App - Основное окно приложения
"""

import sys
import os
import traceback
import json
from datetime import datetime

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QPushButton, QFrame, QMessageBox,
    QComboBox, QDialog
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon

from locales import get_text
from account_editor import AccountEditor
from progress_editor import ProgressEditor
from statistics_window import StatisticsWindow
from analysis_window import AnalysisWindow

CURRENT_LANG = "en"
CURRENT_THEME = "dark"

def global_exception_handler(exc_type, exc_value, exc_tb):
    """Перехватывает все необработанные исключения"""
    error_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_tb))

    log_path = os.path.join(os.path.dirname(sys.executable), "error.log") if getattr(sys, 'frozen', False) else "error.log"
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"\n--- {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")
            f.write(error_msg)
    except:
        pass

    lang = CURRENT_LANG if CURRENT_LANG in ["en", "ru"] else "en"
    theme = CURRENT_THEME

    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setWindowTitle(get_text("error_window_title", lang))
    msg.setText(get_text("error_critical", lang))
    msg.setDetailedText(error_msg[:800])

    if theme == "light":
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #f0f0f0;
            }
            QMessageBox QLabel {
                color: #333333;
            }
            QMessageBox QPushButton {
                background-color: #f0f0f0;
                color: #333333;
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 5px 15px;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #e0e0e0;
            }
            QMessageBox QTextEdit {
                background-color: #ffffff;
                color: #333333;
                border: 1px solid #cccccc;
                border-radius: 4px;
            }
            QTextEdit QScrollBar:vertical {
                background-color: #f0f0f0;
                width: 12px;
                border-radius: 6px;
            }
            QTextEdit QScrollBar::handle:vertical {
                background-color: #cccccc;
                border-radius: 6px;
                min-height: 20px;
            }
            QTextEdit QScrollBar::handle:vertical:hover {
                background-color: #aaaaaa;
            }
            QTextEdit QScrollBar::add-line:vertical,
            QTextEdit QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QTextEdit QScrollBar:horizontal {
                background-color: #f0f0f0;
                height: 12px;
                border-radius: 6px;
            }
            QTextEdit QScrollBar::handle:horizontal {
                background-color: #cccccc;
                border-radius: 6px;
                min-width: 20px;
            }
            QTextEdit QScrollBar::handle:horizontal:hover {
                background-color: #aaaaaa;
            }
            QTextEdit QScrollBar::add-line:horizontal,
            QTextEdit QScrollBar::sub-line:horizontal {
                width: 0px;
            }
        """)
    else:
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #1e1e1e;
            }
            QMessageBox QLabel {
                color: #e0e0e0;
            }
            QMessageBox QPushButton {
                background-color: #3d3d3d;
                color: #e0e0e0;
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 5px 15px;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #4d4d4d;
            }
            QMessageBox QTextEdit {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #444444;
                border-radius: 4px;
            }
            QTextEdit QScrollBar:vertical {
                background-color: #2d2d2d;
                width: 12px;
                border-radius: 6px;
            }
            QTextEdit QScrollBar::handle:vertical {
                background-color: #555555;
                border-radius: 6px;
                min-height: 20px;
            }
            QTextEdit QScrollBar::handle:vertical:hover {
                background-color: #777777;
            }
            QTextEdit QScrollBar::add-line:vertical,
            QTextEdit QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QTextEdit QScrollBar:horizontal {
                background-color: #2d2d2d;
                height: 12px;
                border-radius: 6px;
            }
            QTextEdit QScrollBar::handle:horizontal {
                background-color: #555555;
                border-radius: 6px;
                min-width: 20px;
            }
            QTextEdit QScrollBar::handle:horizontal:hover {
                background-color: #777777;
            }
            QTextEdit QScrollBar::add-line:horizontal,
            QTextEdit QScrollBar::sub-line:horizontal {
                width: 0px;
            }
        """)

    msg.exec()
    sys.exit(1)

sys.excepthook = global_exception_handler


class MainWindow(QMainWindow):
    """Главное окно приложения"""

    DEFAULT_THEME = "dark"      # "dark" или "light"
    DEFAULT_LANGUAGE = "en"      # "en" или "ru"

    accounts_updated = Signal()

    def __init__(self):
        super().__init__()
        self.current_language = "en"
        self.current_account = None
        self.current_account_data = None
        self.current_account_index = -1
        self.game_data = None
        self.accounts = []
        self.dark_theme = True

        global CURRENT_LANG
        CURRENT_LANG = self.current_language
        global CURRENT_THEME
        CURRENT_THEME = "dark"

        self.init_ui()

        if not self.load_game_data():
            sys.exit(1)
            return

        self.ensure_accounts_dir()
        self.scan_accounts()
        self.update_accounts_combo()
        self.update_ui_texts()
        self.update_theme()

        self._apply_account_settings()

        self.accounts_updated.connect(self.on_accounts_updated)

    def init_ui(self):
        """Настройка интерфейса"""
        self.setWindowTitle(get_text("window_title", self.current_language))
        self.setFixedSize(800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)

        top_panel = QFrame()
        top_panel.setFrameShape(QFrame.StyledPanel)
        top_layout = QHBoxLayout(top_panel)
        top_layout.setContentsMargins(10, 5, 10, 5)

        left_layout = QHBoxLayout()
        left_layout.setSpacing(5)

        self.account_combo = QComboBox()
        self.account_combo.currentIndexChanged.connect(self.on_account_selected)
        self.account_combo.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.account_combo.setMinimumWidth(150)
        self.account_combo.setMaximumWidth(600)
        left_layout.addWidget(self.account_combo)

        self.refresh_btn = QPushButton("🔄")
        self.refresh_btn.setFixedSize(32, 32)
        self.refresh_btn.setToolTip(get_text("refresh_tooltip", self.current_language))
        self.refresh_btn.clicked.connect(self.refresh_accounts)
        left_layout.addWidget(self.refresh_btn)

        self.open_folder_btn = QPushButton("📁")
        self.open_folder_btn.setFixedSize(32, 32)
        self.open_folder_btn.setToolTip(get_text("open_folder_tooltip", self.current_language))
        self.open_folder_btn.clicked.connect(self.open_accounts_folder)
        left_layout.addWidget(self.open_folder_btn)

        top_layout.addLayout(left_layout)
        top_layout.addStretch()

        self.theme_btn = QPushButton("🌙")
        self.theme_btn.setFixedSize(32, 32)
        self.theme_btn.setToolTip(get_text("theme_tooltip", self.current_language))
        self.theme_btn.clicked.connect(self.toggle_theme)
        top_layout.addWidget(self.theme_btn)

        main_layout.addWidget(top_panel)

        center_frame = QFrame()
        center_frame.setFrameShape(QFrame.StyledPanel)
        center_layout = QVBoxLayout(center_frame)
        center_layout.setContentsMargins(40, 30, 40, 30)
        center_layout.setSpacing(12)

        self.title_label = QLabel(get_text("app_title", self.current_language))
        self.title_label.setAlignment(Qt.AlignCenter)
        center_layout.addWidget(self.title_label)

        center_layout.addSpacing(10)

        self.button_icons = {
            "btn_create_account": "➕",
            "btn_edit_account": "✏️",
            "btn_add_progress": "📝",
            "btn_analysis": "🔍",
            "btn_statistics": "📊",
            "btn_exit": "🚪"
        }

        self.btn_create_account = self.create_center_button(
            "btn_create_account", self.open_create_account
        )
        self.btn_edit_account = self.create_center_button(
            "btn_edit_account", self.open_edit_account
        )
        self.btn_add_progress = self.create_center_button(
            "btn_add_progress", self.open_add_progress
        )
        self.btn_analysis = self.create_center_button(
            "btn_analysis", self.open_analysis
        )
        self.btn_statistics = self.create_center_button(
            "btn_statistics", self.open_statistics
        )
        self.btn_exit = self.create_center_button(
            "btn_exit", self.close_app
        )

        center_layout.addWidget(self.btn_create_account)
        center_layout.addWidget(self.btn_edit_account)
        center_layout.addWidget(self.btn_add_progress)
        center_layout.addWidget(self.btn_analysis)
        center_layout.addWidget(self.btn_statistics)
        center_layout.addWidget(self.btn_exit)

        center_layout.addStretch()

        main_layout.addWidget(center_frame)

        bottom_panel = QFrame()
        bottom_panel.setFrameShape(QFrame.StyledPanel)
        bottom_layout = QHBoxLayout(bottom_panel)
        bottom_layout.setContentsMargins(10, 5, 10, 5)

        self.version_label = QLabel("v?")
        bottom_layout.addWidget(self.version_label)

        bottom_layout.addStretch()

        self.lang_btn = QPushButton("EN")
        self.lang_btn.setFixedSize(50, 30)
        self.lang_btn.clicked.connect(self.toggle_language)
        bottom_layout.addWidget(self.lang_btn)

        main_layout.addWidget(bottom_panel)

    def create_center_button(self, btn_id, callback):
        """Создаёт большую кнопку для центра"""
        btn = QPushButton()
        btn.setMinimumHeight(55)
        btn.setMinimumWidth(280)
        btn.clicked.connect(callback)
        btn.setObjectName(btn_id)
        return btn

    def update_center_buttons(self):
        """Обновляет текст на центральных кнопках"""
        for btn_id, icon in self.button_icons.items():
            btn = self.findChild(QPushButton, btn_id)
            if btn:
                btn.setText(f"{icon} {get_text(btn_id, self.current_language)}")

    def toggle_theme(self):
        self.dark_theme = not self.dark_theme
        global CURRENT_THEME
        CURRENT_THEME = "dark" if self.dark_theme else "light"
        self.update_theme()
        self._save_account_settings()

    def update_theme(self):
        """Обновляет тему всего приложения"""
        if self.dark_theme:
            self.theme_btn.setText("🌙")
            self.theme_btn.setToolTip(get_text("theme_tooltip", self.current_language))
            self._apply_dark_theme()
        else:
            self.theme_btn.setText("☀️")
            self.theme_btn.setToolTip(get_text("theme_tooltip", self.current_language))
            self._apply_light_theme()

    def _apply_dark_theme(self):
        """Применяет тёмную тему"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QFrame {
                background-color: #2d2d2d;
                border: 1px solid #444444;
                border-radius: 8px;
            }
            QLabel {
                color: #e0e0e0;
            }
            QComboBox {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 5px 8px;
                min-height: 30px;
            }
            QComboBox:hover {
                border: 1px solid #777777;
            }
            QComboBox:focus {
                border: 1px solid #4CAF50;
            }
            QComboBox::drop-down {
                border: none;
                background-color: transparent;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: #2d2d2d;
                color: #e0e0e0;
                selection-background-color: #4CAF50;
                selection-color: white;
                border: 1px solid #555555;
                outline: none;
            }
            QMessageBox {
                background-color: #1e1e1e;
            }
            QMessageBox QLabel {
                color: #e0e0e0;
            }
            QMessageBox QPushButton {
                background-color: #3d3d3d;
                color: #e0e0e0;
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 5px 15px;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #4d4d4d;
            }
            QPushButton {
                background-color: #3d3d3d;
                color: #e0e0e0;
                border: 1px solid #555555;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                padding: 12px;
            }
            QPushButton:hover {
                background-color: #4d4d4d;
                border: 1px solid #777777;
            }
            QPushButton:pressed {
                background-color: #2d2d2d;
            }
            QPushButton:disabled {
                background-color: #2a2a2a;
                color: #555555;
                border: 1px solid #3d3d3d;
            }
        """)

        self.title_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #e0e0e0;")
        self.version_label.setStyleSheet("color: #666666; font-size: 12px;")

        for btn in [self.refresh_btn, self.open_folder_btn, self.theme_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #e0e0e0;
                    border: 1px solid #555555;
                    border-radius: 4px;
                    font-size: 16px;
                    padding: 0px;
                    margin: 0px;
                }
                QPushButton:hover {
                    background-color: #3d3d3d;
                }
            """)

        self.lang_btn.setStyleSheet("""
            QPushButton {
                font-weight: bold;
                background-color: transparent;
                color: #e0e0e0;
                border: 1px solid #555555;
                border-radius: 4px;
                font-size: 12px;
                padding: 0px;
                margin: 0px;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
            }
        """)

    def _apply_light_theme(self):
        """Применяет светлую тему"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QFrame {
                background-color: #ffffff;
                border: 1px solid #cccccc;
                border-radius: 8px;
            }
            QLabel {
                color: #333333;
            }
            QComboBox {
                background-color: #ffffff;
                color: #333333;
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 5px 8px;
                min-height: 30px;
            }
            QComboBox:hover {
                border: 1px solid #aaaaaa;
            }
            QComboBox:focus {
                border: 1px solid #4CAF50;
            }
            QComboBox::drop-down {
                border: none;
                background-color: transparent;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: #ffffff;
                color: #333333;
                selection-background-color: #4CAF50;
                selection-color: white;
                border: 1px solid #cccccc;
                outline: 0px;
            }
            QComboBox QAbstractItemView::item {
                background-color: #ffffff;
                color: #333333;
                padding: 5px;
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: #4CAF50;
                color: white;
            }
            QMessageBox {
                background-color: #f0f0f0;
            }
            QMessageBox QLabel {
                color: #333333;
            }
            QMessageBox QPushButton {
                background-color: #f0f0f0;
                color: #333333;
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 5px 15px;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton {
                background-color: #f0f0f0;
                color: #333333;
                border: 1px solid #cccccc;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                padding: 12px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
                border: 1px solid #aaaaaa;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
            QPushButton:disabled {
                background-color: #e8e8e8;
                color: #999999;
                border: 1px solid #dddddd;
            }
        """)

        self.title_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #333333;")
        self.version_label.setStyleSheet("color: #999999; font-size: 12px;")

        for btn in [self.refresh_btn, self.open_folder_btn, self.theme_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #333333;
                    border: 1px solid #cccccc;
                    border-radius: 4px;
                    font-size: 16px;
                    padding: 0px;
                    margin: 0px;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
            """)

        self.lang_btn.setStyleSheet("""
            QPushButton {
                font-weight: bold;
                background-color: transparent;
                color: #333333;
                border: 1px solid #cccccc;
                border-radius: 4px;
                font-size: 12px;
                padding: 0px;
                margin: 0px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)

    def get_data_dir(self):
        """Возвращает путь к папке data/ рядом с .exe"""
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        else:
            # Запущено как скрипт
            base_dir = os.path.dirname(os.path.abspath(__file__))

        return os.path.join(base_dir, "data")

    def get_accounts_dir(self):
        """Возвращает путь к папке data/accounts"""
        return os.path.join(self.get_data_dir(), "accounts")

    def ensure_accounts_dir(self):
        """Проверка наличия папки data/accounts"""
        accounts_dir = self.get_accounts_dir()
        if not os.path.exists(accounts_dir):
            try:
                os.makedirs(accounts_dir)
                return True
            except Exception:
                return False
        return True

    def scan_accounts(self):
        accounts_dir = self.get_accounts_dir()
        self.accounts = []

        if not os.path.exists(accounts_dir):
            return

        for f in os.listdir(accounts_dir):
            if not f.endswith(".json"):
                continue

            file_path = os.path.join(accounts_dir, f)
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    account_data = json.load(file)

                if not isinstance(account_data, dict):
                    continue
                if "account_name" not in account_data:
                    continue
                if "owned_characters" not in account_data:
                    continue
                if not isinstance(account_data["owned_characters"], list):
                    continue

                if self.game_data:
                    for char_id in account_data["owned_characters"]:
                        if char_id not in self.game_data.get("characters", {}):
                            continue

                self.accounts.append({
                    "file": f,
                    "path": file_path,
                    "data": account_data
                })

            except:
                continue

        self.accounts.sort(key=lambda x: x["data"].get("account_name", "").lower())

    def refresh_accounts(self):
        self.scan_accounts()
        self.update_accounts_combo()
        count = len(self.accounts)
        self.show_message(get_text("refresh_done", self.current_language).format(count))

    def update_accounts_combo(self):
        self.account_combo.blockSignals(True)
        self.account_combo.clear()

        if not self.accounts:
            self.account_combo.addItem(get_text("no_accounts", self.current_language))
            self.current_account = None
            self.current_account_data = None
            self.current_account_index = -1
        else:
            for account in self.accounts:
                name = account["data"].get("account_name", "Unknown")
                self.account_combo.addItem(name)

            if 0 <= self.current_account_index < len(self.accounts):
                self.account_combo.setCurrentIndex(self.current_account_index)
            else:
                self.account_combo.setCurrentIndex(0)
                self.current_account_index = 0
                self.current_account_data = self.accounts[0]["data"]
                self.current_account = self.current_account_data.get("account_name", "Unknown")

        self.account_combo.blockSignals(False)
        self.update_ui_texts()
        self.update_buttons_state()
        self._apply_account_settings()

    def on_account_selected(self, index):
        if index < 0 or index >= len(self.accounts):
            self.current_account = None
            self.current_account_data = None
            self.current_account_index = -1
            self.update_ui_texts()
            return

        self.current_account_index = index
        self.current_account_data = self.accounts[index]["data"]
        self.current_account = self.current_account_data.get("account_name", "Unknown")
        self._apply_account_settings()
        self.update_ui_texts()
        self.update_buttons_state()

    def _apply_account_settings(self):
        """Применяет настройки (тему и язык) из текущего аккаунта"""
        if self.current_account_data is None:
            return

        theme = self.current_account_data.get("theme", self.DEFAULT_THEME)
        if theme == "light" and self.dark_theme:
            self.dark_theme = False
            self.update_theme()
        elif theme == "dark" and not self.dark_theme:
            self.dark_theme = True
            self.update_theme()

        language = self.current_account_data.get("language", self.DEFAULT_LANGUAGE)
        if language != self.current_language:
            self.current_language = language
            global CURRENT_LANG
            CURRENT_LANG = self.current_language
            self.lang_btn.setText(self.current_language.upper())
            self.update_ui_texts()

    def on_accounts_updated(self):
        self.scan_accounts()
        self.update_accounts_combo()

    def load_game_data(self):
        """Загружает game_data_v*.json из папки data/"""
        data_dir = self.get_data_dir()

        if not os.path.exists(data_dir):
            self.show_error(get_text("error_data_folder_not_found", self.current_language).format(data_dir))
            return False

        game_files = []
        for f in os.listdir(data_dir):
            if f.startswith("game_data_v") and f.endswith(".json"):
                game_files.append(f)

        if not game_files:
            self.show_error(get_text("error_game_data_not_found", self.current_language).format(
                os.path.join(data_dir, "game_data_v*.json")
            ))
            return False

        def get_version(filename):
            try:
                version_str = filename.replace("game_data_v", "").replace(".json", "")
                return [int(x) for x in version_str.split(".")]
            except:
                return [0, 0]

        game_files.sort(key=get_version, reverse=True)
        latest_file = game_files[0]
        file_path = os.path.join(data_dir, latest_file)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                self.game_data = json.load(f)

            if "characters" not in self.game_data:
                self.show_error(get_text("error_game_data_no_characters", self.current_language).format(latest_file))
                return False

            if "sets" not in self.game_data:
                self.show_error(get_text("error_game_data_no_sets", self.current_language).format(latest_file))
                return False

            version = self.game_data.get("version", "unknown")
            self.version_label.setText(f"v{version}")
            print(get_text("info_game_data_loaded", self.current_language).format(version, latest_file))
            return True

        except json.JSONDecodeError as e:
            self.show_error(get_text("error_game_data_json_parse", self.current_language).format(latest_file, str(e)))
            return False

        except Exception as e:
            self.show_error(get_text("error_game_data_load", self.current_language).format(latest_file, str(e)))
            return False

    def open_create_account(self):
        if self.game_data is None:
            self.show_error(get_text("error_data_not_loaded", self.current_language))
            return

        editor = AccountEditor(
            parent=self,
            game_data=self.game_data,
            account_data=None,
            lang=self.current_language,
            accounts_dir=self.get_accounts_dir(),
            dark_theme=self.dark_theme
        )

        if editor.exec() == QDialog.DialogCode.Accepted:
            self.scan_accounts()
            self.update_accounts_combo()
            if self.accounts:
                self.current_account_index = 0
                self.current_account_data = self.accounts[0]["data"]
                self._save_account_settings()

    def open_edit_account(self):
        if self.game_data is None:
            self.show_error(get_text("error_data_not_loaded", self.current_language))
            return

        if self.current_account_data is None:
            self.show_error(get_text("error_no_account_selected", self.current_language))
            return

        if self.current_account_index < 0 or self.current_account_index >= len(self.accounts):
            self.show_error(get_text("error_account_not_found", self.current_language))
            return

        editor = AccountEditor(
            parent=self,
            game_data=self.game_data,
            account_data=self.current_account_data,
            lang=self.current_language,
            accounts_dir=self.get_accounts_dir(),
            dark_theme=self.dark_theme
        )

        if editor.exec() == QDialog.DialogCode.Accepted:
            self.scan_accounts()
            self.update_accounts_combo()
            if self.current_account_index < len(self.accounts):
                self.on_account_selected(self.current_account_index)

    def open_add_progress(self):
        if self.current_account_data is None:
            self.show_error(get_text("error_no_account_selected", self.current_language))
            return

        if self.game_data is None:
            self.show_error(get_text("error_data_not_loaded", self.current_language))
            return

        editor = ProgressEditor(
            parent=self,
            game_data=self.game_data,
            account_data=self.current_account_data,
            lang=self.current_language,
            dark_theme=self.dark_theme
        )

        editor.progress_added.connect(self.on_progress_added)
        editor.progress_removed.connect(self.on_progress_removed)
        editor.exec()

    def on_progress_removed(self, progress_data):
        """Обработчик удаления прогресса"""
        self.scan_accounts()
        self.update_accounts_combo()
        if self.current_account_index < len(self.accounts):
            self.on_account_selected(self.current_account_index)

    def on_progress_added(self, progress_data):
        self.scan_accounts()
        self.update_accounts_combo()
        if self.current_account_index < len(self.accounts):
            self.on_account_selected(self.current_account_index)

    def open_statistics(self):
        """Открывает окно статистики"""
        if self.current_account_data is None:
            self.show_error(get_text("error_no_account_selected", self.current_language))
            return

        if self.game_data is None:
            self.show_error(get_text("error_data_not_loaded", self.current_language))
            return

        stats_window = StatisticsWindow(
            parent=self,
            game_data=self.game_data,
            account_data=self.current_account_data,
            lang=self.current_language,
            dark_theme=self.dark_theme
        )
        stats_window.exec()

    def open_analysis(self):
        """Открывает окно анализа наборов"""
        if self.current_account_data is None:
            self.show_error(get_text("error_no_account_selected", self.current_language))
            return

        if self.game_data is None:
            self.show_error(get_text("error_data_not_loaded", self.current_language))
            return

        analysis_window = AnalysisWindow(
            parent=self,
            game_data=self.game_data,
            account_data=self.current_account_data,
            lang=self.current_language,
            dark_theme=self.dark_theme
        )
        analysis_window.exec()

    def toggle_language(self):
        if self.current_language == "en":
            self.current_language = "ru"
        else:
            self.current_language = "en"

        global CURRENT_LANG
        CURRENT_LANG = self.current_language

        self.lang_btn.setText(self.current_language.upper())
        self.update_ui_texts()
        self._save_account_settings()

    def update_buttons_state(self):
        """Обновляет состояние кнопок в зависимости от наличия аккаунта"""
        has_account = self.current_account_data is not None

        self.btn_edit_account.setEnabled(has_account)
        if has_account:
            self.btn_edit_account.setToolTip("")
        else:
            self.btn_edit_account.setToolTip(
                get_text("tooltip_select_account_first", self.current_language)
            )

    def update_ui_texts(self):
        self.setWindowTitle(get_text("window_title", self.current_language))
        self.title_label.setText(get_text("app_title", self.current_language))
        self.refresh_btn.setToolTip(get_text("refresh_tooltip", self.current_language))
        self.open_folder_btn.setToolTip(get_text("open_folder_tooltip", self.current_language))
        self.update_center_buttons()
        self.update_buttons_state()

    def _save_account_settings(self):
        """Сохраняет текущие настройки (тему и язык) в файл аккаунта"""
        if self.current_account_data is None or self.current_account_index < 0:
            return

        self.current_account_data["theme"] = "dark" if self.dark_theme else "light"
        self.current_account_data["language"] = self.current_language

        if self.current_account_index < len(self.accounts):
            account = self.accounts[self.current_account_index]
            file_path = account["path"]

            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(self.current_account_data, f, ensure_ascii=False, indent=2)
                self.log(f"Настройки сохранены в {file_path}")
            except Exception as e:
                self.log(f"Ошибка сохранения настроек: {e}")

    def open_accounts_folder(self):
        accounts_dir = self.get_accounts_dir()
        if not os.path.exists(accounts_dir):
            try:
                os.makedirs(accounts_dir)
            except:
                self.show_message(get_text("error_folder_create", self.current_language))
                return
        try:
            os.startfile(accounts_dir)
        except:
            self.show_message(get_text("error_folder_fail", self.current_language))

    def _style_message_box(self, msg):
        """Применяет стиль к QMessageBox в зависимости от темы"""
        if not self.dark_theme:
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: #f0f0f0;
                }
                QMessageBox QLabel {
                    color: #333333;
                }
                QMessageBox QPushButton {
                    background-color: #f0f0f0;
                    color: #333333;
                    border: 1px solid #cccccc;
                    border-radius: 4px;
                    padding: 5px 15px;
                    min-width: 80px;
                }
                QMessageBox QPushButton:hover {
                    background-color: #e0e0e0;
                }
            """)
        else:
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: #1e1e1e;
                }
                QMessageBox QLabel {
                    color: #e0e0e0;
                }
                QMessageBox QPushButton {
                    background-color: #3d3d3d;
                    color: #e0e0e0;
                    border: 1px solid #555555;
                    border-radius: 4px;
                    padding: 5px 15px;
                    min-width: 80px;
                }
                QMessageBox QPushButton:hover {
                    background-color: #4d4d4d;
                }
            """)

    def show_message(self, text):
        """Показывает информационное сообщение без звука"""
        msg = QMessageBox(self)
        msg.setWindowTitle("Info" if self.current_language == "en" else "Информация")
        msg.setText(text)
        self._style_message_box(msg)
        msg.exec()

    def show_error(self, text):
        """Показывает сообщение об ошибке и закрывает приложение (если критическая)"""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Error" if self.current_language == "en" else "Ошибка")
        msg.setText(text)
        self._style_message_box(msg)
        msg.exec()

    def log(self, message):
        """Вывод отладочного сообщения"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"[{timestamp}] MainWindow: {message}")

    def close_app(self):
        self.close()

    def closeEvent(self, event):
        event.accept()


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = MainWindow()

    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app_icon.png")
    if os.path.exists(icon_path):
        window.setWindowIcon(QIcon(icon_path))
        app.setWindowIcon(QIcon(icon_path))

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
