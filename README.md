# Multi-Agent-Failures

Running the code
```bash
OPENAI_API_KEY=[your key] python3 run_twoplayer.py envs/basic-2-agents.0.2.json --num_steps 10
```

Running multiple conversation
```bash
bash run_multiple.sh envs/2-agents/hard/2-agents-mistralvsmistral.json 20 10
```

# Project README.md
## Project Overview

This project is centered around the implementation of multiple Large Language Model (LLM) agents in a game-like scenario. The game is designed in two different setups, each with a unique set of agents and objectives.

## Setup 1: Alice and Bob

In the first setup, we have two agents: Alice and Bob. Alice is the attacker whose goal is to find the secret key that Bob possesses. Bob, on the other hand, is the defender who is tasked with protecting his secret key from Alice.

## Setup 2: Alice, Bob, and Charlie

The second setup introduces a third agent, Charlie, who acts as an intermediary between Alice and Bob. Charlie can communicate with both Alice and Bob. The objective remains the same for Alice and Bob, but Charlie's role adds an extra layer of complexity to the game.

## LLM Backends

The LLM backends for both setups are different and require specific configurations. 

### Setup 1: Alice and Bob Backend

[To be completed]

### Setup 2: Alice, Bob, and Charlie Backend

[To be completed]

Please refer to the respective sections for detailed instructions on how to configure the LLM backends for each setup.



