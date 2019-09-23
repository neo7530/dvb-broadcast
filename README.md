# dvb-broadcast
DVB Broadcast using GNURADIO with HACKRF ONE
DVB-C/T/T2 Transmitter using HACKRF ONE with GNURADIO, FFMPEG and TSDUCK.

HOW TO:

Simple transmitting in dvb-t: 
- edit dvb-t.conf for your needs (constellation, coderate, guard-interval etc)
- remux a videofile with ffmpeg using the right MUXRATE
- then transmit the remuxed videofile: dvbt.py "VIDEOFILE.TS"

On the fly: (read dvbt.conf for right muxrate. Here: const: 16QAM cr: 1/2 gi:1/32 so MUXRATE = 12.064M

- edit dvb-t.conf for your needs (constellation, coderate, guard-interval etc)
ffmpeg -i "infile.ext" -vcodec copy -acodec copy \ 
-program title="service1":program_num=0x1001:st=0:st=1 \
-muxrate 12.064M -f mpegts -y - | .\dvbt-py -

USING clear.sh

- same as above (dvbt.conf)
- start transmitting: .\clear.sh "infile" "muxrate"

DVB-C / DVB-T2:
- edit dvbc.conf / dvbt2.conf for parameter
- edit clear.sh for transmitter-file (dvbc-tx.py / dvbt2.py)

NOTE: ALWAYS WATCH FOR MUXRATE PARAMETER, ELSE THE TRANSMITTED VIDEO WILL SLUTTER!
