#!/bin/sh

if [ "$ALGORITHM" = "lamport" ]; then 
    echo "Running Lamport Algorithm..."
    if [ "$NODE" = "node1" ]; then
        exec python3 lamport/node1.py
    elif [ "$NODE" = "node2" ]; then
        exec python3 lamport/node2.py
    fi
elif [ "$ALGORITHM" = "election" ]; then
    echo "Running Leader Election Algorithm..."
    if [ "$NODE" = "node1" ]; then
        exec python3 leader_election/node1.py
    elif [ "$NODE" = "node2" ]; then
        exec python3 leader_election/node2.py
    else
        exec python3 leader_election/node3.py
    fi
else
    echo "Running Mutex Algorithm..."
    if [ "$NODE" = "node1" ]; then
        exec python3 mutex/node1.py
    elif [ "$NODE" = "node2" ]; then
        exec python3 mutex/node2.py
    else
        exec python3 mutex/node3.py
    fi
fi
