# user management tools

Uses [signal-cli-rest-api](https://github.com/bbernhard/signal-cli-rest-api) to interrogate your Signal contacts and group memberships.

This requires you to register the `signal-cli-rest-api` instance as a linked device on whatever account you want to scan (presumably your personal account). This will cause some of your Signal information to be decrypted on your computer. You should only consider doing this on a computer you control and trust.

## list_users

Lists all the known users, preferring UUID (aka ACI), but defaulting to phone number or username if that is all that's avaialble. 

## scan_for_user

This app scans your contacts for a given tag or UUID. If it finds a user with the given UUID, or finds the tag in any of the nickname or notes fields, it will list all the groups where that user is found.

## quick start

Start the REST wrapper around signal-cli:
```
 mkdir $HOME/.local/share/signal-rest
 docker run --detach --name signal-rest -p 8080:8080 \                 
      --volume $HOME/.local/share/signal-rest:/home/.local/share/signal-cli \
      -e 'MODE=native' bbernhard/signal-cli-rest-api:0.100
```

Register the client as a linked device by scanning the [registration QR code](http://localhost:8080/v1/qrcodelink?device_name=signal-api) in the signal app.

Run the app to scan for people who have "REMOVED" in thier note field:
```
uv run python scan_for_tag.py --phone +PHONENUMBER --tag REMOVED
```

Once the scan is complete you should probably do these things:
- unlink your account from the app
- `docker stop signal-rest`
- `rm -rf $HOME/.local/share/signal-rest`

## discussion

The Signal UI does not display a stable identifier for contacts. This presents a challenge for groups attempting to track or identify troublemakers in large group settings. The profile display name can change at will (people often put status information in their profile names). The security number is intentionally designed to be non-durable, and can be intentionally changed by reinstalling the app without a backup (at the cost of losing message history, but not losing contacts or group memberships).

Individual users can tag users by attaching a note or a nickname to the account. These notations will survive changes in the underlying account profile name, phone number, and security number, because they are associated internally with the Account Credential Identifier (ACI), a unique 128-bit number. However, these notations are not shared across users.

These tools report the ACI of the user's contacts and allow the user to search contacts for tags they may have placed in notes or nicknames. The ACI can then be shared to other users to allow them to search for those users in their contacts and groups.

It seems to be the case that the only way to change the ACI is to delete the old account and register with Signal again, but that new account will not be connected to users or groups from the old account.

- ["Understanding every one of Signal’s identifiers"](https://freedom.press/digisec/blog/signal-identifiers/), Freedom of the Press Foundation
- [What is a safety number and why do I see that it changed?](https://support.signal.org/hc/en-us/articles/360007060632-What-is-a-safety-number-and-why-do-I-see-that-it-changed), Signal.org
- ["Decrypting messages: Extracting digital evidence from signal desktop for windows"](https://doi.org/10.1016/j.fsidi.2025.301941), Paulino, Negrão, Frade, and Domingues, Forens. Sci. Int. Digit. Investig. vol. 54, 2025
- ["Signal Infiltrator Check"](https://github.com/schlach/signal-check), schlach

## dependencies

relies on the [pysignalclirestapi](https://pypi.org/project/pysignalclirestapi/) package which is authored by the same person who maintains [signal-cli-rest-api](https://github.com/bbernhard/signal-cli-rest-api). That package in turn pulls in a handful of other [dependencies](./uv.lock).
