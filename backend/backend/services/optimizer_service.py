import os

from backend.models.Task import Task
from backend.models.Node import Node
from backend.models.Cell import Cell
from backend.services.db_service import get_all_entries, get_entry_by_id
from backend.services.file_handle_service import get_file_content
from backend.services.fuzzy_control.fuzzyIntegrated import FuzzyIntegrated


def optimize_model():
    # Get JSON from database
    optimizer_input = get_file_content("_ProcessGraph").content
    # Iterate over nodes
    