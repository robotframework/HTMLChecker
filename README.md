A [Robot Framework](http://robotframework.org) test library for running checks and validations on HTML files.

Downloads are available at https://github.com/robotframework/HTMLChecker/downloads

Developing
----------
[Paver](http://paver.github.com/paver/) is used as a build tool.

Available tasks are:

* `atest` - run the acceptance tests
* `doc`  - create library documentation
* `dist` - create source distribution
* `bdist_wininst` - create graphical Windows installer (needs to run on a Windows box)
* `release` - runs `doc`, `sdist` and `git tag`

Version number is defined in `pavement.py`

