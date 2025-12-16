# SDN Internet2 Emulation with Ryu and Mininet
This guide provides the step-by-step instructions to set up, run, and test the Software-Defined Networking (SDN) emulation environment using the Ryu controller and a simplified 10-node Internet2 topology in Mininet.

The topology script (`topo.py`) includes realistic link constraints (latency and bandwidth) using `TCLink` for performance evaluation.

## 1. Prerequisites and Dependencies

The following software and packages are required. Note that this setup specifically targets **Python 3.8** to ensure compatibility with older Ryu dependencies.

### 1.1 System Dependencies* **Mininet:** Must be installed globally on your system.
```bash
# Common command for Debian/Ubuntu systems
sudo apt install mininet

```


* **Python 3.8:** Required for Ryu compatibility.
```bash
sudo apt install python3.8 python3.8-venv

```


* **iperf:** Required for throughput testing.
```bash
sudo apt install iperf

```



### 1.2 Python Dependencies (within VENV)| Package | Purpose |
| --- | --- |
| **ryu** | The OpenFlow controller application. |
| **eventlet** | Ryu's concurrent networking library. |

## 2. Setup Instructions (Python VENV)
Follow these steps to create a dedicated Python 3.8 environment and install Ryu.

### Step 2.1: Create and Activate VENV```bash
# 1. Create the virtual environment using Python 3.8 explicitly
python3.8 -m venv ryu_venv

# 2. Activate the environment
source ryu_venv/bin/activate

```

*(Your terminal prompt should now show `(ryu_venv)`.)*

###Step 2.2: Install Ryu and Dependencies```bash
# Install Ryu
(ryu_venv) pip install ryu

```

### Step 2.3: Critical Fix for Ryu (If Needed)
If you encounter the `ImportError: cannot import name 'ALREADY_HANDLED' from 'eventlet.wsgi'`, you **must manually edit** the Ryu source code:

1. Open the problematic file (path may vary slightly):
```bash
(ryu_venv) nano ryu_venv/lib/python3.8/site-packages/ryu/app/wsgi.py

```


2. **Add** the constant definition **before** the class starts:
```python
ALREADY_HANDLED = 1

class _AlreadyHandledResponse(Response):

```

## 3. Running the Application (Ordered Commands)
The Mininet script (`topo.py`) must be executed **outside** the VENV using `sudo`, while Ryu must run **inside** the VENV.

| Order | Terminal | Environment | Command | Purpose |
| --- | --- | --- | --- | --- |
| **1.** | Terminal A | `(ryu_venv)` | `ryu-manager ryu.app.simple_switch_13` | Start the Ryu controller application. (Keep running) |
| **2.** | Terminal B | **(Global)** | `deactivate` | **Crucial:** Exit the VENV to use global Mininet modules. |
| **3.** | Terminal B | **(Global)** | `sudo python3 topo.py` | Start the Mininet topology and connect switches to Ryu. **This will open the Mininet CLI.** |

---

## 4. Testing and Performance Evaluation Commands
Once the Mininet CLI (`mininet>`) starts, use these commands to validate connectivity and measure performance.

### 4.1 Connectivity Validation
Verify that the Ryu controller is correctly learning the topology and installing basic L2 forwarding rules.

| Command | Purpose | Expected Result |
| --- | --- | --- |
| `mininet> pingall` | Verify end-to-end connectivity across all 10 hosts. | Should show `0% dropped`. |
| `mininet> h2 ping -c 3 h3` | Test connectivity and measure base latency. | RTT should reflect the configured link delay (e.g., \approx 10 \text{ ms} for 5 \text{ ms} delay). |
| `mininet> s1 ovs-ofctl dump-flows unix:/var/run/openvswitch/s1.mgmt -O OpenFlow13` | **Test SDN Control Plane:** Inspect the flow table on switch s1. **This command confirms the Ryu is installing rules.** | Must show `priority=1` flows installed by Ryu for L2 forwarding and the default `CONTROLLER` action. |

### 4.2 Performance Evaluation (Latency and Throughput)Measure the impact of the `TCLink` constraints you configured.

#### A. Latency Test (Ping)Test the longest path to see the cumulative delay.

```bash
mininet> h1 ping -c 3 h10

```

* **Analysis:** The Round Trip Time (RTT) should be the sum of all one-way delays (\text{delay} value) along the path from h1 to h10, multiplied by two.

####B. Throughput Test (iperf)Measure the effective bandwidth (vazão) between two end-hosts.

1. **Start Server on h1:**
```bash
mininet> h1 iperf -s &

```


2. **Run Client from h10:**
```bash
mininet> h10 iperf -c 10.0.0.1

```



* **Analysis:** The resulting bandwidth in Mbits/sec should be limited by the lowest `bw` value (the **bottleneck**) configured on any link along the path between h1 and h10.

* **Analysis:** The Round Trip Time (RTT) should be the sum of all one-way delays (\text{delay} value) along the path from h1 to h10, multiplied by two.

#### B. Throughput Test (iperf)
Measure the effective bandwidth (vazão) between two end-hosts.

1. **Start Server on h1:**
```bash
mininet> h1 iperf -s &

```


2. **Run Client from h10:**
```bash
mininet> h10 iperf -c 10.0.0.1

```



* **Analysis:** The resulting bandwidth in Mbits/sec should be limited by the lowest `bw` value (the **bottleneck**) configured on any link along the path between h1 and h10.
