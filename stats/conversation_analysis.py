import os
import json
import openai

def main():
    # Load your OpenAI API key
    openai.api_key = os.environ["OPENAI_API_KEY"]

    directory = 'output/report_output'
    agent_dirs = [f"{directory}/2_agents/", f"{directory}/3_agents/"]
    for agent_dir in agent_dirs:
        for root, dirs, files in os.walk(agent_dir):
            for dir in dirs:
                # Load the conversation prompt 
                if (agent_dir == agent_dirs[0]):
                    conv_prompt_file = 'conv_analysis/2_agent_analysis_pmpt.json'
                else:
                    conv_prompt_file = 'conv_analysis/3_agent_analysis_pmpt.json'
                if not os.path.exists(conv_prompt_file):
                    print(f"No conversation analysis prompt file: {conv_prompt_file}")
                    break

                # Load the config of the conversation 
                config_file = os.path.join(root, dir, 'config.json')
                if not os.path.exists(config_file):
                    print(f"No config file in the directory: {config_file}")
                    break

                # Load the conversation 
                history_file = os.path.join(root, dir, 'history.json')
                if not os.path.exists(history_file):
                    print(f"No history file in the directory: {history_file}")
                    break

                # If there is no history directory then it's not latest model
                if not os.path.exists(os.path.join(root,dir,'history/')):
                    print(f"No history directory thus not up to date \n")
                    print(f"Exiting the program \n")
                    break
                
                # Load the conversation prompt
                with open(conv_prompt_file, 'r') as f:
                    conv_prompt = json.load(f)
                # Load the config
                with open(config_file, 'r') as f:
                    config = json.load(f)
                # Load the conversation history
                with open(history_file, 'r') as f:
                    history = json.load(f)
                # Create the messages list
                messages = [{"role":"system","content": conv_prompt["Your goal"]}]

                if (agent_dir == agent_dirs[0]):
                    messages.append({"role":"system", "content": f"Here are the two roles give to the models, the first one is {config['players'][0]['name']} with role, {config['players'][0]['role_desc']} the second player is {config['players'][1]['name']} with role, {config['players'][1]['role_desc']}"})
                else:
                    messages.append({"role":"system", "content": f"Here are the three roles give to the models, the first one is {config['players'][0]['name']} with role, {config['players'][0]['role_desc']} the second player is {config['players'][1]['name']} with role, {config['players'][1]['role_desc']} the third player is {config['players'][2]['name']} with role, {config['players'][2]['role_desc']}"})

                for message in history:
                    messages.append({"role": "user", "content": message["content"]})
                messages.append({"role": "system", "content": conv_prompt["Last line"]})

                with open(f'{agent_dir}{dir}/GPT4_review_prompt.json', 'w') as f:
                    json.dump(messages, f)

                for i in range(0,4):
                    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                    print("Now is the response")
                    print("\n")

                # Pass the prompt to the GPT-4 API
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    max_tokens=400,
                    temperature=0.9
                )

                with open(f'{agent_dir}{dir}/GPT4_analysis.json', 'w') as f:
                    json.dump(response, f)

                print(f'{agent_dir}{dir}/GPT4_review_prompt.json')
                print(f'{agent_dir}{dir}/GPT4_analysis.json')
                # Remove once we run full analysis
                break
            break

if __name__ == "__main__":
    main()
