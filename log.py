#!/usr/bin/env python3

import requests
import datetime
import argparse

def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description='Log github views of public repositories for an organization',     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-o', '--data_file_path', type=str, help='Path to .tsv file where data is stored', default="data.tsv")
    parser.add_argument('-t', '--secret_token_path', type=str, help='Path to one line text file with authentication token', default="secret_token")
    parser.add_argument('-v', '--verbose', action='store_true', help='Turn on verbose output')
    parser.add_argument('-n', '--org_name', default="trinhlab", help='Organization name')

    args = parser.parse_args()

    # Get repo names
    resp = requests.get(f'https://api.github.com/orgs/{args.org_name}/repos')
    repo_names = [repo['name'] for repo in resp.json()]

    # Get traffic
    with open(args.secret_token_path, "r") as f:
        secret_token = f.read().splitlines()[0]

    def write_row():
        if args.verbose:
            print("\t".join([name, log_timestamp, github_timestamp, count, uniques]))
        f.write("{}\n".format("\t".join([name, log_timestamp, github_timestamp, count, uniques])))

    headers = { "Authorization": f"token {secret_token}"}
    parameters = {"per": "week"}
    log_timestamp = datetime.datetime.now().isoformat().split(".")[0] #remove miliseconds
    with open(args.data_file_path, 'a') as f:
        for name in repo_names:
            # Github returns the last two weeks
            resp = requests.get(f"https://api.github.com/repos/{args.org_name}/{name}/traffic/views", headers=headers, params=parameters)
            info = resp.json()

            # Table headers:
            # repo_name | log_timestamp | github_timestamp | count | unique
            if not info['views']:
                github_timestamp =''
                count = '0'
                uniques = '0'
                write_row()
            else:
                for week in info['views']:
                    github_timestamp = week['timestamp']
                    count = str(week['count'])
                    uniques = str(week['uniques'])
                    write_row()


if __name__ == '__main__':
   main()
