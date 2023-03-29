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
    def __init__(self):
        self.note_operation_buttons = None
        self.active_item = 0
        self.side_listbox_categories = None
        self.side_listbox_active_category = None
        self.created_oper_button = None
        self.created_cat_button = None
        self.pop_up_buttons = {}
        self.operation_button_add = OperationButtonAdd(win, self.pop_up_buttons)
        self.operation_button_delete = OperationButtonDelete(win)
        self.category_button_action = CategoryButtonAction(win)
        self.x_note_buttons = None

    def create_interface(self):
        # Creating a logo
        Label(text="Quick notes", width=13, bg="#787D46",
              font=("Times New Romans", 20)).place(x=10, y=10)

        # Creating buttons to control notes
        self.note_operation_buttons = {"create new note": self.operation_button_add.add_note_button}
        self.x_note_buttons, y_note_buttons = 190, 29
        for caption, button_function in self.note_operation_buttons.items():
            self.create_operation_button(button_symbol=caption, button_action=button_function,
                                         x_button=self.x_note_buttons, y_button=y_note_buttons)
            self.x_note_buttons += 130

        # Creating a side list of categories
        side_frame_categories = Frame(win)
        side_frame_categories.place(x=8, y=70)

        self.side_listbox_categories = Listbox(side_frame_categories, width=12, height=15,
                                               font=("Georgia", 20), fg="black",
                                               bg="#E4BA6A", border=3, relief="flat", )

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

        # self.category_button_action.settings_category(8, 70)
        #
        # add_new_category_comm = lambda x=200, y=70: self.category_button_action.settings_category(x, y)
        # self.create_category_button(button_symbol="category settings", button_actions=add_new_category_comm,
        #                             x_button=5, y_button=430)

        # Show the area where all the notes will be
        self.note_display_interface()

    def create_operation_button(self, button_symbol, button_action, x_button, y_button):
        operating_button_command = lambda: button_action()
        self.created_oper_button = Button(win, text=f"{button_symbol}", bg="#787D46", activebackground="#90956C",
                                          font=("Georgia", 14), fg="white", activeforeground="#FBF5E3",
                                          width=120, height=20, border=0, relief="flat", highlightbackground="#90956C",
                                          command=operating_button_command)
        if button_symbol != "create new note":
            self.pop_up_buttons[button_symbol] = self.created_oper_button
        self.created_oper_button.place(x=x_button, y=y_button)

    def create_category_button(self, button_symbol, button_actions, x_button, y_button):
        category_button_command = lambda: button_actions()
        self.created_cat_button = Button(win, text=f"{button_symbol}", bg="#E4BA6A", activebackground="#F2D091",
                                         font=("Georgia", 16), fg="#3C4013", activeforeground="#4C5117",
                                         width=180, height=24, border=0, relief="flat", highlightbackground="#F2D091",
                                         command=category_button_command)
        self.created_cat_button.place(x=x_button, y=y_button)

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
                self.side_listbox_categories.itemconfig(item, bg="#F2D9AA", fg="#4C5117",
                                                        selectbackground="#F2D9AA", selectforeground="#4C5117")
            else:
                self.side_listbox_categories.itemconfig(item, bg="#E4BA6A", fg="#3C4013",
                                                        selectbackground="#FBF5E3", selectforeground="#787D46")

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
                                         x_button=self.x_note_buttons, y_button=29)
            self.create_operation_button(button_symbol="note window", button_action=window_note_lambda,
                                         x_button=self.x_note_buttons + 130, y_button=29)
            # Changing the color of the current data
            for label in labels_list:
                label.config(fg="#ffffff", bg="#787D46")

            # Go around all the data on frame and change the color of all but the current one
            for child in frame_to_display.winfo_children():
                if isinstance(child, Label):
                    if child.cget('bg') == "#787D46" and child not in labels_list:
                        child.config(fg="#787D46", bg="#F1EBD8")

        # Creating names for note columns
        note_legend_name_and_position = {
            "HEAD": (215, 80),
            "DESCRIPTION": (365, 80),
            "ADDITIONAL": (643, 80),
            "CATEGORY": (870, 80)
        }
        for legend_name, legend_position in note_legend_name_and_position.items():
            note_title_legend = Label(win, text=legend_name, bg="#F1EBD8", fg="#787D46",
                                      font=("Arial", 12, "bold"), anchor="w", width=21)
            note_title_legend.place(x=legend_position[0], y=legend_position[1])

        # Create an area to display notes
        notes_display_frame = Frame(win)
        notes_display_frame.grid(row=0, column=0, padx=205, pady=100)

        # Create a Scrollbar and create a Canvas for this
        notes_canvas = Canvas(notes_display_frame, width=775, height=480)
        scrollbar_for_notes_canvas = Scrollbar(notes_display_frame, orient="vertical",
                                               command=notes_canvas.yview)
        notes_canvas.configure(yscrollcommand=scrollbar_for_notes_canvas.set,
                               bg="#F1EBD8", borderwidth=0, highlightthickness=0)
        notes_canvas.pack(side="left", fill="both", expand=True)

        # Create a frame to display data on canvas
        frame_to_display = Frame(notes_canvas)
        frame_to_display.configure(bg="#F1EBD8")
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
                    line_under_note = Label(frame_to_display, bg="#787D45", width=note_column_value[2], pady=1, padx=1)
                    line_under_note.grid(row=note_num, column=note_column_value[3],
                                         padx=note_column_value[4], pady=4, sticky="se")

                    note_data = Label(frame_to_display, text=f"{all_database_notes[note_num][note_column_value[0]]}",
                                      fg="#787D46", bg="#F1EBD8", width=note_column_value[2], anchor="w")
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

    @staticmethod
    def open_note_information(label):
        for i in label:
            print(i.cget('text'))

        # Updating the notes interface area when categories change
        Label(win, bg="#F1EBD8", border=4, relief="sunken").place(x=190, y=55, relwidth=1, relheight=1)


if __name__ == "__main__":
    """Creating a window and running the program"""
    win = Tk()
    win_w, win_h = 1000, 600
    win.title("Quick notes")
    win.geometry(f"{win_w}x{win_h}+400+250")
    win.resizable(False, False)

    Label(win, bg="#787D46", height=3, relief="raised", border=4).place(x=0, y=-3, relwidth=1)
    Label(win, bg="#E4BA6A", border=4, width=20, relief="sunken").place(x=0, y=55, relheight=1)
    Label(win, bg="#F1EBD8", border=4, relief="sunken").place(x=190, y=55, relwidth=1, relheight=1)

    app = QuickNotesApp()

    app.create_interface()

    win.mainloop()
