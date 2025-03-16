from glob import glob
import pandas as pd
import re


def load_subtitles_dataset(dataset_path):
    subtitles_paths = glob(dataset_path+'/*.ass')

    def extract_season_episode(subtitles_paths):
        match = re.search(r"Season (\d+) - (\d+)", subtitles_paths)
        if match:
            season = int(match.group(1))
            episode = int(match.group(2))
            return (season, episode)
        return (0, 0)  # Default if the regex doesn't match

    subtitles_paths.sort(key=extract_season_episode)

    scripts = []
    episode_num = []

    for path in subtitles_paths:

        # Read Lines
        with open(path, 'r') as file:
            lines = file.readlines()
            lines = lines[27:]
            lines = [",".join(line.split(',')[9:]) for line in lines]

        lines = [line.replace('\\N', ' ') for line in lines]
        script = " ".join(lines)

        episode = int(path.split('-')[-1].split('.')[0].strip())

        scripts.append(script)
        episode_num.append(episode)

    df = pd.DataFrame.from_dict({"episode": episode_num, "script": scripts})
    return df
