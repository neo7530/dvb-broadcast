#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Dvbc Tx Wxgui
# Generated: Mon Nov  5 17:19:56 2018
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import blocks
from gnuradio import dtv
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import ConfigParser
import dvbc
import osmosdr
import time
import wx
import sys


class dvbc_tx_WXGUI(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Dvbc Tx Wxgui")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self._symrate_config = ConfigParser.ConfigParser()
        self._symrate_config.read('./dvbc.conf')
        try: symrate = self._symrate_config.getint('dvbc', 'symbolrate')
        except: symrate = 0
        self.symrate = symrate
        self._mode_config = ConfigParser.ConfigParser()
        self._mode_config.read('./dvbc.conf')
        try: mode = self._mode_config.get('dvbc', 'mode')
        except: mode = 0
        self.mode = mode
        self._center_freq_config = ConfigParser.ConfigParser()
        self._center_freq_config.read('./dvbc.conf')
        try: center_freq = self._center_freq_config.getint('hackrf', 'frequency')
        except: center_freq = 0
        self.center_freq = center_freq
        self.samp_rate = samp_rate = symrate * 2
        self.rrc_taps = rrc_taps = 100
        self._rf_gain_config = ConfigParser.ConfigParser()
        self._rf_gain_config.read('./dvbc.conf')
        try: rf_gain = self._rf_gain_config.getint('hackrf', 'rf-gain')
        except: rf_gain = 0
        self.rf_gain = rf_gain
        self._if_gain_config = ConfigParser.ConfigParser()
        self._if_gain_config.read('./dvbc.conf')
        try: if_gain = self._if_gain_config.getint('hackrf', 'if-gain')
        except: if_gain = 0
        self.if_gain = if_gain
        self.anz0 = anz0 = str(center_freq/1000000)+"MHZ / "+mode+" / "+str(symrate/1000)+" kSym/s"

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
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=center_freq,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=1024,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title='FFT Plot',
        	peak_hold=False,
        )
        self.Add(self.wxgui_fftsink2_0.win)
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


        self._anz0_static_text = forms.static_text(
        	parent=self.GetWin(),
        	value=self.anz0,
        	callback=self.set_anz0,
        	label='Parameter',
        	converter=forms.str_converter(),
        )
        self.Add(self._anz0_static_text)

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
        self.connect((self.fft_filter_xxx_0, 0), (self.wxgui_fftsink2_0, 0))    

    def get_symrate(self):
        return self.symrate

    def set_symrate(self, symrate):
        self.symrate = symrate
        self.set_samp_rate(self.symrate * 2)
        self.set_anz0(str(self.center_freq/1000000)+"MHZ / "+self.mode+" / "+str(self.symrate/1000)+" kSym/s")

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
        self.set_anz0(str(self.center_freq/1000000)+"MHZ / "+self.mode+" / "+str(self.symrate/1000)+" kSym/s")

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.wxgui_fftsink2_0.set_baseband_freq(self.center_freq)
        self.osmosdr_sink_1.set_center_freq(self.center_freq, 0)
        self.set_anz0(str(self.center_freq/1000000)+"MHZ / "+self.mode+" / "+str(self.symrate/1000)+" kSym/s")

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)
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

    def get_if_gain(self):
        return self.if_gain

    def set_if_gain(self, if_gain):
        self.if_gain = if_gain
        self.osmosdr_sink_1.set_if_gain(self.if_gain, 0)

    def get_anz0(self):
        return self.anz0

    def set_anz0(self, anz0):
        self.anz0 = anz0
        self._anz0_static_text.set_value(self.anz0)


def main(top_block_cls=dvbc_tx_WXGUI, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
