# Multi-Agent-Failures

Running the code
```bash
OPENAI_API_KEY=[your key] python3 run_twoplayer.py envs/basic-2-agents.0.2.json --num_steps 10
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

As a part of our ongoing research, we have conducted several experiments involving different Learning Logic Model (LLM) agents. These agents were set against each other in various configurations, and the resulting interactions were thoroughly analyzed.

The following table provides a concise overview of the matchups between the different models:

| Attacker | Defender |
|----------|----------|
| GPT-4    | GPT-4    |
| GPT-4    | GPT-3.5-turbo |
| GPT-4    | Mistral  |
| GPT-3.5-turbo | GPT-3.5-turbo |
| GPT-3.5-turbo | Mistral |
| Mistral  | Mistral  |

The attacker models used in these experiments include GPT-4, GPT-3.5-turbo, and Mistral. Similarly, the defender models comprise GPT-4, GPT-3.5-turbo, and Mistral.
However, it is important to note that due to the inherent advantages of certain models over others, we have consciously decided to exclude the following matchups from our experiments:
- Attacker: GPT-3.5-turbo VS Defender: GPT-4
- Attacker: Mistral VS Defender: GPT-4
- Attacker: Mistral VS Defender: GPT-3.5-turbo
This decision was made to ensure a fair and balanced evaluation of the capabilities of each model.

### Setup 2: Alice, Bob, and Charlie Backend

[To be completed]

Please refer to the respective sections for detailed instructions on how to configure the LLM backends for each setup.



