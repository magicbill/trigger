# Trigger

Trigger is a modern task/job scheduler (cron replacement) written in Python.

## Features (eventually)

1. Daemon to replace cron.
2. Jobs are specified as iterables that yield a datetime or timedelta for when they should run next and provide an execute function for performing some action.  The execute calls are done asynchronously.
3. State is saved so that triggers can continue running from where they left off.
4. User-level configuration.

## Status

This is a prototype implementation. There is not yet built-in daemon functionality and the state is not currently saved. There is no advanced configuration.  To add/remove jobs, you must edit the list returned by the ```get_triggers``` function in ```samples.py```.
