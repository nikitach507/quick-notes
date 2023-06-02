import hashlib
import os
import re

from lib_imports import *
from database.user_database_action import UserDatabaseAction


class RegistrationUser:
    def __init__(self, side_window, main_window, operation_buttons_window, auth_user_object):
        self.side_frame = side_window
        self.main_frame = main_window
        self.operation_buttons_frame = operation_buttons_window
        self.auth_user_object = auth_user_object
        self.label = None
        self.entry = None
        self.block_side_frame_message = None
        self.error_message = None

    def user_create(self, obj_main_app):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        if not self.block_side_frame_message:
            self.block_side_frame_message = Label(self.side_frame, text="LOG IN\nOR\nSIGN UP\n\nFOR QUICK NOTES",
                                                  bg=PALETTE["main"]["2color"],
                                                  fg=PALETTE["text"]["1color"],
                                                  font=("Impact", 20, "bold"),
                                                  )
            self.block_side_frame_message.place(x=25, y=245)

        create_account_frame = Frame(self.main_frame, bg=PALETTE["main"]["1color"],
                                     borderwidth=1, relief="solid",
                                     width=600, height=350,
                                     padx=60, pady=30)
        create_account_frame.place(x=90, y=85)

        label_title = Label(create_account_frame, text="Create an account",
                            bg=PALETTE["main"]["1color"],
                            font=("Impact", 22))
        label_title.place(x=0, y=0)

        account_fields = [
            ("First Name", 70),
            ("Last Name", 120),
            ("Email", 170),
            ("Password", 220)
        ]

        input_account_info = []
        for name_label, y_pos in account_fields:
            text_label = Label(create_account_frame, text=name_label + ":",
                               bg=PALETTE["main"]["1color"],
                               font=("Impact", 16))
            text_label.place(x=0, y=y_pos, anchor="w")

            data_entry = Entry(create_account_frame, width=40,
                               bg=PALETTE["main"]["1color"],
                               border=1, relief="flat",
                               highlightthickness=2,
                               font=("Arial", 16),
                               highlightbackground=PALETTE["main"]["3color"],
                               highlightcolor=PALETTE["main"]["3color"])
            data_entry.place(x=95, y=y_pos + 2, anchor="w")
            input_account_info.append(data_entry)

        comm_create = lambda: self.create_account(input_account_info[0], input_account_info[1],
                                                  input_account_info[2], input_account_info[3],
                                                  obj_main_app)
        # Кнопка "Create account"
        button_create_account = Button(create_account_frame, text="Create account",
                                       bg=PALETTE["secondary"]["1color"],
                                       fg=PALETTE["text"]["1color"],
                                       font=("Arial", 14),
                                       width=190,
                                       command=comm_create)
        button_create_account.place(x=275, y=265,anchor="w")

        # Текст "Already have an account? Log in"
        label_login = Label(create_account_frame, text="Already have an account? ",
                            bg=PALETTE["main"]["1color"],
                            font=("Arial", 14))
        label_login.place(x=0, y=265, anchor="w")

        # Ссылка (или кнопка) "Log in"
        button_login = Button(create_account_frame, text="Log in", relief="flat",
                              bg=PALETTE["secondary"]["4color"],
                              fg=PALETTE["text"]["1color"],
                              font=("Arial", 14),
                              cursor="hand2",
                              command=self.auth_user_object.user_auth
                              )
        button_login.place(x=175, y=265, anchor="w")

    def create_account(self, first, last, email, password, obj_main_app):
        first_name = first.get()
        last_name = last.get()
        email_data = email.get()

        if self._check_availability_input_data(first_name, last_name, email_data, password.get()):
            password_hash = hashlib.sha256(password.get().encode()).hexdigest()

            salt = os.urandom(16).hex()

            UserDatabaseAction.add_user_info("users", email_data, password_hash,
                                             salt, first_name, last_name)
            obj_main_app.user_auth(after_reg=email_data)

    def _check_availability_input_data(self, first, last, email, password):
        all_data = {
            "First name": first,
            "Last name": last,
            "Email": email,
            "Password": password
        }

        if self.error_message:
            self.error_message.destroy()
        for name, data in all_data.items():
            if data == "":
                message = f"The '{name}' range must be either 1 or 256 characters long.\n" \
                          f"Currently {len(data)} characters"
                self._draw_error_message(message)
                return False
            if name == "Email":
                if not "@" in data:
                    message = f"Please enter the correct email"
                    self._draw_error_message(message)
                    return False
                all_data_in_email = UserDatabaseAction.output_all_data_in_column("users", "email")
                if data in all_data_in_email:
                    message = f"This email '{data}' is already registered in the system"
                    self._draw_error_message(message)
                    return False
            if name == "Password":
                password_regex = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[A-Za-z\d]{8,}$"
                if not re.match(password_regex, data):
                    message = "The password must meet the following requirements:\n" \
                              "- At least 8 characters long\n" \
                              "- Contains at least 1 uppercase letter\n" \
                              "- Contains at least 1 lowercase letter\n" \
                              "- Contains at least 1 digit"
                    self._draw_error_message(message)
                    return False
        return True

    def _draw_error_message(self, text):
        self.error_message = Label(self.main_frame, text=text,
                                   width=66,
                                   bg=PALETTE["secondary"]["4color"],
                                   border=1, relief="flat")
        self.error_message.place(x=91, y=435)