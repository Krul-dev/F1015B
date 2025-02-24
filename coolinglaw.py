#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Raul Gomez
Date: 2025-02-18
Description: 
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation




def get_user_input():
    print("\nThis application will help you model the change in temeperature of a body using Newton's cooling law.\nTo create this model, we will need two measurements of time and temperature, and the temperature of the medium.\nAfter that you will be asked for a final time and the model will show you the temperature of the body at that time.\nYou will also be shown an animation of the temperature change.\n")
    while True:
        try:
            first_time=float(input("Enter the time of the first measurement: "))
            break  # Exit the loop if the input is valid
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    while True:
        try:
            first_temperature=float(input("Enter the first temperature measurement: "))
            break  # Exit the loop if the input is valid
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    while True:
        try:
            second_time=float(input("Enter the time of the second measurement: "))
            if second_time<=first_time:
                print("Invalid input. The second time must be greater than the first time.")
                continue
            break  # Exit the loop if the input is valid
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    while True:
        try:
            second_temperature=float(input("Enter the second temperature measurement: "))
            if first_temperature==second_temperature:
                print("Temperature will remain constant. Please enter a different value.")
                continue
            break  # Exit the loop if the input is valid
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    while True:
        try:
            environment_temperature=float(input("Enter the temperature of the environment: "))
            if (first_temperature<second_temperature) and (environment_temperature<=second_temperature):
                print("Temperature was increasing, so the environment temperature should be larger than the second temperature measured.")
                continue
            if (first_temperature>second_temperature) and (environment_temperature>=second_temperature):
                print("Temperature was decreasing, so the environment temperature should be smaller than the second temperature measured.")
                continue
            break  # Exit the loop if the input is valid
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    while True:
        try:
            final_time=float(input("Enter the final time where you want to measure temperature: "))
            if final_time<=second_time:
                print("Invalid input. The final time must be greater than the second time.")
                continue
            break  # Exit the loop if the input is valid
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    return (first_time,first_temperature,second_time,second_temperature,environment_temperature,final_time) 


def newton_cooling_law(first_time,first_temperature,second_time,second_temperature,environment_temperature): 
    def newton_cooling_function(tiempo):
        t=tiempo
        a=(second_temperature - environment_temperature) / (first_temperature - environment_temperature)
        C=first_temperature - environment_temperature
        T_M=environment_temperature
        t1=first_time
        t2=second_time
        temperature = T_M + C*np.power(a, ( (t-t1)/(t2-t1) ) )
        return temperature

    return newton_cooling_function



(first_time,first_temperature,second_time,second_temperature,environment_temperature,final_time) = get_user_input()

newton_cooling_function=newton_cooling_law(first_time,first_temperature,second_time,second_temperature,environment_temperature)

print("\nThe temperature at time",final_time,"is",newton_cooling_function(final_time))

# Create figure and axis
fig, ax = plt.subplots(figsize=(14, 8))
time_data = np.linspace(first_time, final_time, 100)
object_temperature_data = newton_cooling_function(time_data)
environment_temperature_data=np.full(100,environment_temperature)
object_temperature_line, = ax.plot([], [], lw=2)  # Empty plot to start
environment_temperature_line, = ax.plot([], [], lw=2)  # Empty plot to start

time_interval=final_time-first_time
final_temperature=newton_cooling_function(final_time)

temperature_interval=np.abs(first_temperature-environment_temperature)
# Set axis limits
ax.set_xlim(first_time-time_interval*0.1, final_time + time_interval*0.1)
ax.set_ylim(np.minimum(environment_temperature,first_temperature)-0.1*temperature_interval, np.maximum(environment_temperature,first_temperature)+0.1*temperature_interval)


# Set axis labels
ax.set_xlabel('Time',labelpad=15)
ax.set_ylabel('Temperature',labelpad=15)



# Set title
ax.set_title('Modeling of temperature using Newton\'s Cooling Law',pad=20)

if first_temperature>second_temperature:
    location='upper right'
else:
    location='lower right'

# Set legend
ax.legend(['Object temperature', 'Environment temperature'],
          frameon=True,
          fancybox=False,
          loc=location,
      labelspacing=1.2)



# Function to update the animation
def update(frame):
    object_temperature_line.set_data(time_data[:frame], object_temperature_data[:frame])  # Reveal more of the curve gradually
    environment_temperature_line.set_data(time_data[:frame], environment_temperature_data[:frame])  # Reveal more of the curve gradually
    return object_temperature_line, environment_temperature_line

# Create animation
ani = animation.FuncAnimation(fig, update, frames=len(time_data), interval=50, blit=True)

plt.show()

