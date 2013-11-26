# Nmap Service

This is a HTTP service that allows clients to find out what ports they
have open to the world.

This was written for use in Sensu, allowing servers to find out what
ports they have externally. Since it's intended to be run on an
externally accessible machine, you can require users to pass a key
argument. You can generate a secret file by:

    $ tr -dc _A-Z-a-z-0-9 </dev/urandom | head -c20 > SECRET

The server will check for this file on startup.

## Running the code

You will need Python 3.

    $ virtualenv ~/.envs/nmapservice -p python3
    $ . ~/.envs/nmapservice/bin/activate
    $ pip install -r requirements.pip
    $ DEBUG=y python server.py

## Deploying

On your production server, simply run:

    $ gunciorn server:app

If you're not inside the virtualenv, you can do:

    $ ~/.envs/nmapservice/bin/gunicorn server:app

Both of these commands need to run inside the source directory.

## License

MIT license.
