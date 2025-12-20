## About
This project implements three distributed algorithms: Lamport's Clock Algorithm for clock synchronization, Ring Algorithm for leader election and Token Ring Algorithm for mutual exclusion.

## Running the Simulation
Run the Docker containers by setting an environment variable, following the examples:

### To run Lamport's Clock Algorithm
```bash
ALGORITHM=lamport docker compose up
```

### To run Ring Algorithm for leader election
```bash
ALGORITHM=election docker compose up
```

### To run Token Ring Algorithm for mutual exclusion
```bash
ALGORITHM=mutex docker compose up
```

If the environment variable is not defined, the mutex algorithm will be execute by default. The output can be seen in the docker compose logs and in the shared_file.txt in /resources for the mutex algorithm.
