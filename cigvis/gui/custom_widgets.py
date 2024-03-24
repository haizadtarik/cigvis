# Copyright (c) 2023 Jintao Li.
# Computational and Interpretation Group (CIG),
# University of Science and Technology of China (USTC).
# All rights reserved.
"""
Some custom widgets
"""
from typing import List
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore, QtGui
import numpy as np

CANVAS_SIZE = (800, 600)  # (width, height)

INT_validator = QtCore.QRegExp(r"^[1-9][0-9]*$")
FLOAT_validator = QtCore.QRegExp(r"[-+]?[0-9]*\.?[0-9]+")


class EditableComboBox(qtw.QComboBox):
    changed = QtCore.pyqtSignal(str)  # 自定义的信号

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.activated.connect(self.on_changed)
        self.setEditable(True)  # 允许手动输入
        self.setInsertPolicy(qtw.QComboBox.NoInsert)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            self.changed.emit(self.currentText())  # 当按下Enter键时，发出自定义信号
        else:
            super().keyPressEvent(event)

    def on_changed(self):
        self.changed.emit(self.currentText())


class MyQSpinBox(qtw.QSpinBox):
    changed = QtCore.pyqtSignal(int)

    def stepBy(self, steps):
        super().stepBy(steps)
        self.changed.emit(self.value())

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            self.changed.emit(self.value())
        elif event.key() == QtCore.Qt.Key_Up:
            if self.value() >= self.maximum():
                return
            value = self.value() + 1
            self.setValue(value)
            self.changed.emit(value)
        elif event.key() == QtCore.Qt.Key_Down:
            if self.value() <= self.minimum():
                return
            value = self.value() - 1
            self.setValue(value)
            self.changed.emit(value)
        else:
            super().keyPressEvent(event)


class MyQDoubleSpinBox(qtw.QDoubleSpinBox):
    changed = QtCore.pyqtSignal(float)

    def stepBy(self, steps):
        super().stepBy(steps)
        self.changed.emit(self.value())

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            self.changed.emit(self.value())
        else:
            super().keyPressEvent(event)


class MyQLineEdit(qtw.QLineEdit):

    def setTextAndEmit(self, text):
        self.setText(text)
        # 手动调用处理函数
        self.editingFinished.emit()


class UnpickRadioButton(qtw.QRadioButton):

    def __init__(self, title, parent=None):
        super(UnpickRadioButton, self).__init__(title, parent)

    def mousePressEvent(self, event):
        # 重写鼠标按下事件，但不调用基类的事件处理，阻止选中状态的改变
        pass

    def mouseReleaseEvent(self, event):
        # 重写鼠标释放事件，同样不调用基类的事件处理
        pass


class RadioButtonPanel(qtw.QWidget):

    def __init__(self, names, hori=True, parent=None):
        super(RadioButtonPanel, self).__init__(parent)
        self.names = names
        self.radioButtons = []

        # 选择布局方向
        self.layout = qtw.QHBoxLayout(self) if hori else qtw.QVBoxLayout(self)

        # 创建并添加单选按钮到布局
        for name in names:
            radioButton = UnpickRadioButton(name)
            self.layout.addWidget(radioButton)
            self.radioButtons.append(radioButton)
            # 连接单选按钮的信号
            radioButton.toggled.connect(self.onRadioButtonChanged)

        # 设置第一个单选按钮为默认选中状态
        self.radioButtons[0].setChecked(True)
        self.selected = self.names[0]

    def onRadioButtonChanged(self):
        # 当单选按钮的状态改变时触发
        radioButton = self.sender()
        if radioButton.isChecked():
            self.selected = radioButton.text()
            for rad in self.radioButtons:
                if rad != radioButton:
                    rad.setChecked(False)

    def getCurrentSelection(self):
        return self.selected


class ToggleButton(qtw.QPushButton):

    def __init__(self, title=None, usesfix=False, exclu=True, parent=None):
        if usesfix:
            title = title + " OFF"
        self.usesfix = usesfix
        super().__init__(title, parent)
        self.title = title
        self.exclu = exclu
        self.setCheckable(True)
        self.toggled.connect(self.onToggle)

    def onToggle(self, checked):
        if self.exclu:
            parent = self.parent()
            if parent:
                parent.updateToggleState(self, checked)

        if not self.usesfix:
            return
        if checked:
            self.setText(self.title + " ON")
        else:
            self.setText(self.title + " OFF")


class RectP:

    def __init__(self,
                 x0: float = None,
                 y0: float = None,
                 x1: float = None,
                 y1: float = None) -> None:
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

    def add_p0(self, x0, y0):
        self.x0 = x0
        self.y0 = y0

    def add_p1(self, x1, y1):
        self.x1 = x1
        self.y1 = y1

    def add_p0event(self, event):
        self.x0 = event.xdata
        self.y0 = event.ydata

    def add_p1event(self, event):
        self.x1 = event.xdata
        self.y1 = event.ydata

    @classmethod
    def from_points(cls, p0: List, p1: List):
        # p1, p2可以是任何有x和y属性的对象
        return cls(p0[0], p0[1], p1[0], p1[1])

    @classmethod
    def from_events(cls, e0, e1):
        return cls(e0.xdata, e0.ydata, e1.xdata, e1.ydata)

    def to_start_size(self):
        width = abs(self.x1 - self.x0)
        height = abs(self.y1 - self.y0)
        return [self.x0, self.y0, width, height]

    def to_points(self):
        return [self.x0, self.y0, self.x1, self.y1]


class BaseWidget(qtw.QWidget):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

    def addwidgets(self, layout, widgets):
        for widget in widgets:
            layout.addWidget(widget)

    def addlayout(self, layout, sublayouts):
        for sublayout in sublayouts:
            layout.addLayout(sublayout)
