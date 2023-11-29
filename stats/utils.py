import glob
from pathlib import Path
import json
import subprocess

def dir_path(output_root = 'output/report_output'):
    directories = []
    # The pattern '**' matches any files or directories (including those starting with '.')
    # The pattern '*/' matches any directory
    for dir in glob.glob(f"{output_root}/*/*/"):
        dir_path = Path(dir)
        directories.append(dir_path)

    return directories

def json_maker():
    directories = dir_path()
    # Load existing data
    try:
        with open('stats/category_stats.json', 'r') as f:
            existing_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []

    for i, dir in enumerate(directories, start=1):
        # Progress Metric
        print(f"Iteration {i} / {len(directories)}: {dir} \n")
        print(f"Now running analysis of the {dir.name} conversation \n")
    
        # Check for repetition
        data_str = json.dumps(existing_data)
        if str(dir) in data_str:
            print(f"Has already added this conversation into the json file \n")
            continue
        
        analysis_file = Path(dir, 'GPT4_analysis.json')
        if not analysis_file.exists():
            print(f"The current dir doesn't have a GPT4_analysis.json {analysis_file} \n")
            continue
        # Load the JSON file
        with open(analysis_file, 'r') as f:
            data = json.load(f)
        # Extract the message content
        content = data.get('choices', [{}])[0].get('message', {}).get('content', '')
        # Extract the required information
        categories = {
            "Honesty": re.search(r"Honesty: (\d+)", content).group(1) if re.search(r"Honesty: (\d+)", content) else "Not found",
            "Persuasion": re.search(r"Persuasion: (\d+)", content).group(1) if re.search(r"Persuasion: (\d+)", content) else "Not found",
            "Straight-forwardness": re.search(r"Straight-?forwardness: (\d+)", content).group(1) if re.search(r"Straight-forwardness: (\d+)", content) else "Not found"
        }

        # Prepare the output data
        output_data = {
            "name": dir.name,
            "categories": categories
        }
        # Append the output data to the existing data
        existing_data.append(output_data)

    # Write the existing data back to the JSON file
    with open('stats/category_stats.json', 'w') as f:
        json.dump(existing_data, f, indent=4)

def search_for_grep(text):
    # The command you want to execute
    command = f"pcregrep -rMl '{text}' output/report_output"
    # Run the command
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    # Get the output
    output, error = process.communicate()
    # If there was an error
    if error:
        print(f"Error: {error.decode()}")
    # If the command was successful
    if output:
        parts=output.decode().split("/")
        history_file_path = "/".join(parts[:4]) + "/history.json"
        return history_file_path
    
def print_history_items(history_file_path):
    with open(history_file_path, 'r') as f:
        data = json.load(f)
        with open('stats/temp_hist.txt', 'w') as outfile:
            for item in data:
                print(f" \\textbf {{ {item['agent_name']} }} :", file=outfile)
                print(f"{item['content']} \n \n", file=outfile)

import re

def extract_from_files(dir_path):
    files_to_extract = ('config.json', 'result.json')
    result = {
        'exp_path': dir_path
    }
    for file in files_to_extract:
        try:
            with open(dir_path / file) as f:
                data = json.load(f)
        except:
            data = None
        result[file.split('.')[0]] = data

        # Extract the password from the config file
        if file == 'config.json' and data is not None:
            for player in data.get('players', []):
                if player.get('name') == 'Bob':
                    role_desc = player.get('role_desc', '')
                    password_match = re.search(r'You know a secret password:\s*([^\n]*)', role_desc)
                    if password_match:
                        result['password'] = password_match.group(1)
                    else:
                        raise Exception(f'Password not found in {role_desc}')
    
    # Extract the last file from the history folder
    history_dir = dir_path / 'history'
    if history_dir.exists() and history_dir.is_dir():
        history_files = sorted(history_dir.glob('*.json'))
        if history_files:
            try:
                with open(history_files[-1]) as f:
                    data = json.load(f)
            except:
                data = None
            result['history'] = data
    return result


