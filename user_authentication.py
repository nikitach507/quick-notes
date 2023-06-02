import hashlib
import os

from database.user_database_action import UserDatabaseAction
from user_registration import RegistrationUser
from lib_imports import *


class AuthenticationUser:
    def __init__(self, side_window, main_window, operation_buttons_window):
        self.side_frame = side_window
        self.main_frame = main_window
        self.operation_buttons_frame = operation_buttons_window
        self.reg_user = RegistrationUser(
            self.side_frame, self.main_frame, self.operation_buttons_frame, self
        )
        self.label = None
        self.entry = None
        self.block_side_frame_message = None
        self.error_message = None
        self.user_id = None
        self.comm_create = False

    def user_auth(self, obj_main_app, after_reg):
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
                                     width=600, height=250,
                                     padx=60, pady=30)
        create_account_frame.place(x=90, y=145)

        label_title = Label(create_account_frame, text="Sign in to Quick Notes",
                            bg=PALETTE["main"]["1color"],
                            font=("Impact", 22))
        label_title.place(x=0, y=0)

        account_fields = [
            ("Email", 70),
            ("Password", 120)
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

            if name_label == "Email":
                if after_reg:
                    data_entry.insert(0, after_reg)

            if name_label == "Password":
                data_entry.configure(show="*")

            input_account_info.append(data_entry)

        comm_sign_in = lambda: self.check_user(input_account_info[0], input_account_info[1], obj_main_app)

        button_sign_in = Button(create_account_frame, text="Sign in",
                                bg=PALETTE["secondary"]["1color"],
                                fg=PALETTE["text"]["1color"],
                                font=("Arial", 14),
                                width=190,
                                command=comm_sign_in)
        button_sign_in.place(x=275, y=165, anchor="w")

        # Текст "Already have an account? Log in"
        label_sign_up = Label(create_account_frame, text="New to Quick Notes?",
                              bg=PALETTE["main"]["1color"],
                              font=("Arial", 14))
        label_sign_up.place(x=0, y=165, anchor="w")

        comm_create = lambda: self.reg_user.user_create(obj_main_app)
        button_sign_up = Button(create_account_frame, text="Sign up", relief="flat",
                                bg=PALETTE["secondary"]["4color"],
                                fg=PALETTE["text"]["1color"],
                                font=("Arial", 14),
                                cursor="hand2",
                                command=comm_create)
        button_sign_up.place(x=175, y=165, anchor="w")

    def check_user(self, email, password, obj_main_app):
        email_data = email.get()

        if self._check_input_data(email_data, password.get()):
            user_id = UserDatabaseAction.active_user_id("users", email_data)
            obj_main_app.user_id = user_id
            obj_main_app.create_app_interface(user_id)

    def _check_input_data(self, email, password):
        all_data = {
            "Email": email,
            "Password": password
        }
        if self.error_message:
            self.error_message.destroy()
        for name, data in all_data.items():
            all_data_in_email = UserDatabaseAction.output_all_data_in_column("users", "email")
            if name == "Email" and data not in all_data_in_email:
                message = f"Email or password is incorrect. Please try again."
                self._draw_error_message(message)
                return False
            else:
                password_info = UserDatabaseAction.output_user_hash_psw_salt("users", all_data["Email"])
                original_password_salt = password_info["password_hash"] + password_info["salt"]
                original_hash_user = hashlib.sha256(original_password_salt.encode()).hexdigest()

                current_password_hash = hashlib.sha256(all_data["Password"].encode()).hexdigest()
                current_password_salt = current_password_hash + password_info["salt"]
                current_hash_user = hashlib.sha256(current_password_salt.encode()).hexdigest()

                if current_hash_user != original_hash_user:
                    message = f"Email or password is incorrect. Please try again."
                    self._draw_error_message(message)
                    return False
        return True

    def _draw_error_message(self, text):
        self.error_message = Label(self.main_frame, text=text,
                                   width=66,
                                   bg=PALETTE["secondary"]["4color"],
                                   border=1, relief="flat")
        self.error_message.place(x=91, y=395)