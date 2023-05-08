import logging
import sys
from tkinter import *
from tkinter.ttk import Combobox
from tkinter.ttk import Style

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
        self.update_button = None
        self.note_sorting = "newest"
        self.pop_up_buttons = {}
        self.previous_actions = set()
        self.operation_button_add = OperationButtonAdd(self.main_win, self.pop_up_buttons)
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

        self.side_listbox_categories = Listbox(side_frame_categories, width=15,
                                               fg=QuickNotesApp.PALETTE["text"]["1color"],
                                               font=("Arial", 20), relief='flat',
                                               bg=QuickNotesApp.PALETTE["main"]["2color"]
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
        self.operation_button_add.add_note_button()

    def create_operation_button(self, button_symbol, button_action, x_button):
        operating_button_command = lambda: button_action()
        self.created_oper_button = Button(self.upper_win, text=f"{button_symbol}",
                                          bg=QuickNotesApp.PALETTE["main"]["1color"],
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

        def change_active_data_color(labels_list, active_note, active_id):
            if len(self.pop_up_buttons) == 2:
                for button in self.pop_up_buttons.values():
                    button.destroy()
            delete_note_lambda = lambda id=active_id, object=app, current_cat=note_category: \
                self.operation_button_delete.delete_note_button(id, object, current_cat)
            window_note_lambda = lambda note_data_label=active_note: \
                self.operation_button_delete.open_new_window(note_data_label)
            self.create_operation_button(button_symbol="delete the note", button_action=delete_note_lambda,
                                         x_button=self.x_note_buttons)
            self.create_operation_button(button_symbol="note window", button_action=window_note_lambda,
                                         x_button=self.x_note_buttons + 130)

            # Go around all the data on frame and change the color of all but the current one
            for child in frame_to_display.winfo_children():
                if isinstance(child, Label):

                    if child.cget('bg') == QuickNotesApp.PALETTE["main"]["3color"] and child in labels_list:
                        for label in active_note.winfo_children()[3:-1]:
                            label.config(bg=QuickNotesApp.PALETTE["main"]["1color"])
                        child.config(bg=QuickNotesApp.PALETTE["main"]["1color"])
                    else:
                        for label in child.winfo_children()[3:-1]:
                            label.config(bg=QuickNotesApp.PALETTE["main"]["3color"])
                        child.config(bg=QuickNotesApp.PALETTE["main"]["3color"])

        def handle_combobox(event, current_category):
            selected = combo.current()
            if selected == 0:
                combo.current(0)
                self.note_sorting = "newest"
            elif selected == 1:
                combo.current(1)
                self.note_sorting = "oldest"
            elif selected == 2:
                combo.current(2)
                self.note_sorting = "atoz"
            elif selected == 3:
                combo.current(3)
                self.note_sorting = "ztoa"
            self.note_display_interface(current_category)

        for widget in self.main_win.winfo_children():
            widget.destroy()

        # Create an area to display notes
        self.notes_display_frame = Frame(self.main_win, bg=QuickNotesApp.PALETTE["main"]["3color"])
        self.notes_display_frame.grid(row=0, column=0, padx=10, pady=10)
        values = ['by creation date (newest)',
                  'by creation date (oldest)',
                  'by name (A to Z)',
                  'by name (Z to A)']

        # name = Label(self.notes_display_frame, text=note_category, width=50)
        # name.pack(side="left", expand=True)
        # Создание Combobox
        combo = Combobox(self.notes_display_frame, values=values)
        combo.configure(background=QuickNotesApp.PALETTE["main"]["3color"], state="readonly")

        combo.bind("<<ComboboxSelected>>", lambda event, current_cat=note_category: handle_combobox(event, current_cat))
        if self.note_sorting == "newest":
            combo.current(0)
        elif  self.note_sorting == "oldest":
            combo.current(1)
        elif self.note_sorting == "atoz":
            combo.current(2)
        elif  self.note_sorting == "ztoa":
            combo.current(3)

        combo.pack(padx=5)
        # Create a Scrollbar and create a Canvas for this
        notes_canvas = Canvas(self.notes_display_frame, width=765, height=525)
        scrollbar_for_notes_canvas = Scrollbar(self.notes_display_frame, orient="vertical",
                                               command=notes_canvas.yview)
        notes_canvas.configure(yscrollcommand=scrollbar_for_notes_canvas.set,
                               bg=QuickNotesApp.PALETTE["main"]["3color"], borderwidth=0, highlightthickness=0)
        notes_canvas.pack(side="left", fill="both", expand=True, pady=1)

        # Отображение Combobox

        # Create a frame to display data on canvas
        frame_to_display = Frame(notes_canvas)
        frame_to_display.configure(bg=QuickNotesApp.PALETTE["main"]["3color"])
        frame_to_display.bind("<Configure>",
                              lambda e: notes_canvas.configure(scrollregion=notes_canvas.bbox("all")))
        notes_canvas.create_window((0, 0), window=frame_to_display, anchor="nw")

        # Getting all notes into a list from the database
        all_database_notes = NotesDatabaseAction.select_all_notes(table_name="notes_info", category=note_category,
                                                                  sorting=self.note_sorting)
        if len(all_database_notes) > 5:
            scrollbar_for_notes_canvas.pack(side="right", fill="y")

        all_note_data = list()
        # Write out all the data in the frame
        for note_num in range(len(all_database_notes)):
            note_frame = Label(frame_to_display)
            note_frame.configure(bg=QuickNotesApp.PALETTE["main"]["3color"])

            index_frame = Label(note_frame, text=f"{all_database_notes[note_num]['id']}")

            category_label = Label(note_frame, text=f"{all_database_notes[note_num]['note_category']}",
                                   font=("Arial bold", 13),
                                   bg=QuickNotesApp.PALETTE["secondary"]["1color"],
                                   fg=QuickNotesApp.PALETTE["main"]["3color"],
                                   anchor="nw")

            datetime_label = Label(note_frame, text=f"{str(all_database_notes[note_num]['created_at'])[:10]}",
                                   font=("Arial bold", 13),
                                   bg=QuickNotesApp.PALETTE["secondary"]["1color"],
                                   fg=QuickNotesApp.PALETTE["main"]["3color"],
                                   anchor="nw")
            line_spacing_cleanup_name = ' '.join(all_database_notes[note_num]['note_name'][:56].split())
            if len(all_database_notes[note_num]['note_name']) > 56:
                line_spacing_cleanup_name += "..."
            # Second row with title
            title_label = Label(note_frame, text=f"{line_spacing_cleanup_name}", font=("Arial", 16, "bold"),
                                bg=QuickNotesApp.PALETTE["main"]["3color"], fg="white",
                                anchor="nw")
            line_spacing_cleanup = ' '.join(all_database_notes[note_num]['note_description'][:80].split())
            if len(all_database_notes[note_num]['note_description']) > 80:
                line_spacing_cleanup += "..."
            # Third row with description
            description_label = Label(note_frame, text=f"{line_spacing_cleanup}",
                                      bg=QuickNotesApp.PALETTE["main"]["3color"], font=("Arial", 12),
                                      anchor="nw")

            empty_cell = Frame(note_frame, width=755, height=2, bg=QuickNotesApp.PALETTE["main"]["1color"])

            category_label.grid(row=0, column=0, padx=2, pady=2, sticky="w")
            datetime_label.grid(row=0, column=1, sticky="e", padx=2, pady=2)  # ne
            title_label.grid(row=1, column=0, columnspan=2, pady=10, sticky="w")
            description_label.grid(row=2, column=0, columnspan=2, sticky="w")
            empty_cell.grid(row=3, column=0, columnspan=2, pady=5, sticky="news")

            all_note_data.append(note_frame)
            for place in (note_frame, title_label):
                place.bind("<Button-1>",
                           lambda event, labels=tuple(all_note_data),
                                  active_note=note_frame,
                                  active_id=all_database_notes[note_num]['id']: change_active_data_color(
                               labels, active_note, active_id))
                place.bind("<Double-Button-1>",
                           lambda event, active_note=note_frame: self.open_note_information(
                               active_note.winfo_children()[0].cget("text")))
                # place.bind("<Button-1>",
                #            lambda event, active_note=note_frame: self.open_note_information(
                #                active_note.winfo_children()[0].cget("text")))

            note_frame.pack(anchor="nw")
            all_note_data.clear()

        for pop_up_button in self.pop_up_buttons.values():
            pop_up_button.destroy()

    def open_note_information(self, note_id):
        def check_changes(text_area):
            column_of_change = "note_description" if text_area == desc_text_area else "note_name"
            current_content = text_area.get("1.0", "end-1c")
            original_content = info_note[0][column_of_change]
            if current_content != original_content:
                self.update_button.config(state="normal", bg=QuickNotesApp.PALETTE["secondary"]["1color"],
                                          fg=QuickNotesApp.PALETTE["text"]["1color"])
                self.previous_actions.add(column_of_change)
            elif len(self.previous_actions) == 1 and column_of_change in self.previous_actions:
                self.update_button.config(state="disabled")
                self.previous_actions.remove(column_of_change)
            else:
                self.previous_actions.remove(column_of_change)

            truncators = {"note_name": variation_truncator_name, "note_description": variation_truncator_desc}

            for key_t, truncator in truncators.items():
                if not truncator.winfo_ismapped() and key_t in self.previous_actions:
                    truncator.place(x=605, y=77) if key_t == "note_name" else truncator.place(x=605, y=527)
                elif truncator.winfo_ismapped() and key_t not in self.previous_actions:
                    truncator.place_forget()


        for widget in self.main_win.winfo_children():
            widget.destroy()

        info_note = NotesDatabaseAction.select_note("notes_info", note_id)

        # Updating the notes interface area when categories change
        self.open_note_frame = Frame(self.main_win, bg=QuickNotesApp.PALETTE["main"]["1color"],
                                     highlightbackground=QuickNotesApp.PALETTE["main"]["1color"],
                                     highlightthickness=2, relief="flat",
                                     highlightcolor=QuickNotesApp.PALETTE["main"]["1color"])
        self.open_note_frame.pack(side="left", padx=5, pady=5, anchor="nw")
        self.supplementary_frame = Frame(self.main_win, bg=QuickNotesApp.PALETTE["main"]["3color"],
                          highlightthickness=0, relief="flat")
        self.supplementary_frame.pack(side="right", expand=True, padx=2, pady=5, anchor="nw")

        nested_data = {}
        self.previous_actions = set()

        name_text_area = Text(self.open_note_frame, height=3, relief="flat", width=43,
                              bg=QuickNotesApp.PALETTE["main"]["3color"],font=("Arial", 24, "bold"),
                              fg=QuickNotesApp.PALETTE["text"]["1color"], wrap="word",
                              highlightthickness=0, padx=10, pady=5)

        name_text_area.insert(INSERT, info_note[0]["note_name"])
        name_text_area.pack(anchor="nw")

        desc_text_area = Text(self.open_note_frame, height=19, width=67, wrap="word", font=("Arial", 16),
                              bg=QuickNotesApp.PALETTE["main"]["3color"], highlightthickness=0,
                              tabs=15, tabstyle="tabular", takefocus=False, padx=10, pady=5,
                              spacing1=5, undo=True
                              )
        desc_text_area.insert(INSERT, info_note[0]["note_description"])
        desc_text_area.pack(pady=4, anchor="nw")

        supplementary_info = {"Category": info_note[0]['note_category'].upper(),
                              "Date of addition": str(info_note[0]['created_at'])[:10],
                              "Time of addition": str(info_note[0]['created_at'])[10:]
                              }
        for title, info in supplementary_info.items():
            Label(self.supplementary_frame, text=title.upper(), width=16,
                  bg=QuickNotesApp.PALETTE["main"]["3color"],
                  fg=QuickNotesApp.PALETTE["text"]["2color"],
                  font=("Arial", 12, "bold"),
                  ).pack(pady=2)
            Label(self.supplementary_frame, text=info, width=16,
                  bg=QuickNotesApp.PALETTE["text"]["2color"],
                  fg=QuickNotesApp.PALETTE["main"]["3color"],
                  font=("Arial", 15, "bold"),
                  ).pack(pady=10)

        nested_data["note_name"] = name_text_area
        nested_data["note_description"] = desc_text_area

        number_allowed_characters_name = NotesDatabaseAction.select_number_characters("notes_info", "note_name")
        number_allowed_characters_desc = NotesDatabaseAction.select_number_characters("notes_info", "note_description")

        update_comm = lambda: (self.operation_button_add.saving_received_data("update", name_text_area, desc_text_area,
                                                                              info_note[0]["note_category"], nested_data,
                                                                              number_allowed_characters_name,
                                                                              number_allowed_characters_desc, note_id),
                               self.open_note_information(note_id))

        self.update_button = Button(self.main_win, text="Update", border=3, relief="flat",
                                    disabledforeground=QuickNotesApp.PALETTE["text"]["3color"],
                                    disabledbackground=QuickNotesApp.PALETTE["main"]["1color"],
                                    activebackground=QuickNotesApp.PALETTE["secondary"]["1color"],
                                    activeforeground=QuickNotesApp.PALETTE["text"]["2color"],
                                    state="disabled",
                                    command=update_comm)
        self.update_button.place(x=665, y=515)

        variation_truncator_name = Canvas(self.open_note_frame, width=15, height=15, bg=QuickNotesApp.PALETTE["main"]["3color"],
                                          highlightthickness=0, relief="flat")
        variation_truncator_desc = Canvas(self.open_note_frame, width=15, height=15,
                                          bg=QuickNotesApp.PALETTE["main"]["3color"],
                                          highlightthickness=0, relief="flat")
        # координаты вершин треугольника
        x1, y1 = 5, 15
        x2, y2 = 15, 15
        x3, y3 = 15, 5
        # canvas.place(x=10, y=10)
        # canvas.place(x=100, y=100)

        # нарисовать треугольник

        variation_truncator_name.create_polygon(x1, y1, x2, y2, x3, y3, fill=QuickNotesApp.PALETTE["secondary"]["1color"])
        variation_truncator_desc.create_polygon(x1, y1, x2, y2, x3, y3,
                                                fill=QuickNotesApp.PALETTE["secondary"]["1color"])

        name_text_area.bind("<KeyRelease>", lambda e: check_changes(name_text_area))
        desc_text_area.bind("<KeyRelease>", lambda e: check_changes(desc_text_area))



if __name__ == "__main__":
    """Creating a window and running the program"""
    win = Tk()
    win_w, win_h = 1000, 600
    win.title("Quick notes")
    win.geometry(f"{win_w}x{win_h}+200+150")
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

