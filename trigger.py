''' Trigger task/job scheduler.

Trigger runs jobs.  Jobs are implemented as classes that are iterables that
return datetime or timedelta instances and additionally have an execute method
for performing some action.'''

import datetime
import thread
import time

import Queue


class TriggerBase(object):
  def __iter__(self):
    return self

  def execute(self):
    raise NotImplemented

  def schedule(self):
    raise NotImplemented

  def next(self):
    self.execute()
    return self.schedule()


class AsyncTriggerBase(TriggerBase):
  def next(self):
    thread.start_new_thread(self.execute, tuple())
    return self.schedule()


class TriggerServer(object):
  def __init__(self, triggers=None):
    self.pq = Queue.PriorityQueue()
    now = datetime.datetime.now()
    for trigger in triggers:
      self.pq.put((now, trigger))

  def _process_trigger(self, trigger, last=None):
    if not last:
      last = datetime.datetime.now()
    try:
      expiration = trigger.next()
    except StopIteration:
      print 'Trigger threw StopIteration.'
      return None
    if isinstance(expiration, datetime.timedelta):
      expiration = last + expiration
    if not isinstance(expiration, datetime.datetime):
      print ('Trigger returned an invalid type "%s" (expected datetime or '
             'timedelta): %s' % (type(expiration), expiration))
      return None
    return expiration

  def run_one(self, trigger, last=None):
    expiration = self._process_trigger(trigger, last)
    if expiration is not None:
      self.pq.put((expiration, trigger))
    else:
      print 'Retiring job: %s' % type(trigger)

  def run_forever(self):
    while not self.pq.empty():
      expiration, trigger = self.pq.get()
      time_left = (expiration - datetime.datetime.now()).total_seconds()
      if time_left > 0.0:
        time.sleep(time_left)
      self.run_one(trigger, expiration)
    print 'All triggers exhausted.  Exiting.'
