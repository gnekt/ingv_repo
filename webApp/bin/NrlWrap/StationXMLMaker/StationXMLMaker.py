import obspy
from obspy.core.inventory import Inventory, Network, Station, Channel, Site
from obspy.clients.nrl.client import LocalNRL
from bin.NrlWrap.NRLWrap import NRLWrap
from obspy import read
import json
import os
import numpy


class StationXMLMaker:
    """
    A class used to represent a Station in therm of XML
    ...
    Attributes
    ----------
    my_nrl : NRLWrap
        the connection to the NRL database
    channels : list<Channel>
        the station's channel

    network :

    Methods
    -------
    get_channels()
        Return the channels of the station

    get_inventory()
        Return the inventory of the station

    get_
    """

    def __init__(self, root=".\\res"):
        if not os.path.exists(root):
            os.mkdir(root)
        self.my_nrl = NRLWrap(root)

    def get_channels(self):
        raise NotImplementedError

    def get_inventory(self):
        raise NotImplementedError

    def get_network(self):
        raise NotImplementedError

    def get_station(self):
        raise NotImplementedError

    def set_network(self):
        raise NotImplementedError

    def set_inventory(self):
        raise NotImplementedError

    def set_station(self):
        raise NotImplementedError

    def set_channel(self):
        raise NotImplementedError

    def make_xml(self, p_format="stationxml", p_validate=True, p_file_name="debug.xml"):
        self.network.stations.append(self.station)
        self.inventory.networks.append(self.network)
        self.inventory.write(p_file_name, format=p_format, validate=p_validate)




class JsonToStationXML(StationXMLMaker):
    def __init__(self, p_json_file):
        super(JsonToStationXML, self).__init__()
        reader = json.load(p_json_file)
        self.json_station = reader["Station"]
        # Initialization of attribute's station
        self.inventory = None
        self.network = None
        self.station = None
        self.channels = None
        # Initialization raw information about every attributes
        self.inventory_raw = None
        self.network_raw = None
        self.station_raw = None
        self.channels_raw = None
        #
        self.set_inventory()
        self.set_station()
        self.set_channel()
        self.set_network()

    def get_channels(self):
        return self.json_station["channels"]

    def get_inventory(self):
        return self.json_station["inventory"]

    def get_network(self):
        return self.json_station["network"]

    def get_station(self):
        return self.json_station["station"]

    def set_network(self):
        self.network_raw = self.get_network()
        self.network = Network(code=self.network_raw["code"], stations=[], description=self.network_raw["description"],
                               start_date=obspy.UTCDateTime(self.network_raw["start_date"]))

    def set_inventory(self):
        self.inventory_raw = self.get_inventory()
        self.inventory = Inventory(networks=[], source=self.inventory_raw["creator"])

    def set_station(self):
        self.station_raw = self.get_station()
        self.station = Station(code=self.station_raw["name"], latitude=self.station_raw["latitude"],
                               longitude=self.station_raw["longitude"], elevation=self.station_raw["elevation"],
                               creation_date=obspy.UTCDateTime(self.station_raw["creation_date"]),
                               site=Site(name=self.station_raw["site_name"]))

    def set_channel(self):
        self.channels = []
        self.channels_raw = self.get_channels()
        p_datalogger = ()
        p_sensor = ()
        for channel in self.channels_raw:
            temp_channel = Channel(code=channel["code"], location_code=channel["location_code"],
                                   latitude=channel["latitude"], longitude=channel["longitude"],
                                   elevation=channel["elevation"], depth=channel["depth"],
                                   azimuth=channel["azimuth"], dip=channel["dip"], sample_rate=channel["sample_rate"])

            temp_list = []
            for value in channel["datalogger"].values():
                if not value is None:
                    temp_list.append(value)
            p_datalogger = tuple(temp_list)
            temp_list.clear()
            for value in channel["sensor"].values():
                if not value is None:
                    temp_list.append(value)
            p_sensor = tuple(temp_list)
            temp_channel.response = self.my_nrl.get_response(datalogger_keys=p_datalogger, sensor_keys=p_sensor)
            self.station.channels.append(temp_channel)


class NRLToStationXML(StationXMLMaker):
    def __init__(self,root):
        super(NRLToStationXML, self).__init__(root)
        self.inventory = None
        self.network = None
        self.station = None
        self.channels = None
        # Initialization raw information about every attributes
        self.inventory_raw = None
        self.network_raw = None
        self.station_raw = None
        self.channels_raw = None

        self.channels = []

    def get_channels(self):
        return self.channels

    def get_inventory(self):
        return self.inventory

    def get_network(self):
        return self.network

    def get_station(self):
        return self.station

    def set_network(self, code="", description="", start_date="2020,2,1,0,0,0.00"):
        self.network_raw = {"code": code, "description": description, "start_date": start_date}
        self.network = Network(code=self.network_raw["code"], stations=[], description=self.network_raw["description"],
                               start_date=obspy.UTCDateTime(self.network_raw["start_date"]))

    def set_inventory(self, p_creator=""):
        self.inventory_raw = {"creator": p_creator}
        self.inventory = Inventory(networks=[], source=self.inventory_raw["creator"])

    def set_station(self, p_name="", p_latitude=0, p_longitude=0, p_elevation=0, p_creation_date="2020,2,1,0,0,0.00",
                    p_site_name=""):
        self.station_raw = {"name": p_name, "latitude": p_latitude, "longitude": p_longitude, "elevation": p_elevation,
                            "creation_date": p_creation_date, "site_name": p_site_name}
        self.station = Station(code=self.station_raw["name"], latitude=self.station_raw["latitude"],
                               longitude=self.station_raw["longitude"], elevation=self.station_raw["elevation"],
                               creation_date=obspy.UTCDateTime(self.station_raw["creation_date"]),
                               site=Site(name=self.station_raw["site_name"]))

    def set_channel(self, p_code="", p_location_code="", p_latitude=0, p_longitude=0, p_elevation=0, p_depth=0,
                    p_azimuth=0, p_dip=0, p_sample_rate=0, p_sensor=None, p_datalogger=None):
        self.channels_raw = {"code": p_code, "location_code": p_location_code, "latitude": p_latitude,
                             "longitude": p_longitude, "elevation": p_elevation, "depth": p_depth, "azimuth": p_azimuth,
                             "dip": p_dip, "sample_rate": p_sample_rate, "sensor": p_sensor, "datalogger": p_datalogger}

        temp_channel = Channel(code=self.channels_raw["code"], location_code=self.channels_raw["location_code"],
                               latitude=self.channels_raw["latitude"], longitude=self.channels_raw["longitude"],
                               elevation=self.channels_raw["elevation"], depth=self.channels_raw["depth"],
                               azimuth=self.channels_raw["azimuth"], dip=self.channels_raw["dip"],
                               sample_rate=self.channels_raw["sample_rate"])
        temp_channel.response = self.my_nrl.get_response(datalogger_keys=p_datalogger, sensor_keys=p_sensor)
        self.channels.append(temp_channel)

    def make_xml(self, p_format="stationxml", p_validate=True, p_file_name="debug.xml"):
        if isinstance(self, NRLToStationXML):
            for temp_channel in self.channels:
                self.station.channels.append(temp_channel)
        super().make_xml(p_format, p_validate, p_file_name)
