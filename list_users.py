import argparse
from pysignalclirestapi import SignalCliRestApi 
from util import display_name, signal_address

parser = argparse.ArgumentParser()
parser.add_argument('--url', default="http://localhost:8080")
parser.add_argument('--phone', required=True)
args = parser.parse_args()

def main():
    print("Hello from signal-id!")
    signal = SignalCliRestApi(args.url, args.phone)
    for contact in signal.get_contacts():
        print(f'{display_name(contact)} / address: {signal_address(contact)}')

if __name__ == "__main__":
    main()
