import unittest
import random
import timeit
from timeit import default_timer as timer
import subprocess
from subprocess import Popen, PIPE, STDOUT

def stress(n):
  instr = ['SET','GET','UNSET','BEGIN','NUMEQUALTO','ROLLBACK','COMMIT','END']
  randvals = [random.randrange(1,10001,1) for _ in range (n)]
  for test in randvals:
    print(random.choice(instr), test, test)


class NinjaDBWrapper():
  def __init__(self):
    self.process = Popen('python ninjadb.py', stdout=PIPE, stdin=PIPE, stderr=STDOUT, bufsize = 1)

  def send(self, line):
    # communicate returns tuple (stdout, stderr)
    res, _ = self.process.communicate(line)
    #res, _ = self.process.communicate(input=line.encode('utf-8'))
    #self.process.stdin.write(line)
    return res

  def close(self):
    self.process.terminate()

  def runAndClose(self, filename):
    with open(filename) as fhandle:
      fcontents = fhandle.read()
      output = self.send(fcontents)
      self.close()
      return output


class TestNinjaDB(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super(TestNinjaDB, self).__init__(*args, **kwargs)

    # for 32bit python
    self.cases = [100, 1000, 10000, 100000, 1000000]
    # using 64bit python? use this:
    #self.cases = [100, 1000, 10000, 100000, 1000000, 10000000]
    self.minCase = min(self.cases)
    self.maxCase = max(self.cases)

    self.tests = [('test_01.txt', 'test_01.assert.txt'),
                 ('test_02.txt', 'test_02.assert.txt'),
                 ('test_03.txt', 'test_03.assert.txt'),
                 ('test_04.txt', 'test_04.assert.txt')]

  # for each test file run and compare to the assertion
  def test_runtest_files(self):
    print('\nRunning and asserting all test files in directory ./tests\n')


    for tfile, tassert in self.tests:
      ninjadb = NinjaDBWrapper()
      runresult = ninjadb.runAndClose('./tests/' + tfile)
      shouldbe = open('./tests/' + tassert).read()
      # ignore CR and LF
      runresult = map(str.strip, runresult.strip().split('\n'))
      shouldbe = map(str.strip, shouldbe.strip().split('\n'))
      # ignore the welcome header
      runresult = runresult[1:]
      failmessage = 'Test %s did not pass!' % tfile
      self.assertEqual(runresult, shouldbe, failmessage)

  # helper function that runs performance tests
  def performance_test(self, cases, lines):
    # set up each case
    for case in cases:
      ninjadb = NinjaDBWrapper()
      # select only case amount of lines and convert to string
      t = '\n'.join(map(str, lines[:case]))

      start = timer()
      ninjadb.send(t)
      end = timer()

      elapsed = end - start
      average = elapsed / case
      print('elapsed: %f, averaging: %f, items: %d' % (elapsed, average, case))
      # finally we close this instance
      ninjadb.close()


 # if SET has a performance of O(1) the average should remain constant
 # NOTE: the memory requirements excede that of python 32 bit can provide
  def test_perf_set(self):
    print('\nRunning SET performance test %s to %s' % (self.minCase, self.maxCase))
    lines = ['SET %s %s' % (x, x) for x in xrange(1,self.maxCase)]
    self.performance_test(self.cases, lines)

  def test_perf_get(self):
    print('\nRunning SET & GET performance test %s to %s interpolated' % (self.minCase, self.maxCase))
    lines = ['SET %s %s\nGET %s' % (x, x, x) for x in xrange(1,self.maxCase)]
    self.performance_test(self.cases, lines)

  def test_perf_unset(self):
    print('\nRunning SET & UNSET performance test %s to %s interpolated' % (self.minCase, self.maxCase))
    lines = ['SET %s %s\nUNSET %s' % (x, x, x) for x in xrange(1,self.maxCase)]
    self.performance_test(self.cases, lines)

  def test_perf_numequalto(self):
    print('\nRunning SET & NUMEQUALTO performance test %s to %s interpolated' % (self.minCase, self.maxCase))
    lines = ['SET %s %s\nNUMEQUALTO %s' % (x, x, x) for x in xrange(1,self.maxCase)]
    self.performance_test(self.cases, lines)

  def test_perf_begin(self):
    print('\nRunning SET & BEGIN performance test %s to %s interpolated' % (self.minCase, self.maxCase))
    lines = ['SET %s %s\nBEGIN' % (x, x) for x in xrange(1,self.maxCase)]
    self.performance_test(self.cases, lines)



if __name__ == '__main__':
  unittest.main()
