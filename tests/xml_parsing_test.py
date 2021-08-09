import xml.etree.ElementTree as ET

tree = ET.parse("../configuration/ServerConfiguration.xml")

root = tree.getroot()

element = root.find("MessageBrokerProperty")

port = int(element.find("Port").text)

print(port)

print(bool(element.attrib["Center"]))

print(bool(root.find("InteractionManagerStart").text))


test = dict()
test["a"] = 1
tt = dict()
tt["b"] = 2
tt.update(test)
tt["a"] = 3
print(test)
