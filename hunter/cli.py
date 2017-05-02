# Copyright 2015 Alan Vezina. All rights reserved.
import argparse
from csv import DictReader
import json
import time
from functools import reduce
from hunter import HunterClient

THROTTLE = 0.2


def reduce_sources(sources):
    def reducer(value, element):
        value.append(element['uri'])

        return value

    return ';'.join(reduce(reducer, sources, []))


def validate_search_file(reader: DictReader):
    field_names = reader.fieldnames

    if 'domain' not in field_names:
        print('domain column is required')
        return False

    return True


def validate_find_file(reader: DictReader):
    valid = True
    field_names = reader.fieldnames

    if 'domain' not in field_names:
        print('domain column is required')

    if 'first_name' not in field_names:
        print('first_name column is required')

    if 'last_name' not in field_names:
        print('last_name column is required')

    return valid


def validate_verify_file(reader: DictReader):
    field_names = reader.fieldnames

    if 'email' not in field_names:
        print('email column is required')
        return False

    return True


def search(client: HunterClient, domain, limit, offset, type_, print_header=True, is_file_output=False):
    if is_file_output:
        header = 'domain,email,type,sources'
        line_format = '{},{},{},{}'
    else:
        header = 'Domain\tEmail\tType\tSources'
        line_format = '{}\t{}\t{}\t{}'

    try:
        data = client.search(domain, limit, offset, type_)
    except Exception as e:
        print('Error during search request: {}'.format(e))
    else:
        for data in data['emails']:
            email = data['value']
            type_ = data['type']
            sources = reduce_sources(data['sources'])

            if print_header:
                print(header)
                print_header = False

            print(line_format.format(domain, email, type_, sources))


def find(client: HunterClient, domain, first_name, last_name, print_header=True, is_file_output=False):
    try:
        data = client.find(domain, first_name, last_name)
    except Exception as e:
        print('Error during find request: {}'.format(e))
    else:
        sources = reduce_sources(data['sources'])
        if is_file_output:
            if print_header:
                print('domain,first_name,last_name,email,score,sources')

            print('{},{},{},{},{},{}'.format(domain, first_name, last_name, data['email'], data['score'], sources))
        else:
            print('Domain:\t{}'.format(domain))
            print('First Name:\t{}'.format(first_name))
            print('Last Name:\t{}'.format(last_name))
            print('Email:\t{}'.format(data['email']))
            print('Score:\t{}'.format(data['score']))
            print('Sources:\t{}'.format(json.dumps(sources, indent=2)))


def verify(client: HunterClient, email, print_header=True, is_file_output=False):
    try:
        data = client.verify(email)
    except Exception as e:
        print('Error during verify request: {}'.format(e))
    else:
        sources = reduce_sources(data['sources'])
        if is_file_output:
            if print_header:
                print('email,result,score,sources')

            print('{},{},{},{}'.format(email, data['result'], data['score'], sources))
        else:
            print('Email:\t{}'.format(email))
            print('Result:\t{}'.format(data['result']))
            print('Score:\t{}'.format(data['score']))
            print('Sources:\t{}'.format(json.dumps(sources, indent=2)))


def handle_search_file(client: HunterClient, reader: DictReader):
    if not validate_search_file(reader):
        return

    print_header = True

    for line in reader:
        domain = line['domain'].strip()
        limit = line.get('limit', 10)
        offset = line.get('offset', 0)
        type_ = line.get('type')
        search(client, domain, limit, offset, type_, print_header=print_header, is_file_output=True)
        print_header = False
        time.sleep(THROTTLE)


def handle_find_file(client: HunterClient, reader: DictReader):
    if not validate_find_file(reader):
        return

    print_header = True

    for line in reader:
        domain = line['domain'].strip()
        first_name = line['first_name'].strip()
        last_name = line['last_name'].strip()
        find(client, domain, first_name, last_name, print_header=print_header, is_file_output=True)
        print_header = False
        time.sleep(THROTTLE)


def handle_verify_file(client: HunterClient, reader: DictReader):
    if not validate_verify_file(reader):
        return

    print_header = True

    for line in reader:
        email = line['email']
        verify(client, email, print_header=print_header, is_file_output=True)
        print_header = False
        time.sleep(THROTTLE)


def handle_cli(command, api_key, domain=None, limit=10, offset=0, type=None, first_name=None, last_name=None, email=None,
               file=None):
    client = HunterClient(api_key)
    reader = None

    if file is not None:
        file = open(file)
        reader = DictReader(file)

    if command == 'search':
        if file:
            handle_search_file(client, reader)
        elif domain:
            print('Searching {} for emails'.format(domain))

            if limit:
                print('Limit: {}'.format(limit))

            if offset:
                print('Offset: {}'.format(offset))

            if type:
                print('Type: {}'.format(type))

            search(client, domain, limit, offset, type)
        else:
            print('domain is required when using the find command')
    elif command == 'find':
        if file:
            handle_find_file(client, reader)
        else:
            valid = True

            if not domain:
                print('domain is required when using the find command')

            if not first_name:
                print('first_name is required when using the find command')

            if not last_name:
                print('last_name is required when using the find command')

            if valid:
                print('Finding email for {}, {}, {}'.format(domain, first_name, last_name))
                find(client, domain, first_name, last_name)
    elif command == 'verify':
        if file:
            handle_verify_file(client, reader)
        elif email:
            print('Verifying deliverability of {}'.format(email))
            verify(client, email)
        else:
            print('email is required when using the verify command')
    else:
        print('Invalid command {}'.format(command))

    if file:
        file.close()


def main():
    """
    TODO: parse args here
    :return:
    """
    parser = argparse.ArgumentParser(description='Hunter CLI')
    parser.add_argument('command', help='The API command to run. Choices: search, verify or find')
    parser.add_argument('api_key', help='The API key for your account')
    parser.add_argument('--domain', help='Required for search and find commands')
    parser.add_argument('--limit', help='Optional, used with search command.')
    parser.add_argument('--offset', help='Optional, used with search command.')
    parser.add_argument('--type', help='Optional, used with search command')
    parser.add_argument('--first_name', help='Required for find command')
    parser.add_argument('--last_name', help='Required for find command')
    parser.add_argument('--email', help='Required for verify command')
    file_help = 'Path to a CSV to be used with the specified command. CSV must have a column for each argument used'
    parser.add_argument('--file', help=file_help)
    args = parser.parse_args()

    handle_cli(**vars(args))


if __name__ == '__main__':
    main()
