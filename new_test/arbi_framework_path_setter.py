import sys
import os

arbi_framework_dir = "\\".join(os.getcwd().split("\\")[:-1])
print(arbi_framework_dir)
sys.path.append(arbi_framework_dir)
print(sys.path)
