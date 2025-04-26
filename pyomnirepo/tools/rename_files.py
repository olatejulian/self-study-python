import os
import re

path = os.path.dirname(__file__)

regex_numbers = re.compile('[0-9][0-9]x[0-9][0-9]')
regex_episode_title = re.compile('[a-zA-z\u00C0-\u00FF]*\s')

regex_avi = re.compile('{.avi}')

file_name = 'That \'70s show - 03x09 algum título aleatório de sitcom aqui.avi'

get_numbers = re.search(regex_numbers, file_name)

get_episode_title = re.findall(regex_episode_title, file_name)

print (regex_avi.match(file_name))

# print(get_numbers)

# print(get_episode_title)

season, episode = get_numbers.group().split('x')

# list_files = os.listdir(path)
# for file_name in list_files:
#     get_numbers = re.search(regex_numbers, file_name)

#     get_episode_title = re.search(regex_episode_title, file_name)


# episode_title = ''.replace(' ', '_')

# new_file_name = f'that_70s_show_S{season}_E{episode}_{episode_title}.avi'

# new_subtitle_name = f'that_70s_show_S{season}_E{episode}_{episode_title}.srt'

# rename_file(file_name, new_file_name)
