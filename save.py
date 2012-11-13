#!/usr/bin/python

import shlex

class PrisonSave(dict):
  def __init__(self, filename):
    self.__repr__ = printPrisonDict
    super(dict, self).__init__()
    with open(filename) as f:
      parser = TokenParser(self)
      for line in f:
        tokens = shlex.split(line)
        for token in tokens:
          parser.parse(token)

def printPrisonDict(self, depth = 0):
  def printkey(key):
    if ' ' in key:
      key = '''"%s"''' % key
    return key.ljust(19 + 2 * depth) + " "
  objs = [] 
  values = []
  for key, value in self.iteritems():
    if isinstance(value, dict):
		objs.append(
      '''BEGIN %s %s\n END\n''' % (printkey(key), 
                                 printPrisonDict(value, depth + 1)) )
    else:
      values.append(printkey(key) + value)
  return "\n".join(values) + ''.join(objs)
      
     
class TokenParser:
  def __init__(self, manip):
    self.mode = self.NAME
    self.manip = manip
    self.stack = []

  def parse(self, token):
    if self.mode == self.NAME:
      if token == "BEGIN":
        self.mode = self.OBJNAME
      elif token == "END":
        self.manip = self.stack.pop()
      else:
        self.newvalName = token
        self.mode = self.VALUE
      return
    if self.mode == self.VALUE:
      self.manip[self.newvalName] = token
      self.mode = self.NAME
      return
    if self.mode == self.OBJNAME:
      self.stack.append(self.manip)
      self.manip[token] = dict()
      self.manip = self.manip[token]
      self.mode = self.NAME
      return

  # These are a crude enum.
  def NAME():
    pass
  def VALUE():
    pass
  def OBJNAME():
    pass        

      

TESTFILE = "Prison Architect/saves/ted.prison"
