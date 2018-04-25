# MIPS Processor Implemented with Python and Icarus Verilog
## CS3339 Semester Project Spring 2018
[![Build Status](https://semaphoreci.com/api/v1/projects/60cb7614-3fe5-40f7-9c80-8cf79916ae93/1881968/badge.svg)](https://semaphoreci.com/grantslape-61/cs3339-mips32)
[![CodeFactor](https://www.codefactor.io/repository/github/grantslape/cs3339-mips32/badge)](https://www.codefactor.io/repository/github/grantslape/cs3339-mips32)

This project simulates a MIPS-like 5 stage pipeline through co-simulation between Python and Icarus Verilog.
The machine is implemented with a 32-bit architecture through the myHDL library.
### Execution :rocket:
From the project root:
1. Make sure Icarus Verilog is installed. Available on Homebrew for MacOS.  For Ubuntu:
```shell
    $ sudo apt-get install iverilog
```
2. Create a virtual env if you don't already have one:
```shell
    $ pip install virtualenv
    $ virtualenv venv
```
3. Activate and install MyHDL:
```shell
    $ source venv/bin/activate
    $ pip install -r requirements.txt
```
4. Set up Cosimulation:
```shell
    $ cd venv/share/myhdl/cosimulation/icarus
    $ make
    $ cd ../../../../..
    $ mv venv/share/myhdl/cosimulation/icarus/myhdl.vpi ./lib
```
5. Add modules to PYTHONPATH:
```shell
    $ export PYTHONPATH=`pwd`
```
6. Execute processor!
```shell
    $ python main.py
```

### Repository Explained :mag_right:
- **docs/:**
Find in depth instructions on how to run this repository through an Oracle virtual box.
Other files such as structure of modules and the operation codes for the arithmetic logic unit used in the machine.
  - Here's a snapshot of structure.txt, every module is described by the inputs and outputs as well as what module each signal came
  from or is going to.
![](https://github.com/grantslape/CS3339-MIPS32/docs/images/structure_pic.png)
- **Main.py:**
To kick off the simulation we start by running the main.py file at the root of the directory.
This is the driver to the simulation. Inside of main.py will be the code that initializes all of the components
of our processor so that we can also begin the simulation within this same file.

	- Main.py also includes a series of output statements that tell us all our signals and modules are
working together properly. The output gives us a clear idea of the 5 stages of the pipeline.
![](https://github.com/grantslape/CS3339-MIPS32/docs/images/image.png)
- **src/:**
Holds all the elements necessary to simulate the 5-stage pipeline co-simulation
  - commons/: modules that get called regularly by the component modules of the machine. (ex. clock)
  - python/: all the component modules of the machine written in the Python language.
  Notice that each file has a second co-simulation function, this is how we are able to simulate the python and verilog side-by-side
  - verilog/: all the component modules of the machine written in the verilog hardware description language. The directory also
  includes test benches for every module denoted with "_tb" following the specific module name.

- **lib/:**
Holds all of the static files used in the simulation. Files that represent the instruction memory and data memory are stored here.

- **test/:**
Stores the tests used to check that both the python and verilog are working in sync.

To test all modules (from root):
```shell
python test/test_all_modules.py
```
To test a specific module (from root):
```shell
python test/test_module_name.py
```
>run these commands only after you've gone through the Execution steps.

### Links :key:
- [myHDL Download](myhdl.org)
- [myHDL Documentation](http://docs.myhdl.org/en/master/index.html)

- [iverilog Download](http://iverilog.wikia.com/wiki/Installation_Guide)

- [virtualenv Download](https://virtualenv.pypa.io/en/stable/)

### Authors :computer:
- Grant Slape
- Isaac Jaimes
- Patrick Vinas
- Mark Gitthens
- Serena Gutierrez
- Natalie Garza
- Huan Wu

### Acknowledgements :book:
Computer Organization and Design: The Hardware/Software Interface *by David Patterson and John Hennessy*
