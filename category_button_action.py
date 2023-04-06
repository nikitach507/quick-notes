import tkinter

from database.category_database_action import CategoryDatabaseAction
from main import *


class CategoryButtonAction:
    def __init__(self, root):
        self.root = root
        self.active_item = 0
        self.side_listbox_categories = None
        self.side_listbox_active_category = None
        self.permissible_action = ["side_list", "general_list"]