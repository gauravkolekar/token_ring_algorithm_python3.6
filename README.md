# Implementation of Token Ring Algorithm including Leader Election:

This repository contains code that implements token ring algorithm. This code also contains the logic for electing a new leader if the orignal cordinator goes down.

# Content of this repository:

This repository contains node4.py, node1.py, node2.py, node3.py. These python files simulate

# How to run this code:

Secnario:

1. Single election:
run node4.py, node1.py, node2.py, node3.py in this order. Look at the output's of node 4. You will see token been passed
at high speed. Than close the node 4 program. You will see leader election take place. You will see node 3 become the
leader. Than again start node 4, you will see node 4 start election and leader election take place.

2. Multiple election:

Please go to node 2 and comment the timeout from 21. Uncomment command for timeout for 15. Without this multiple
election won't work.
run node4.py, node1.py, node2.py, node3.py in this order. Look at the output's of node 4. You will see token been passed
at high speed. Than close the node 4 program. You will see leader election take place by both node 1 and node 2.
You will see node 3 become the leader. Than again start node 4, you will see node 4 start election and leader election
take place.