import os
import json
import openai

# Load your OpenAI API key
open_ai_key = input()

openai.api_key = open_ai_key if (open_ai_key == '')  else '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'

def main():
    directory = '../output/'
    count = 0
    for root, dirs, files in os.walk(directory):
        for dir in dirs:
            # Load the conversation prompt 
            conv_prompt_file = 'prompts/conv_prompt.json'
            if not os.path.exists(conv_prompt_file):
                print(f"No conversation analysis prompt file: {conv_prompt_file}")
                break

            # Load the config of the conversation 
            config_file = os.path.join(root, dir, 'config.json')
            if not os.path.exists(config_file):
                print(f"No config file in the directory: {dir}")
                break

            # Load the conversation 
            history_file = os.path.join(root, dir, 'history.json')
            if not os.path.exists(history_file):
                print(f"No history file in the directory: {dir}")
                break

            json_files = [config_file, history_file, conv_prompt_file]
            data = []
            for file in json_files:
                with open(file, 'r') as f:
                    data.append(json.load(f))

            # Convert the appended data to a string
            prompt = json.dumps(data)

            print(prompt)

            """
            for i in range(0,4):
                print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                print("Now is the response")
                print("\n")
            
            # Pass the prompt to the GPT-4 API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-instruct-0914",
                messages=prompt,
                max_tokens=400,
                temperature=0.9
            )
            print(response)

            with open(f'analysis/analysis_of_{dir}.json', 'w') as f:
                json.dump(response, f)
            """
            count += 1 
            if (count == 1):
                break            


if __name__ == "__main__":
    main()
