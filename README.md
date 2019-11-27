# Simian Army Fault Injection Framework


## Setup

Install from root project folder with

```bash
pip install .
```

## Usage

There is no command line usage. After installation import the `simainarmy` module into the disered network enviornment.
The currently included monkeys are made for this [simulator](https://github.com/RealVNF/coordination-simulation).
Therefore, to integrade the Simian Army into another environment, adaptations for the monkeys need to be done.
Further, an adapter, similar to [this one](https://git.cs.upb.de/kaiha/bachelorarbeit/blob/master/simianarmy/Adapter.py), that handles communication between the Simian Army and the environemnt is needed.