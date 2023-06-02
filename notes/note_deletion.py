from database.notes_database_action import NotesDatabaseAction
from lib_imports import *


class NoteDeletion:
    @staticmethod
    def delete_note_button(user_id, current_id: int):
        """
        Deletes a note from the database and updates the note display interface.

        Args:
            current_id (int): The ID of the note to be deleted.
        """
        answer = messagebox.askokcancel(
            "Delete Note", "Are you sure you want to delete the note?"
        )
        if answer:
            NotesDatabaseAction.delete_note("notes_info", user_id=user_id, note_id=current_id)