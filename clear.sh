ffmpeg -i $1 \
-vcodec copy \
-acodec mp2 \
-program title="service1":program_num=0x1001:st=0:st=1 \
-muxrate $2 \
-f mpegts -y - | \
tsp -v \
-I file \
-P filter --max-payload-size 0 --negate -s \
-P svrename -n "NeoVision HD" -p "NeoVision" service1 \
-O file | ./dvbt2.py -
