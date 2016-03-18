class DBStore:
  def __init__(self):
    self.db = {}
    self.valCount = {}

  def set(self, index, value):
    # if updating remove the old value first
    # in order to update the valCount
    if index in self.db:
      self.unset(index)

    self.db.update({index: value})
    newCount = self.valCount.get(value, 0) + 1
    self.valCount.update({value: newCount})

  def get(self, index):
    return self.db.get(index)

  def unset(self, index):
    if index in self.db:
      oldValue = self.get(index)
      newCount = self.valCount.get(oldValue, 1) - 1
      self.valCount.update({oldValue: newCount})
      del self.db[index]


  def getCount(self, value):
    return self.valCount.get(value, 0)
