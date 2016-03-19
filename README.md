# NinjaDB

This is NinjaDB a simple on-memory database similar to Redis.
Created in response to a coding challenge by [Thumbtack](http://thumbtack.com)

The first implementation was done based on a BST data model. Mid project
I reached the conclusion that ultimate performance could be achieved with two
dictionaries (hash tables in parseltongue) while also simplifying the code.

The implementation is separated in `ninjadb.py` which provides the interface and
`dbstore.py` which handles the `DBStore` object that manages the actual model.

## Running

The application should be run with Python 2.7, it doesn't require any additional
modules apart from the standard library.

To run, issue `python ninjadb.py`  
To test, issue `python test.py`

## Supported commands

NinjaDB supports the following commands.

- SET
- GET  
- UNSET
- NUMEQUALTO
- BEGIN
- ROLLBACK
- COMMIT
- END

The commands can also be lowercase or mixed case.
Any invalid arguments and commands are discarded with an error notice.


## Command reference

SET
> SET myFavoriteColor blue

Variable names and their values must be separated by a space, and so they may
not contain spaces inside.

ie. `SET my fav color cool blue` is incorrect.

---

GET
> GET myFavoriteColor

This commands outputs 'blue'

---

UNSET
> UNSET myFavoriteColor

This deletes the variable myFavoriteColor

---

NUMEQUALTO
> NUMEQUALTO blue

Calculates the count of variables where blue is the value.

---

BEGIN

It begins a new transaction that can be either commited or rolledback.

---

ROLLBACK

The database is recovered to the state when the last BEGIN was issued.

---

COMMIT

It commits ALL transactions up to that point.

---

END

Exit the program.

---

## Testing and performance

Testing is automated in `test.py`.

All commands are tested for a correct and fast response. The test input files
are located at `./tests/` with their corresponding output assertions.

The performance tests uses more than 4GB of RAM when testing above 1M items.
It's best to run a 64bit version of Python to avoid memory limit issues.
The scales of the test can be changed at `self.cases = [100, 1000, 10000,
100000, 1000000]`
in the `test.py` script.

All methods* have a O(1) (constant) average runtime.
There is a startup cost to initialize the database each time it's run,
that's why there is a bigger average time on smaller data sets.

Note that the database runs everything in a single thread, and does not get to
benefit from multi-core systems.


> The following performance test was in a dual Xeon workstation with 48GBs of
< RAM.
>
> Testing more than 100M items started to slow down the inserts due to RAM
> exhaustion and having to store the data in the SSD.
> - Dual X5670 at 2.93GHz
> - 48GB of DDR3 ECC Registered RAM
> - Python 2.7.11 64bit
> - Windows 10 64bit

```
C:\Users\ibarr\ninjadb (master)
λ C:\Python27x64\python.exe test.py

Running SET & BEGIN performance test 100 to 10000000 interpolated
elapsed: 0.079192, averaging: 0.000792, items: 100
elapsed: 0.084621, averaging: 0.000085, items: 1000
elapsed: 0.157763, averaging: 0.000016, items: 10000
elapsed: 0.951519, averaging: 0.000010, items: 100000
elapsed: 9.470616, averaging: 0.000009, items: 1000000
elapsed: 93.974771, averaging: 0.000009, items: 10000000
.
Running SET & GET performance test 100 to 10000000 interpolated
elapsed: 0.076332, averaging: 0.000763, items: 100
elapsed: 0.083215, averaging: 0.000083, items: 1000
elapsed: 0.146190, averaging: 0.000015, items: 10000
elapsed: 0.816347, averaging: 0.000008, items: 100000
elapsed: 7.606623, averaging: 0.000008, items: 1000000
elapsed: 77.057782, averaging: 0.000008, items: 10000000
.
Running SET & NUMEQUALTO performance test 100 to 10000000 interpolated
elapsed: 0.078494, averaging: 0.000785, items: 100
elapsed: 0.082751, averaging: 0.000083, items: 1000
elapsed: 0.155198, averaging: 0.000016, items: 10000
elapsed: 0.850766, averaging: 0.000009, items: 100000
elapsed: 7.981352, averaging: 0.000008, items: 1000000
elapsed: 80.930924, averaging: 0.000008, items: 10000000
.
Running SET performance test 100 to 10000000
elapsed: 0.076280, averaging: 0.000763, items: 100
elapsed: 0.081526, averaging: 0.000082, items: 1000
elapsed: 0.112757, averaging: 0.000011, items: 10000
elapsed: 0.489432, averaging: 0.000005, items: 100000
elapsed: 4.336637, averaging: 0.000004, items: 1000000
elapsed: 43.285739, averaging: 0.000004, items: 10000000
.
Running SET & UNSET performance test 100 to 10000000 interpolated
elapsed: 0.076576, averaging: 0.000766, items: 100
elapsed: 0.083114, averaging: 0.000083, items: 1000
elapsed: 0.152977, averaging: 0.000015, items: 10000
elapsed: 0.879447, averaging: 0.000009, items: 100000
elapsed: 8.362718, averaging: 0.000008, items: 1000000
elapsed: 83.080214, averaging: 0.000008, items: 10000000
.
Running and asserting all test files in directory ./tests.

.
----------------------------------------------------------------------
Ran 6 tests in 453.302s

OK
```
