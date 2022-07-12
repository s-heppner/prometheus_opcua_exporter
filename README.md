# prometheus_opcua_exporter
OPC-UA Exporter for Prometheus using 
[python-opcua](https://github.com/FreeOpcUa/python-opcua) 
and [prometheus_client](https://github.com/prometheus/client_python)


## Try it out yourself

For your convenience and to show how to configure this exporter, this repository comes with an example OPCUA Server.
This way, you can very quickly set it up:

- Install the requirements
  `pip3 install -r requirements.txt`
- Start the example server
  `python3 example_server.py`
- Start the prometheus exporter
  `python3 opcua_exporter.py`
- Navigate to [http://localhost:8000](http://localhost:8000)
- Refresh after 15 seconds and notice, how the value of the `example_variable` increased

## How to Use:

Modify `config.ini` to suit your needs

Enter the nodes you want to collect into the `node_config.csv` file. 
It is important, that you do not change the first line.
Format is the following:

  - `NodePath`: String Path to the Node
  - `MetricName`: Name of the metric in Prometheus. Must match the regex `[a-zA-Z_:][a-zA-Z0-9_:]*`. 
    For more information, see the [Prometheus Documentation](https://prometheus.io/docs/practices/naming/) on that topic
  - `Documentation`: A descriptive string of what this metric means. Cannot contain a `,` (since it's the 
    separator in the csv)

Then, you can run the `opcua_exporter.py`. 


## Run as a Service

Todo: Describe how to Run as a Service


