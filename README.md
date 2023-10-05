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

As a part of our ongoing research, we have conducted several experiments involving different Large Language Models (LLM) agents. These agents were set against each other in various configurations, and the resulting interactions were thoroughly analyzed.

The following table provides a concise overview of the matchups between the different models:

| Attacker | Defender |
|----------|----------|
| GPT-4    | GPT-4    |
| GPT-4    | GPT-3.5-turbo |
| GPT-4    | Mistral  |
| GPT-3.5-turbo | GPT-3.5-turbo |
| GPT-3.5-turbo | Mistral |
| Mistral  | Mistral  |
| Mistral  | GPT-3.5-turbo |
| Mistral  | GPT-4    |
| GPT-3.5-turbo  | GPT-3.5-turbo |

The attacker models used in these experiments include GPT-4, GPT-3.5-turbo, and Mistral. Similarly, the defender models comprise GPT-4, GPT-3.5-turbo, and Mistral.
We have tested every possible combination of these models against each other. This decision was made to ensure a fair and balanced evaluation of the capabilities of each model.

### Setup 2: Alice, Bob, and Charlie Backend

The configuration of these models has been arranged in a distinct manner for this phase of our study. 

The model Alice continues to assume the role of the attacker, while Bob persists as the defender. However, a novel element in this setup is the introduction of a third agent, Charlie. Charlie functions as an intermediary, possessing the ability to communicate with both Alice and Bob. 

It is important to note that direct communication between Alice and Bob is not permitted in this setup. Consequently, for Alice to extract the requisite information from Bob, she is compelled to interact via Charlie. This unique arrangement provides a fresh perspective and adds a layer of complexity to our ongoing investigation of Large Language Models.

The following table provides a concise overview of the matchups between the different models:

| Attacker | Intermediary | Defender | Dificulty |
|----------|--------------|----------|-----------|
| GPT-4    | GPT-3.5-turbo | GPT-3.5-turbo | Curious |
| GPT-4    | GPT-3.5-turbo | Mistral  | Curious
| GPT-4    | GPT-3.5-turbo | GPT-3.5-turbo | Neutral |
| GPT-4    | GPT-3.5-turbo | Mistral  | Neutral |
| GPT-4    | GPT-3.5-turbo | GPT-3.5-turbo | Defensive |
| GPT-4    | GPT-3.5-turbo | Mistral  | Defensive | 


## Final conclusions and findings 

Read the rest of the report with our finding in our website

| Website | Report |
|---------|--------|
|[Link to our website](https://second-order-jailbreak.romaingrx.com/2_agents/A_Mistral_D_Mistral_simple_20231001_233353)|[Download our report](https://docs.google.com/document/d/1OY5fOWC2_Zf1cCfdAV8PxrL3lwignZi6R_6Mv8vnDoI/export?format=pdf)|



