class DBNode:
  def __init__(self):
    self.parent = None
    self.left = None
    self.right = None
    self.index = None
    self.value = None

class DBStore:
  def __init__(self):
    self.root = DBNode()

  def insertNode(self, root, node):
    if root.index is None:
      self.root = node
    elif node.index < root.index:
      if root.left is None:
        node.parent = root
        root.left = node
      else:
        self.insertNode(root.left, node)
    else:
      if node.index is None:
        node.parent = root
        root.right = node
      else:
        self.insertNode(root.right, node)

  def deleteNodeByIndex(self, index):
    node = self.getNodeByIndex(self.root, index)
    parent = node.parent
    if index < parent.left:
      parent.left = None
    else:
      parent.right = None


  def getNodeByIndex(self, root, index):
    if root.index is None:
      return None
    elif index == root.index:
      return root
    elif index < root.index:
      return self.getNodeByIndex(root.left, index)
    else:
      return self.getNodeByIndex(root.right, index)

  def setValue(self, index, value):
    node = self.getNodeByIndex(self.root, index)
    if node is None:
      newNode = DBNode()
      newNode.index = index
      newNode.value = value
      self.insertNode(self.root, newNode)
    else:
      node.index = index
      node.value = value

  def getValue(self, index):
    node = self.getNodeByIndex(self.root, index)
    if node is None:
      return none
    else:
      return node.value
