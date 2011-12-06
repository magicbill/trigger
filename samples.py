import datetime

class Print10(object):
  def __iter__(self):
    return self

  def next(self, last):
    return last + datetime.timedelta(seconds=10)

  def execute(self):
    print 10

class Print5(object):
  def __iter__(self):
    return self

  def next(self, _):
    return datetime.timedelta(seconds=5)

  def execute(self):
    print 5

def get_triggers():
  return [Print10(), Print5()]
