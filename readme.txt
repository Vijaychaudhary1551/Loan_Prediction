# commands for setting up docker and git
sudo yum install -y docker
sudo yum install -y git
sudo systemctl start docker
git clone https://github.com/ShreyasK2411/Loan_Prediction.git

# copy the setup file to home directory
# and run the script in sudo mode

# copy the last line of the file to the systems /etc/hosts
docker exec -it hbase-docker cat /etc/hosts
echo hbase-docker <IP> >> /etc/hosts


# downloading the data
mkdir .kaggle
mv /home/ec2-user/Loan_Prediction/kaggle.json .kaggle
chmod 777 .kaggle/kaggle.json
# go to /dev/ and download the dataset
# change the permissions of the folder
# exit the sudo mode and then download the data
kaggle datasets download -d mrmorj/alfabattle-20

sudo unzip alfabattle-20.zip -d /run

# run the toHBase.py file
sudo python3 toHBase.py
column family name = details
file path = /run/alfabattle2_train_transactions_contest/train_transactions_contest


# commands for building and running docker image
sudo docker build . -t webserver
sudo docker exec -it webserver echo <IP> >> /etc/hosts
docker run -p 8767:8767 --name website -d webserver

