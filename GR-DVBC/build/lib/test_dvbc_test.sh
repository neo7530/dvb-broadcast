#!/bin/sh
export VOLK_GENERIC=1
export GR_DONT_LOAD_PREFS=1
export srcdir=/home/marco/compile/gr-dvbc/lib
export PATH=/home/marco/compile/gr-dvbc/build/lib:$PATH
export LD_LIBRARY_PATH=/home/marco/compile/gr-dvbc/build/lib:$LD_LIBRARY_PATH
export PYTHONPATH=$PYTHONPATH
test-dvbc 
