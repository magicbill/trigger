''' Trigger task/job scheduler.

Trigger runs jobs.  Jobs are implemented as classes that are iterables that
return datetime or timedelta instances and additionally have an execute method
for performing some action.'''

import datetime
import sys
import thread
import time

import Queue

# TODO: Don't hard code this. Figure out how best to handle it.
import samples

def _get_next(trigger, last=None):
  if not last:
    last = datetime.datetime.now()
  try:
    expiration = trigger.next(last)
  except StopIteration:
    print 'StopIteration'
    return None
  if isinstance(expiration, datetime.timedelta):
    expiration = last + expiration
  if not isinstance(expiration, datetime.datetime):
    raise TypeError(
        'Trigger returned an invalid type "%s" (expected datetime or '
        'timedelta): %s' % (type(expiration), expiration))
  return expiration

def _put_next(trigger, pq, last=None):
  expiration = _get_next(trigger, last)
  if expiration is not None:
    pq.put((expiration, trigger))
  else:
    print 'Expiration was none, retiring job: %s' % type(trigger)

def _execute_in_thread(trigger):
  trigger.execute()

def _execute(trigger):
  thread.start_new_thread(_execute_in_thread, (trigger,))

def _next(trigger, pq, last=None):
  _put_next(trigger, pq, last)

def initialize(triggers):
  pq = Queue.PriorityQueue()
  for trigger in triggers:
    _next(trigger, pq)
  return pq

def run(pq):
  while not pq.empty():
    expiration, trigger = pq.get()
    time_left = (expiration - datetime.datetime.now()).total_seconds()
    if time_left > 0.0:
      time.sleep(time_left)
    # Asynchronously execute the trigger.
    _execute(trigger)
    # Synchronously get the next trigger expiration and put into PQ.
    _next(trigger, pq, expiration)

def main(triggers):
  # Initialize the PQ with all of the triggers.
  pq = initialize(triggers)
  # Run forever, or until there are no more triggers.
  run(pq)

if __name__ == '__main__':
  triggers = set()
  for trigger_module in [samples]:
    triggers.update(trigger_module.get_triggers())
  main(triggers)
