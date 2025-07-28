import sys
import random
from PyQt5.QtWidgets import (
    QApplication, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QWidget, QGraphicsOpacityEffect
)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QRect, QEasingCurve
from PyQt5.QtGui import QFont, QColor, QPainter, QBrush, QIcon
from PyQt5.QtMultimedia import QSound


class ToggleSwitch(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setFixedSize(80, 36)
        self.setStyleSheet("background-color: transparent;")

    def paintEvent(self, event):
        radius = 18
        width = self.width()
        height = self.height()

        bg_color = QColor("#4cd137" if self.isChecked() else "#dcdde1")
        circle_color = QColor("#ffffff")

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(bg_color))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, width, height, radius, radius)

        x_pos = width - 34 if self.isChecked() else 2
        painter.setBrush(QBrush(circle_color))
        painter.drawEllipse(x_pos, 2, 32, 32)

        super().paintEvent(event)


class Pomodoro(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("THE ULTIMATE POMODORO")
        self.setGeometry(500, 200, 800, 400)
        self.setWindowIcon(QIcon("pomodoro-icon.png"))  # 👈 Added line
        self.theme = "light"
        self.initUI()

    def initUI(self):
        self.start_btn = QPushButton("Start", self)
        self.stop_btn = QPushButton("Stop", self)
        self.reset_btn = QPushButton("Reset", self)

        self.toggle_theme_btn = ToggleSwitch(self)
        self.toggle_theme_btn.clicked.connect(self.toggle_theme)
        self.theme_label = QLabel("🌗 Toggle Theme", self)
        self.theme_label.setAlignment(Qt.AlignCenter)

        self.time_label = QLabel("00:00", self)
        self.time_label.setAlignment(Qt.AlignCenter)

        self.mode_label = QLabel("Mode: Focus 🧠", self)
        self.mode_label.setObjectName("modeLabel")
        self.mode_label.setAlignment(Qt.AlignCenter)

        self.quote_label = QLabel("", self)
        self.quote_label.setAlignment(Qt.AlignCenter)
        self.quote_label.setObjectName("quoteLabel")

        hbox = QHBoxLayout()
        hbox.addWidget(self.start_btn)
        hbox.addWidget(self.stop_btn)
        hbox.addWidget(self.reset_btn)

        vbox = QVBoxLayout()
        vbox.addWidget(self.time_label)
        vbox.addLayout(hbox)
        vbox.addWidget(self.mode_label)
        vbox.addWidget(self.quote_label)

        theme_box = QVBoxLayout()
        theme_box.addWidget(self.toggle_theme_btn, alignment=Qt.AlignCenter)
        theme_box.addWidget(self.theme_label, alignment=Qt.AlignCenter)
        vbox.addLayout(theme_box)

        self.setLayout(vbox)

        self.start_btn.clicked.connect(self.start_timer)
        self.stop_btn.clicked.connect(self.stop_timer)
        self.reset_btn.clicked.connect(self.reset_timer)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        self.pomodoro_count = 0
        self.mode = "focus"
        self.timer_running = False

        self.durations = {
            "focus": 5,
            "short_break": 5 * 60,
            "long_break": 15 * 60
        }

        self.remaining_time = self.durations["focus"]
        self.time_label.setText(self.format_time(self.remaining_time))

        self.quotes = [
            "You’re crushing it 🚀",
            "Rest but never quit 💪",
            "Focus fuels success 🧠",
            "Keep going, champ 👑",
            "Breaks make brains sharper ✨",
            "One step closer to greatness 👟"
        ]

        self.apply_theme()

    def start_timer(self):
        if self.timer_running:
            return
        self.timer.start(1000)
        self.timer_running = True

    def stop_timer(self):
        self.timer.stop()
        self.timer_running = False

    def reset_timer(self):
        self.timer.stop()
        self.timer_running = False
        self.mode = "focus"
        self.remaining_time = self.durations[self.mode]
        self.time_label.setText(self.format_time(self.remaining_time))
        self.mode_label.setText("Mode: Focus 🧠")
        self.quote_label.setText("")

    def update_timer(self):
        self.remaining_time -= 1
        self.time_label.setText(self.format_time(self.remaining_time))

        if self.remaining_time <= 0:
            self.timer.stop()
            self.timer_running = False
            try:
                QSound.play("alarm.wav")
            except:
                pass
            self.show_quote()

            if self.mode == "focus":
                self.pomodoro_count += 1
                if self.pomodoro_count % 4 == 0:
                    self.switch_mode("long_break")
                else:
                    self.switch_mode("short_break")
            else:
                self.switch_mode("focus")

    def switch_mode(self, new_mode):
        self.mode = new_mode
        self.remaining_time = self.durations[new_mode]
        self.time_label.setText(self.format_time(self.remaining_time))

        if new_mode == "focus":
            self.mode_label.setText("Mode: Focus 🧠")
        elif new_mode == "short_break":
            self.mode_label.setText("Short Break 🎃💆‍♂️")
        else:
            self.mode_label.setText("Long Break 🍹💼")

        self.animate_mode_label()
        self.start_timer()

    def show_quote(self):
        quote = random.choice(self.quotes)
        self.quote_label.setText(quote)
        self.animate_fade_in(self.quote_label)

    def animate_mode_label(self):
        anim = QPropertyAnimation(self.mode_label, b"geometry")
        anim.setDuration(500)
        start_rect = self.mode_label.geometry()
        anim.setStartValue(QRect(start_rect.x(), start_rect.y() - 20, start_rect.width(), start_rect.height()))
        anim.setEndValue(start_rect)
        anim.setEasingCurve(QEasingCurve.OutBounce)
        anim.start()
        self.anim = anim

    def animate_fade_in(self, widget):
        opacity = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(opacity)
        self.fade_anim = QPropertyAnimation(opacity, b"opacity")
        self.fade_anim.setDuration(1000)
        self.fade_anim.setStartValue(0)
        self.fade_anim.setEndValue(1)
        self.fade_anim.start()

    def toggle_theme(self):
        self.theme = "dark" if self.toggle_theme_btn.isChecked() else "light"
        self.apply_theme()

    def apply_theme(self):
        if self.theme == "dark":
            self.setStyleSheet("""
                QWidget {
                    background-color: #0d0d0d;
                }
                QPushButton {
                    background-color: #5f27cd;
                    color: white;
                    font-size: 18px;
                    font-weight: 600;
                    padding: 12px 24px;
                    border-radius: 14px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #341f97;
                }
                QLabel {
                    font-size: 72px;
                    font-weight: bold;
                    color: #f1f1f1;
                }
                #modeLabel {
                    font-size: 42px;
                    font-weight: 600;
                    color: #ccc;
                    padding-top: 16px;
                }
                #quoteLabel {
                    font-size: 24px;
                    font-weight: 500;
                    color: #aaa;
                    padding-top: 10px;
                }
            """)
        else:
            self.setStyleSheet("""
                QWidget {
                    background-color: #f0f4f8;
                }
                QPushButton {
                    background-color: #3a86ff;
                    color: white;
                    font-size: 18px;
                    font-weight: 600;
                    padding: 12px 24px;
                    border-radius: 14px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #265dff;
                }
                QLabel {
                    font-size: 72px;
                    font-weight: bold;
                    color: #1a1a1a;
                }
                #modeLabel {
                    font-size: 42px;
                    font-weight: 600;
                    color: #333;
                    padding-top: 16px;
                }
                #quoteLabel {
                    font-size: 24px;
                    font-weight: 500;
                    color: #555;
                    padding-top: 10px;
                }
            """)

    def format_time(self, time):
        minutes, seconds = divmod(time, 60)
        return f"{minutes:02d}:{seconds:02d}"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Pomodoro()
    widget.show()
    sys.exit(app.exec_())
