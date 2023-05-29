from database.category_database_action import CategoryDatabaseAction
from database.notes_database_action import NotesDatabaseAction
from lib_imports import *
from side_category_list import SideCategoryList


class CategoryEdit:
    def __init__(self, main_window, operation_buttons_window, side_window):
        self.side_frame = side_window
        self.main_frame = main_window
        self.operation_buttons_frame = operation_buttons_window
        self.side_listbox_categories = SideCategoryList(
            self.main_frame, self.operation_buttons_frame, self.side_frame
        )
        self.error_message = None

    def create_interface_edit_category_win(self):
        if self.side_listbox_categories.side_listbox_active_category != "All notes":
            edit_window = Toplevel()
            edit_window.title("EDIT THE CATEGORY NAME")
            edit_window.resizable(False, False)
            edit_window.grab_set()
            edit_window.attributes("-topmost", True)

            screen_width = edit_window.winfo_screenwidth()
            screen_height = edit_window.winfo_screenheight()
            window_width = 400
            window_height = 150
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2

            edit_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
            edit_window.configure(bg=PALETTE["main"]["1color"])

            self.draw_input_category(edit_window)
            self.draw_button_edit(edit_window)
        else:
            messagebox.showinfo("Message", "Select a category to change")
            # form = Toplevel(bg=PALETTE["secondary"]["4color"])
            # form.title("Message")
            # window_width = 300
            # window_height = 50
            # screen_width = form.winfo_screenwidth()
            # screen_height = form.winfo_screenheight()
            #
            # x = (screen_width - window_width) // 2
            # y = (screen_height - window_height) // 2
            # form.geometry(f"{window_width}x{window_height}+{x}+{y}")
            # form.resizable(False, False)
            #
            # Label(form, text="Select a category to change",
            #       bg=PALETTE["secondary"]["4color"],
            #       font=("Arial", 20, "bold")).pack(pady=10)
            #
            # form.attributes("-topmost", True)
            # form.after(1000, form.destroy)

    def draw_input_category(self, window):
        self.input_cat = Entry(window, bg=PALETTE["main"]["3color"], width=40,
                               cursor="ibeam",
                               font=("Arial", 16),
                               bd=3, relief="flat",
                               highlightthickness=2,
                               highlightcolor=PALETTE["main"]["3color"],
                               highlightbackground=PALETTE["main"]["3color"],
                               )

        self.input_cat.insert(0, self.side_listbox_categories.side_listbox_active_category)
        self.input_cat.pack(pady=40, anchor="center")

    def draw_button_edit(self, window):
        editing_comm = lambda: self._action_after_press_edit(window, self.input_cat.get())

        button = Button(window, text="Edit", bg=PALETTE["secondary"]["1color"],
                        fg=PALETTE["text"]["1color"],
                        activebackground=PALETTE["main"]["3color"],
                        activeforeground=PALETTE["text"]["1color"],
                        width=130, height=20,
                        command=editing_comm,
                        )
        button.place(x=136, y=80)

    def _action_after_press_edit(self, window, current_input):
        if self.check_input_data(window, current_input):
            CategoryDatabaseAction().edit_category("note_category",
                                                   self.side_listbox_categories.side_listbox_active_category,
                                                   current_input),
            NotesDatabaseAction.edit_category_in_note("notes_info",
                                                      self.side_listbox_categories.side_listbox_active_category,
                                                      current_input,
                                                      ),
            self.close_window_after_adding(window, current_input)

    def check_input_data(self, window, current_input):
        allowed_characters = CategoryDatabaseAction.select_number_characters("note_category", "name_cat")
        all_database_categories = CategoryDatabaseAction.all_categories_list(
            "note_category")

        if len(current_input) > allowed_characters or len(current_input) < 1:
            if self.error_message:
                self.error_message.destroy()
            self.error_message = Label(window,
                                       text=f"Category names must be between 1 and {allowed_characters} characters.\n"
                                            f"Current count: {len(current_input)}", justify="left",
                                       bg=PALETTE["main"]["1color"],
                                       fg=PALETTE["secondary"]["4color"])
            self.error_message.place(x=12, y=3)
            return False
        elif current_input in all_database_categories:
            if self.error_message:
                self.error_message.destroy()
            self.error_message = Label(window,
                                       text=f"The name of the category {current_input} already exists", justify="left",
                                       bg=PALETTE["main"]["1color"],
                                       fg=PALETTE["secondary"]["4color"])
            self.error_message.place(x=12, y=10)
            return False
        return True

    def close_window_after_adding(self, window, current_input):
        window.destroy()
        self.side_listbox_categories.create_side_category_list(note_category=current_input)
