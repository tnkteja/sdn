#!/usr/bin/python

#! /usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI

from pox import POX

class SingleSwitchTopo(Topo):
    "Single switch connected to n hosts."
    def build(self, n=2):
        switch = self.addSwitch("s1")
        # Python's range(N) generates 0..N-1
        for h in xrange(n):
            host = self.addHost("h%s"%h)
            self.addLink(host, switch)

"Create and test a simple network"
topo = SingleSwitchTopo()

net = Mininet(topo, conr)
net.start()
print "Dumping host connections"
dumpNodeConnections(net.hosts)

print "Testing network connectivity"
net.pingAll()

#Start mininet and hold on the  CLI
CLI(net)
net.stop()
