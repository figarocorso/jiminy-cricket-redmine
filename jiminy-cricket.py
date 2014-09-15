#!/usr/bin/python
# PYTHON_ARGCOMPLETE_OK

import sys

import argparse
import argcomplete
import json
import requests
import yaml

import string_operations
import number_operations
import date_operations

sys.modules['string_operations'] = string_operations
sys.modules['number_operations'] = number_operations
sys.modules['date_operations'] = date_operations

# Debug variables
issues_file = 'mocks/issues.json'
detailed_issues_file = 'mocks/detailed-issues.json'

# Redmine credentials
username = "" # your api key
password = "" # not used, could be random

# Other variables
restrictions_file = "restrictions.yaml"
url_prefix = "https://projects.zentyal.com/"
in_progress_status = 'In Progress'

# Helpers
def load_restrictions(path):
    with open(path, 'r') as stream:
        return yaml.load(stream)

def get(dictionary, component):
    return dictionary[component] if component in dictionary else "None"


# Second level functions (and further)
def check_constraint(component_type, operation, limit, value):
    module = component_type + '_operations'
    function = component_type + '_' + operation

    return getattr(sys.modules[module], function)(value, limit)

def issue_has_to_be_shown(issue, constraints):
    result = True

    for field, checkings in constraints.iteritems():
        field_value = get(issue, field)
        if ('component' in checkings) and (checkings['component'].lower() != 'none'):
            field_value = get(field_value, checkings['component'])

        result = result and check_constraint(get(checkings, 'component-type'),
                                            get(checkings, 'operation'),
                                            get(checkings, 'value'),
                                            field_value)

    return result

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

def process_detailed_issue(issue, developers):
    name = ""

    if 'assigned_to' in issue:
        name = issue['assigned_to']['name']

    if (name) and (name not in developers):
        developers[name] = {}

    if ('status' in issue) and (issue['status']['name'] == in_progress_status):
        if 'work-in-progress' not in developers[name]:
            developers[name]['work-in-progress'] = 0

        developers[name]['work-in-progress'] += 1

    if 'journals' in issue:
        for journal in issue['journals']:
            name = journal['user']['name']
            if name not in developers:
                developers[name] = {}

            if 'last-update' not in developers[name]:
                developers[name]['last-update'] = journal['created_on']

            if developers[name]['last-update'] < journal['created_on']:
                developers[name]['last-update'] = journal['created_on']



def merge_results(result, results):
    classify = get(result, 'classify')
    result.pop('classify', None)
    message = get(result, 'message')
    result.pop('message', None)

    if classify not in results:
        results[classify] = {}

    if message not in results[classify]:
        results[classify][message] = []

    results[classify][message].append(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Jiminy Cricket will parse Zentyal internal issues tracker and analyze it following the rules written in the file restrictions.yaml')

    parser.add_argument('-d', '--debug', help="Instead of requesting the info from the Redmine server, we take it from JSON files.", action='store_true')

    subparsers = parser.add_subparsers(title="Analysis depth", dest="depth")
    quick_parser = subparsers.add_parser('quick', help="The fastest analysis, only a quick review taking the 'issue' restrictions")
    developer_parser = subparsers.add_parser('developer', help="Deeper analysis of each ticket. Also includes 'developer' retrictions. This option takes much longer")

    args = parser.parse_args()
    argcomplete.autocomplete(parser)

    issues = []
    if args.debug:
        with open(issues_file, 'r') as stream:
            issues = json.load(stream)['issues']
        with open(detailed_issues_file, 'r') as stream:
            detailed_issues = json.load(stream)

    # TODO: Gather R&D projects issues using requests.get
    restrictions = load_restrictions(restrictions_file)

    results = {}
    for issue in issues:
        result = process_issue(issue, restrictions['issue'])
        if result:
            merge_results(result, results)

    if 'developer' in args.depth:
        developers = {}
        for detailed_issue in detailed_issues:
            process_detailed_issue(detailed_issue['issue'], developers)

    for developer, details in developers.iteritems():
        print developer
        print details
        print

    for priority, prioritized_results in results.iteritems():
        print priority
        for set_name, set_results in prioritized_results.iteritems():
            print "  " + set_name
            for result in set_results:
                print '    ' + get(result, 'subject') + ' (' + get(result, 'url') + ')'
