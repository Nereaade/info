import tkinter as tk
from tkinter import messagebox
import random
import time

def bubble_sort(arr, draw_bars, speed):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                draw_bars(arr, ["red" if x == j or x == j+1 else "white" for x in range(len(arr))], speed)
        draw_bars(arr, ["lightblue" for _ in range(len(arr))], speed)

def insertion_sort(arr, draw_bars, speed):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
        draw_bars(arr, ["red" if x == j else "white" for x in range(len(arr))], speed)
    draw_bars(arr, ["lightblue" for _ in range(len(arr))], speed)

def selection_sort(arr, draw_bars, speed):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        draw_bars(arr, ["red" if x == i or x == min_idx else "white" for x in range(len(arr))], speed)
    draw_bars(arr, ["lightblue" for _ in range(len(arr))], speed)

def draw_bars(arr, colors, speed):
    canvas.delete("all")
    bar_width = width // len(arr)
    for i, val in enumerate(arr):
        canvas.create_rectangle(i * bar_width, height - val, (i + 1) * bar_width, height, fill=colors[i])
    root.update()
    time.sleep(speed)

def generate_random_sequence():
    global array
    array = [random.randint(10, height-10) for _ in range(num_elements.get())]
    draw_bars(array, ["lightblue" for _ in range(len(array))], speed_slider.get())

def reset():
    global array
    array = [random.randint(10, height-10) for _ in range(num_elements.get())]
    draw_bars(array, ["lightblue" for _ in range(len(array))], speed_slider.get())

def start_sorting():
    global sorting
    if not sorting:
        sorting = True
        selected_algorithm = algorithm_var.get()
        if selected_algorithm == "Bubble Sort":
            bubble_sort(array, draw_bars, speed_slider.get())
        elif selected_algorithm == "Insertion Sort":
            insertion_sort(array, draw_bars, speed_slider.get())
        elif selected_algorithm == "Selection Sort":
            selection_sort(array, draw_bars, speed_slider.get())
        sorting = False

root = tk.Tk()
root.geometry("800x600")
root.title("Proiect Sortare")

width = 800
height = 400
canvas = tk.Canvas(root, width=width, height=height, bg="black")
canvas.pack()

algorithm_var = tk.StringVar(value="Bubble Sort")
algorithms = ["Bubble Sort", "Insertion Sort", "Selection Sort"]
algorithm_menu = tk.OptionMenu(root, algorithm_var, *algorithms)
algorithm_menu.pack()

num_elements = tk.IntVar(value=50)
num_elements_slider = tk.Scale(root, from_=5, to_=100, orient="horizontal", label="Numer elements", variable=num_elements)
num_elements_slider.pack()

speed_slider = tk.DoubleVar(value=0.1)
speed_slider_widget = tk.Scale(root, from_=0.01, to_=1, orient="horizontal", label="Animation speed", resolution=0.01, variable=speed_slider)
speed_slider_widget.pack()

start_button = tk.Button(root, text="START", command=start_sorting)
start_button.pack()

reset_button = tk.Button(root, text="STOP", command=reset)
reset_button.pack()

random_button = tk.Button(root, text="Generează aleatoriu", command=generate_random_sequence)
random_button.pack()

array = [random.randint(10, height-10) for _ in range(num_elements.get())]
sorting = False

root.mainloop()