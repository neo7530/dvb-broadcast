/* -*- c++ -*- */

#define DVBC_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "dvbc_swig_doc.i"

%{
#include "dvbc/dvbc_config.h"
#include "dvbc/symbolmapper_bb.h"
#include "dvbc/modulator_bc.h"
%}


%include "dvbc/dvbc_config.h"
%include "dvbc/symbolmapper_bb.h"
GR_SWIG_BLOCK_MAGIC2(dvbc, symbolmapper_bb);
%include "dvbc/modulator_bc.h"
GR_SWIG_BLOCK_MAGIC2(dvbc, modulator_bc);
