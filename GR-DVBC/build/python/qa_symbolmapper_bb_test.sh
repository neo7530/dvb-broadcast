#!/bin/sh
export VOLK_GENERIC=1
export GR_DONT_LOAD_PREFS=1
export srcdir=/home/marco/compile/gr-dvbc/python
export PATH=/home/marco/compile/gr-dvbc/build/python:$PATH
export LD_LIBRARY_PATH=/home/marco/compile/gr-dvbc/build/lib:$LD_LIBRARY_PATH
export PYTHONPATH=/home/marco/compile/gr-dvbc/build/swig:$PYTHONPATH
/usr/bin/python2 /home/marco/compile/gr-dvbc/python/qa_symbolmapper_bb.py 
