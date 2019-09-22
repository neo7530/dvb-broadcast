ffmpeg -i $1 \
-vcodec copy \
-acodec mp2 \
-program title="service1":program_num=0x1001:st=0:st=1 \
-muxrate $2 \
-f mpegts -y - | \
tsp -v \
-I file \
-P filter --max-payload-size 0 --negate -s \
-P scrambler service1 --ecmg localhost:8888 --super-cas-id 0x06020000 --channel-id 0x0001 --pid-ecm 0x1ec1 --cp-duration 7 --access-criteria 100a7530100a2710 \
-P svrename -n "NeoVision HD" -p "NeoVision" service1 \
-O file | ./dvbt.py -
