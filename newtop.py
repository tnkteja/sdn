#! /usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI

#from pox import POX

class SingleSwitchTopo(Topo):
    """
    High-level API: The high-level API adds a topology template abstraction,
    the Topo class, which provides the ability to create reusable, parametrized
    topology templates. These templates can be passed to the mn command
    (via the --custom option) and used from the command line.
    """
    "Single switch connected to n hosts."

    def build(self, n=2):
        switch = self.addSwitch("s1")
        # Python's range(N) generates 0..N-1
        for h in xrange(n):
            #linkparams={"bw":10,"delay":'5ms',"loss":10,"max_queue_size":1000,"use_htb":True}
            linkparams={}
            """
            maximum queue size of 1000 packets using the Hierarchical Token Bucket rate limiter
            and netem delay/loss emulator. The parameter bw is expressed as a number in Mbit;
            delay is expressed as a string with units in place (e.g. '5ms', '100us', '1s');
            loss is expressed as a percentage (between 0 and 100); and max_queue_size is expressed in packets.
            """

            """
            Mid-level API: The mid-level API adds the Mininet object which
            serves as a container for nodes and links. It provides a number of
            methods (such as addHost(), addSwitch(), and addLink()) for adding
            nodes and links to a network, as well as network configuration,
            startup and shutdown (notably start() and stop().)
            """
            host = self.addHost("h%s"%h)
            self.addLink(host, switch,**linkparams)

"Create and test a simple network"
topo = SingleSwitchTopo()

net = Mininet(topo)
net.start()

dumphost= lambda h:  ("IP: "+h.IP(),"MAC: "+h.MAC()) if "MAC" in h.__dict__.keys() or "IP" in h.__dict__.keys() else None
print dumphost(net["h1"])
print net.keys()
print dumphost(net['c0'])

print "Dumping host connections"
dumpNodeConnections(net.hosts)

print "Testing network connectivity"
net.pingAll()

#Start mininet and hold on the  CLI
#CLI(net)
net.stop()
