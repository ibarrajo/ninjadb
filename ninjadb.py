import sys
import signal

# This is the model for the database
from dbstore import DBStore

class NinjaDB:
  def __init__(self):
    self.exit = False
    # SIGINT handler, exit gracefully
    signal.signal(signal.SIGINT, lambda signal, frame: sys.exit(0))

    print('Welcome to NinjaDB 0.0.3')

    # Initialize DBStore object
    self.db = DBStore()

  def main(self):
    # start main loop until exit is True
    while not self.exit:
      try:
        #sys.stdout.write('> ')
        rawCMD = raw_input()
        args = rawCMD.strip().split(' ')
        if len(args) > 0:
          # make the command uppercase
          args[0] = args[0].upper()

      #exit if we've reached the end of the file
      except EOFError:
        self.exit = True
        break

      if args[0] == 'SET' and lengthIs(args, 3):
        self.db.set(args[1], args[2])

      elif args[0] == 'GET' and lengthIs(args, 2):
        res = self.db.get(args[1])
        # print either the value or NULL if it does not exist
        print('NULL' if res is None else res)

      elif args[0] == 'UNSET' and lengthIs(args, 2):
        self.db.unset(args[1])

      elif args[0] == 'NUMEQUALTO' and lengthIs(args, 2):
        count = self.db.getCount(args[1])
        print(count)

      elif args[0] == 'BEGIN':
        self.db.begin()

      elif args[0] == 'ROLLBACK':
        if self.db.delta == -1:
          print('NO TRANSACTION')
        else:
          self.db.rollback()

      elif args[0] == 'COMMIT':
        if self.db.delta == -1:
          print('NO TRANSACTION')
        else:
          self.db.commit()

      elif args[0] == 'END':
        self.exit = True
        break

      else:
        print('Invalid command entered: %s' % args[0])

# Helper function used to check the arguments length
def lengthIs(array, length):
  return len(array) == length


if __name__ == '__main__':
  ninja = NinjaDB()
  ninja.main()
