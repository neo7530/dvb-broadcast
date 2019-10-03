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

#ifndef INCLUDED_DVBC_SYMBOLMAPPER_BB_IMPL_H
#define INCLUDED_DVBC_SYMBOLMAPPER_BB_IMPL_H

#include <dvbc/symbolmapper_bb.h>

namespace gr {
  namespace dvbc {

    class symbolmapper_bb_impl : public symbolmapper_bb
    {
     private:
      int output_bits;
      int input_index;
      int output_index;
      int mask;
      unsigned int ik_prev;
      unsigned int qk_prev;

     public:
      symbolmapper_bb_impl(dvbc_constellation_t constellation);
      ~symbolmapper_bb_impl();

      void forecast (int noutput_items, gr_vector_int &ninput_items_required);

      int general_work(int noutput_items,
           gr_vector_int &ninput_items,
           gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);
    };

  } // namespace dvbc
} // namespace gr

#endif /* INCLUDED_DVBC_SYMBOLMAPPER_BB_IMPL_H */

