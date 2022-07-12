import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="prometheus_opcua_exporter",
    version="1.0.0",
    author="Sebastian Heppner",
    author_email="s.heppner@plt.rwth-aachen.de",
    description="An OPC-UA Exporter for Prometheus based on the official Python prometheus-client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=["opcua_exporter"]
)
