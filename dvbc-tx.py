#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Dvbc Tx Nogui
# Generated: Mon Nov  5 17:08:30 2018
##################################################

from gnuradio import blocks
from gnuradio import dtv
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import ConfigParser
import dvbc
import osmosdr
import time
import sys

class dvbc_tx_NOGUI(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Dvbc Tx Nogui")

        ##################################################
        # Variables
        ##################################################
        self._symrate_config = ConfigParser.ConfigParser()
        self._symrate_config.read('./dvbc.conf')
        try: symrate = self._symrate_config.getint('dvbc', 'symbolrate')
        except: symrate = 0
        self.symrate = symrate
        self.samp_rate = samp_rate = symrate * 2
        self.rrc_taps = rrc_taps = 100
        self._rf_gain_config = ConfigParser.ConfigParser()
        self._rf_gain_config.read('./dvbc.conf')
        try: rf_gain = self._rf_gain_config.getint('hackrf', 'rf-gain')
        except: rf_gain = 0
        self.rf_gain = rf_gain
        self._mode_config = ConfigParser.ConfigParser()
        self._mode_config.read('./dvbc.conf')
        try: mode = self._mode_config.get('dvbc', 'mode')
        except: mode = 0
        self.mode = mode
        self._if_gain_config = ConfigParser.ConfigParser()
        self._if_gain_config.read('./dvbc.conf')
        try: if_gain = self._if_gain_config.getint('hackrf', 'if-gain')
        except: if_gain = 0
        self.if_gain = if_gain
        self._center_freq_config = ConfigParser.ConfigParser()
        self._center_freq_config.read('./dvbc.conf')
        try: center_freq = self._center_freq_config.getint('hackrf', 'frequency')
        except: center_freq = 0
        self.center_freq = center_freq

	infile = str(sys.argv[1])

	if mode == "16QAM":
		mod = dvbc.MOD_16QAM
	elif mode == "32QAM":
		mod = dvbc.MOD_32QAM
	elif mode == "64QAM":
		mod = dvbc.MOD_64QAM
	elif mode == "128QAM":
		mod = dvbc.MOD_128QAM
	elif mode == "256QAM":
		mod = dvbc.MOD_256QAM
	else:
		sys.stderr.write("MODE IN CONFIG WRONG! Values: 16QAM, 32QAM, 64QAM, 128QAM or 256QAM \n");
        	sys.exit(1)

	print "Frequency: ", center_freq/1000000, "Mhz / Mode: ",mode ,"/ Symbolrate: ",symrate/1000 ,"\n"

        ##################################################
        # Blocks
        ##################################################
        self.osmosdr_sink_1 = osmosdr.sink( args="numchan=" + str(1) + " " + 'hackrf,buffers=128,buflen=32768' )
        self.osmosdr_sink_1.set_sample_rate(samp_rate)
        self.osmosdr_sink_1.set_center_freq(center_freq, 0)
        self.osmosdr_sink_1.set_freq_corr(0, 0)
        self.osmosdr_sink_1.set_gain(rf_gain, 0)
        self.osmosdr_sink_1.set_if_gain(if_gain, 0)
        self.osmosdr_sink_1.set_bb_gain(0, 0)
        self.osmosdr_sink_1.set_antenna('', 0)
        self.osmosdr_sink_1.set_bandwidth(8750000, 0)
          
        self.fft_filter_xxx_0 = filter.fft_filter_ccc(1, (firdes.root_raised_cosine(0.85, samp_rate, samp_rate/2, 0.15, rrc_taps)), 1)
        self.fft_filter_xxx_0.declare_sample_delay(0)
        self.dvbc_symbolmapper_bb_0 = dvbc.symbolmapper_bb(mod)
        self.dvbc_modulator_bc_0 = dvbc.modulator_bc(mod)
        self.dtv_dvbt_reed_solomon_enc_0 = dtv.dvbt_reed_solomon_enc(2, 8, 0x11d, 255, 239, 8, 51, 8)
        self.dtv_dvbt_energy_dispersal_0 = dtv.dvbt_energy_dispersal(1)
        self.dtv_dvbt_convolutional_interleaver_0 = dtv.dvbt_convolutional_interleaver(136, 12, 17)

	if infile == "-":
		self.blocks_file_descriptor_source_0 = blocks.file_descriptor_source(gr.sizeof_char*1, 0, True)
	else:
        	self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, infile, True)


        ##################################################
        # Connections
        ##################################################

	if infile == "-":
		self.connect((self.blocks_file_descriptor_source_0, 0), (self.dtv_dvbt_energy_dispersal_0, 0))
	else:
        	self.connect((self.blocks_file_source_0, 0), (self.dtv_dvbt_energy_dispersal_0, 0))    
        

	self.connect((self.dtv_dvbt_convolutional_interleaver_0, 0), (self.dvbc_symbolmapper_bb_0, 0))    
        self.connect((self.dtv_dvbt_energy_dispersal_0, 0), (self.dtv_dvbt_reed_solomon_enc_0, 0))    
        self.connect((self.dtv_dvbt_reed_solomon_enc_0, 0), (self.dtv_dvbt_convolutional_interleaver_0, 0))    
        self.connect((self.dvbc_modulator_bc_0, 0), (self.fft_filter_xxx_0, 0))    
        self.connect((self.dvbc_symbolmapper_bb_0, 0), (self.dvbc_modulator_bc_0, 0))    
        self.connect((self.fft_filter_xxx_0, 0), (self.osmosdr_sink_1, 0))    

    def get_symrate(self):
        return self.symrate

    def set_symrate(self, symrate):
        self.symrate = symrate
        self.set_samp_rate(self.symrate * 2)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.osmosdr_sink_1.set_sample_rate(self.samp_rate)
        self.fft_filter_xxx_0.set_taps((firdes.root_raised_cosine(0.85, self.samp_rate, self.samp_rate/2, 0.15, self.rrc_taps)))

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps
        self.fft_filter_xxx_0.set_taps((firdes.root_raised_cosine(0.85, self.samp_rate, self.samp_rate/2, 0.15, self.rrc_taps)))

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain
        self.osmosdr_sink_1.set_gain(self.rf_gain, 0)

    def get_mode(self):
        return self.mode

    def set_mode(self, mode):
        self.mode = mode
        self._mode_config = ConfigParser.ConfigParser()
        self._mode_config.read('./dvbc.conf')
        if not self._mode_config.has_section('dvbc'):
        	self._mode_config.add_section('dvbc')
        self._mode_config.set('dvbc', self.mode, str(None))
        self._mode_config.write(open('./dvbc.conf', 'w'))

    def get_if_gain(self):
        return self.if_gain

    def set_if_gain(self, if_gain):
        self.if_gain = if_gain
        self.osmosdr_sink_1.set_if_gain(self.if_gain, 0)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.osmosdr_sink_1.set_center_freq(self.center_freq, 0)


def main(top_block_cls=dvbc_tx_NOGUI, options=None):

    tb = top_block_cls()
    tb.start()
    if not str(sys.argv[1]) == "-":
    	try:
    	    raw_input('Press Enter to quit: ')
    	except EOFError:
    	    pass
    	tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
