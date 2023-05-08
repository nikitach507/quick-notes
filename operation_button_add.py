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
        self.name_form = None
        self.desc_form = None
        self.name_char_count_error = None
        self.desc_char_count_error = None
        self.pop_up_notes_button = pop_up_notes_button

    def add_note_button(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        # Updating the interface area when clicking on the button
        if len(self.pop_up_notes_button) != 0:
            for button in self.pop_up_notes_button.values():
                button.destroy()

        nested_data = {}

        header_label = Label(self.root, text="CREATE A NOTE", bg=QuickNotesApp.PALETTE["main"]["3color"],
                             fg=QuickNotesApp.PALETTE["text"]["1color"],
                             font=("Arial", 15, "bold"), anchor="w")
        header_label.pack(padx=10, pady=10, anchor="nw")

        number_allowed_characters_name = NotesDatabaseAction.select_number_characters("notes_info", "note_name")
        number_allowed_characters_desc = NotesDatabaseAction.select_number_characters("notes_info", "note_description")

        self.name_form = Text(self.root, height=1, width=39, bg=QuickNotesApp.PALETTE["secondary"]["2color"], wrap="none",
                              border=3, relief="flat", selectborderwidth=0, highlightthickness=0, font=("Arial", 24, "bold"),
                              fg=QuickNotesApp .PALETTE["main"]["3color"], undo=True,
                              insertbackground=QuickNotesApp.PALETTE["main"]["2color"])
        self.name_form.pack(padx=10, pady=3, anchor="nw")

        self.desc_form = Text(self.root, height=24, width=60, bg=QuickNotesApp.PALETTE["secondary"]["2color"], wrap="word",
                              border=2, relief="flat", selectborderwidth=0, highlightthickness=0, font=("Arial", 16),
                              fg=QuickNotesApp.PALETTE["main"]["3color"], undo=True, tabs=15, tabstyle="tabular",
                              spacing1=5, padx=5,
                              insertbackground=QuickNotesApp.PALETTE["main"]["2color"])
        self.desc_form.pack(padx=10, pady=0, anchor="nw")

        for form in (self.name_form, self.desc_form):
            form.bind('<KeyRelease>', lambda e:
            self.check_input_length(number_allowed_characters_name, number_allowed_characters_desc))

        nested_data["note_name"] = self.name_form
        nested_data["note_description"] = self.desc_form
        saving_comm = lambda: self.saving_received_data("save", self.name_form, self.desc_form,
                                                        self.selected_category, nested_data,
                                                        number_allowed_characters_name, number_allowed_characters_desc)
        # Create a button to add data to the database
        save_button = Button(self.root, text="Save", bg=QuickNotesApp.PALETTE["secondary"]["1color"],
                             fg=QuickNotesApp.PALETTE["text"]["1color"],
                             activebackground=QuickNotesApp.PALETTE["secondary"]["1color"],
                             border=3, relief="flat", activeforeground=QuickNotesApp.PALETTE["text"]["2color"],
                             command=saving_comm)
        save_button.place(x=670, y=495)

        category_name_label = Label(self.root, text="CATEGORY(*):", bg=QuickNotesApp.PALETTE["main"]["3color"],
                                    fg=QuickNotesApp.PALETTE["secondary"]["2color"],
                                    font=("Arial", 13, "bold"))
        category_name_label.place(x=580, y=10)

        # Creating a frame for selecting categories
        select_category_frame = Frame(self.root)
        select_category_frame.place(x=580, y=45)

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

    def saving_received_data(self, action: Literal["save", "update"],
                             save_name_form, save_desc_form, current_category, nested_data,
                             allowed_characters_name, allowed_characters_desc, note_id=None):
        """
            This function works with the button to save and add to the database.
            :param action: Action the button should perform
            :type action: str
        """
        # Checks that all data is available before it is stored
        if len(save_name_form.get('1.0', 'end-1c')) <= allowed_characters_name \
                and len(save_desc_form.get('1.0', 'end-1c')) <= allowed_characters_desc:
            if self.presence_check_necessary_data(save_name_form, current_category):
                get_input_data = {}
                for name_column, data_column in nested_data.items():
                    get_input_data[name_column] = data_column.get("1.0", "end-1c")
                    get_input_data["note_category"] = current_category
                    # After adding to the dictionary, clear the area
                    if action == "save":
                        data_column.delete("1.0", END)

                note = NotesDatabaseAction(get_input_data["note_name"], get_input_data["note_description"],
                                           get_input_data["note_category"])
                # Adding to the database
                if action == "save":
                    note.add_note("notes_info")
                    self.selected_category = ""
                elif action == "update":
                    note.edit_note(table_name="notes_info", note_id=note_id)
                self.selected_category = ""
        elif len(save_name_form.get('1.0', 'end-1c')) > allowed_characters_name:
            messagebox.showerror("Error",
                                 f"The header must have a maximum of {allowed_characters_name} characters, "
                                 f"now you have {len(save_name_form.get('1.0', 'end-1c'))}")
        elif len(save_desc_form.get('1.0', 'end-1c')) > allowed_characters_desc:
            messagebox.showerror("Error",
                                 f"The description must have a maximum of {allowed_characters_desc} characters, "
                                 f"now you have {len(save_desc_form.get('1.0', 'end-1c'))}")

    def check_input_length(self, allowed_characters_name, allowed_characters_desc):
        block_count_name, block_count_desc = 1000, 19000
        current_count_name = len(self.name_form.get('1.0', 'end-1c'))
        current_count_desc = len(self.desc_form.get('1.0', 'end-1c'))
        # Function to check the number of characters
        if block_count_name > current_count_name > allowed_characters_name:
            if self.name_char_count_error is not None:
                self.name_char_count_error.destroy()
            self.name_char_count_error = Label(self.root, text=f"Maximum number of characters "
                                                               f"in the header: {allowed_characters_name}, "
                                                    f"now characters: {current_count_name}",
                                               bg=QuickNotesApp.PALETTE["main"]["3color"],
                                               fg=QuickNotesApp.PALETTE["secondary"]["4color"])
            self.name_char_count_error.place(x=343, y=25)
        elif current_count_name >= block_count_name:
            if self.name_char_count_error is not None:
                self.name_char_count_error.destroy()
            self.name_form.configure(state="disable")
            self.name_char_count_error = Label(self.root, text=f"The input field for the header is locked. "
                                                               f"Now characters: {current_count_name}",
                                               bg=QuickNotesApp.PALETTE["main"]["3color"],
                                               fg=QuickNotesApp.PALETTE["secondary"]["4color"])
            self.name_char_count_error.place(x=395, y=25)
        else:
            if self.name_char_count_error is not None:
                self.name_char_count_error.destroy()

        if block_count_desc > current_count_desc > allowed_characters_desc:
            if self.desc_char_count_error is not None:
                self.desc_char_count_error.destroy()
            self.desc_char_count_error = Label(self.root, text=f"Maximum number of characters "
                                                               f"in the description: {allowed_characters_desc}.\n"
                                                               f"Now characters: {current_count_desc}",
                                               wraplength=190, justify="left",
                                               bg=QuickNotesApp.PALETTE["main"]["3color"],
                                               fg=QuickNotesApp.PALETTE["secondary"]["4color"])
            self.desc_char_count_error.place(x=580, y=280)
        elif current_count_desc >= block_count_desc:
            if self.desc_char_count_error is not None:
                self.desc_char_count_error.destroy()
            self.desc_form.configure(state="disable")
            self.desc_char_count_error = Label(self.root, text=f"The input field for the description is locked.\n"
                                                               f"Now characters: {current_count_desc}",
                                               wraplength=190, justify="left",
                                               bg=QuickNotesApp.PALETTE["main"]["3color"],
                                               fg=QuickNotesApp.PALETTE["secondary"]["4color"])
            self.desc_char_count_error.place(x=580, y=280)

        else:
            if self.desc_char_count_error is not None:
                self.desc_char_count_error.destroy()

    def presence_check_necessary_data(self, save_name_form, name_category):
        # Function to check the note title and category
        if len(save_name_form.get('1.0', 'end-1c')) == 0 or name_category == "":
            messagebox.showerror("Error",
                                 f"The main condition for creating a note is to write "
                                 f"a title and select a category")
            return False
        return True

    @staticmethod
    def info_note_button():
        print("info")
