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