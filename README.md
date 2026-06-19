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

## dependencies

relies on the [pysignalclirestapi](https://pypi.org/project/pysignalclirestapi/) package which is authored by the same person who maintains [signal-cli-rest-api](https://github.com/bbernhard/signal-cli-rest-api). That package in turn pulls in a handful of other [dependencies](./uv.lock).