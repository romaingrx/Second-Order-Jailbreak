from pathlib import Path
import utils
import json
import re
def main():
    directories = utils.dir_path()
    # Load existing data
    try:
        with open('category_stats.json', 'r') as f:
            existing_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []
    for i, dir in enumerate(directories, start=1):
        # Progress Metric
        print(f"Iteration {i} / {len(directories)}: {dir} \n")
        print(f"Now running analysis of the {dir.name} conversation \n")
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
            "Straight-forwardness": re.search(r"Straight-forwardness: (\d+)", content).group(1) if re.search(r"Straight-forwardness: (\d+)", content) else "Not found"
        }
        # Prepare the output data
        output_data = {
            "name": dir.name,
            "categories": categories
        }
        # Append the output data to the existing data
        existing_data.append(output_data)
    # Write the existing data back to the JSON file
    with open('category_stats.json', 'w') as f:
        json.dump(existing_data, f, indent=4)
if __name__ == "__main__":
    main()
