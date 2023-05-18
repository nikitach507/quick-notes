from database.notes_database_action import NotesDatabaseAction
from lib_imports import Literal, Optional, Text, messagebox


class NoteDataSaver:
    """
    A class that handles saving and adding data to the database.
    """

    @staticmethod
    def saving_received_data(
            action: Literal["save", "update"],
            save_name_form: Text,
            save_desc_form: Text,
            current_category: str,
            nested_data: dict,
            allowed_characters_name: int,
            allowed_characters_desc: int,
            note_id: Optional[int] = None,
    ):
        """
        Handles the action of saving or updating data in the database.

        Args:
            action (str): The action to perform (either "save" or "update").
            save_name_form (tkinter.Text): The form field for the name of the note.
            save_desc_form (tkinter.Text): The form field for the description of the note.
            current_category (str): The selected category for the note.
            nested_data (dict): Nested data structure containing additional data.
            allowed_characters_name (int): The maximum number of characters allowed
            for the name.
            allowed_characters_desc (int): The maximum number of characters allowed
            for the description.
            note_id (Optional[int]): The ID of the note (for update action), defaults to None.
        """
        validate_input_length = (
                len(save_name_form.get("1.0", "end-1c")) <= allowed_characters_name
                and len(save_desc_form.get("1.0", "end-1c")) <= allowed_characters_desc)

        if validate_input_length:
            if NoteDataSaver.presence_check_necessary_data(
                    save_name_form, current_category):
                get_input_data = NoteDataSaver._get_input_data(
                    nested_data, current_category, action)
                note = NotesDatabaseAction(
                    get_input_data["note_name"],
                    get_input_data["note_description"],
                    get_input_data["note_category"],
                )
                # Adding to the database
                if action == "save":
                    note.add_note("notes_info")
                elif action == "update":
                    note.edit_note(table_name="notes_info", note_id=note_id)
                    return True
        else:
            NoteDataSaver._check_number_of_characters(
                save_name_form,
                save_desc_form,
                allowed_characters_name,
                allowed_characters_desc,
            )

    @staticmethod
    def presence_check_necessary_data(save_name_form: Text, name_category: str):
        """
        Checks if the necessary data (name and category) are present.

        Args:
            save_name_form (tkinter.Text): The form field for the name of the note.
            name_category (str): The selected category for the note.

        Returns:
            bool: True if both name and category are present, False otherwise.
        """
        # Function to check the note title and category
        if len(save_name_form.get("1.0", "end-1c")) == 0 or name_category == "":
            messagebox.showerror(
                "Error",
                "The main condition for creating a note is to write "
                "a title and select a category",
            )
            return False
        return True

    @staticmethod
    def _get_input_data(nested_data: dict, current_category: str, action: str):
        """
        Extracts the input data from the form fields and returns a dictionary.

        Args:
            nested_data (dict): Nested data structure containing additional data.
            current_category (str): The selected category for the note.
            action (str): The action to perform (either "save" or "update").

        Returns:
            get_input_data (dict): A dictionary containing the input data.
        """
        get_input_data = {}
        for name_column, data_column in nested_data.items():
            get_input_data[name_column] = data_column.get("1.0", "end-1c")
            get_input_data["note_category"] = current_category
            if action == "save":
                data_column.delete("1.0", "end")
        return get_input_data

    @staticmethod
    def _check_number_of_characters(
            save_name_form: Text,
            save_desc_form: Text,
            allowed_characters_name: int,
            allowed_characters_desc: int,
    ):
        """
        Checks if the length of the name and description exceeds the maximum allowed characters.

        Args:
            save_name_form (Text): The form field for the name of the note.
            save_desc_form (Text): The form field for the description of the note.
            allowed_characters_name (int): The maximum number of characters allowed
            for the name.
            allowed_characters_desc (int): The maximum number of characters allowed
            for the description.
        """
        if len(save_name_form.get("1.0", "end-1c")) > allowed_characters_name:
            messagebox.showerror(
                "Error",
                f"The header must have a maximum of {allowed_characters_name} characters, "
                f"now you have {len(save_name_form.get('1.0', 'end-1c'))}",
            )
        elif len(save_desc_form.get("1.0", "end-1c")) > allowed_characters_desc:
            messagebox.showerror(
                "Error",
                f"The description must have a maximum of {allowed_characters_desc} characters, "
                f"now you have {len(save_desc_form.get('1.0', 'end-1c'))}",
            )
        return False
