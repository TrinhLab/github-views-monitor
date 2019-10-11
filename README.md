# Usage monitor

Monitor views of software distributed through Github.
The metric is views (individuals visiting the repository page) which takes into account unique individuals.
Currently the total number of downloads cannot be monitored. Only release download and clones, but not zip downloads.

The data is stored in a table named data.tsv with the following headers:
- repo_name: Name of repository
- log_timestamp: Time the request was done by us
- github_timestamp: Time github recorded the data
- count: Total number of visits
- unique: Total number of unique visitors


# Running

Requires credentials for github api:
https://developer.github.com/v3/#authentication
You can generate an authentication token here (needs push permission, which can be granted with public_repo scope):
https://github.com/settings/tokens

run `./log.py -h` for more info

Set up as cronjob to run regularly, for example to run once a week (Sunday at midnight to be specific):

`0 0 * * 0 /path/to/usage-monitor/log.py -o /path/to/usage-monitor/data.tsv -t /path/to/usage-monitor/secret_token`

# Notes
Currently it is just monitoring the data, after sufficient data is available a function to plot it will be added
