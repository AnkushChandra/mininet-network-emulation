from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.node import Node, Host, OVSSwitch, OVSKernelSwitch, Controller, RemoteController, DefaultController
from mininet.log import setLogLevel, info
from mininet.cli import CLI

class LineTopo( Topo ):
   def __init__( self , **kwargs):
       super(LineTopo, self).__init__(**kwargs)
       
       # Adding the 3 hosts
       h1 = self.addHost('h1')
       h2 = self.addHost('h2')
       h3 = self.addHost('h3')

       # Adding the 3 switches
       s1 = self.addSwitch('s1')
       s2 = self.addSwitch('s2')

       # creating links between the switches
       self.addLink(h1, s1, intfName1='h1-eth0',intfName2='s1-eth1')
       self.addLink(h2, s1, intfName1='h2-eth0',intfName2='s1-eth2')
       self.addLink(h3, s2, intfName1='h3-eth0',intfName2='s2-eth2')
       self.addLink(s1, s2, intfName1='s1-eth3',intfName2='s2-eth1')


def run():
    # Initialising the network topology class
    topo = LineTopo()
    net = Mininet( topo=topo,
                   switch = OVSKernelSwitch, 
                controller = DefaultController,
                autoSetMacs = True
                ) 
    net.start()

    CLI( net )
    net.stop()


if __name__ == '__main__':
    setLogLevel( 'info' )
    run()