#!/usr/bin/env python3

import requests
import time
import sys

SEARCH_API_TEMPLATE: str = 'https://www.songsterr.com/api/search?pattern={}&inst=undefined&tuning=undefined&difficulty=undefined&size=50&from=0&more=true'
DEFAULT_DELAY_S: float = 1.0
DEFAULT_OUTPUT_FILE_PATH: str = 'existing_tabs.txt'
HELP_MSG = '''Usage: songsterr.py file_with_search_strings.txt [delay_between_requests_in_seconds]
Search strings should be separated by a new line.
Delay may be a floating point value.'''

def search(search_str: str, is_exact: bool = True) -> dict:
    if is_exact:
        search_str = f'"{search_str}"'
    url = SEARCH_API_TEMPLATE.format(search_str)

    headers = {
        "Content-Type": "application/json"
    }
    response = requests.get(url)
    if not response.ok:
        return {'error': True,
                'status_code': response.status_code}

    data = response.json()
    return data

def get_formated_results(my_title: str, tabs: list) -> None:
    if not tabs:
        return ''
    available_songs = ''.join(
            [f'\n    {tab["artist"]} - {tab["title"]}'
                for tab in tabs])
    return f'{my_title}{available_songs}'

def get_existing_songs(search_str) -> str:
    """
    :returns: foramted string containg search results if any
    """
    if not search_str:
        return ''  # skip empty lines
    data = search(search_str)
    if data.get('error'):
        raise Exception(f'The search ended with an error: {data["status_code"]}')
    return get_formated_results(search_str, data['records'])

def get_args() -> (str, float):
    """
    :returns: (file path with search strings, delay in seconds)
    """
    args_count = len(sys.argv)
    if args_count < 2 or args_count > 3:
        print(HELP_MSG)
        return '', DEFAULT_DELAY_S
    delay = float(sys.argv[2]) if args_count >= 3 else DEFAULT_DELAY_S
    return sys.argv[1], delay

def get_search_strs_from_file(input_path: str) -> dict[str]:
    with open(input_path, 'r', encoding='utf-8') as input_file:
        return input_file.readlines()

def get_all_songs(search_strs: str) -> list[str]:
    results = []
    for search_str in search_strs:
        try:
            result = get_existing_songs(search_str.strip())
            if result:
                results.append(result)
                print(result)  # print during execution
        except Exception as exc:
            print(exc)
            break
        time.sleep(delay)
    return results

def write_results_to_file(results) -> None:
    if not results:
        return
    with open(DEFAULT_OUTPUT_FILE_PATH, 'w', encoding='utf-8') as output_file:
        output_file.write('\n'.join(results))

input_path, delay = get_args()
if not input_path:
    exit(1)

search_strs = get_search_strs_from_file(input_path)
results = get_all_songs(search_strs)
write_results_to_file(results)

