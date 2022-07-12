import opcua
import time

# setup our server
server = opcua.Server()
server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")

# setup our own namespace, not really necessary but should as spec
uri = "http://examples.freeopcua.github.io"
idx = server.register_namespace(uri)

# get Objects node, this is where we should put our nodes
objects = server.get_objects_node()

# populating our address space
myobj = objects.add_object(idx, "MyObject")
myvar = myobj.add_variable(idx, "MyVariable", 6.7)
print(myvar.nodeid)
myvar.set_writable()  # Set MyVariable to be writable by clients

# starting!
server.start()
if __name__ == '__main__':
    try:
        count = 0
        while True:
            time.sleep(1)
            count += 0.1
            myvar.set_value(count)
    finally:
        # close connection, remove subcsriptions, etc
        server.stop()
