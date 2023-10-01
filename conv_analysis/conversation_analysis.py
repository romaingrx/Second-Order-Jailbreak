import os
import json
import openai


def main():
    # Load your OpenAI API key
    open_ai_key = "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"
    openai.api_key =  open_ai_key

    directory = 'output/'
    for root, dirs, files in os.walk(directory):
        for dir in dirs:
            # Load the conversation prompt 
            conv_prompt_file = 'conv_analysis/conv_prompt.json'
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
            messages = [
                {"role":"system","content": conv_prompt["Your goal"]}
            ]
            
            for message in history:
                messages.append({"role": "user", "content": message["content"]})
            messages.append({"role": "system", "content": conv_prompt["Last line"]})

            with open(f'conv_analysis/prompts/{dir}.json', 'w') as f:
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

            with open(f'conv_analysis/analysis/analysis_of_{dir}.json', 'w') as f:
                json.dump(response, f)

            break
        break

if __name__ == "__main__":
    main()
