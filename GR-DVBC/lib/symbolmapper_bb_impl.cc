/* -*- c++ -*- */
/* 
 * Copyright 2018 Ron Economos.
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "symbolmapper_bb_impl.h"
#include <stdio.h>

namespace gr {
  namespace dvbc {

    symbolmapper_bb::sptr
    symbolmapper_bb::make(dvbc_constellation_t constellation)
    {
      return gnuradio::get_initial_sptr
        (new symbolmapper_bb_impl(constellation));
    }

    /*
     * The private constructor
     */
    symbolmapper_bb_impl::symbolmapper_bb_impl(dvbc_constellation_t constellation)
      : gr::block("symbolmapper_bb",
              gr::io_signature::make(1, 1, sizeof(unsigned char)),
              gr::io_signature::make(1, 1, sizeof(unsigned char)))
    {
      switch (constellation)
      {
        case MOD_16QAM:
          output_bits = 4;
          mask = 0x3;
          set_output_multiple(2);
          break;
        case MOD_32QAM:
          output_bits = 5;
          mask = 0x7;
          set_output_multiple(8);
          break;
        case MOD_64QAM:
          output_bits = 6;
          mask = 0xf;
          set_output_multiple(4);
          break;
        case MOD_128QAM:
          output_bits = 7;
          mask = 0x1f;
          set_output_multiple(8);
          break;
        case MOD_256QAM:
          output_bits = 8;
          mask = 0x3f;
          set_output_multiple(2);
          break;
      }
      input_index = 0;
      output_index = 0;
      ik_prev = 0;
      qk_prev = 0;
    }

    /*
     * Our virtual destructor.
     */
    symbolmapper_bb_impl::~symbolmapper_bb_impl()
    {
    }

    void
    symbolmapper_bb_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
      ninput_items_required[0] = (noutput_items * output_bits) / 8;
    }

    int
    symbolmapper_bb_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
      const unsigned char *in = (const unsigned char *) input_items[0];
      unsigned char *out = (unsigned char *) output_items[0];
      int symbols = noutput_items;
      int consumed = 0;
      int produced = 0;
      unsigned int ak, bk, ik, qk;
      unsigned char tempin, tempout;

      while(produced < symbols) {
        if(input_index == 0) {
          tempin = in[consumed++];
        }
        if(output_index == 0) {
          tempout = 0;
        }
        tempout |= ((tempin >> (0x7 - input_index)) & 0x01) << (output_bits - 1 - output_index);

        input_index = (input_index + 1) & 0x7;
        output_index = (output_index + 1);
        if (output_index == output_bits) {
          output_index = 0;
        }
        if(output_index == 0) {
          ak = tempout >> (output_bits - 1);
          bk = (tempout >> (output_bits - 2)) & 0x1;
          ik = (!(ak ^ bk)) && (ak ^ ik_prev) || (ak ^ bk) && (ak ^ qk_prev);
          qk = (!(ak ^ bk)) && (bk ^ qk_prev) || (ak ^ bk) && (bk ^ ik_prev);
          ik_prev = ik;
          qk_prev = qk;
          tempout &= mask;
          tempout |= (ik << (output_bits - 1));
          tempout |= (qk << (output_bits - 2));
          out[produced++] = tempout;
        }
      }

      // Tell runtime system how many input items we consumed on
      // each input stream.
      consume_each(consumed);

      // Tell runtime system how many output items we produced.
      return produced;
    }

  } /* namespace dvbc */
} /* namespace gr */

