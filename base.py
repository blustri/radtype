from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QTextEdit, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCharFormat, QBrush, QColor, QPalette
from words import generate, wordsPerMinute, rawWPM
import sys, time

# Base window
class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("radtype")
        self.setFixedSize(512,512)
        
# Palette (Dark mode)
class Palette(QPalette):
    def __init__(self):
        super().__init__()
        self.setColor(QPalette.Window, QColor(53, 53, 53))
        self.setColor(QPalette.WindowText, Qt.white)
        self.setColor(QPalette.Base, QColor(25, 25, 25))
        self.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        self.setColor(QPalette.ToolTipBase, Qt.white)
        self.setColor(QPalette.ToolTipText, Qt.white)
        self.setColor(QPalette.Text, Qt.white)
        self.setColor(QPalette.Button, QColor(53, 53, 53))
        self.setColor(QPalette.ButtonText, Qt.white)
        self.setColor(QPalette.BrightText, Qt.red)
        self.setColor(QPalette.Link, QColor(42, 130, 218))
        self.setColor(QPalette.Highlight, QColor(42, 130, 218))
        self.setColor(QPalette.HighlightedText, Qt.black)

# Text box
class textParagraph(QTextEdit):
    def __init__(self, parent):
        super().__init__(parent)
        self.parentWidget = parent
        # Font settings #
        font = self.font()
        font.setPointSize(24)
        font.setFamily("Roboto Medium")
        self.setFont(font)
        self.setStyleSheet("color: darkgray")
        # Text settings #
        self.setReadOnly(False)
        self.setTextInteractionFlags(Qt.TextSelectableByKeyboard)
        # Attributes #
        self.cursorPos = self.textCursor()
        self.startTest()
        self.endPos = self.endCheck()
        self.currentPos = 0
        # Global variables #
        self.testDurationSecs = "0" # Store test duration
        self.testRunning = False
        self.wpmRaw = "0"
        self.wpmCorrect = "0"
# Mostly logic
    def startTest(self):
        # Random words display
        wordsGen = generate(50)
        strings = " ".join(wordsGen)
        rawStrings = "".join(wordsGen)
        # Raw amount of characters
        self.rawLength = len(rawStrings)
        # Amount of correct words
        self.length = len(wordsGen)
        ## print(rawLength) -- used to debug
        self.setPlainText(strings)
        self.endPos = self.endCheck()
        self.currentPos = 0
        self.setTextInteractionFlags(Qt.TextSelectableByKeyboard)
        # Default colors
        textFormat = QTextCharFormat()
        self.cursorPos.select(3)
        textFormat.setForeground(QColor("darkgray"))
        self.cursorPos.mergeCharFormat(textFormat)
        self.mergeCurrentCharFormat(textFormat)
        self.cursorPos.clearSelection()
        self.cursorPos.movePosition(4, 0)

    def endCheck(self):
        tempCursor = self.textCursor()
        tempCursor.movePosition(15, 0)
        endPosition = tempCursor.position()
        tempCursor.movePosition(4, 0)
        return endPosition
        
    # Make keypress move the cursor
    def moveOnKeyPress(self, mode, anchorMode):
        print(self.endPos)
        self.cursorPos.movePosition(mode, anchorMode)
        self.setTextCursor(self.cursorPos)

    # Compare keypress with current letter under cursor to determine color
    def compareLetter(self, currentLetter, keyPressed):
        # Comparison logic
        if currentLetter == keyPressed:
            return QColor(124, 252, 0)
        else:
            return QColor(255, 0, 17)

    # Keypress handling
    def keyPressEvent(self, e):
        print(e.text())
        if not self.testRunning:
            # Start counter
            self.start_time = time.perf_counter()
            self.testRunning = True
        # Stores current letter under cursor
        tempCursor = self.textCursor()
        tempCursor.movePosition(17, 1)
        currentLetter = tempCursor.selectedText()
        tempCursor.movePosition(7, 1)
        tempCursor.clearSelection()
        # Storing each letter pressed in a temporary variable
        keyPressed = e.text()
        # Compares and stores color based on comparison result
        colorResult = self.compareLetter(currentLetter, keyPressed)
        textFormat = QTextCharFormat()       
        # Handles backspace (moves left)
        if e.key() == Qt.Key_Backspace:
            if self.currentPos == 0 or self.currentPos == self.endPos:
                return
            else:
                tempCursor.movePosition(7, 1)
                textFormat.setForeground(QColor("darkgray"))
                tempCursor.mergeCharFormat(textFormat)
                self.mergeCurrentCharFormat(textFormat)
                tempCursor.clearSelection()
                self.moveOnKeyPress(7, 0)
                self.currentPos = self.currentPos - 1
                print(self.currentPos)
        # Handles special key (do nothing)
        elif e.text() == "":
            return
        # Handles every other key (moves right)
        else:
            tempCursor.movePosition(17, 1)
            textFormat.setForeground(colorResult)
            tempCursor.mergeCharFormat(textFormat)
            self.mergeCurrentCharFormat(textFormat)
            tempCursor.clearSelection()
            self.moveOnKeyPress(17, 0)
            self.currentPos = self.currentPos + 1
            print(self.currentPos)
            print(self.cursorPos.atBlockEnd())
            # End reached state
            if self.cursorPos.atBlockEnd():
                self.setTextInteractionFlags(Qt.NoTextInteraction)
                self.clearFocus()
                # Updating the timer, calculate WPM (Raw and correct)
                self.end_time = time.perf_counter()
                self.testDurationSecs = (self.end_time - self.start_time)
                self.testDurationMins = self.testDurationSecs / 60
                print(f"Test finished in: {self.testDurationSecs:.1f} seconds")
                self.wpmRaw = rawWPM(self.testDurationMins, self.rawLength)
                self.parentWidget.updateDisplay()

# Label
class Label(QLabel):
    def __init__(self):
        super().__init__()
        # Font settings #
        font = self.font()
        font.setPointSize(18)
        font.setFamily("Roboto Light")
        self.setFont(font)

# GUI Layout
class Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.textBox = textParagraph(self)
        testDuration = self.textBox.testDurationSecs
        wpmRaw = self.textBox.wpmRaw
        # wpmCorrect = self.textBox.wpmCorrect -- TODO
        self.buttonStart = QPushButton("Restart")
        self.buttonStart.clicked.connect(self.randomWords)
        self.timeDisplay = Label()
        self.wpmDisplay = Label()
        self.timeDisplay.setText(f"Time: {testDuration}")
        self.wpmDisplay.setText(f"Raw: {wpmRaw}")
        # Layouts
        vLayout = QVBoxLayout(self)
        hLayout = QHBoxLayout(self)
        # Adding widgets to layout
        vLayout.addWidget(self.textBox)
        vLayout.addLayout(hLayout)
        hLayout.addStretch()
        hLayout.addWidget(self.wpmDisplay)
        hLayout.addStretch()
        hLayout.addWidget(self.timeDisplay)
        hLayout.addStretch()
        vLayout.addWidget(self.buttonStart)
    # Restart button method
    def randomWords(self):
        self.textBox.startTest()
        self.textBox.setFocus()
    # Updating the label text display method
    def updateDisplay(self):
        self.wpmDisplay.setText(f"Raw: {self.textBox.wpmRaw:.0f}")
        self.timeDisplay.setText(f"Time: {self.textBox.testDurationSecs:.1f}")
