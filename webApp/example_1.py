from bin.NrlWrap.StationXMLMaker.StationXMLMaker import NRLToStationXML,JsonToStationXML
from bin.Utils import Utils
from bin.Utils.Utils import *

myStation = NRLToStationXML(retrieve_config_value(["application","module_configuration","NRLWrap","root"]))
myStation.set_inventory("INGV")
myStation.set_network("UM","TEST","2020,2,1,0,0,0.00")
myStation.set_station("TEST",-38.22918,147.274075,26,"2020,2,1,0,0,0.00","Naples")
a = ["Guralp","CMG-40T","60s - 100Hz","800"]
b = ["Custom","Gilda"]
myStation.set_channel("HHZ","",-38.22918,147.274075,26,0,90,0,250,p_sensor=a,p_datalogger=b)
# dwawewrwerwerer
myStation.make_xml(p_file_name="nrl_test.xml")
myStation.make_xml(p_file_name="nrl_test.xml")
myStation = None
myStation = JsonToStationXML(open("station.json","r"))
myStation.make_xml(p_file_name="json-test.xml")



