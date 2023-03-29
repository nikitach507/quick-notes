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

    def add_note_button(self):
        def saving_received_data():
            current_category = self.selected_category
            # Checks that all data is available before it is stored
            if presence_check_necessary_data(nested_data, current_category):
                get_input_data = {}
                for name_column, data_column in nested_data.items():
                    get_input_data[name_column] = data_column.get()
                    get_input_data["name_cat"] = current_category
                    # After adding to the dictionary, clear the area
                    data_column.delete(0, END)
                # Adding to the database
                note = NotesDatabaseAction(get_input_data["head"], get_input_data["description"],
                                           get_input_data["additional"], get_input_data["name_cat"])
                note.add_note("notes_info")

        def character_count_check(attached_data, number_character):
            # Function to check the number of characters
            if len(attached_data) < int(number_character):
                return True
            else:
                messagebox.showerror("Error", f"Maximum number of characters exceeded ({number_character})")
                return False

        def presence_check_necessary_data(inspection_data, name_category):
            # Function to check the note title and category
            if inspection_data["head"].get() == "" or name_category == "":
                messagebox.showerror("Error",
                                     f"The main condition for creating a note is to write "
                                     f"a title and select a category")
                return False
            return True

        # Updating the interface area when clicking on the button
        Label(self.root, bg="#F1EBD8", border=4, relief="sunken").place(x=190, y=55, relwidth=1, relheight=1)

        if len(self.pop_up_notes_button) != 0:
            for button in self.pop_up_notes_button.values():
                button.destroy()

        header_label = Label(self.root, text="ADD A NEW NOTE DATA", bg="#F1EBD8", fg="#787D46",
                             font=("Arial", 15, "bold"), anchor="w")
        header_label.place(x=220, y=80)

        # Dictionary of column names to be used
        names_addition_data = {
            "head": "HEADER(*):",
            "description": "DESCRIPTION:",
            "additional": "ADDITIONAL:"
        }
        # Dictionary for saving nested data
        nested_data = {}

        position_x_name, position_y_name = 220, 130
        position_x_input, position_y_input = 220, 180
        position_x_reminder, position_y_reminder = 220, 155

        for db_column_name, name_input in names_addition_data.items():
            number_allowed_characters = NotesDatabaseAction.select_number_characters("notes_info", db_column_name)
            name_label = tkinter.Label(self.root, text=name_input, bg="#F1EBD8", fg="#787D46", font=("Arial", 13, "bold"))
            name_label.place(x=position_x_name, y=position_y_name)
            input_form = Entry(self.root, width=50, bg="#F1EBD8", fg="black", border=2, relief="flat",
                               highlightbackground="#787D46", insertbackground="black", selectbackground="#787D46",
                               validate="key", validatecommand=(self.root.register(character_count_check),
                                                                "%P", number_allowed_characters))
            input_form.place(x=position_x_input, y=position_y_input)

            # Creating a reminder about the number of allowed characters
            sign_reminder_text = f"MAX {number_allowed_characters} characters"
            sign_reminder_label = Label(self.root, text=sign_reminder_text, bg="#F1EBD8", fg="#A64141",
                                        font=("Arial", 13, "bold"), anchor="w")
            sign_reminder_label.place(x=position_x_reminder, y=position_y_reminder)

            # Adding data to the dictionary and changing positions
            nested_data[db_column_name] = input_form
            position_y_name += 90
            position_y_input += 90
            position_y_reminder += 90

        # Create a button to add data to the database
        save_button = Button(self.root, text="Save", bg="#787D46", fg="#F1EBD8", activebackground="#F1EBD8",
                             border=3, relief="flat", activeforeground="#787D46", command=saving_received_data)
        save_button.place(x=800, y=450)

        category_name_label = Label(self.root, text="CATEGORY(*):", bg="#F1EBD8", fg="#787D46",
                                    font=("Arial", 13, "bold"))
        category_name_label.place(x=746, y=130)

        # Creating a frame for selecting categories
        select_category_frame = Frame(self.root)
        select_category_frame.place(x=750, y=179)

        self.category_listbox = Listbox(select_category_frame, width=19, height=7, font=("Arial", 15),
                                        bg="#F1EBD8", border=3, relief="sunken")
        category_listbox_scrollbar = Scrollbar(select_category_frame, command=self.category_listbox.yview)
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
                self.category_listbox.itemconfig(item, bg="#F2D9AA", fg="#4C5117", selectbackground="#F2D9AA",
                                                 selectforeground="#4C5117")
            else:
                self.category_listbox.itemconfig(item, bg="#F1EBD8", fg="#787D46", selectbackground="#FBF5E3",
                                                 selectforeground="#787D46")



    @staticmethod
    def info_note_button():
        print("info")
