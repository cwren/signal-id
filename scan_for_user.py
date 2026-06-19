import argparse
from pysignalclirestapi import SignalCliRestApi 
from util import display_name, signal_address

parser = argparse.ArgumentParser()
parser.add_argument('--url', default="http://localhost:8080")
parser.add_argument('--phone', required=True)
parser.add_argument('--tag', default="")
parser.add_argument('--uuid', default="")
args = parser.parse_args()

def main():
    print("Hello from signal-id!")
    if not args.uuid and not args.tag:
        print('you must supply either a tag or a UUID (aka ACI) to scan for')
        exit(2)
    signal = SignalCliRestApi(args.url, args.phone)
    groups = []
    for contact in signal.get_contacts():
        tag_bag = [
            contact['note'],
            contact['nickname']['name'],
            contact['nickname']['given_name'],
            contact['nickname']['family_name']
        ]
        if ((args.tag and any(args.tag in note for note in tag_bag)) or
            (args.uuid and args.uuid == contact['uuid'])):
            print(f'found {display_name(contact)}')
            print(f'\taddress: {signal_address(contact)}')
            if not groups:
                groups = signal.list_groups()
            hit = False
            for group in groups:
                if contact['uuid'] in group['members']:
                   print(f'\tis in group {group['name']}')
                   hit = True
            if not hit:
                print('\tnot found in any group')


if __name__ == "__main__":
    main()
