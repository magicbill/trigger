import datetime
import sys
import time

import Queue

# TODO: Don't hard code this. Figure out how best to handle it.
import samples

def _next(trigger):
  try:
    expiration = trigger.next()
  except StopIteration:
    return None
  if isinstance(expiration, datetime.timedelta):
    expiration = datetime.datetime.now() + expiration
  return expiration

def _put_next(trigger, pq):
  expiration = _next(trigger)
  if expiration is not None:
    pq.put((expiration, trigger))

def initialize(triggers):
  pq = Queue.PriorityQueue()
  for trigger in triggers:
    _put_next(trigger, pq)
  return pq

def run(pq):
  if pq.empty():
    return
  while not pq.empty():
    expiration, trigger = pq.get()
    time_left = expiration - datetime.datetime.now()
    if time_left.total_seconds() > 0.0:
      time.sleep(time_left.total_seconds())
    _put_next(trigger, pq)

def main(triggers):
  pq = initialize(triggers)
  run(pq)

if __name__ == '__main__':
  triggers = set()
  for trigger_module in [samples]:
    triggers.update(trigger_module.get_triggers())
  main(triggers)
