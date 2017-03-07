# dhuutils
Utilities for DHU students written in Python.

### Prerequisite
- [Python](https://www.python.org/) 3
- [requests](https://pypi.python.org/pypi/requests)
- [pyquery](https://pypi.python.org/pypi/pyquery)

### Components

#### student
Core functions.

#### select_course
Course selection utility. A course selection id should be provided.

#### delete_course
Course deletion utility. Note that this can only delete courses which have been matriculated. Since deleting courses is dangerous and
comparatively complicated, a list of selected courses is printed.

#### score_report
Score report fetching utility. A term (semester) should be provided to indicate which score report is demanded.
The format of a term is "xxxxyyyya" or "xxxxyyyys", where "xxxx" is the starting year, "yyyy" equals to "xxxx" + 1, "a" stands for the
first half of a school year, and "s" the second half.

#### schedule
Class schedule fetching utility. The same as above, a term should be provided.
