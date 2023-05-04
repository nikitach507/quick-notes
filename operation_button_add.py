from tkinter import messagebox
import tkinter
from main import *
from database.notes_database_action import *
from database.category_database_action import *


class OperationButtonAdd:
    def __init__(self, root, pop_up_notes_button):
        self.root = root
        self.category_listbox = None
        self.selected_category = ""
        self.active_item = None
        self.pop_up_notes_button = pop_up_notes_button

    def add_note_button(self, main_win):
        for widget in main_win.winfo_children():
            widget.destroy()
        # Updating the interface area when clicking on the button
        if len(self.pop_up_notes_button) != 0:
            for button in self.pop_up_notes_button.values():
                button.destroy()

        nested_data = {}

        header_label = Label(main_win, text="CREATE A NOTE", bg=QuickNotesApp.PALETTE["main"]["3color"],
                             fg=QuickNotesApp.PALETTE["text"]["1color"],
                             font=("Arial", 15, "bold"), anchor="w")
        header_label.place(x=10, y=10)

        input_form = Text(main_win, height=1, width=54, bg=QuickNotesApp.PALETTE["secondary"]["2color"], wrap="none",
                         border=3, relief="flat", selectborderwidth=0, highlightthickness=0, font=("Arial", 24, "bold"),
                          fg=QuickNotesApp.PALETTE["main"]["3color"],
                          insertbackground=QuickNotesApp.PALETTE["main"]["2color"])
        input_form.place(x=10, y=50)

        desc_form = Text(main_win, height=24, width=61, bg=QuickNotesApp.PALETTE["secondary"]["2color"], wrap="word",
                         border=3, relief="flat", selectborderwidth=0, highlightthickness=0, font=("Arial", 16),
                         fg=QuickNotesApp.PALETTE["main"]["3color"],
                         insertbackground=QuickNotesApp.PALETTE["main"]["2color"])
        desc_form.place(x=10, y=87)

        nested_data["note_name"] = input_form
        nested_data["note_description"] = desc_form
        saving_comm = lambda data=nested_data: self.saving_received_data(data)

        # Create a button to add data to the database
        save_button = Button(main_win, text="Save", bg=QuickNotesApp.PALETTE["secondary"]["1color"],
                             fg=QuickNotesApp.PALETTE["text"]["1color"],
                             activebackground=QuickNotesApp.PALETTE["secondary"]["1color"],
                             border=3, relief="flat", activeforeground=QuickNotesApp.PALETTE["text"]["2color"],
                             command=saving_comm)
        save_button.place(x=670, y=495)

        category_name_label = Label(main_win, text="CATEGORY(*):", bg=QuickNotesApp.PALETTE["main"]["3color"],
                                    fg=QuickNotesApp.PALETTE["secondary"]["2color"],
                                    font=("Arial", 13, "bold"))
        category_name_label.place(x=580, y=100)

        # Creating a frame for selecting categories
        select_category_frame = Frame(main_win)
        select_category_frame.place(x=580, y=135)

        self.category_listbox = Listbox(select_category_frame, width=19, height=7, font=("Arial", 15),
                                        bg=QuickNotesApp.PALETTE["main"]["3color"], border=3, relief="sunken")
        category_listbox_scrollbar = Scrollbar(select_category_frame, command=self.category_listbox.yview,
                                               troughcolor=QuickNotesApp.PALETTE["main"]["3color"],
                                               )
        self.category_listbox.configure(yscrollcommand=category_listbox_scrollbar.set)

        # Getting all categories into a list from the database
        all_database_categories = CategoryDatabaseAction.all_categories_list("note_category")
        all_database_categories.insert(0, "")

        # Add the resulting categories to the area
        for category in all_database_categories:
            self.category_listbox.insert(END, category)

        # Bind event handlers to the list
        self.category_listbox.bind("<<ListboxSelect>>", self.on_select_category_listbox)
        self.category_listbox.bind("<ButtonRelease-1>", self.on_release_category_listbox)

        # Set the default active item
        self.category_listbox.selection_set(0)
        self.active_item = 0
        self.update_color_category_listbox()

        self.category_listbox.pack(side=LEFT, fill=BOTH, expand=True)
        category_listbox_scrollbar.pack(side=LEFT, fill=Y)

        # # Dictionary of column names to be used
        # names_addition_data = {
        #     "head": "HEADER(*):",
        #     "description": "DESCRIPTION:",
        #     "additional": "ADDITIONAL:"
        # }
        # # Dictionary for saving nested data
        # nested_data = {}
        #
        # position_x_name, position_y_name = 10, 60
        # position_x_input, position_y_input = 10, 110
        # position_x_reminder, position_y_reminder = 10, 85
        #
        # for db_column_name, name_input in names_addition_data.items():
        #     number_allowed_characters = NotesDatabaseAction.select_number_characters("notes_info", db_column_name)
        #     name_label = tkinter.Label(main_win, text=name_input, bg=QuickNotesApp.PALETTE["main"]["3color"],
        #                                fg=QuickNotesApp.PALETTE["text"]["1color"],
        #                                font=("Arial", 13, "bold"))
        #     name_label.place(x=position_x_name, y=position_y_name)
        #     input_form = Entry(main_win, width=50, bg=QuickNotesApp.PALETTE["main"]["3color"],
        #                        fg=QuickNotesApp.PALETTE["text"]["1color"], border=2, relief="flat", state="normal",
        #                        highlightbackground=QuickNotesApp.PALETTE["secondary"]["2color"], insertbackground=QuickNotesApp.PALETTE["secondary"]["2color"],
        #                        selectbackground=QuickNotesApp.PALETTE["secondary"]["1color"],
        #                        validate="key", validatecommand=(main_win.register(self.character_count_check),
        #                                                         "%P", number_allowed_characters))
        #     input_form.place(x=position_x_input, y=position_y_input)
        #
        #     # Creating a reminder about the number of allowed characters
        #     sign_reminder_text = f"MAX {number_allowed_characters} characters"
        #     sign_reminder_label = Label(main_win, text=sign_reminder_text, bg=QuickNotesApp.PALETTE["main"]["3color"],
        #                                 fg=QuickNotesApp.PALETTE["secondary"]["4color"],
        #                                 font=("Arial", 13, "bold"), anchor="w")
        #     sign_reminder_label.place(x=position_x_reminder, y=position_y_reminder)
        #
        #     # Adding data to the dictionary and changing positions
        #     nested_data[db_column_name] = input_form
        #     position_y_name += 90
        #     position_y_input += 90
        #     position_y_reminder += 90

    # The note the note the note the note the note The note the note the note the note the note
    def on_select_category_listbox(self, event):
        # List item selection event handler
        widget = event.widget
        selection = widget.curselection()
        if selection:
            item_index = selection[0]
            if item_index != self.active_item:
                self.category_listbox.selection_clear(self.active_item)
                self.active_item = item_index
                self.update_color_category_listbox()
                self.selected_category = widget.get(self.active_item)

    def on_release_category_listbox(self, event):
        # Mouse button release event handler
        widget = event.widget
        item_index = widget.nearest(event.y)
        if item_index != self.active_item:
            self.category_listbox.selection_clear(self.active_item)
            self.active_item = item_index
            self.category_listbox.selection_set(self.active_item)
            self.update_color_category_listbox()

    def update_color_category_listbox(self):
        # Updating the color of the active item
        for item in range(self.category_listbox.size()):
            if item == self.active_item:
                self.category_listbox.itemconfig(item,
                                                 selectbackground=QuickNotesApp.PALETTE["main"]["1color"],
                                                 selectforeground=QuickNotesApp.PALETTE["text"]["1color"])
            else:
                self.category_listbox.itemconfig(item, bg=QuickNotesApp.PALETTE["main"]["3color"],
                                                 fg=QuickNotesApp.PALETTE["text"]["2color"])

    def saving_received_data(self, nested_data):
        current_category = self.selected_category
        # Checks that all data is available before it is stored
        if self.presence_check_necessary_data(nested_data, current_category):
            get_input_data = {}
            for name_column, data_column in nested_data.items():
                get_input_data[name_column] = data_column.get("1.0", "end-1c")
                get_input_data["note_category"] = current_category
                # After adding to the dictionary, clear the area
                data_column.delete("1.0", END)
            # Adding to the database
            note = NotesDatabaseAction(get_input_data["note_name"], get_input_data["note_description"],
                                       get_input_data["note_category"])
            note.add_note("notes_info")

    @staticmethod
    def character_count_check(attached_data, number_character):
        # Function to check the number of characters
        if len(attached_data) < int(number_character):
            return True
        else:
            messagebox.showerror("Error", f"Maximum number of characters exceeded ({number_character})")
            return False

    @staticmethod
    def presence_check_necessary_data(inspection_data, name_category):
        # Function to check the note title and category
        if inspection_data["note_name"] == "" or name_category == "":
            messagebox.showerror("Error",
                                 f"The main condition for creating a note is to write "
                                 f"a title and select a category")
            return False
        return True

    @staticmethod
    def info_note_button():
        print("info")
