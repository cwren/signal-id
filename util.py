from collections import Counter

def display_name(contact):
    if contact['nickname']['name']:
        return contact['nickname']['name']
    if contact['nickname']['given_name'] or contact['nickname']['family_name']:
        return f'{contact['nickname']['given_name']} {contact['nickname']['family_name']}'
    if contact['name']:
        return contact['name']
    if contact['profile_name']:
        return contact['profile_name']
    if contact['profile']['given_name'] or contact['profile']['lastname']:
        return f'{contact['profile']['given_name']} {contact['profile']['lastname']}'
    return 'Unknown'


def signal_address(contact):
    if contact['uuid']:
        return contact['uuid']
    if contact['number']:
        return contact['number']
    if contact['username']:
        return contact['username']
    else:
        return 'Unknown'
    
class Directory():
    def __init__(self, signal):
        self.identites = signal.list_indentities()
        self.contacts = signal.get_contacts()
        self.initialize_contact_list()


    def initialize_contact_list(self):
        counter = Counter()
        for id in self.identites:
            id['safety_number_a'] = id['safety_number'][:35]
            id['safety_number_b'] = id['safety_number'][-35:]
            counter.update([id['safety_number_a'], id['safety_number_b']])
        self.my_safety_number = counter.most_common(1)[0][0]
        
        for id in self.identites:
            id['safety_number'] = id['safety_number_a'] if id['safety_number_a'] != self.my_safety_number else id['safety_number_b']
        safety_by_uuid = { id['uuid'] : id['safety_number'] for id in self.identites }
        safety_by_number = { id['number'] : id for id in self.identites }
        
        for contact in self.contacts:
            if contact['uuid'] in safety_by_uuid:
                contact['safety_number'] = safety_by_uuid[contact['uuid']]
            elif contact['number'] in safety_by_number:
                contact['safety_number'] = safety_by_number[contact['number']]
            else:
                contact['safety_number'] = 'Unknown'
            contact['display_name'] = display_name(contact)
            contact['address'] = signal_address(contact)
            

    def matches_safety(self, contact, probe_input):
        probes = []
        if len(probe_input) == 35:
            # if half a safety number, use it as the probe
            probes.append(probe_input)
        else:
            # if full safety number, make sure half isn't ours, then search for both halves
            probes = [ p for p in [probe_input[:35], probe_input[-35:]] if p != self.my_safety_number ]
        return any([p == contact['safety_number'] for p in probes])