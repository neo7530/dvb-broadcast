#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Dvbt Tx
# Generated: Sun Nov  4 17:03:37 2018
##################################################

from gnuradio import blocks
from gnuradio import digital
from gnuradio import dtv
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from optparse import OptionParser
import ConfigParser
import osmosdr
import time
import sys

class DVBT_TX(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Dvbt Tx")

        ##################################################
        # Variables
        ##################################################
        self._bandwidth_config = ConfigParser.ConfigParser()
        self._bandwidth_config.read('./dvbt.conf')
        try: bandwidth = self._bandwidth_config.getint('dvbt', 'bandwidth')
        except: bandwidth = 8000000
        self.bandwidth = bandwidth
        self.samp_rate = samp_rate = (bandwidth/7)*8
        self._rf_gain_config = ConfigParser.ConfigParser()
        self._rf_gain_config.read('./dvbt.conf')
        try: rf_gain = self._rf_gain_config.getint('hackrf', 'rf_gain')
        except: rf_gain = 0
        self.rf_gain = rf_gain
        self._mode_config = ConfigParser.ConfigParser()
        self._mode_config.read('./dvbt.conf')
        try: mode = self._mode_config.get('dvbt', 'mode')
        except: mode = 0
        self.mode = mode
        self._if_gain_config = ConfigParser.ConfigParser()
        self._if_gain_config.read('./dvbt.conf')
        try: if_gain = self._if_gain_config.getint('hackrf', 'if_gain')
        except: if_gain = 0
        self.if_gain = if_gain
        self._guard_interval_config = ConfigParser.ConfigParser()
        self._guard_interval_config.read('./dvbt.conf')
        try: guard_interval = self._guard_interval_config.get('dvbt', 'guard_interval')
        except: guard_interval = 0
        self.guard_interval = guard_interval
        self._frequency_config = ConfigParser.ConfigParser()
        self._frequency_config.read('./dvbt.conf')
        try: frequency = self._frequency_config.getint('hackrf', 'frequency')
        except: frequency = 858000000
        self.frequency = frequency
        self._constellation_config = ConfigParser.ConfigParser()
        self._constellation_config.read('./dvbt.conf')
        try: constellation = self._constellation_config.get('dvbt', 'constellation')
        except: constellation = 0
        self.constellation = constellation
        self._coderate_config = ConfigParser.ConfigParser()
        self._coderate_config.read('./dvbt.conf')
        try: coderate = self._coderate_config.get('dvbt', 'coderate')
        except: coderate = 0
        self.coderate = coderate

	infile = str(sys.argv[1])

	#Constellation QPSK 16QAM 64QAM
	if constellation == "QPSK":
		const = dtv.MOD_QPSK
	elif constellation == "16QAM":
		const = dtv.MOD_16QAM
	elif constellation == "64QAM":
		const = dtv.MOD_64QAM
	else:
		sys.stderr.write("CONSTELLATION IN CONFIG WRONG! Values: QPSK, 16QAM or 64QAM \n");
        	sys.exit(1)

	# Coderate 1/2 2/3 3/4 5/6 7/8	

	if coderate == "1/2":
		codr = dtv.C1_2
	elif coderate == "2/3":
		codr = dtv.C2_3
	elif coderate == "3/4":
		codr = dtv.C3_4
	elif coderate == "5/6":
		codr = dtv.C5_6
	elif coderate == "7/8":
		codr = dtv.C7_8
	else:
		sys.stderr.write("CODERATE IN CONFIG WRONG! Values: 1/2, 2/3, 3/4, 5/6 or 7/8 \n");
        	sys.exit(1) 


	if mode == "2k":
		factor = 1
		carriers = 2048
		modus = dtv.T2k
	elif mode == "8k":
		factor = 4
		carriers = 8192
		modus = dtv.T8k
	else:
		sys.stderr.write("MODE IN CONFIG WRONG! Values: 2k or 8k \n");
        	sys.exit(1) 



	#guard_interval dtv.GI_1_32 1/4 1/8 1/16 1/32
	if guard_interval == "1/4":
		guardi = dtv.GI_1_4
		gi = carriers / 4
	elif guard_interval == "1/8":
		guardi = dtv.GI_1_8
		gi = carriers / 8
	elif guard_interval == "1/16":
		guardi = dtv.GI_1_16
		gi = carriers / 16
	elif guard_interval == "1/32":
		guardi = dtv.GI_1_32
		gi = carriers / 32
	else:
		sys.stderr.write("GUARD_INTERVAL IN CONFIG WRONG! Values: 1/4, 1/8, 1/16 or 1/32 \n");
        	sys.exit(1)



 
        ##################################################
        # Blocks
        ##################################################
        self.osmosdr_sink_0 = osmosdr.sink( args="numchan=" + str(1) + " " + '' )
        self.osmosdr_sink_0.set_sample_rate(samp_rate)
        self.osmosdr_sink_0.set_center_freq(frequency, 0)
        self.osmosdr_sink_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0.set_gain(rf_gain, 0)
        self.osmosdr_sink_0.set_if_gain(if_gain, 0)
        self.osmosdr_sink_0.set_bb_gain(0, 0)
        self.osmosdr_sink_0.set_antenna('', 0)
        self.osmosdr_sink_0.set_bandwidth(0, 0)
          
        self.fft_vxx_0 = fft.fft_vcc(carriers, False, (window.rectangular(carriers)), True, 1)
        self.dtv_dvbt_symbol_inner_interleaver_0 = dtv.dvbt_symbol_inner_interleaver((1512 * factor), modus, 1)
        self.dtv_dvbt_reference_signals_0 = dtv.dvbt_reference_signals(gr.sizeof_gr_complex, (1512 * factor), carriers, const, dtv.NH, codr, codr, guardi, modus, 1, 0)
        self.dtv_dvbt_reed_solomon_enc_0 = dtv.dvbt_reed_solomon_enc(2, 8, 0x11d, 255, 239, 8, 51, (8 * factor))
        self.dtv_dvbt_map_0 = dtv.dvbt_map((1512 * factor), const, dtv.NH, modus, 1)
        self.dtv_dvbt_inner_coder_0 = dtv.dvbt_inner_coder(1, (1512 * factor), const, dtv.NH, codr)
        self.dtv_dvbt_energy_dispersal_0 = dtv.dvbt_energy_dispersal(1 * factor)
        self.dtv_dvbt_convolutional_interleaver_0 = dtv.dvbt_convolutional_interleaver((136 * factor), 12, 17)
        self.dtv_dvbt_bit_inner_interleaver_0 = dtv.dvbt_bit_inner_interleaver((1512 * factor), const, dtv.NH, modus)
        self.digital_ofdm_cyclic_prefixer_0 = digital.ofdm_cyclic_prefixer(carriers, carriers+(gi), 0, '')
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((0.0022097087, ))

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


        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.osmosdr_sink_0, 0))    
        self.connect((self.digital_ofdm_cyclic_prefixer_0, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.dtv_dvbt_bit_inner_interleaver_0, 0), (self.dtv_dvbt_symbol_inner_interleaver_0, 0))    
        self.connect((self.dtv_dvbt_convolutional_interleaver_0, 0), (self.dtv_dvbt_inner_coder_0, 0))    
        self.connect((self.dtv_dvbt_energy_dispersal_0, 0), (self.dtv_dvbt_reed_solomon_enc_0, 0))    
        self.connect((self.dtv_dvbt_inner_coder_0, 0), (self.dtv_dvbt_bit_inner_interleaver_0, 0))    
        self.connect((self.dtv_dvbt_map_0, 0), (self.dtv_dvbt_reference_signals_0, 0))    
        self.connect((self.dtv_dvbt_reed_solomon_enc_0, 0), (self.dtv_dvbt_convolutional_interleaver_0, 0))    
        self.connect((self.dtv_dvbt_reference_signals_0, 0), (self.fft_vxx_0, 0))    
        self.connect((self.dtv_dvbt_symbol_inner_interleaver_0, 0), (self.dtv_dvbt_map_0, 0))    
        self.connect((self.fft_vxx_0, 0), (self.digital_ofdm_cyclic_prefixer_0, 0))    

    def get_bandwidth(self):
	print bandwidth
        return self.bandwidth

    def set_bandwidth(self, bandwidth):
        self.bandwidth = bandwidth
        self.set_samp_rate((self.bandwidth/7)*8)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.osmosdr_sink_0.set_sample_rate(self.samp_rate)

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain
        self.osmosdr_sink_0.set_gain(self.rf_gain, 0)

    def get_mode(self):
        return self.mode

    def set_mode(self, mode):
        self.mode = mode

    def get_if_gain(self):
        return self.if_gain

    def set_if_gain(self, if_gain):
        self.if_gain = if_gain
        self.osmosdr_sink_0.set_if_gain(self.if_gain, 0)

    def get_guard_interval(self):
        return self.guard_interval

    def set_guard_interval(self, guard_interval):
        self.guard_interval = guard_interval
        self._guard_interval_config = ConfigParser.ConfigParser()
        self._guard_interval_config.read('./dvbt.conf')
        if not self._guard_interval_config.has_section('dvbt'):
        	self._guard_interval_config.add_section('dvbt')
        self._guard_interval_config.set('dvbt', self.guard_interval, str(None))
        self._guard_interval_config.write(open('./dvbt.conf', 'w'))

    def get_frequency(self):
        return self.frequency

    def set_frequency(self, frequency):
        self.frequency = frequency
        self.osmosdr_sink_0.set_center_freq(self.frequency, 0)

    def get_constellation(self):
        return self.constellation

    def set_constellation(self, constellation):
        self.constellation = constellation

    def get_coderate(self):
        return self.coderate

    def set_coderate(self, coderate):
        self.coderate = coderate
        self._coderate_config = ConfigParser.ConfigParser()
        self._coderate_config.read('./dvbt.conf')
        if not self._coderate_config.has_section('dvbt'):
        	self._coderate_config.add_section('dvbt')
        self._coderate_config.set('dvbt', self.coderate, str(None))
        self._coderate_config.write(open('./dvbt.conf', 'w'))


def main(top_block_cls=DVBT_TX, options=None):

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
