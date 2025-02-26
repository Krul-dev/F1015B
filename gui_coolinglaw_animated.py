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
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout, QFormLayout, QFrame
)
from PyQt6.QtGui import QDoubleValidator
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.animation import FuncAnimation


class NewtonCoolingGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Newton's Cooling Law Model")
        self.setGeometry(100, 100, 1200, 600)

        # Main Layout
        main_layout = QHBoxLayout()

        # Left panel - Instruction and Input Fields
        left_panel = QVBoxLayout()

        # Instruction Label
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
        self.inputs = {}
        input_labels = [
            "First Time:", "First Temperature:", "Second Time:", 
            "Second Temperature:", "Environment Temperature:", "Final Time:"
        ]
        
        for label, default_value in zip(input_labels, ["0", "100", "5", "80", "25", "20"]):
            lbl = QLabel(label, self)
            form_layout.addRow(lbl)
            line_edit = QLineEdit(self)
            line_edit.setValidator(QDoubleValidator())  # Only allow numeric input
            line_edit.setText(default_value)  # Set default value
            form_layout.addRow(line_edit)
            self.inputs[label] = line_edit

        # Add form layout to left panel
        left_panel.addLayout(form_layout)

        # Compute Button
        self.compute_button = QPushButton("Compute", self)
        self.compute_button.clicked.connect(self.compute_temperature)
        left_panel.addWidget(self.compute_button)

        # Result Display
        self.result_label = QLabel("Temperature at final time: ", self)
        left_panel.addWidget(self.result_label)

        self.result2_label = QLabel("Cooling constant: ", self)
        left_panel.addWidget(self.result2_label)



        # Right panel - Animation
        self.figure, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvas(self.figure)
        right_panel = QVBoxLayout()
        right_panel.addWidget(self.canvas)

        # Add panels to main layout
        main_layout.addLayout(left_panel, 2)  # Left panel takes 2/3 of space
        main_layout.addLayout(right_panel, 3) # Right panel takes 3/3 of space
        self.setLayout(main_layout)

        # To keep track of the current animation object
        self.ani = None

        # Initialize the animation 
        self.compute_temperature()

    def compute_temperature(self):
        try:
            first_time = float(self.inputs["First Time:"].text())
            first_temperature = float(self.inputs["First Temperature:"].text())
            second_time = float(self.inputs["Second Time:"].text())
            second_temperature = float(self.inputs["Second Temperature:"].text())
            environment_temperature = float(self.inputs["Environment Temperature:"].text())
            final_time = float(self.inputs["Final Time:"].text())

            if second_time <= first_time:
                raise ValueError("Second time must be greater than first time.")
            if first_temperature == second_temperature:
                raise ValueError("First and second temperature must be different.")
            if final_time <= second_time:
                raise ValueError("Final time must be greater than second time.")
            if (first_temperature<second_temperature) and (environment_temperature<=second_temperature):
                raise ValueError("Temperature was increasing, so the environment temperature should be larger than the second temperature measured.")
            if (first_temperature>second_temperature) and (environment_temperature>=second_temperature):
                raise ValueError("Temperature was decreasing, so the environment temperature should be smaller than the second temperature measured.")



            # Compute Temperature at Final Time
            self.newton_cooling_function = self.newton_cooling_law(
                first_time, first_temperature, second_time, second_temperature, environment_temperature
            )
            final_temp = self.newton_cooling_function(final_time)

            initial_deviation = first_temperature - environment_temperature 
            cooling_ration = (second_temperature - environment_temperature) / initial_deviation 
            cooling_constant = -np.log(cooling_ration) / (second_time - first_time)

            self.result_label.setText(f"Temperature at final time: {final_temp:.2f}")
            self.result2_label.setText(f"Cooling constant: {cooling_constant:.2f}")

            # Stop the previous animation (if any) before starting a new one
            if self.ani is not None:
                self.ani.event_source.stop()  # Stop the animation
                self.ax.clear()  # Clear the previous axes

            # Start new animation
            self.animate_temperature_change(
                first_time, first_temperature, second_time, second_temperature, environment_temperature, final_time
 
            )

        except ValueError as e:
            QMessageBox.critical(self, "Input Error", str(e))

    def newton_cooling_law(self, first_time, first_temperature, second_time, second_temperature, environment_temperature):
        def newton_cooling_function(t):
            a = (second_temperature - environment_temperature) / (first_temperature - environment_temperature)
            C = first_temperature - environment_temperature
            return environment_temperature + C * np.power(a, (t - first_time) / (second_time - first_time))

        return newton_cooling_function

    def animate_temperature_change(self, first_time, first_temperature, second_time, second_temperature,environment_temperature, final_time):
        self.ax.clear()

        self.time_data = np.linspace(first_time, final_time, 100)
        self.object_temperature_data = self.newton_cooling_function(self.time_data)
        self.environment_temperature_data = np.full(100, environment_temperature)

        self.object_temperature_line, = self.ax.plot([], [], lw=2, label="Object Temperature")
        self.environment_temperature_line, = self.ax.plot([], [], lw=2, label="Environment Temperature")

        # Set axis limits
        time_interval = final_time - first_time
        temperature_interval = abs(first_temperature - environment_temperature)
        self.ax.set_xlim(first_time - 0.1 * time_interval, final_time + 0.1 * time_interval)
        self.ax.set_ylim(min(environment_temperature, first_temperature) - 0.1 * temperature_interval, 
                         max(environment_temperature, first_temperature) + 0.1 * temperature_interval)

        # Labels & Title
        self.ax.set_xlabel("Time",labelpad=15)
        self.ax.set_ylabel("Temperature",labelpad=10)
        self.ax.set_title("Newton's Cooling Law Simulation")

        if first_temperature>second_temperature:
            location='upper right'
        else:
            location='lower right'

        # Set legend
        self.ax.legend(
        frameon=True,
        fancybox=False,
        loc=location,
        labelspacing=1.2)


        # Matplotlib Animation
        self.ani = FuncAnimation(self.figure, self.update_animation, frames=len(self.time_data), interval=50, blit=True)

        # Redraw canvas
        self.canvas.draw()

    def update_animation(self, frame):
        self.object_temperature_line.set_data(self.time_data[:frame], self.object_temperature_data[:frame]) 
        self.environment_temperature_line.set_data(self.time_data[:frame], self.environment_temperature_data[:frame])  
        return self.object_temperature_line, self.environment_temperature_line


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NewtonCoolingGUI()
    window.show()
    sys.exit(app.exec())

