import json
import matplotlib.pyplot as plt
import json
from heapq import nlargest, nsmallest

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

    print("What do you want to do? \n")
    print("1. Create a json with the different categories ided by GPT [Honesty, Persuasion, Straight-forwardness] \n")
    print("2. Plot the different categories ided by GPT \n")
    print("3. Cherry pick from the different categories \n")
    print("4. All of the above \n")
    match input(): 
        case 1: 
            json_maker()
        case 2:
            plot_maker()
        case 3: 
            cherry_picker()
        case 4:
            json_maker()
            plot_maker()
            cherry_picker()
        case _:
            print("No action selected pls select action \n")
            main()
            

if __name__ == "__main__":
    main()
