# Mininet Network Emulation

This repository contains two Mininet experiments demonstrating **IP routing** and **SDN (Layer 2)** concepts.

---

## 📘 Overview

- **Experiment 1 (`exp1.py`)** – Demonstrates IPv4 routing between multiple subnets using two Linux routers.  
- **Experiment 2 (`exp2.py`)** – Demonstrates SDN-style flow-based forwarding using Open vSwitch (OVS) and `ovs-ofctl`.

---

## ⚙️ Requirements

- Linux environment (Ubuntu recommended)
- [Mininet](http://mininet.org) installed
- Open vSwitch (OVS)
- Python 3

### Installation (if needed)
```bash
sudo apt update
sudo apt install mininet openvswitch-switch -y
```

---

## Experiment 1 – IP Routing

### Topology
```
+-------+     +-------+     +-------+     +-------+
|  h1   |-----|  r1   |-----|  r2   |-----|  h3   |
|10.0.0.1|     |10.0.1.1|     |10.0.1.2|     |10.0.2.2|
+-------+     +-------+     +-------+     +-------+
                /
               /                      
       +-------+
       |  h2   |
       |10.0.3.2|
       +-------+
```

### Objective
Learn how to:
- Configure routers to forward packets between subnets.
- Set static routes for inter-subnet communication.
- Verify routing using ICMP pings.

### ▶️ Run
```bash
sudo python3 exp1.py
```

This will:
1. Create the topology shown above.
2. Enable IP forwarding on routers.
3. Add static routes:
   - r1 → 10.0.2.0/24 via 10.0.1.2  
   - r2 → 10.0.0.0/24 via 10.0.1.1  
   - r2 → 10.0.3.0/24 via 10.0.1.1
4. Run the following ping tests automatically:
   - h1 → h3  
   - h2 → h3  
   - h3 → h1  
   - h3 → h2
5. Save routing tables and ping results to `result1.txt`.

### Example Output (`result1.txt`)
```
*** Routing Table on r1 ***
default via 10.0.1.2 dev r1-eth1 
10.0.0.0/24 dev r1-eth0 proto kernel scope link src 10.0.0.3 
10.0.1.0/24 dev r1-eth1 proto kernel scope link src 10.0.1.1 
10.0.2.0/24 via 10.0.1.2 dev r1-eth1 

*** Routing Table on r2 ***
default via 10.0.1.1 dev r2-eth0 
10.0.1.0/24 dev r2-eth0 proto kernel scope link src 10.0.1.2 
10.0.2.0/24 dev r2-eth1 proto kernel scope link src 10.0.2.1 
10.0.0.0/24 via 10.0.1.1 dev r2-eth0 
10.0.3.0/24 via 10.0.1.1 dev r2-eth0 

=== h1 -> h3 ===
PING 10.0.2.2 (10.0.2.2) 56(84) bytes of data.
64 bytes from 10.0.2.2: icmp_seq=1 ttl=62 time=0.785 ms

=== h2 -> h3 ===
PING 10.0.2.2 (10.0.2.2) 56(84) bytes of data.
64 bytes from 10.0.2.2: icmp_seq=1 ttl=62 time=0.732 ms

=== h3 -> h1 ===
PING 10.0.0.1 (10.0.0.1) 56(84) bytes of data.
64 bytes from 10.0.0.1: icmp_seq=1 ttl=62 time=0.741 ms

=== h3 -> h2 ===
PING 10.0.3.2 (10.0.3.2) 56(84) bytes of data.
64 bytes from 10.0.3.2: icmp_seq=1 ttl=62 time=0.751 ms
```

---

## Experiment 2 – SDN (Layer 2 Switching)

### Topology
```
+-------+     +-------+     +-------+     +-------+
|  h1   |-----|  s1   |-----|  s2   |-----|  h3   |
|10.0.0.1|     |       |     |       |     |10.0.0.3|
+-------+     +---+---+     +-------+     +-------+
                |
                |
             +---+---+
             |  h2   |
             |10.0.0.2|
             +-------+
```

### ▶️ Run
```bash
sudo python3 exp2.py
```

This will:
1. Build the L2 topology using two OVS switches (`s1`, `s2`).
2. Test connectivity between hosts (`h1 → h3`, `h2 → h3`).
3. Save results to `result2.txt`.
4. Launch a Mininet CLI for manual flow rule experiments.

---

## Flow Rules

From another terminal (while `exp2.py` is running):

```bash
sudo ovs-ofctl show s1
sudo ovs-ofctl dump-flows s1
```

Then add the following flow rules on `s1`:

```bash
sudo ovs-ofctl del-flows s1
sudo ovs-ofctl add-flow s1 "in_port=2,actions=drop"
sudo ovs-ofctl add-flow s1 "in_port=1,actions=output:3"
```

Now return to the Mininet CLI and type:
```
exit
```

The script will automatically record the flow table and new ping results to `result2.txt`.

---

### Example Output (`result2.txt`)
```
=== BEFORE adding flows ===
--- h1 -> h3 ---
64 bytes from 10.0.0.3: icmp_seq=1 ttl=64 time=0.423 ms

--- h2 -> h3 ---
64 bytes from 10.0.0.3: icmp_seq=1 ttl=64 time=0.467 ms

=== s1 (before) ===
NXST_FLOW reply (xid=0x4):
 (no flows)

=== Commands to add flows on s1 ===
sudo ovs-ofctl del-flows s1
sudo ovs-ofctl add-flow s1 "in_port=2,actions=drop"
sudo ovs-ofctl add-flow s1 "in_port=1,actions=output:3"

=== AFTER adding flows ===
--- h1 -> h3 (after rules) ---
64 bytes from 10.0.0.3: icmp_seq=1 ttl=64 time=0.398 ms

--- h2 -> h3 (after rules) ---
ping: sendmsg: Network is unreachable
```

---

## 📄 File Structure

```
.
├── exp1.py
├── exp2.py
├── result1.txt
├── result2.txt
└── README.md
```

---

