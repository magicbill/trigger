import datetime

import trigger

class Print10(trigger.AsyncTriggerBase):
  def execute(self):
    print 10

  def schedule(self):
    return datetime.timedelta(seconds=10)

class Print5(trigger.TriggerBase):
  def execute(self):
    print 5

  def schedule(self):
    return datetime.timedelta(seconds=5)

def get_triggers():
  return [Print10(), Print5()]

if __name__ == '__main__':
  server = trigger.TriggerServer(get_triggers())
  server.run_forever()
