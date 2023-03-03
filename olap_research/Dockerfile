FROM openkbs/jre-mvn-py3:latest

COPY ./requirements.txt requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt

RUN sudo useradd -rm -d /home/ubuntu -s /bin/bash -g root -G sudo,developer -u 1001 ubuntu && sudo chown ubuntu:root -R /home/developer
USER ubuntu

WORKDIR /home/ubuntu

CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]