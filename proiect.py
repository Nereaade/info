import tkinter as tk
from tkinter import messagebox
import random
import time
import threading

def reset_colors(length):
    return ["lightblue" for _ in range(length)]

def highlight(indices, length, highlight_color="red", default_color="white"):
    return [highlight_color if i in indices else default_color for i in range(length)]

def draw_bars(canvas, arr, colors):
    canvas.delete("all")
    bar_width = canvas.winfo_width() // len(arr)
    for i, val in enumerate(arr):
        canvas.create_rectangle(i * bar_width, canvas.winfo_height() - val,
                                (i + 1) * bar_width, canvas.winfo_height(), fill=colors[i])
    canvas.update_idletasks()

def bubble_sort(array, draw_bars, speed, stop_event):
    n = len(array)
    i = 0
    j = 0
    while i < n:
        if stop_event.is_set():  # Check if stop is requested
            return i, j
        while j < n - i - 1:
            if stop_event.is_set():
                return i, j
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
                draw_bars(array, highlight([j, j + 1], n))  # Highlight comparisons
                time.sleep(speed)
            j += 1
        i += 1
        j = 0
        draw_bars(array, reset_colors(n), speed)
    return -1, -1  # Sorting finished

def insertion_sort(array, draw_bars, speed, stop_event):
    i = 1
    while i < len(array):
        if stop_event.is_set():
            return i
        key = array[i]
        j = i - 1
        while j >= 0 and key < array[j]:
            if stop_event.is_set():
                return i
            array[j + 1] = array[j]
            j -= 1
            draw_bars(array, highlight([j + 1], len(array)))  # Highlight movement
            time.sleep(speed)
        array[j + 1] = key
        i += 1
    return -1  # Sorting finished

def selection_sort(array, draw_bars, speed, stop_event):
    n = len(array)
    i = 0
    while i < n:
        if stop_event.is_set():
            return i
        min_idx = i
        for j in range(i + 1, n):
            if stop_event.is_set():
                return i
            if array[j] < array[min_idx]:
                min_idx = j
        array[i], array[min_idx] = array[min_idx], array[i]
        draw_bars(array, highlight([i, min_idx], n))  # Highlight swapping
        time.sleep(speed)
        i += 1
    return -1  # Sorting finished

def stop_sorting():
    global sorting, stop_event
    sorting = False
    stop_event.set()  # Signal the sorting thread to stop

def start_sorting():
    global sorting, stop_event
    if sorting:
        return
    sorting = True
    stop_event.clear()  # Clear stop event for new sorting
    selected_algorithm = algorithm_var.get()

    # Start the sorting in a new thread
    threading.Thread(target=run_sorting, args=(selected_algorithm, stop_event)).start()

def run_sorting(selected_algorithm, stop_event):
    if selected_algorithm == "Bubble Sort":
        bubble_sort(array, lambda arr, colors, speed=speed_slider.get(): draw_bars(canvas, arr, colors), speed_slider.get(), stop_event)
    elif selected_algorithm == "Insertion Sort":
        insertion_sort(array, lambda arr, colors, speed=speed_slider.get(): draw_bars(canvas, arr, colors), speed_slider.get(), stop_event)
    elif selected_algorithm == "Selection Sort":
        selection_sort(array, lambda arr, colors, speed=speed_slider.get(): draw_bars(canvas, arr, colors), speed_slider.get(), stop_event)

    # Notify when sorting is complete
    messagebox.showinfo("Sorting Complete", f"{selected_algorithm} finished sorting!")

def resume_sorting():
    global sorting, stop_event
    if sorting:
        return
    sorting = True
    stop_event.clear()  # Clear stop event for new sorting
    selected_algorithm = algorithm_var.get()

    # Start the sorting in a new thread
    threading.Thread(target=run_sorting, args=(selected_algorithm, stop_event)).start()

def reset():
    global array
    generate_random_sequence()

def generate_random_sequence():
    global array
    root.update()
    canvas_height = canvas.winfo_height()
    if canvas_height < 20:
        messagebox.showerror("Error", "Canvas height too small!")
        return
    array = [random.randint(10, canvas_height - 10) for _ in range(num_elements.get())]
    draw_bars(canvas, array, reset_colors(len(array)))

def setup_ui():
    root = tk.Tk()
    root.geometry("800x600")
    root.title("Sorting Visualizer")

    canvas = tk.Canvas(root, width=800, height=400, bg="black")
    canvas.pack()

    return root, canvas

root, canvas = setup_ui()

algorithm_var = tk.StringVar(value="Bubble Sort")
algorithms = ["Bubble Sort", "Insertion Sort", "Selection Sort"]
algorithm_menu = tk.OptionMenu(root, algorithm_var, *algorithms)
algorithm_menu.pack()

num_elements = tk.IntVar(value=50)
num_elements_slider = tk.Scale(root, from_=5, to_=100, orient="horizontal", label="Number of Elements", variable=num_elements)
num_elements_slider.pack()

speed_slider = tk.DoubleVar(value=0.1)
speed_slider_widget = tk.Scale(root, from_=0.01, to_=1, orient="horizontal", label="Animation Speed", resolution=0.01, variable=speed_slider)
speed_slider_widget.pack()

start_button = tk.Button(root, text="START", command=start_sorting)
start_button.pack()

stop_button = tk.Button(root, text="STOP", command=stop_sorting)
stop_button.pack()

resume_button = tk.Button(root, text="RESUME", command=resume_sorting)
resume_button.pack()

reset_button = tk.Button(root, text="RESET", command=reset)
reset_button.pack()

random_button = tk.Button(root, text="Generate Random Sequence", command=generate_random_sequence)
random_button.pack()

exit_button = tk.Button(root, text="Exit", command=root.destroy)
exit_button.pack()

array = []
sorting = False
stop_event = threading.Event()  # Event to signal stopping sorting

generate_random_sequence()
root.mainloop()
