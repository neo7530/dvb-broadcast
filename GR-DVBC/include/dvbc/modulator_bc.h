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

#ifndef INCLUDED_DVBC_MODULATOR_BC_H
#define INCLUDED_DVBC_MODULATOR_BC_H

#include <dvbc/api.h>
#include <dvbc/dvbc_config.h>
#include <gnuradio/block.h>

namespace gr {
  namespace dvbc {

    /*!
     * \brief Modulates DVB-C symbols.
     * \ingroup dvbc
     *
     * Input: 4,5,6,7,or 8-bit symbols. \n
     * Output: 16,32,64,128 or 256QAM modulated complex IQ values. \n
     */
    class DVBC_API modulator_bc : virtual public gr::block
    {
     public:
      typedef boost::shared_ptr<modulator_bc> sptr;

      /*!
       * \brief Create a DVB-C modulator.
       *
       * \param constellation DVB-C constellation (16,32,64,128 or 256QAM).
       */
      static sptr make(dvbc_constellation_t constellation);
    };

  } // namespace dvbc
} // namespace gr

#endif /* INCLUDED_DVBC_MODULATOR_BC_H */

