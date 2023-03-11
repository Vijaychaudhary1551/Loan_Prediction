docker pull dajobe/hbase
mkdir data
id=$(docker run --name=hbase-docker -h hbase-docker -d -v $PWD/data:/data dajobe/hbase)
docker exec -it hbase-docker /opt/hbase/bin/start-hbase.sh

yum install -y gcc
yum install -y python3-devel
pip3 install happybase
pip3 install pyspark

# setup spark on ec2
amazon-linux-extras install java-openjdk11
wget https://dlcdn.apache.org/spark/spark-3.3.2/spark-3.3.2-bin-hadoop3.tgz
tar -xzf spark-3.3.2-bin-hadoop3.tgz
mv spark-3.3.2-bin-hadoop3 spark
echo export SPARK_HOME=/home/ec2-user/spark >> .bashrc
echo export PATH=$PATH:$SPARK_HOME/bin >> .bashrc
source ~/.bashrc
