FROM ubuntu:22.04

WORKDIR /code

COPY ./*.py /code

COPY ./*.sh /code

RUN chmod +x linkAccount.sh

RUN apt update

RUN apt install curl -y

RUN curl -sL -o /etc/apt/trusted.gpg.d/morph027-signal-cli.asc https://packaging.gitlab.io/signal-cli/gpg.key

RUN echo "deb https://packaging.gitlab.io/signal-cli signalcli main" | tee /etc/apt/sources.list.d/morph027-signal-cli.list

RUN apt update

RUN apt-get install signal-cli-native -y

RUN apt-get install qrencode python3 -y

# CMD ./linkAccount.sh signalCliContainer;python3 main.py

CMD ./start.sh dockerBot

# todo 
# X copy files into container
# - persistant login 
# - setup script
#   X checks if logged in
#   X if not links device
# X run bot
# - tests endpoint in make
# - tests runs on build
# - 
