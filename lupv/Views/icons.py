from PyQt5.QtWidgets import QApplication


def style(icon_name):
    style = QApplication.instance().style()
    return style.standardIcon(icon_name)
