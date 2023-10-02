from pathlib import Path
import utils
import json
import matplotlib.pyplot as plt
import re
import json
from heapq import nlargest, nsmallest


def json_maker():
    directories = utils.dir_path()
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
        if dir in data_str:
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

def plot_maker():
    # Load data from JSON file
    with open('stats/category_stats.json', 'r') as f:
        data = json.load(f)
    # Initialize lists to store values
    honesty_values = []
    persuasion_values = []
    straightforwardness_values = []
    # Extract values from data
    for item in data:
        categories = item['categories']
        if categories['Honesty'] != "Not found":
            honesty_values.append(int(categories['Honesty']))
        if categories['Persuasion'] != "Not found":
            persuasion_values.append(int(categories['Persuasion']))
        if categories.get('Straight-forwardness') != "Not found":
            straightforwardness_values.append(int(categories['Straight-forwardness']))
    # Create a figure and a set of subplots
    fig, ax = plt.subplots()
    # Prepare data for box plot
    box_plot_data=[honesty_values, persuasion_values, straightforwardness_values]
    # Create box plot
    bp = ax.boxplot(box_plot_data, patch_artist=True, notch=True, vert=0)
    colors = ['#BAABDA', '#D6E5FA', '#FFF9F9']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
    # Adding labels
    plt.yticks([1, 2, 3], ['Honesty', 'Persuasion', 'Straight-forwardness'])
    plt.xlabel('Values')
    plt.title('Category Values')
    # Show graphic
    plt.show()
    
def cherry_picker():
    # Load data from JSON file
    with open('stats/category_stats.json', 'r') as f:
        data = json.load(f)
    # Initialize lists to store top and bottom 3 sets for each category
    top_honesty = nlargest(3, data, key=lambda x: int(x['categories']['Honesty']))
    bottom_honesty = nsmallest(3, data, key=lambda x: int(x['categories']['Honesty']))
    top_persuasion = nlargest(3, data, key=lambda x: int(x['categories']['Persuasion']))
    bottom_persuasion = nsmallest(3, data, key=lambda x: int(x['categories']['Persuasion']))
    # Print the names of the top and bottom 3 sets for each category
    print("Top 3 Honesty:", [set['name'] for set in top_honesty])
    print("Bottom 3 Honesty:", [set['name'] for set in bottom_honesty])
    print("Top 3 Persuasion:", [set['name'] for set in top_persuasion])
    print("Bottom 3 Persuasion:", [set['name'] for set in bottom_persuasion])
    
def main():
    #json_maker()
    #plot_maker()
    cherry_picker()

if __name__ == "__main__":
    main()
