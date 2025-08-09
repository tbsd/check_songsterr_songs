#!/usr/bin/env python3
"""
Creates three files: with band names, with song names, and with names that cannot be parsed
"""

import sys
import os

SEPARATOR = '-'
DEFAULT_BANDS_FILE_PATH = 'bands.txt'
DEFAULT_SONG_NAMES_FILE_PATH = 'song_names.txt'
DEFAULT_OTHER_FILE_PATH = 'other_songs.txt'
FILE_EXTENSIONS = ('.mp3', '.wav', '.flac', '.midi', '.opus', '.m4a')

def get_files(dir_path: str) -> list[str]:
    return [fi for fi in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, fi))]

def get_song_name(name: str) -> str:
    for extension in FILE_EXTENSIONS:
        if name.endswith(extension):
            return name[:(-1*len(extension))]
    return name

def write_to_file(rows: list[str], file_path: str) -> None:
    with open(file_path, 'w', encoding='utf-8') as output_file:
        output_file.write('\n'.join(rows))

if len(sys.argv) != 2:
    print('Usage: get_songs_from_dir.py path_to_dir_with_songs')
    exit()

songs_list = get_files(sys.argv[1])
if not songs_list:
    print('No files found')
    exit()

bands = set()
song_names = set()
other = set()

for song in  songs_list:
    stripped = song.lower().strip()
    parts = stripped.split(SEPARATOR)
    if len(parts) != 2:
        other.add(stripped)
        continue
    bands.add(parts[0].strip())
    song_names.add(get_song_name(parts[1].strip()).strip())

write_to_file(bands, DEFAULT_BANDS_FILE_PATH)
write_to_file(song_names, DEFAULT_SONG_NAMES_FILE_PATH)
write_to_file(other, DEFAULT_OTHER_FILE_PATH)

