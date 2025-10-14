from PySide6.QtCore import Property, QEasingCurve, QPropertyAnimation, Qt
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QLabel


class LoadingSpinner(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(60, 60)
        self._angle = 0

        self._animation = QPropertyAnimation(self, b"angle")
        self._animation.setDuration(800)
        self._animation.setStartValue(0)
        self._animation.setEndValue(360)
        self._animation.setLoopCount(-1)
        self._animation.setEasingCurve(QEasingCurve.Type.Linear)

    @Property(int)
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value: int):
        self._angle = value
        self.update()

    def startAnimation(self):
        self._animation.start()

    def stopAnimation(self):
        self._animation.stop()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        pen = QPen(QColor("#2196F3"))
        pen.setWidth(4)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)

        rect = self.rect().adjusted(10, 10, -10, -10)
        start_angle = (self._angle - 60) * 16
        span_angle = 270 * 16

        painter.drawArc(rect, start_angle, span_angle)
