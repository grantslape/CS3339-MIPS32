# CS3339-MIPS32
Class Project for CS3339
[![Build Status](https://semaphoreci.com/api/v1/projects/60cb7614-3fe5-40f7-9c80-8cf79916ae93/1881968/badge.svg)](https://semaphoreci.com/grantslape-61/cs3339-mips32)
[![CodeFactor](https://www.codefactor.io/repository/github/grantslape/cs3339-mips32/badge)](https://www.codefactor.io/repository/github/grantslape/cs3339-mips32)
## Execution
From the project root:
1. Make sure Icarus Verilog is installed. Available on Homebrew for MacOS.  For Ubuntu:
```shell
    $ sudo apt-get install iverilog
```
1. Create a virtual env if you don't already have one:
```shell
    $ pip install virtualenv
    $ virtualenv venv
```
2. Activate and install MyHDL:
```shell
    $ source venv/bin/activate
    $ pip install -r requirements.txt
```
3. Set up Cosimulation:
```shell
    $ cd venv/share/myhdl/cosimulation/icarus
    $ make
    $ cd ../../../../..
    $ mv venv/share/myhdl/cosimulation/icarus/myhdl.vpi ./lib
```
3. Run tests!
```shell
    $ python test/test_all_modules.py
```
