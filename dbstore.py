class DBStore:
  def __init__(self):
    self.db = {}
    self.valCount = {}
    # the database log of instructions
    self.history = []
    # the log level (aka history[delta])
    self.delta = -1

  def set(self, index, value):
    self.log('SET', index, value)
    # if updating remove update the valCount
    if index in self.db:
      oldValue = self.get(index)
      newCount = self.valCount.get(oldValue, 1) - 1
      self.valCount.update({oldValue: newCount})
    self.db.update({index: value})
    newCount = self.valCount.get(value, 0) + 1
    self.valCount.update({value: newCount})

  def get(self, index):
    return self.db.get(index)

  def unset(self, index):
    self.log('UNSET', index, None)
    if index in self.db:
      oldValue = self.get(index)
      newCount = self.valCount.get(oldValue, 1) - 1
      self.valCount.update({oldValue: newCount})
      del self.db[index]


  def getCount(self, value):
    return self.valCount.get(value, 0)

  def log(self, action, index, newValue):
    # if not doing any transactions, ignore the log
    if self.delta == -1:
      return
    else:
      oldValue = self.db.get(index)
      self.history[self.delta].append([action, index, newValue, oldValue])


  # unplay the actions of the current delta and recalculate valCount
  def rollback(self):
    # can't rollback to nothing..
    if self.delta < 0:
      return
    log = self.history[self.delta]
    log.reverse()
    for line in log:
      instr = line[0]
      index = line[1]
      newValue = line[2]
      oldValue = line[3]
      # we need to unset if it was set
      if instr == "SET":
        if index in self.db:
          del self.db[index]
        self.db.update({index: oldValue})
      # viceversa
      elif instr == "UNSET":
          self.db.update({index: oldValue})
    self.rebuildCounts()
    self.delta -= 1

  # set up a new delta
  def begin(self):
    self.delta += 1
    self.history.append([])

  # all changes are commited, clear the history and delta level
  def commit(self):
    self.history = []
    # maintain the minimum value for delta (-1)
    self.delta = -1


  # rebuild the valCount dictionary
  def rebuildCounts(self):
    valList = self.db.values()
    valDict = list(valList)
    self.valCount = dict(map(lambda x: (x, valList.count(x)), valDict))
    # sometimes a stray None results after rebuilding
    if None in self.valCount:
      del self.valCount[None]
