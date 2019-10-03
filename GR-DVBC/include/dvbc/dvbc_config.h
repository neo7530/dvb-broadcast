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

#ifndef INCLUDED_DVBC_CONFIG_H
#define INCLUDED_DVBC_CONFIG_H

#define TRUE 1
#define FALSE 0

namespace gr {
  namespace dvbc {

    enum dvbc_constellation_t {
      MOD_16QAM = 0,
      MOD_32QAM,
      MOD_64QAM,
      MOD_128QAM,
      MOD_256QAM,
    };

  } // namespace dvbc
} // namespace gr

typedef gr::dvbc::dvbc_constellation_t dvbc_constellation_t;

#endif /* INCLUDED_DVBC_CONFIG_H */

