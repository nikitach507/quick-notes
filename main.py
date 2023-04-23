import logging
import sys
from tkinter import *

from operation_button_add import *
from operation_button_delete import *
from database.notes_database_action import *
from database.category_database_action import *
from category_button_action import *

if sys.platform == 'darwin':
    from tkmacosx import Button


class QuickNotesApp:
    PALETTE = {
        "main": {
            "1color": "#213040",
            "2color": "#131415",
            "3color": "#18222D",
        },
        "text": {
            "1color": "#FFFFFF",
            "2color": "#B2C2D5",
            "3color": "#898A8A",
        },
        "secondary": {
            "1color": "#53A6E0",
            "2color": "#B2C2D5",
            "3color": "#898A8A",
            "4color": "#EF5B5B",
        }
    }

    def __init__(self, upper_area, side_area, main_area):
        self.upper_win = upper_area
        self.side_win = side_area
        self.main_win = main_area

        self.note_operation_buttons = None
        self.active_item = 0
        self.side_listbox_categories = None
        self.side_listbox_active_category = None
        self.created_oper_button = None
        self.created_cat_button = None
        self.notes_display_frame = None
        self.open_note_frame = None
        self.pop_up_buttons = {}
        self.operation_button_add = OperationButtonAdd(win, self.pop_up_buttons)
        self.operation_button_delete = OperationButtonDelete(win)
        self.category_button_action = CategoryButtonAction(win)
        self.x_note_buttons = None

        logging.basicConfig(filename='quick_notes_log_file.log', level=logging.DEBUG,
                            format='%(asc''time)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        self.logger = logging.getLogger(__name__)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        self.logger.addHandler(console_handler)

    def create_interface(self):

        # Creating buttons to control notes
        self.note_operation_buttons = {"create new note": self.switch_add_note}
        self.x_note_buttons = 0
        for caption, button_function in self.note_operation_buttons.items():
            self.create_operation_button(button_symbol=caption, button_action=button_function,
                                         x_button=self.x_note_buttons)
            self.x_note_buttons += 130

        # Creating a side list of categories
        side_frame_categories = Frame(self.side_win)
        side_frame_categories.place(x=8, y=30)

        self.side_listbox_categories = Listbox(side_frame_categories, width=12,
                                               fg=QuickNotesApp.PALETTE["text"]["1color"],
                                               font=("Arial", 20),
                                               bg=QuickNotesApp.PALETTE["main"]["2color"], relief="flat",
                                               )

        side_scrollbar_categories = Scrollbar(side_frame_categories)
        side_scrollbar_categories.configure(command=self.side_listbox_categories.yview)

        self.side_listbox_categories.configure(yscrollcommand=side_scrollbar_categories.set)

        # Getting all categories into a list from the database
        all_database_categories = CategoryDatabaseAction.all_categories_list("note_category")
        all_database_categories.insert(0, "All notes")

        # Add the resulting categories to the area
        for category in all_database_categories:
            self.side_listbox_categories.insert(END, category)

        # Bind event handlers to the list
        self.side_listbox_categories.bind("<<ListboxSelect>>", self.on_select_side_listbox)
        self.side_listbox_categories.bind("<ButtonRelease-1>", self.on_release_side_listbox)

        # Set the default active item
        self.side_listbox_categories.selection_set(0)
        self.update_color_side_listbox()
        self.side_listbox_categories.pack(side=LEFT, fill=BOTH, expand=True)

        # Show scrollbar only if there are more than {n} categories
        if len(all_database_categories) > 15:
            side_scrollbar_categories.pack(side=LEFT, fill=Y)

        # Show the area where all the notes will be
        self.note_display_interface()

    def switch_add_note(self):
        for widget in self.main_win.winfo_children():
            widget.destroy()
        self.operation_button_add.add_note_button(self.main_win)

    def create_operation_button(self, button_symbol, button_action, x_button):
        operating_button_command = lambda: button_action()
        self.created_oper_button = Button(self.upper_win, text=f"{button_symbol}", bg=QuickNotesApp.PALETTE["main"]["1color"],
                                          font=("Georgia", 14), fg=QuickNotesApp.PALETTE["text"]["2color"],
                                          activebackground=QuickNotesApp.PALETTE["main"]["1color"],
                                          activeforeground=QuickNotesApp.PALETTE["text"]["1color"],
                                          width=120, height=18, border=4, relief="flat",
                                          command=operating_button_command)
        if button_symbol != "create new note":
            self.pop_up_buttons[button_symbol] = self.created_oper_button
        self.created_oper_button.place(x=x_button, y=-2)

    def on_select_side_listbox(self, event):
        # List item selection event handler
        widget = event.widget
        selection = widget.curselection()
        if selection:
            item_index = selection[0]
            if item_index != self.active_item:
                self.side_listbox_categories.selection_clear(self.active_item)
                self.active_item = item_index
                self.update_color_side_listbox()
                self.side_listbox_active_category = widget.get(self.active_item)
                for widget in self.main_win.winfo_children():
                    widget.destroy()
                self.note_display_interface(self.side_listbox_active_category)

    def on_release_side_listbox(self, event):
        # Mouse button release event handler
        widget = event.widget
        item_index = widget.nearest(event.y)
        if item_index != self.active_item:
            self.side_listbox_categories.selection_clear(self.active_item)
            self.active_item = item_index
            self.side_listbox_categories.selection_set(self.active_item)
            self.update_color_side_listbox()

    def update_color_side_listbox(self):
        # Updating the color of the active item
        for item in range(self.side_listbox_categories.size()):
            if item == self.active_item:
                self.side_listbox_categories.itemconfig(item, selectbackground=QuickNotesApp.PALETTE["main"]["2color"],
                                                        selectforeground=QuickNotesApp.PALETTE["text"]["1color"])
            else:
                self.side_listbox_categories.itemconfig(item, bg=QuickNotesApp.PALETTE["main"]["2color"],
                                                        fg=QuickNotesApp.PALETTE["text"]["3color"])

    def note_display_interface(self, note_category="All notes"):
        def change_active_data_color(labels_list):
            if len(self.pop_up_buttons) == 2:
                for button in self.pop_up_buttons.values():
                    button.destroy()
            delete_note_lambda = lambda note_data_label=labels_list: \
                self.operation_button_delete.delete_note_button(note_data_label)
            window_note_lambda = lambda note_data_label=labels_list: \
                self.operation_button_delete.open_new_window(note_data_label)
            self.create_operation_button(button_symbol="delete the note", button_action=delete_note_lambda,
                                         x_button=self.x_note_buttons)
            self.create_operation_button(button_symbol="note window", button_action=window_note_lambda,
                                         x_button=self.x_note_buttons + 130)
            # Changing the color of the current data
            for label in labels_list:
                label.config(fg=QuickNotesApp.PALETTE["text"]["1color"], bg=QuickNotesApp.PALETTE["main"]["1color"])

            # Go around all the data on frame and change the color of all but the current one
            for child in frame_to_display.winfo_children():
                if isinstance(child, Label):

                    if child.cget('bg') == QuickNotesApp.PALETTE["main"]["1color"] and child not in labels_list and child.cget('text'):
                        child.config(fg=QuickNotesApp.PALETTE["text"]["2color"],
                                     bg=QuickNotesApp.PALETTE["main"]["3color"])

        # Creating names for note columns
        note_legend_name_and_position = {
            "HEAD": (215, 40),
            "DESCRIPTION": (365, 40),
            "ADDITIONAL": (643, 40),
            "CATEGORY": (870, 40)
        }
        for widget in self.main_win.winfo_children():
            widget.destroy()

        self.titles_display_frame = Frame(self.main_win, bg="red", width=270, height=20)
        self.titles_display_frame.configure(bg="red")
        column_title = 0
        for legend_name, legend_position in note_legend_name_and_position.items():
            note_title_legend = Label(self.titles_display_frame, text=legend_name, bg=QuickNotesApp.PALETTE["main"]["3color"],
                                      fg=QuickNotesApp.PALETTE["text"]["1color"],
                                      font=("Arial", 12, "bold"), anchor="w", width=21)
            note_title_legend.grid(row=0, column=column_title)
            column_title += 1
        self.titles_display_frame.place(x=10, y=10)
        if self.open_note_frame:
            self.open_note_frame.pack_forget()
        # Create an area to display notes
        self.notes_display_frame = Frame(self.main_win)
        self.notes_display_frame.grid(row=0, column=0, padx=10, pady=50)

        # Create a Scrollbar and create a Canvas for this
        notes_canvas = Canvas(self.notes_display_frame, width=775, height=480)
        scrollbar_for_notes_canvas = Scrollbar(self.notes_display_frame, orient="vertical",
                                               command=notes_canvas.yview)
        notes_canvas.configure(yscrollcommand=scrollbar_for_notes_canvas.set,
                               bg=QuickNotesApp.PALETTE["main"]["3color"], borderwidth=0, highlightthickness=0)
        notes_canvas.pack(side="left", fill="both", expand=True)

        # Create a frame to display data on canvas
        frame_to_display = Frame(notes_canvas)
        frame_to_display.configure(bg=QuickNotesApp.PALETTE["main"]["3color"])
        frame_to_display.bind("<Configure>",
                              lambda e: notes_canvas.configure(scrollregion=notes_canvas.bbox("all")))
        notes_canvas.create_window((0, 0), window=frame_to_display, anchor="nw")

        # Getting all notes into a list from the database
        all_database_notes = NotesDatabaseAction.select_all_notes(table_name="notes_info", category=note_category)
        if len(all_database_notes) > 15:
            scrollbar_for_notes_canvas.pack(side="right", fill="y")

        # Dictionary, which defines the position of notes data
        # {name: (column_name, padx_data, width_line, column_number_line, padx_line)}
        note_data_and_line = {
            "notes_column_id": "id",
            "notes_column_head": ('head', 1, 16, 0, 0),
            "notes_column_description": ('description', 2, 30, 1, 2),
            "notes_column_additional": ('additional', 1, 24, 2, 1),
            "notes_column_category": ('name_cat', 0, 10, 3, 0)

        }
        all_note_data = list()

        # Write out all the data in the frame
        for note_num in range(len(all_database_notes)):
            for note_column_name, note_column_value in note_data_and_line.items():
                if note_column_name != "notes_column_id":
                    line_under_note = Label(frame_to_display, bg=QuickNotesApp.PALETTE["main"]["1color"], width=note_column_value[2], pady=1, padx=1)
                    line_under_note.grid(row=note_num, column=note_column_value[3],
                                         padx=note_column_value[4], pady=4, sticky="se")

                    note_data = Label(frame_to_display, text=f"{all_database_notes[note_num][note_column_value[0]]}",
                                      fg=QuickNotesApp.PALETTE["text"]["2color"],
                                      bg=QuickNotesApp.PALETTE["main"]["3color"], width=note_column_value[2],
                                      anchor="w")
                    note_data.grid(row=note_num, column=note_column_value[3],
                                   padx=note_column_value[1], pady=5, sticky="e")
                    all_note_data.append(note_data)
                else:
                    note_data = Label(frame_to_display, text=f"{all_database_notes[note_num][note_column_value]}")
                    all_note_data.append(note_data)
            for note_label in all_note_data:
                note_label.bind("<Button-1>",
                                lambda event, labels=tuple(all_note_data): change_active_data_color(labels))
                note_label.bind("<Double-Button-1>",
                                lambda event, labels=tuple(all_note_data): self.open_note_information(labels))
            all_note_data.clear()

        for pop_up_button in self.pop_up_buttons.values():
            pop_up_button.destroy()

    def open_note_information(self, label):
        all_text_label = {}
        for index, text_in_label in enumerate(label):
            all_text_label[index] = text_in_label.cget("text")

        # Updating the notes interface area when categories change
        for widget in self.main_win.winfo_children():
            widget.destroy()

        # удалить   main_frame_in_main

        self.open_note_frame = Frame(self.main_win)
        self.open_note_frame.pack(padx=10, pady=100)

        name_text_area = Text(self.open_note_frame, height=3, relief="flat", border=3, width=100,
                              bg=QuickNotesApp.PALETTE["main"]["3color"],
                              font=("Georgia", 20), tabs=1043, fg=QuickNotesApp.PALETTE["text"]["1color"])
        name_text_area.insert(INSERT, all_text_label[1])
        name_text_area.pack()

        # Создаем вторую область Text
        desc_text_area = Text(self.open_note_frame, height=5, width=100, )
        desc_text_area.insert(INSERT, all_text_label[2])
        desc_text_area.pack()

        # Создаем третью область Text
        addit_text_area = Text(self.open_note_frame, height=3, width=100)
        addit_text_area.insert(INSERT, all_text_label[3])
        addit_text_area.pack()


if __name__ == "__main__":
    """Creating a window and running the program"""
    win = Tk()
    win_w, win_h = 1000, 600
    win.title("Quick notes")
    win.geometry(f"{win_w}x{win_h}+400+250")
    win.resizable(False, False)

    side_frame = Frame(win, bg=QuickNotesApp.PALETTE["main"]["2color"], border=3, relief="flat",
                       width=200,
                       highlightthickness=1, highlightbackground=QuickNotesApp.PALETTE["main"]["1color"])
    side_frame.place(x=0, y=0, relheight=1)
    upper_frame = Frame(win, bg=QuickNotesApp.PALETTE["main"]["1color"], height=30, border=4)
    upper_frame.place(x=200, y=0, relwidth=1)

    main_frame = Frame(win, bg=QuickNotesApp.PALETTE["main"]["3color"], border=4)
    main_frame.place(x=200, y=30, relwidth=1, relheight=1)
    app = QuickNotesApp(upper_frame, side_frame, main_frame)

    app.create_interface()

    win.mainloop()

# main
# 1. #787D46  #213040 -> light blue
# 2. #E4BA6A   #131415 -> not clear black
# 3. #F1EBD8  #18222D -> dark blue

# text color
# 1. #FFFFFF -> clear white ACTIVE
# 2. #B2C2D5 -> white-blue MID-ACTIVE
# 3. #898A8A -> gray NON ACTIVE

# additional_color
# 1. #2CA6FF -> Azure
# 2. #B2C2D5 -> white-blue
# 3. #898A8A -> gray
# 4. #EF5B5B -> light red WARNING
