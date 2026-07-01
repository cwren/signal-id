import argparse
from pysignalclirestapi import SignalCliRestApi 
from util import Directory

parser = argparse.ArgumentParser()
parser.add_argument('--url', default="http://localhost:8080")
parser.add_argument('--phone', required=True)
parser.add_argument('--show_safety', action="store_true")
args = parser.parse_args()

def main():
    print("Hello from signal-id!")
    signal = SignalCliRestApi(args.url, args.phone)
    directory = Directory(signal)
    for contact in directory.contacts:
        record = f'{contact['display_name']} / address: {contact['address']}'
        if args.show_safety:
            record += f'\n\tsafety_number: {contact['safety_number']}'
        
        print(record)

if __name__ == "__main__":
    main()

