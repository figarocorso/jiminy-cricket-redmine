#!/usr/bin/python

import yaml
import json
import requests

# Debug variables
debug = True
issues_file = 'mocks/issues.json'

# Redmine credentials
username = "" # your api key
password = "" # not used, could be random

# Other variables
restrictions_file = "restrictions.yaml"
url_prefix = "https://projects.zentyal.com/"

# Helpers
def load_restrictions(path):
    with file(path, 'r') as stream:
        return yaml.load(stream)

def get(issue, component):
    return issue[component] if component in issue else "None"


# Second level functions
def issue_has_to_be_shown(issue, constraints):
    return True

def cataloge_issue(issue, actions):
    result = {}
    result['url'] = url_prefix + "issues/" + str(get(issue, 'id'))
    result['subject'] = get(issue, 'subject')

    for key, value in actions.iteritems():
        result[key] = value

    return result


# Main functions
def process_issue(issue, restrictions):
    result = {}
    for rule_name, rule in restrictions.iteritems():
        if issue_has_to_be_shown(issue, rule['constraints']):
            result = cataloge_issue(issue, rule['actions'])
            break

    return result

def merge_results(result, results):
    classify = result['classify']
    result.pop('classify', None)
    message = result['message']
    result.pop('message', None)

    if classify not in results:
        results[classify] = {}

    if message not in results[classify]:
        results[classify][message] = []

    results[classify][message].append(result)


# Main program
if debug:
    with file(issues_file, 'r') as stream:
        issues = json.load(stream)['issues']
# TODO: Gather R&D projects issues using requests.get

restrictions = load_restrictions(restrictions_file)

results = {}
for issue in issues:
    result = process_issue(issue, restrictions['issue'])
    merge_results(result, results)

print results
