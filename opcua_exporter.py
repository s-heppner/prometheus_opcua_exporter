import configparser
import os
import sys
import time
from typing import List
import dataclasses
import csv

import opcua
import prometheus_client


config = configparser.ConfigParser()
if len(sys.argv) > 1:
    # A config dir was provided
    config.read(sys.argv[1])
else:
    # Choose the default config location
    config.read((
        os.path.join(os.path.dirname(__file__), "config.ini"),
        os.path.join(os.path.dirname(__file__), "config.ini.default")
    ))

# Read in all the configuration variables
SERVER_PORT = int(config["GENERAL"]["port"])
REFRESH_TIME = int(config["GENERAL"]["refresh_time"])
OPCUA_SERVER_ADDRESS = config["GENERAL"]["opcua_server_address"]
NODE_CONFIG_FILE = config["GENERAL"]["node_config_file"]


@dataclasses.dataclass
class OPCUAGauge:
    metric_name: str
    node_path: str
    gauge: prometheus_client.Gauge


# Read in the nodes
GAUGES: List[OPCUAGauge] = []
with open(NODE_CONFIG_FILE, "r") as file:
    reader = csv.DictReader(file, delimiter=";")
    for row in reader:
        if row["NodeId.Identifier"] == "":
            continue  # Skip empty lines
        node_path: str = row["NodeId.Identifier"]
        display_name: str = row["DisplayName"]
        description: str = row["Description"]
        metric_name: str = row["Prometheus Metric Name"]
        documentation: str = f"{node_path} - {description}"
        GAUGES.append(OPCUAGauge(metric_name, node_path, prometheus_client.Gauge(metric_name, documentation)))


def update_metric_value(opcua_gauge: OPCUAGauge, opcua_client: opcua.Client):
    """
    Update the metric with the given name
    """
    try:
        opcua_node = opcua_client.get_node(opcua_gauge.node_path)
        current_value = opcua_node.get_value()
    except Exception as e:
        print("Could not get node value of {}: {}".format(opcua_gauge.node_path, e))
        return
    opcua_gauge.gauge.set(current_value)


def update_all_metrics():
    try:
        opcua_client = opcua.Client(OPCUA_SERVER_ADDRESS)
        opcua_client.connect()
    except Exception as e:
        print("Could not connect to OPC-UA Server: {}".format(e))
        return
    for opcua_gauge in GAUGES:
        update_metric_value(opcua_gauge, opcua_client)
    opcua_client.disconnect()


if __name__ == '__main__':
    print("Found the following gauges:")
    for gauge in GAUGES:
        print(gauge)
    prometheus_client.start_http_server(SERVER_PORT)
    while True:
        print("Updating Nodes")
        update_all_metrics()
        print("Waiting {} seconds".format(REFRESH_TIME))
        time.sleep(REFRESH_TIME)
