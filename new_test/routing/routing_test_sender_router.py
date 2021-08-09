from arbi_agent.server_launcher import ServerLauncher
import time

if __name__ == '__main__':
    launcher = ServerLauncher("../../configuration/RouterSenderConfiguration.xml")
    while True:
        time.sleep(1)

