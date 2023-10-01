import os

def dir_scan():
    output_root = 'output/report_output'
    agent_dirs = [f"{output_root}/2_agents/", f"{output_root}/3_agents/"]

    directories = []
    for agent_dir in agent_dirs:
        for root, dirs, files in os.walk(agent_dir):
            directories.append(dirs)

            break

    print(directories)
    return directories


