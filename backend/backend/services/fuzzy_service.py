import os

from backend.models.Task import Task
from backend.models.Node import Node
from backend.models.Cell import Cell
from backend.services.db_service import get_all_entries, get_entry_by_id
from backend.services.fuzzy_control.fuzzyIntegrated import FuzzyIntegrated

XMLpath = "backend/services/fuzzy_control/xml_data"


def calculate_kpi_fuzzy():
    # Get list of Nodes to iterate over
    fzy = FuzzyIntegrated()
    fzy.fuzzyLogic(os.path.join(os.getcwd(), XMLpath))
    nodes = get_all_entries(db_class=Node)
    # Iterate over nodes
    for node in nodes:
        task = get_entry_by_id(Task, node.task_id)  # get Task from ID
        cell = get_entry_by_id(Cell, node.cell_id)  # get Cell from ID
        node.update_by_fuzzy(fzy.evaluateTimeKPI(task.get(), cell.get()))
    return {"success": True}