from collections import Counter

def cleanup_config(config):
    if not 'groups' in config:
        config['groups'] = {}
    for gid in config['groups']:
        if 'group_name' not in config['groups'][gid]:
            config['groups'][gid]['group_name'] = 'Unknown'

        if 'monitor_group' not in config['groups'][gid]:
            config['groups'][gid]['monitor_group'] = True

        if 'warnings' not in config['groups'][gid]:
            config['groups'][gid]['warnings'] = {}

        for uuid in config['groups'][gid]['warnings']:
            if 'display_name' not in config['groups'][gid]['warnings'][uuid]:
                config['groups'][gid]['warnings'][uuid]['display_name'] = 'Unknown'

            if 'pass' not in config['groups'][gid]['warnings'][uuid]:
                config['groups'][gid]['warnings'][uuid]['report'] = True


def should_monitor_group(config, group):
    gid = group['internal_id']
    if gid not in config['groups']:
        config['groups'][gid] = {
            'group_name': group['name'],
            'monitor_group': True,
            'warnings': {}, 
        }
    else:
        config['groups'][gid]['group_name'] = group['name'] # update group name

    return config['groups'][gid]['monitor_group']


def should_report_contact_in_group(config, group, contact):
    if should_monitor_group(config, group):
        gid = group['internal_id']
        uid = contact['uuid']
        if uid not in config['groups'][gid]['warnings']:
            config['groups'][gid]['warnings'][uid] = {
                    'display_name': contact['display_name'],
                    'report': True
                }
        else:
            config['groups'][gid]['warnings'][uid]['display_name'] = contact['display_name'] # update group name
        return config['groups'][gid]['warnings'][uid]['report']
    else:
        return False


def trim_config(config, directory, groups):
    valid_gids = [ group['internal_id'] for group in groups ]
    valid_uids = [ contact['uuid'] for contact in directory.contacts ]

    config['groups'] = { gid: data for gid, data in config['groups'].items() if gid in valid_gids }
    for gid in config['groups']:
        config['groups'][gid]['warnings'] = { uid: data for uid, data in config['groups'][gid]['warnings'].items() if uid in valid_uids }


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