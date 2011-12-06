import datetime

def print1():
  while(True):
    print 1
    yield datetime.datetime.now() + datetime.timedelta(seconds=1)

def print5():
  while(True):
    print 5
    yield datetime.timedelta(seconds=5)

def get_triggers():
  return [print1(), print5()]
