from base import Main, Widget, Palette
import sys
from PyQt5.QtWidgets import QApplication

# App exec
dark_mode = Palette()
app = QApplication(sys.argv)
app.setStyle("Fusion")
app.setPalette(dark_mode)
baseGUI = Main()
parentWidget = Widget()
baseGUI.setCentralWidget(parentWidget)
baseGUI.show()
app.exec()