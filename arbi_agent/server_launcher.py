import xml.etree.ElementTree as ET

from arbi_agent.configuration import ServerLauncherConstants
from arbi_agent.framework import arbi_framework_server


class ServerLauncher:
    def __init__(self, *args):
        broker_port = ServerLauncherConstants.BROKER_PORT
        broker_host = ServerLauncherConstants.BROKER_HOST
        broker_name = ServerLauncherConstants.BROKER_NAME
        broker_type = ServerLauncherConstants.BROKER_TYPE
        configuration_path = ServerLauncherConstants.DEFAULT_CONFIGURATION_LOCATION
        center_url = None

        if len(args) > 0:
            configuration_path = args[0]

        tree = ET.parse(configuration_path)
        configuration_element = tree.getroot()
        broker_property_element = configuration_element.find("MessageBrokerProperty")
        if broker_property_element is not None:
            broker_port = broker_property_element.find("Port").text
            broker_host = broker_property_element.find("Host").text
            broker_name = broker_property_element.find("Name").text
            if broker_property_element.attrib["Center"].lower() == "true":
                broker_type = 0
            else:
                broker_type = 2

        center_router_element = configuration_element.find("RouterProperty")
        if center_router_element is not None:
            port = center_router_element.find("Port").text
            host = center_router_element.find("Host").text
            center_url = "tcp://" + host + ":" + str(port)

        broker_url = "tcp://" + broker_host + ":" + str(broker_port)

        print("Broker URL :", broker_url)
        print("Center URL : ", center_url)

        server = arbi_framework_server.ArbiFrameworkServer(server_name=broker_name, broker_type=broker_type)
        server.start(broker_url=broker_url, center_url=center_url)


if __name__ == "__main__":
    ServerLauncher()
    input()
