import os

file = os.path.abspath(__file__)

project_dir = os.path.dirname(file)
parent_dir = os.path.dirname(project_dir)
print(parent_dir)