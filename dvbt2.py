#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Dvbt2 Master
# Generated: Tue Nov  6 18:22:49 2018
##################################################

from gnuradio import blocks
from gnuradio import digital
from gnuradio import dtv
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import ConfigParser
import osmosdr
import time
import sys

class DVBT2_Master(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Dvbt2 Master")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = (8000000.0 * 8) / 7
        self._rf_gain_config = ConfigParser.ConfigParser()
        self._rf_gain_config.read('./dvbt2.conf')
        try: rf_gain = self._rf_gain_config.getint('hackrf', 'rf-gain')
        except: rf_gain = 0
        self.rf_gain = rf_gain
        self._if_gain_config = ConfigParser.ConfigParser()
        self._if_gain_config.read('./dvbt2.conf')
        try: if_gain = self._if_gain_config.getint('hackrf', 'if-gain')
        except: if_gain = 0
        self.if_gain = if_gain
        self._center_freq_config = ConfigParser.ConfigParser()
        self._center_freq_config.read('./dvbt2.conf')
        try: center_freq = self._center_freq_config.getint('hackrf', 'frequency')
        except: center_freq = 0
        self.center_freq = center_freq
        self._band_width_config = ConfigParser.ConfigParser()
        self._band_width_config.read('./dvbt2.conf')
        try: band_width = self._band_width_config.getint('hackrf', 'bandwidth')
        except: band_width = 0
        self.band_width = band_width
        self._VERSION_config = ConfigParser.ConfigParser()
        self._VERSION_config.read('./dvbt2.conf')
        try: VERSION = self._VERSION_config.getint('dvbt2', 'version')
        except: VERSION = 0
        self.VERSION = VERSION
        self._PREAMBLE_config = ConfigParser.ConfigParser()
        self._PREAMBLE_config.read('./dvbt2.conf')
        try: PREAMBLE = self._PREAMBLE_config.get('dvbt2', 'preamble')
        except: PREAMBLE = '0'
        self.PREAMBLE = PREAMBLE
        self._PILOT_config = ConfigParser.ConfigParser()
        self._PILOT_config.read('./dvbt2.conf')
        try: PILOT = self._PILOT_config.getint('dvbt2', 'pilot-pattern')
        except: PILOT = 0
        self.PILOT = PILOT
        self._PAPR_config = ConfigParser.ConfigParser()
        self._PAPR_config.read('./dvbt2.conf')
        try: PAPR = self._PAPR_config.get('dvbt2', 'papr')
        except: PAPR = '0'
        self.PAPR = PAPR
        self._L1MOD_config = ConfigParser.ConfigParser()
        self._L1MOD_config.read('./dvbt2.conf')
        try: L1MOD = self._L1MOD_config.get('dvbt2', 'L1-mod')
        except: L1MOD = '0'
        self.L1MOD = L1MOD
        self._GI_config = ConfigParser.ConfigParser()
        self._GI_config.read('./dvbt2.conf')
        try: GI = self._GI_config.get('dvbt2', 'guard-interval')
        except: GI = '0'
        self.GI = GI
        self._FFTSIZE_config = ConfigParser.ConfigParser()
        self._FFTSIZE_config.read('./dvbt2.conf')
        try: FFTSIZE = self._FFTSIZE_config.get('dvbt2', 'fft-size')
        except: FFTSIZE = '0'
        self.FFTSIZE = FFTSIZE
        self._FECBLKS_config = ConfigParser.ConfigParser()
        self._FECBLKS_config.read('./dvbt2.conf')
        try: FECBLKS = self._FECBLKS_config.getint('dvbt2', 'fec-blocks')
        except: FECBLKS = 0
        self.FECBLKS = FECBLKS
        self._DATASYM_config = ConfigParser.ConfigParser()
        self._DATASYM_config.read('./dvbt2.conf')
        try: DATASYM = self._DATASYM_config.getint('dvbt2', 'datasymbols')
        except: DATASYM = 0
        self.DATASYM = DATASYM
        self._CONSTELLATION_config = ConfigParser.ConfigParser()
        self._CONSTELLATION_config.read('./dvbt2.conf')
        try: CONSTELLATION = self._CONSTELLATION_config.get('dvbt2', 'constellation')
        except: CONSTELLATION = '0'
        self.CONSTELLATION = CONSTELLATION
        self._CODERATE_config = ConfigParser.ConfigParser()
        self._CODERATE_config.read('./dvbt2.conf')
        try: CODERATE = self._CODERATE_config.get('dvbt2', 'coderate')
        except: CODERATE = '0'
        self.CODERATE = CODERATE
        self._CARREXT_config = ConfigParser.ConfigParser()
        self._CARREXT_config.read('./dvbt2.conf')
        try: CARREXT = self._CARREXT_config.get('dvbt2', 'ext-carriers')
        except: CARREXT = '0'
        self.CARREXT = CARREXT

	infile = str(sys.argv[1])

	if VERSION == 111:
		ver = dtv.VERSION_111
	elif VERSION == 131:
		ver = dtv.VERSION_131
	else:
		sys.stderr.write("VERSION IN CONFIG WRONG! Values: 111 or 131 \n");
		sys.exit(1)

	if PREAMBLE == "SISO":
		preamb = dtv.PREAMBLE_T2_SISO
	elif PREAMBLE == "MISO":
		preamb = dtv.PREAMBLE_T2_MISO
	else:
		sys.stderr.write("PREAMBLE IN CONFIG WRONG! Values: SISO or MISO \n");
		sys.exit(1)			

	if PILOT == 1:
		pil = dtv.PILOT_PP1
	elif PILOT == 2:
		pil = dtv.PILOT_PP2
	elif PILOT == 3:
		pil = dtv.PILOT_PP3
	elif PILOT == 4:
		pil = dtv.PILOT_PP4
	elif PILOT == 5:
		pil = dtv.PILOT_PP5
	elif PILOT == 6:
		pil = dtv.PILOT_PP6
	elif PILOT == 7:
		pil = dtv.PILOT_PP7
	elif PILOT == 8:
		pil = dtv.PILOT_PP8
	else:
		sys.stderr.write("PILOT-PATTERN IN CONFIG WRONG! Values: 1, 2, 3, 4, 5, 6, 7 or 8 \n");
		sys.exit(1)		

	if PAPR == "on":
		pap = dtv.PAPR_ON
	elif PAPR == "off":
		pap = dtv.PAPR_OFF
	else:
		sys.stderr.write("PAPR IN CONFIG WRONG! Values: on or off \n");
		sys.exit(1)

	if L1MOD == "QPSK":
		l1m = dtv.L1_MOD_QPSK
	elif L1MOD == "BPSK":
		l1m = dtv.L1_MOD_BPSK
	elif L1MOD == "16QAM":
		l1m = dtv.L1_MOD_16QAM
	elif L1MOD == "64QAM":
		l1m = dtv.L1_MOD_64QAM
	else:
		sys.stderr.write("L1-MOD IN CONFIG WRONG! Values: QPSK, BPSK, 16QAM or 64QAM \n");
		sys.exit(1)

	if GI == "1/32":
		gint = dtv.GI_1_32
		mul = 1
		div = 32
	elif GI == "1/16":
		gint = dtv.GI_1_16
		mul = 1
		div = 16
	elif GI == "1/8":
		gint = dtv.GI_1_8
		mul = 1
		div = 8
	elif GI == "1/4":
		gint = dtv.GI_1_4
		mul = 1
		div = 4
	elif GI == "1/128":
		gint = dtv.GI_1_128
		mul = 1
		div = 128
	elif GI == "19/128":
		gint = dtv.GI_19_128
		mul = 19
		div = 128
	elif GI == "19/256":
		gint = dtv.GI_19_256
		mul = 19
		div = 256
	else:
		sys.stderr.write("GUARD-INTERVAL IN CONFIG WRONG! Values: 1/32, 1/16, 1/8, 1/4, 1/128, 19/128, 19/256 \n");
		sys.exit(1)

	if FFTSIZE == "16k":
		ffts = dtv.FFTSIZE_16K
		fft_length = 16384
	elif FFTSIZE == "32k":
		ffts = dtv.FFTSIZE_32K
		fft_length = 32768
	else:
		sys.stderr.write("FFTSIZE IN CONFIG WRONG! Values: 16k or 32k \n");
		sys.exit(1)	

	if CONSTELLATION == "QPSK":
		const = dtv.MOD_QPSK
	elif CONSTELLATION == "16QAM":
		const = dtv.MOD_16QAM
	elif CONSTELLATION == "64QAM":
		const = dtv.MOD_64QAM
	elif CONSTELLATION == "256QAM":
		const = dtv.MOD_256QAM
	else:
		sys.stderr.write("CONSTELLATION IN CONFIG WRONG! Values: QPSK 16QAM 64QAM 256QAM \n");
		sys.exit(1)

	if CODERATE == "1/2":
		codr = dtv.C1_2
	elif CODERATE == "2/5":
		codr = dtv.C2_5
	elif CODERATE == "3/5":
		codr = dtv.C3_5
	elif CODERATE == "2/3":
		codr = dtv.C2_3
	elif CODERATE == "3/4":
		codr = dtv.C3_4
	elif CODERATE == "4/5":
		codr = dtv.C4_5
	elif CODERATE == "5/6":
		codr = dtv.C5_6
	else:
		sys.stderr.write("CODERATE IN CONFIG WRONG! Values: 1/2 2/5 3/5 2/3 3/4 4/5 5/6 \n");
		sys.exit(1)
		
	if CARREXT == "on":
		extcarr = dtv.CARRIERS_EXTENDED
	elif CARREXT == "off":
		extcarr = dtv.CARRIERS_NORMAL
	else:
		sys.stderr.write("EXT-CARRIERS IN CONFIG WRONG! Values: on or off \n");
		sys.exit(1)


	cp_length = fft_length+(fft_length * mul) / div
	

        ##################################################
        # Blocks
        ##################################################
        self.osmosdr_sink_0 = osmosdr.sink( args="numchan=" + str(1) + " " + 'hackrf,buffers=128,buflen=32768' )
        self.osmosdr_sink_0.set_sample_rate(samp_rate)
        self.osmosdr_sink_0.set_center_freq(center_freq, 0)
        self.osmosdr_sink_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0.set_gain(rf_gain, 0)
        self.osmosdr_sink_0.set_if_gain(if_gain, 0)
        self.osmosdr_sink_0.set_bb_gain(0, 0)
        self.osmosdr_sink_0.set_antenna('', 0)
        self.osmosdr_sink_0.set_bandwidth(band_width, 0)
          
        self.dtv_dvbt2_pilotgenerator_cc_0 = dtv.dvbt2_pilotgenerator_cc(extcarr, ffts, pil, gint, DATASYM, pap, ver, preamb, dtv.MISO_TX1, dtv.EQUALIZATION_OFF, dtv.BANDWIDTH_8_0_MHZ, fft_length)
        self.dtv_dvbt2_p1insertion_cc_0 = dtv.dvbt2_p1insertion_cc(extcarr, ffts, gint, DATASYM, preamb, dtv.SHOWLEVELS_OFF, 3.3)
        self.dtv_dvbt2_modulator_bc_0 = dtv.dvbt2_modulator_bc(dtv.FECFRAME_NORMAL, const, dtv.ROTATION_OFF)
        self.dtv_dvbt2_interleaver_bb_0 = dtv.dvbt2_interleaver_bb(dtv.FECFRAME_NORMAL, codr, const)
        self.dtv_dvbt2_freqinterleaver_cc_0 = dtv.dvbt2_freqinterleaver_cc(extcarr, ffts, pil, gint, DATASYM, pap, ver, preamb)
        self.dtv_dvbt2_framemapper_cc_0 = dtv.dvbt2_framemapper_cc(dtv.FECFRAME_NORMAL, codr, const, dtv.ROTATION_OFF, FECBLKS, 3, extcarr, ffts, gint, l1m, pil, 2, DATASYM, pap, ver, preamb, dtv.INPUTMODE_NORMAL, dtv.RESERVED_OFF, dtv.L1_SCRAMBLED_OFF, dtv.INBAND_OFF)
        self.dtv_dvbt2_cellinterleaver_cc_0 = dtv.dvbt2_cellinterleaver_cc(dtv.FECFRAME_NORMAL, const, FECBLKS, 3)
        self.dtv_dvb_ldpc_bb_0 = dtv.dvb_ldpc_bb(dtv.STANDARD_DVBT2, dtv.FECFRAME_NORMAL, codr, dtv.MOD_OTHER)
        self.dtv_dvb_bch_bb_0 = dtv.dvb_bch_bb(dtv.STANDARD_DVBT2, dtv.FECFRAME_NORMAL, codr)
        self.dtv_dvb_bbscrambler_bb_0 = dtv.dvb_bbscrambler_bb(dtv.STANDARD_DVBT2, dtv.FECFRAME_NORMAL, codr)
        self.dtv_dvb_bbheader_bb_0 = dtv.dvb_bbheader_bb(dtv.STANDARD_DVBT2, dtv.FECFRAME_NORMAL, codr, dtv.RO_0_35, dtv.INPUTMODE_HIEFF, dtv.INBAND_OFF, 168, 4000000)
        self.digital_ofdm_cyclic_prefixer_0 = digital.ofdm_cyclic_prefixer(fft_length, cp_length , 0, '')
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((0.2, ))


	if infile == "-":
		self.blocks_file_descriptor_source_0 = blocks.file_descriptor_source(gr.sizeof_char*1, 0, True)
	else:
        	self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, infile, True)

        ##################################################
        # Connections
        ##################################################

	if infile == "-":
		self.connect((self.blocks_file_descriptor_source_0, 0), (self.dtv_dvb_bbheader_bb_0, 0))
	else:
        	self.connect((self.blocks_file_source_0, 0), (self.dtv_dvb_bbheader_bb_0, 0))    

        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.osmosdr_sink_0, 0))    
        self.connect((self.digital_ofdm_cyclic_prefixer_0, 0), (self.dtv_dvbt2_p1insertion_cc_0, 0))    
        self.connect((self.dtv_dvb_bbheader_bb_0, 0), (self.dtv_dvb_bbscrambler_bb_0, 0))    
        self.connect((self.dtv_dvb_bbscrambler_bb_0, 0), (self.dtv_dvb_bch_bb_0, 0))    
        self.connect((self.dtv_dvb_bch_bb_0, 0), (self.dtv_dvb_ldpc_bb_0, 0))    
        self.connect((self.dtv_dvb_ldpc_bb_0, 0), (self.dtv_dvbt2_interleaver_bb_0, 0))    
        self.connect((self.dtv_dvbt2_cellinterleaver_cc_0, 0), (self.dtv_dvbt2_framemapper_cc_0, 0))    
        self.connect((self.dtv_dvbt2_framemapper_cc_0, 0), (self.dtv_dvbt2_freqinterleaver_cc_0, 0))    
        self.connect((self.dtv_dvbt2_freqinterleaver_cc_0, 0), (self.dtv_dvbt2_pilotgenerator_cc_0, 0))    
        self.connect((self.dtv_dvbt2_interleaver_bb_0, 0), (self.dtv_dvbt2_modulator_bc_0, 0))    
        self.connect((self.dtv_dvbt2_modulator_bc_0, 0), (self.dtv_dvbt2_cellinterleaver_cc_0, 0))    
        self.connect((self.dtv_dvbt2_p1insertion_cc_0, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.dtv_dvbt2_pilotgenerator_cc_0, 0), (self.digital_ofdm_cyclic_prefixer_0, 0))    

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

    def get_if_gain(self):
        return self.if_gain

    def set_if_gain(self, if_gain):
        self.if_gain = if_gain
        self.osmosdr_sink_0.set_if_gain(self.if_gain, 0)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.osmosdr_sink_0.set_center_freq(self.center_freq, 0)

    def get_band_width(self):
        return self.band_width

    def set_band_width(self, band_width):
        self.band_width = band_width
        self.osmosdr_sink_0.set_bandwidth(self.band_width, 0)

    def get_VERSION(self):
        return self.VERSION

    def set_VERSION(self, VERSION):
        self.VERSION = VERSION

    def get_PREAMBLE(self):
        return self.PREAMBLE

    def set_PREAMBLE(self, PREAMBLE):
        self.PREAMBLE = PREAMBLE

    def get_PILOT(self):
        return self.PILOT

    def set_PILOT(self, PILOT):
        self.PILOT = PILOT

    def get_PAPR(self):
        return self.PAPR

    def set_PAPR(self, PAPR):
        self.PAPR = PAPR

    def get_L1MOD(self):
        return self.L1MOD

    def set_L1MOD(self, L1MOD):
        self.L1MOD = L1MOD

    def get_GI(self):
        return self.GI

    def set_GI(self, GI):
        self.GI = GI

    def get_FFTSIZE(self):
        return self.FFTSIZE

    def set_FFTSIZE(self, FFTSIZE):
        self.FFTSIZE = FFTSIZE

    def get_FECBLKS(self):
        return self.FECBLKS

    def set_FECBLKS(self, FECBLKS):
        self.FECBLKS = FECBLKS

    def get_DATASYM(self):
        return self.DATASYM

    def set_DATASYM(self, DATASYM):
        self.DATASYM = DATASYM

    def get_CONSTELLATION(self):
        return self.CONSTELLATION

    def set_CONSTELLATION(self, CONSTELLATION):
        self.CONSTELLATION = CONSTELLATION

    def get_CODERATE(self):
        return self.CODERATE

    def set_CODERATE(self, CODERATE):
        self.CODERATE = CODERATE

    def get_CARREXT(self):
        return self.CARREXT

    def set_CARREXT(self, CARREXT):
        self.CARREXT = CARREXT


def main(top_block_cls=DVBT2_Master, options=None):

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
