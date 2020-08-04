echo `date`        "scp start..."
cd /mnt/onl/data
tar zcvf stratum.tgz stratum > /dev/null
echo `date`        "tar stratum done..."

cd /home/switch
rm stratum.tgz
rm cache.tgz

mv /mnt/onl/data/stratum.tgz ./
tar zcvf cache.tgz .cache > /dev/null
echo `date`        "tar .cache done..."

./scp.sh stratum.tgz root 192.168.0.227 /root/ onl
./scp.sh cache.tgz root 192.168.0.227 /root/ onl
echo `date`        "scp done..."



