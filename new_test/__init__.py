import os
import sys

print('here')

cwd = os.getcwd()

arbi_agent_path = '\\'.join(cwd.split("\\")[:-1])

if arbi_agent_path not in sys.path:
    sys.path.append(arbi_agent_path)
