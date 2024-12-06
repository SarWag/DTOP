# from requests.auth import HTTPBasicAuth
# from assistant_project.graphdb import GraphDB
# import json
#
# # For development purposes only: Setup credentials --> Otherwise get from database or config file
# serverpath = "http://assistant-wp6.westeurope.cloudapp.azure.com:7200/"
# repository = 'AssistantWP3'
# graph = 'http://www.openrdf.org/schema/sesame#nil'
# # Authentication
# username = 'Assistant'
# password = 'WP345Sync'
# credentials = HTTPBasicAuth(username, password)
# gdb = GraphDB(serverpath, credentials)
#
#
# def import_json():
#     with open('ProcessGraph1_2.json') as json_file:
#         data = json.load(json_file)
#     return data
#
#
# # Global variables:
# process_graph = import_json()
#
#
# def get_start_modules(node):
#     assembly = node["StartAssembly"][0]
#     return assembly["StartModule1"], assembly["StartModule2"]
#
#
#
# def get_tasks_service():
#     return True
#     # tasks = []
#     # for node in process_graph["Node"]:
#     #     task_id = node["TaskID"]
#     #     node_id = node["NodeID"]
#     #     start_module1, start_module2 = get_start_modules(node)
#         # task = {"TaskID": task_id, "NodeID"}
#         # if not tasks.keys().__contains__(task_id):
#         #     Create list for task ID
#             # tasks[task_id] = []
#         # tasks[task_id].append(task)
#
#
# # {
# #     "tasks": [
# #         {
# #             'TaskID': 1,
# #             'StartAssembly_1': "...",
# #             'StartAssembly_2': "...",
# #             'Tasktype': "..."
# #         },
# #         {
# #             'TaskID': 2,
# #             'StartAssembly_1': "...",
# #             'StartAssembly_2': "...",
# #             'Tasktype': "..."
# #         }
# #     ]
#
#
# # }
#
