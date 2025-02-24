#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Raul Gomez
Date: 2025-02-24
Description: 
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLineEdit, QFormLayout, QFrame)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

class NewtonCoolingGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Newton's Cooling Law Simulation")
        self.setGeometry(100, 100, 1000, 600)

        # Main layout
        main_layout = QHBoxLayout()

        # Left panel - Input fields
        left_panel = QVBoxLayout()

        # Instruction label
        instructions = QLabel("""This application models temperature change using Newton's Cooling Law.\n
Enter two measurements of time and temperature, along with the environment temperature.\n
Then specify a final time to predict the object's temperature at that moment.""")
        instructions.setWordWrap(True)
        left_panel.addWidget(instructions)

        # Add a divider (frame)
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)  # Horizontal line
        divider.setFrameShadow(QFrame.Shadow.Sunken)
        left_panel.addWidget(divider)

        # Input form
        form_layout = QFormLayout()
        self.first_time_input = QLineEdit()
        self.first_temperature_input = QLineEdit()
        self.second_time_input = QLineEdit()
        self.second_temperature_input = QLineEdit()
        self.environment_temperature_input = QLineEdit()
        self.final_time_input = QLineEdit()
        
        form_layout.addRow("First Time:", self.first_time_input)
        form_layout.addRow("First Temperature:", self.first_temperature_input)
        form_layout.addRow("Second Time:", self.second_time_input)
        form_layout.addRow("Second Temperature:", self.second_temperature_input)
        form_layout.addRow("Environment Temperature:", self.environment_temperature_input)
        form_layout.addRow("Final Time:", self.final_time_input)
        left_panel.addLayout(form_layout)
        
        # Submit button
        self.run_button = QPushButton("Run Simulation")
        self.run_button.clicked.connect(self.run_simulation)
        left_panel.addWidget(self.run_button)

        # Right panel - Animation
        self.figure, self.ax = plt.subplots(figsize=(5, 4))
        self.canvas = FigureCanvas(self.figure)
        right_panel = QVBoxLayout()
        right_panel.addWidget(self.canvas)
        
        # Add panels to main layout
        main_layout.addLayout(left_panel, 2)  # Left panel takes 2/3 of space
        main_layout.addLayout(right_panel, 3) # Right panel takes 3/3 of space
        self.setLayout(main_layout)

    def run_simulation(self):
        try:
            # Retrieve inputs
            first_time = float(self.first_time_input.text())
            first_temperature = float(self.first_temperature_input.text())
            second_time = float(self.second_time_input.text())
            second_temperature = float(self.second_temperature_input.text())
            environment_temperature = float(self.environment_temperature_input.text())
            final_time = float(self.final_time_input.text())
        except ValueError:
            return  # Invalid input, stop execution

        # Define Newton's Cooling function
        def newton_cooling_function(t):
            a = (second_temperature - environment_temperature) / (first_temperature - environment_temperature)
            C = first_temperature - environment_temperature
            return environment_temperature + C * np.power(a, (t - first_time) / (second_time - first_time))

        # Prepare data for animation
        time_data = np.linspace(first_time, final_time, 100)
        object_temperature_data = newton_cooling_function(time_data)
        environment_temperature_data = np.full(100, environment_temperature)

        self.ax.clear()
        self.ax.set_xlim(first_time, final_time)
        self.ax.set_ylim(min(environment_temperature, first_temperature) - 5,
                          max(environment_temperature, first_temperature) + 5)
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Temperature")
        self.ax.set_title("Newton's Cooling Law")

        # Initialize empty plots
        self.object_temperature_line, = self.ax.plot([], [], lw=2, label="Object Temperature")
        self.environment_temperature_line, = self.ax.plot([], [], lw=2, label="Environment Temperature")
        self.ax.legend()

        # Animation update function
        def update(frame):
            self.object_temperature_line.set_data(time_data[:frame], object_temperature_data[:frame])
            self.environment_temperature_line.set_data(time_data[:frame], environment_temperature_data[:frame])
            return self.object_temperature_line, self.environment_temperature_line

        # Run animation
        self.ani = animation.FuncAnimation(self.figure, update, frames=len(time_data), interval=50, blit=True)
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = NewtonCoolingGUI()
    ex.show()
    sys.exit(app.exec())

