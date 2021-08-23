import tkinter
from tkinter import ttk
import random
import time
import tkinter.messagebox


class SortingVisualizer:
    """
    Main GUI
    """

    def __init__(self, main):
        """
        Init GUI

        :param main: tkinter.Tk()
        """

        self.FINISHED_SORTING = False
        self.box_color = "#5555ff"

        ###### Basic Layout ######
        """_______________________________________
          |       Frame: Buttons and Labels       |
          |---------------------------------------|
          |                                       |
          |       Frame: Canvas + Scrollbar       |
          |                                       |
          |_______________________________________|
        """

        ### Init root
        self.main = main
        self.main.bind("<Key>", self._main_window_action)
        self.main.title("Sorting Algorithm Visualization")
        self.main.maxsize(1500, 600)
        self.main.config(bg="#000000")

        ### Icon
        icon_main = tkinter.PhotoImage(file="icons/icons8-ascending-sorting-48.png")
        self.main.iconphoto(False, icon_main)

        ### Frame: Canvas + Scrollbar
        self.lower_part = tkinter.Frame(self.main, bg="#ddddff")
        ### Bind/Unbind the mousewheel for scrolling
        self.lower_part.bind('<Enter>', self._bound_to_mousewheel)
        self.lower_part.bind('<Leave>', self._unbound_to_mousewheel)
        self.lower_part.grid(row=1, column=0, padx=10, pady=10)

        ### Control-panel
        self.control_panel = tkinter.Frame(self.main, width=1200, height=180, bg="#444444",
                                           highlightbackground="#ffffff", highlightthickness=2)
        self.control_panel.grid(row=0, column=0, padx=20, pady=10)


        ### Canvas
        self.canvas = tkinter.Canvas(self.lower_part, width=1100, height=380, bg="#ffffff",
                                     scrollregion=(0,0,2000,1000))
        self.canvas.grid(row=0, column=0, padx=10, pady=10)

        ###### Basic Layout End ######



        ###### Labels, Buttons, ... ######

        ### Label
        self.label_algorithm = tkinter.Label(self.control_panel, text="Algorithm", height=1,
                                             font=("italic", 13, "normal"), bg="#ddddff")
        self.label_algorithm.grid(row=0, column=0, sticky=tkinter.W, padx=(15,2), pady=5)

        ### Combobox to select algorithm from
        self.algorithm_selection = ttk.Combobox(self.control_panel, textvariable=tkinter.StringVar(),
                                                values=["Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort"],
                                                width=15, font=("italic", 13, "normal"))
        self.algorithm_selection.grid(row=0, column=1, padx=(2,15), pady=5)
        self.algorithm_selection.current(0)

        ### Seperator
        self.seperator1 = ttk.Separator(self.control_panel)
        self.seperator1.grid(row=0, column=2, sticky="ns")

        ### Label
        self.number_samples_label = tkinter.Label(self.control_panel, text="Number of elements",
                                                  height=1, font=("italic", 13, "normal"), bg="#ddddff")
        self.number_samples_label.grid(row=0, column=3, padx=(15,2), pady=5)

        ### Combobox to select the number of random elements
        self.number_samples = ttk.Combobox(self.control_panel, textvariable=tkinter.StringVar(),
                                           values=list(range(2, 11)), width=5, font=("italic", 13, "normal"))
        self.number_samples.grid(row=0, column=4, padx=(2,15), pady=5)
        self.number_samples.current(0)

        ### Seperator
        self.seperator1 = ttk.Separator(self.control_panel)
        self.seperator1.grid(row=0, column=5, sticky="ns")

        ### Label
        self.speed_label = tkinter.Label(self.control_panel, text="Sorting speed", font=("italic", 13, "normal"), bg="#ddddff")
        self.speed_label.grid(row=0, column=6, padx=(15,2), pady=5)

        ### Combobox to select sorting speed
        self.speed = ttk.Combobox(self.control_panel, textvariable=tkinter.StringVar(), values=["Slow", "Normal", "Fast"],
                                  width=10, font=("italic", 13, "normal"))
        self.speed.grid(row=0, column=7, padx=(2,15), pady=5)
        self.speed.current(0)

        ### Seperator
        self.seperator1 = ttk.Separator(self.control_panel)
        self.seperator1.grid(row=0, column=8, sticky="ns")

        ### Button to generate a sequence of random numbers
        self.button_generate = tkinter.Button(self.control_panel, command=self.setup_sorting, text="Generate numbers",
                                              font=("italic", 13, "normal"), pady=0)
        self.button_generate.bind("<Enter>", self._button_generate_enter)
        self.button_generate.bind("<Leave>", self._button_generate_leave)
        self.button_generate.grid(row=0, column=9, padx=(15,2), pady=5)

        ### Button to start sorting
        self.button_sort = tkinter.Button(self.control_panel, command=self.sort, text="Start sorting",
                                          font=("italic", 13, "normal"), pady=0)
        self.button_sort.bind("<Enter>", self._button_start_enter)
        self.button_sort.bind("<Leave>", self._button_start_leave)
        self.button_sort.grid(row=0, column=10, padx=(2,15), pady=5)

        ### Debug Button
        self.button_debug = tkinter.Button(self.control_panel, command=self.debug, text="DEBUG")
        #self.button_debug.grid(row=0, column=11, padx=5, pady=5)

        ### Make the Canvas scrollable
        ### Horizontal scrollbar
        self.hbar = tkinter.Scrollbar(self.lower_part, orient=tkinter.HORIZONTAL)
        self.hbar.grid(row=1, column=0)
        self.hbar.config(command=self.canvas.xview)
        self.canvas.config(xscrollcommand=self.hbar.set)

        ### Vertical scrollbar
        self.vbar = tkinter.Scrollbar(self.lower_part, orient=tkinter.VERTICAL)
        self.vbar.grid(row=0, column=1)
        self.vbar.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.vbar.set)

        ### Helper param
        self.new_boxes = list()


    ######### Event handling functions #########

    ### Quit GUI with q; Display help with h
    def _main_window_action(self, event):
        if event.char == 'q':
            self.main.quit()
        elif event.char == 'h':
            tkinter.messagebox.showinfo(title="Help", message="1. Select algorithm\n"
                                                              "2. Select number of elements\n"
                                                              "3. Select speed\n"
                                                              "4. Generate sequence\n"
                                                              "5. Start sorting")
    ### Change start-button color on <Enter>
    def _button_start_enter(self, event):
        self.button_sort.config(bg="#55ff55")

    ### Change start-button color on <Leave>
    def _button_start_leave(self, event):
        self.button_sort.config(bg="#ffffff")

    ### Change generate-button color on <Enter>
    def _button_generate_enter(self, event):
        self.button_generate.config(bg=self.box_color, font=("italic", 13, "normal"))

    ### Change generate-button color on <Leave>
    def _button_generate_leave(self, event):
        self.button_generate.config(bg="#ffffff", font=("italic", 13, "normal"))

    ### Enable scrolling canvas on <Enter>
    def _bound_to_mousewheel(self, event):
        self.canvas.bind("<MouseWheel>", self._on_vertical)
        self.canvas.bind('<Shift-MouseWheel>', self._on_horizontal)

    ### Disbale scrolling canvas on <Leave>
    def _unbound_to_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    ### Scroll vertical when using the MouseWheel
    def _on_vertical(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    ### Scroll horizontal when using Shift + MouseWheel
    def _on_horizontal(self, event):
        self.canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

    ######################################################################


    def setup_sorting(self):
        """
        This function generates a sequence of random numbers on the canvas depending on the chosen length.
        The function is called when clicking the "Generate" button.

        :return: None
        """

        ### Reset variable when generating a new sequence
        self.FINISHED_SORTING = False

        ### Check if the number of elements is not between 2 and 10
        ### If True: Show warning and set deafult value 10
        if ((n := int(self.number_samples.get())) > 10) or n < 2:
            tkinter.messagebox.showwarning(title="Warning", message=f"'{n}' is not a valid number of elements!")
            self.number_samples.set(str(10))
            return

        ### CLear the canvas
        self.canvas.delete("all")

        ### Parameters for boxes
        self.start_x = 200
        self.start_y = 100
        self.boxSize_x = 50
        self.boxSize_y = 50
        self.spacing = 25

        ### combobox.get() returns a string
        n = int(self.number_samples.get())

        x_tl = self.start_x
        y_tl = self.start_y
        x_br = self.start_x + self.boxSize_x
        y_br = self.start_y + self.boxSize_y

        self.boxes = list()

        ### Create multiple canvas objects in loop
        ### One "box" is a 3-tuple with: (value, box, text_box) ...
        ### ... where value is a generated random value, box and text_box are IDs to recognize the objects on the canvas
        for i in range(n):

            value = random.randint(0,100)
            box = self.canvas.create_rectangle(x_tl, y_tl, x_br, y_br, fill=self.box_color)
            text_box = self.canvas.create_text(x_tl + self.boxSize_x / 2, y_tl + self.boxSize_y / 2, text=value, font=("italic",15,"bold"))

            self.boxes.append((value, box, text_box))

            x_tl = x_tl + self.boxSize_x + self.spacing
            x_br = x_br + self.boxSize_x + self.spacing

        ### Set the number of comparisons back to 0
        self.comparison_label = self.canvas.create_text(100, 20, text="Number of comparisons:", font=("italic", 11, "normal"))
        self.comparison_number = self.canvas.create_text(200, 20, text="0", font=("italic", 11, "normal"))


    def swap(self, box_left, box_right, index_left, index_right):
        """
        This function swaps the position of two boxes.

        Box object: (Value, Rectangle-ID, Text-ID)
        :param box_left: Box object on the left
        :param box_right: Box object on the right
        :param index_left: Index left
        :param index_right: Index right
        :return: None
        """

        box1 = box_left
        box2 = box_right

        speed = self.get_speed()

        ### Get the coordinates of the rectangle
        box1_x_tl, box1_y_tl, box1_x_br, box1_y_br = self.canvas.coords(box1[1])
        box2_x_tl, box2_y_tl, box2_x_br, box2_y_br = self.canvas.coords(box2[1])

        ### Get the coordinates of the text
        text1_x_tl, text1_y_tl = self.canvas.coords(box1[2])
        text2_x_tl, text2_y_tl = self.canvas.coords(box2[2])

        ### Color the boxes red before being swapped
        self.canvas.itemconfig(box1[1], fill="#ee0000")
        self.canvas.itemconfig(box2[1], fill="#ee0000")
        ### An arrow showing the swap
        switch_arrow = self.canvas.create_line(box1_x_br, box1_y_br - self.boxSize_y/2, box2_x_tl, box2_y_tl + self.boxSize_y/2, arrow="both")
        self.canvas.update()

        ### Pause before the swap to help understanding the algorithm
        time.sleep(speed)

        ### Move each rectangle to the x position of the other; y remains unchanged
        self.canvas.move(box1[1], box2_x_tl - box1_x_tl, 0) ### Move the left box by +xy to the right
        self.canvas.move(box2[1], box1_x_tl - box2_x_tl, 0) ### Move the right box by -xy to the left

        ### Repeat for the text
        self.canvas.move(box1[2], text2_x_tl - text1_x_tl, 0)
        self.canvas.move(box2[2], text1_x_tl - text2_x_tl, 0)

        ### Pause
        time.sleep(speed)

        ### Change the colors back and remove the arrow
        self.canvas.itemconfig(box1[1], fill=self.box_color)
        self.canvas.itemconfig(box2[1], fill=self.box_color)
        self.canvas.delete(switch_arrow)
        self.canvas.update()

        ### Switch boxes in self.boxes to keep the right order
        self.boxes[index_left], self.boxes[index_right] = self.boxes[index_right], self.boxes[index_left]

        time.sleep(speed)


    def no_swap(self, box_left, box_right, index_left, index_right):
        """
        This function is called when two boxes should not switched according to the sorting algorithm.

        :param box_left: Box object on the left
        :param box_right: Box object on the right
        :param index_left: Index left
        :param index_right: Index right
        :return: None
        """

        speed = self.get_speed()

        ### Color the boxes green
        self.canvas.itemconfig(box_left[1], fill="#55cc55")
        self.canvas.itemconfig(box_right[1], fill="#55cc55")
        self.canvas.update()

        ### Pause
        time.sleep(speed)

        ### Color the boxes back to blue
        self.canvas.itemconfig(box_left[1], fill=self.box_color)
        self.canvas.itemconfig(box_right[1], fill=self.box_color)
        self.canvas.update()

        time.sleep(speed)

    def finished(self):
        """
        This function marks the end of the sorting algorithm by shortly coloring all boxes green in ascending order

        :return: None
        """

        ### Color boxes green for a short time in ascending order
        for box in self.boxes:
            ### Color green
            self.canvas.itemconfig(box[1], fill="#00ff00")
            self.canvas.update()
            ### Pause
            time.sleep(self.get_speed()/2)
            ### Color back
            self.canvas.itemconfig(box[1], fill=self.box_color)
            self.canvas.update()

        time.sleep(0.5)

        ### Color all boxes green to indicate the end
        for box in self.boxes:
            ### Color green
            self.canvas.itemconfig(box[1], fill="#00ff00")
            self.canvas.update()


        self.FINISHED_SORTING = True


    def copy(self):
        """
        This function creates a list with a copy of the existing boxes and moves them below the existing boxes
        Needed for MergeSort later on

        :return: List of newly created boxes
        """

        new_boxes = list()

        ### Create copies
        for box in self.boxes:

            box_x_tl, box_y_tl, box_x_br, box_y_br = self.canvas.coords(box[1])
            text_x_tl, text_y_tl = self.canvas.coords(box[2])

            new_box = self.canvas.create_rectangle(box_x_tl, box_y_tl, box_x_br, box_y_br, fill=self.box_color)
            new_text = self.canvas.create_text(text_x_tl, text_y_tl, text=box[0], font=("italic",15,"bold"))

            new_boxes.append((box[0], new_box, new_text))

        ### Move new boxes downwards
        for box in new_boxes:

            self.canvas.move(box[1], 0, 75)
            self.canvas.move(box[2], 0, 75)

        self.canvas.update()


        return new_boxes



    def split(self, boxes):
        """
        Helper function for MergeSort.
        Splits a given array of boxes into two, by moving one half to the left and the other half to the right.

        :param boxes: The given array of boxes
        :return: None
        """


        len_arr = len(boxes)
        mid = len_arr // 2

        if len_arr == 1:
            self.new_boxes.append(boxes)
            return

        for i in range(mid):
            self.canvas.move(boxes[i][1], -100 * (len_arr/10), 0)
            self.canvas.move(boxes[i][2], -100 * (len_arr/10), 0)

        for i in range(mid, len_arr):
            self.canvas.move(boxes[i][1], 100 * (len_arr/10), 0)
            self.canvas.move(boxes[i][2], 100 * (len_arr/10), 0)

        self.canvas.update()
        time.sleep(2)

        ###self.boxes = self.copy()
        ###self.split(self.boxes[:mid])
        ###self.split(self.boxes[mid:])


    def get_speed(self):
        """
        This function returns a time-value according to the given speed ["Slow": 1.5, "Normal": 1, "Fast": 0.5]
        :return: The time to pause in seconds
        """

        speed = self.speed.get()
        if speed == "Slow":
            return 1.5
        elif speed == "Normal":
            return 1
        elif speed == "Fast":
            return 0.5
        else:
            return 1


    def debug(self):
        """
        Function which executes test-code

        :return: None
        """

        #self.canvas.itemconfig(self.boxes[0][1], fill="#ff0000")
        self.copy()


    def update_counter(self):
        """
        This function updates the number of comparison variable.

        :return: None
        """

        number = self.canvas.itemcget(self.comparison_number, "text")
        self.canvas.itemconfig(self.comparison_number, text=str(int(number)+1))


    def bubble_sort(self):
        """
        This function implements the BubbleSort algorithm.

        :return: None
        """

        len_arr = len(self.boxes)

        for i in range(len_arr):
            for j in range(0, len_arr-i-1):
                if self.boxes[j][0] > self.boxes[j+1][0]:
                    self.update_counter()
                    self.swap(self.boxes[j], self.boxes[j+1], j, j+1)
                else:
                    self.update_counter()
                    self.no_swap(self.boxes[j], self.boxes[j+1], j, j+1)

            self.canvas.itemconfig(self.boxes[len_arr-i-1][1], fill="#00ff00")
            self.canvas.update()
            time.sleep(0.5)

    def insertion_sort(self):
        """
        This function implements the InsertionSort algorithm.

        :return: None
        """

        len_arr = len(self.boxes)

        for i in range(1, len_arr):

            j = i
            while self.boxes[j-1][0] > self.boxes[j][0] and j > 0:

                self.update_counter()
                self.swap(self.boxes[j-1], self.boxes[j], j-1, j)
                j -= 1

            else:
                self.update_counter()
                self.no_swap(self.boxes[i-1], self.boxes[i], i-1, i)


    def selection_sort(self):
        """
        This function implements the SelectionSort algorithm.

        :return: None
        """

        len_arr = len(self.boxes)
        box1_x_tl, box1_y_tl, box1_x_br, box1_y_br = self.canvas.coords(self.boxes[0][1])

        ### Create two arrows which indicate the position of ...
        ### ... the minimum element
        arrow_current_minimum = self.canvas.create_line(box1_x_tl + self.boxSize_x/2, box1_y_tl, box1_x_tl + self.boxSize_x/2 , box1_y_tl-+ self.boxSize_y/2 ,arrow=tkinter.FIRST, fill='#ff0000')
        ### .. .the current element
        arrow_current_item = self.canvas.create_line(box1_x_tl + self.boxSize_x/2, box1_y_tl, box1_x_tl + self.boxSize_x/2 , box1_y_tl-+ self.boxSize_y/2 ,arrow=tkinter.FIRST, fill="#0000ff")


        for i in range(len_arr):

            min_index = i

            for j in range(i, len_arr):

                ### Get the coordinates of the arrows and the current box
                arrow_item_x_tl, arrow_item_y_tl, arrow_item_x_br, arrow_item_y_br = self.canvas.coords(arrow_current_item)
                arrow_minimum_x_tl, arrow_minimum_y_tl, arrow_minimum_x_br, arrow_minimum_y_br = self.canvas.coords(arrow_current_minimum)
                box1_x_tl, box1_y_tl, box1_x_br, box1_y_br = self.canvas.coords(self.boxes[j][1])

                ### Move arrow_item to the current element
                self.canvas.move(arrow_current_item, (box1_x_tl + self.boxSize_x/2) - arrow_item_x_tl, 0)
                ### Move the arrow slightly to the right so that the arrows do not overlap
                self.canvas.move(arrow_current_item, self.boxSize_x / 5, 0)
                self.canvas.update()
                time.sleep(1)

                ### Check if the current element is the new minimum element
                if self.boxes[min_index][0] < self.boxes[j][0]:
                    self.update_counter()
                else:
                    self.update_counter()
                    ### Move the minimum arrow to the current position
                    min_index = j
                    self.canvas.move(arrow_current_minimum, (box1_x_tl + self.boxSize_x / 2) - arrow_minimum_x_tl, 0)
                    ### Move the minimum arrow slightly to the right so that the arrows do not overlap
                    self.canvas.move(arrow_current_minimum, -self.boxSize_x / 5, 0)
                    self.canvas.update()
                    time.sleep(1)

            if min_index == i:
                pass
            else:
                self.swap(self.boxes[i], self.boxes[min_index], i, min_index)
                self.canvas.update()

            ### Mark the i-th element as sorted
            self.canvas.itemconfig(self.boxes[i][1], fill="#00ff00")
            self.canvas.update()


    def merge_sort(self):
        """
        This function implements the MergeSort algorithm.
        Not ready yet.

        :return: None
        """

        len_arr = len(self.boxes)
        mid = len_arr // 2

        ### Move all boxes to the top
        for box in self.boxes:
            self.canvas.move(box[1], 0, -100)
            self.canvas.move(box[2], 0, -100)


        ### Move the boxes up and remove the space between them
        move_x = -25
        for i in range(0, len_arr):

            self.canvas.move(self.boxes[i][1], 150, 0)
            self.canvas.move(self.boxes[i][2], 150, 0)

            self.canvas.move(self.boxes[i][1], move_x, 0)
            self.canvas.move(self.boxes[i][2], move_x, 0)

            move_x -= 25


        self.boxes = self.copy()
        self.split(self.boxes)
        self.boxes = self.copy()
        self.split(self.boxes[:5])
        self.split(self.boxes[5:])



    def sort(self):
        """
        This function starts the sorting procedure with the selected algorithm.

        :return: None
        """

        ### Check if the speed level is valid
        ### If not: Set the speed to "Normal" and return
        if self.speed.get() not in ["Slow", "Normal", "Fast"]:
            tkinter.messagebox.showwarning(title="Warning", message=f"'{self.speed.get()}' is not a valid speed level!")
            self.speed.set("Normal")
            return

        if self.FINISHED_SORTING == True:
            sorted_sequence = [el[0] for el in self.boxes]
            tkinter.messagebox.showwarning(title="Warning", message=f"Sequence {sorted_sequence} is already sorted!\nPlease generate a new sequence!")
            return

        ### Get the selected algorithm from the combobox
        algorithm = self.algorithm_selection.get()

        ### Start sorting
        ### If the sorting algorithm is invalid: Set the default to "Bubble Sort" and return
        if algorithm == "Bubble Sort":
            self.bubble_sort()
        elif algorithm == "Insertion Sort":
            self.insertion_sort()
        elif algorithm == "Selection Sort":
            self.selection_sort()
        elif algorithm == "Merge Sort":
            tkinter.messagebox.showinfo(title="Merge Sort", message="Merge Sort is not yet available!")
            return

        else:
            tkinter.messagebox.showwarning(title="Warning", message=f"'{self.algorithm_selection.get()}' is not a valid sorting algorithm!\n"
                                                                    f"Please select a different algorithm!")
            self.algorithm_selection.set("Bubble Sort")
            return

        time.sleep(1)
        self.finished()



if __name__ == "__main__":

    root = tkinter.Tk()

    app = SortingVisualizer(root)

    root.mainloop()
