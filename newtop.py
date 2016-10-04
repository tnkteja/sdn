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

"""
If you invoke the Mininet() constructor in your script without specifying a
controller class, by default it will use the Controller() class to create an
instance of the Stanford/OpenFlow reference controller, controller.
Like ovs-controller, it turns your switches into simple learning switches, but
if you have installed controller using Mininet's install.sh -f script, the
patched version of controller should support a large number of switches
(up to 4096 in theory, but you'll probably max out your computing resources
much earlier.) You can also select the reference controller for mn by specifying
--controller ref.
"""
net = Mininet(topo=SingleSwitchTopo())
"""
If you want to use your own controller, you can easily create a custom subclass
of Controller() and pass it into Mininet. An example can be seen in
mininet.controller.NOX(), which invokes NOX classic with a set of modules passed
in as options.
"""
class POXBridge( Controller ):
    "Custom Controller class to invoke POX forwarding.l2_learning"
    def start( self ):
        "Start POX learning switch"
        self.pox = '%s/pox/pox.py' % os.environ[ 'HOME' ]
        self.cmd( self.pox, 'forwarding.l2_learning &' )
    def stop( self ):
        "Stop POX"
        self.cmd( 'kill %' + self.pox )

net = Mininet( topo=SingleSwitchTopo(), controller=POXBridge )
"""
The RemoteController class acts as a proxy for a controller which may be running
anywhere on the control network, but which must be started up and shut down
manually or by some other mechanism outside of Mininet's direct control.
"""
#net = Mininet( topo=topo, controller=lambda name: RemoteController( name, ip='127.0.0.1' ) )
net.addController( 'c0', controller=RemoteController, ip='127.0.0.1', port=6633 )
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
