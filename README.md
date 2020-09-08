About
====

igrid-network-simulations is sensor network simulator for smart grid.


Requirements
------------

For the agent/AP:

- python2.
- pip.
- Wireshark.
- Pre-configured Virtual Machine with Mininet-WIFI [[3.3GB Size] - Ubuntu 18.04 x64](https://drive.google.com/file/d/1gRqGmkyPcw1waBlwfSGnOcucvXsHvATx/view?usp=sharing) -       Mininet-WiFi (_pass: wifi_).


Building Simulations
---------------------

```
  $: git clone https://github.com/RugaCoder/igrid-network-simulations net-sim
  $: cd net-sim
  $: pip install -r requirements.txt 
  $: python2 bin/igrid-net
```

Interface sw-eth1 can be used to capture nodes (sensors) traffic. 