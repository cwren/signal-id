import argparse
from pathlib import Path
from pysignalclirestapi import SignalCliRestApi
from util import Directory, cleanup_config, should_report_contact_in_group, trim_config
import yaml

parser = argparse.ArgumentParser()
parser.add_argument('--url', default="http://localhost:8080")
parser.add_argument('--phone', required=True)
parser.add_argument('--tag', default="")
parser.add_argument('--uuid', default="")
parser.add_argument('--safety', default="")
parser.add_argument('--config', type=Path, default="config.yaml")
parser.add_argument('--create_config', action='store_true')
args = parser.parse_args()

def main():
    save_config = args.create_config
    new_config = True
    config = {}
    if args.config.exists():
        with open(args.config, 'r') as config_file:
            config = yaml.safe_load(config_file)
        save_config = True  # always update the fconfig it it already exists
        new_config = False
    cleanup_config(config)

    if not args.uuid and not args.tag and not args.safety:
        print('you must supply one of tag, UUID (aka ACI), or safety number to scan for')
        exit(2)

    if args.safety:
        if len(args.safety) == 35:
            print('searching for a safety number half')
        elif len(args.safety) == 71:
            print('searching for a whole safety number: may hit on the person who reported the safety number')
        else:
            print('safety number must be either 6 or 12 groups of 5 digits separated by single spaces')
            exit(2)

    if args.uuid:
        print(f'searching for a uuid: {args.uuid}')

    if args.tag:
        print(f'searching for a contact with a tag: {args.tag}')

    signal = SignalCliRestApi(args.url, args.phone)
    directory = Directory(signal)

    groups = signal.list_groups()
    in_contacts = False
    for contact in directory.contacts:
        tag_bag = ' '.join([
            contact['note'],
            contact['nickname']['name'],
            contact['nickname']['given_name'],
            contact['nickname']['family_name']
        ])
        if ((args.tag and args.tag in tag_bag) or
            (args.uuid and args.uuid == contact['uuid']) or
            (args.safety and directory.matches_safety(contact, args.safety))):
            in_contacts = True
            print(f'found {contact['display_name']}')
            print(f'\taddress: {contact['address']}')
            print(f'\tsafety number: {contact['safety_number']}')

            in_groups = False
            for group in groups:
                if contact['uuid'] in group['members']:
                    if should_report_contact_in_group(config, group, contact):
                        print(f'\tis in group {group['name']}')
                        in_groups = True
            if not in_groups:
                print('\tnot found in any monitored group')
                
    trim_config(config, directory, groups)

    if not in_contacts:
        print('no matching contacts found')

    if save_config:
        if new_config:
            print(f'saving config file to {args.config.resolve()}')
            print('This file contains sensitive information, make sure it is stored on secure media.')
        with open(args.config, 'w') as config_file:
            yaml.dump(config, config_file, default_flow_style=False)


if __name__ == "__main__":
    main()
