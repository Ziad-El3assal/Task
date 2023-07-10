import sys
import re
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PySide2.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

# Function to parse the user-entered function and validate the input
def parse_function(expression):
    # Remove all spaces
    expression = expression.replace(" ", "")

    # Replace ^ with **
    expression = expression.replace("^", "**")
    return expression

# Custom Widget to display the Matplotlib figure
class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def plot_function(self, x, y):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(x, y)
        self.canvas.draw()

# Main Window
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Function Plotter")
        self.setGeometry(100, 100, 800, 600)

        # Create GUI elements
        self.function_label = QLabel("Function:")
        self.function_input = QLineEdit()
        self.min_label = QLabel("Min X:")
        self.min_input = QLineEdit()
        self.max_label = QLabel("Max X:")
        self.max_input = QLineEdit()
        self.plot_button = QPushButton("Plot")
        self.plot_button.clicked.connect(self.plot)

        self.status_bar = self.statusBar()

        self.plot_widget = MatplotlibWidget()

        # Main layout
        main_layout = QVBoxLayout()
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.function_label)
        input_layout.addWidget(self.function_input)
        input_layout.addWidget(self.min_label)
        input_layout.addWidget(self.min_input)
        input_layout.addWidget(self.max_label)
        input_layout.addWidget(self.max_input)
        input_layout.addWidget(self.plot_button)
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.plot_widget)
        
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def validate_inputs(self):
        # Validate user inputs for the function, min_x, and max_x
        function = self.function_input.text()
        min_x = self.min_input.text()
        max_x = self.max_input.text()

        if not function:
            self.show_error_message("Please enter a function.")
            return False

        if not min_x or not max_x:
            self.show_error_message("Please enter min and max values for x.")
            return False

        try:
            float(min_x)
            float(max_x)
        except ValueError:
            self.show_error_message("Invalid min or max value for x.")
            return False

        return True

    def show_error_message(self, message):
        # Display an error message box
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText(message)
        msg_box.setWindowTitle("Error")
        msg_box.exec_()

    def plot(self):
        # Perform the function plotting
        if not self.validate_inputs():
            return

        function = parse_function(self.function_input.text())
        if not function:
            self.show_error_message("Invalid function.")
            return

        min_x = float(self.min_input.text())
        max_x = float(self.max_input.text())

        if min_x >= max_x:
            self.show_error_message("Min X must be less than Max X.")
            return

        step = 0.1
        x = np.arange(min_x, max_x + step, step)
        y = eval(function)

        self.plot_widget.plot_function(x, y)
        self.status_bar.showMessage("Function plotted successfully.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
