from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QPen, QBrush, QFont, QPainterPath
from PyQt5.QtCore import Qt, QPoint, QRect
import sys


class FirstTask(QWidget):
    def __init__(self, function):
        super().__init__()

        self.start = -20
        self.end = 20
        self.function = function

        self.function_upper_bound = 1000
        self.function_lower_bound = -1000

        self.init_ui()

    def init_ui(self):
        self.setGeometry(100, 100, 1000, 600)
        self.setWindowTitle('First task')
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)
        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.find_function_min_and_max()
        self.draw_axes(qp)
        self.draw_function(qp)
        qp.end()

    def cartesian_to_screen(self, x, y):
        return round((x - self.start) * self.geometry().width() / (self.end - self.start)), \
               round((y - self.ymax) * self.geometry().height() / (self.ymin - self.ymax))

    def screen_to_cartesian(self, xx, yy):
        return xx * (self.end - self.start) / self.geometry().width() + self.start, \
               yy * (self.ymin - self.ymax) / self.geometry().height() + self.ymax

    def draw_function(self, qp):
        qp.setPen(QPen(Qt.blue, 1, Qt.SolidLine))
        path = QPainterPath(QPoint(*self.cartesian_to_screen(self.start, self.function(self.start))))
        for xx in range(1, self.geometry().width()):
            x, _ = self.screen_to_cartesian(xx, 0)
            _, yy = self.cartesian_to_screen(0, self.function(x))
            path.lineTo(QPoint(xx, yy))
            path.moveTo(QPoint(xx, yy))
        qp.drawPath(path)

    def find_function_min_and_max(self):
        ymin = ymax = self.function(self.start)
        for xx in range(self.geometry().width()):
            x = xx * (self.end - self.start) / self.geometry().width() + self.start
            y = self.function(x)
            ymin = min(ymin, y)
            ymax = max(ymax, y)
        self.ymin = max(self.function_lower_bound, round(ymin))
        self.ymax = min(self.function_upper_bound, round(ymax))

    def draw_axes(self, qp):
        qp.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        xx0, yy0 = self.cartesian_to_screen(0, 0)
        qp.drawLine(xx0, 0, xx0, self.geometry().height())
        qp.drawLine(0, yy0, self.geometry().width(), yy0)
        self.draw_axes_notches(qp)

    def draw_axes_notches(self, qp):
        qp.setBrush(QBrush(Qt.SolidPattern))
        qp.setFont(QFont('Decorative', 7))
        step = max(1, round(self.screen_to_cartesian(32, 0)[0] - self.screen_to_cartesian(0, 0)[0]))
        for x in range(step, max(abs(self.start), abs(self.end)), step):
            xx_right, yy = self.cartesian_to_screen(x, 0)
            xx_left, yy = self.cartesian_to_screen(-x, 0)
            qp.drawLine(xx_right, yy - 2, xx_right, yy + 2)
            qp.drawLine(xx_left, yy - 2, xx_left, yy + 2)
            qp.drawText(QRect(xx_right - 10, yy + 10, 20, 20), Qt.AlignCenter, str(x))
            qp.drawText(QRect(xx_left - 10, yy + 10, 20, 20), Qt.AlignCenter, str(-x))


def foo(x):
    # return math.sin(x) * x ** 2
    return x**2
    # return x**3


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FirstTask(foo)
    sys.exit(app.exec_())

