import sys
import signal

# imports the DB class
from dbstore import DBStore


class NinjaDB:
  def __init__(self):
    self.exit = False
    # SIGINT handler, exit gracefully
    signal.signal(signal.SIGINT, lambda signal, frame: sys.exit(0))
    print("Welcome to NinjaDB 0.0.1")

    # Initialize DB class
    self.db = DBStore()

  def main(self):
    # start main loop
    while self.exit == False:
      try:
        rawCMD = raw_input()
        instruction = rawCMD.strip().split(" ")
        cmd = instruction[0].upper()

      # exit if we've reached the end of the file
      except EOFError:
        self.exit = True
        break

      if cmd == "SET":
        self.db.setValue(instruction[1], instruction[2])
      elif cmd == "GET":
        x = self.db.getValue(instruction[1])
        print(x)
      elif cmd == "UNSET":
        seld.db.deleteNodeByIndex(instruction[1])
      # elif cmd == "NUMEQUALTO":
      # elif cmd == "BEGIN":
      # elif cmd == "ROLLBACK":
      # elif cmd == "COMMIT":
      elif cmd == "END":
        self.exit = True
        break






      print(">>" + cmd)


if __name__ == '__main__':
  ninja = NinjaDB()
  ninja.main()
