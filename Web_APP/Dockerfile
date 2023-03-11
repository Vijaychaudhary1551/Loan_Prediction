FROM python:3.8

USER root

COPY ./requirements.txt /app/requirements.txt

# configuring the environment
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-dev
RUN apt-get install -y gcc
RUN apt-get install -y openjdk-11-jdk
RUN wget https://dlcdn.apache.org/spark/spark-3.3.2/spark-3.3.2-bin-hadoop3.tgz
RUN tar xzf spark-3.3.2-bin-hadoop3.tgz
RUN mv spark-3.3.2-bin-hadoop3 spark
RUN echo export SPARK_HOME=/home/ec2-user/spark >> .bashrc
RUN echo export PATH=$PATH:$SPARK_HOME/bin >> .bashrc

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /app

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD ["app.py" ]
