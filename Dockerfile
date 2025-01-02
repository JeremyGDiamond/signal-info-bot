FROM ubuntu:22.04

WORKDIR /code

RUN apt update

RUN apt install curl -y

RUN apt-get install qrencode python3 pip -y

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --upgrade pwntools

RUN curl -sL -o /etc/apt/trusted.gpg.d/morph027-signal-cli.asc https://packaging.gitlab.io/signal-cli/gpg.key

RUN echo "deb https://packaging.gitlab.io/signal-cli signalcli main" | tee /etc/apt/sources.list.d/morph027-signal-cli.list

RUN apt update

RUN apt-get install signal-cli-native -y

COPY ./*.py /code

COPY ./*.sh /code

RUN chmod +x linkAccount.sh



# CMD ./linkAccount.sh signalCliContainer;python3 main.py

CMD ./containerStart.sh dockerBot
