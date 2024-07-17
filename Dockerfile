FROM ubuntu:22.04

WORKDIR /code

COPY ./*.py /code

COPY ./*.json /code

RUN apt update

RUN apt install curl -y

RUN curl -sL -o /etc/apt/trusted.gpg.d/morph027-signal-cli.asc https://packaging.gitlab.io/signal-cli/gpg.key

RUN echo "deb https://packaging.gitlab.io/signal-cli signalcli main" | tee /etc/apt/sources.list.d/morph027-signal-cli.list

RUN apt update

RUN apt-get install signal-cli-native -y

RUN apt-get install qrencode -y

CMD ["qrencode", "--help"]

# todo 
# X copy files into container
# - persistant login 
# - setup script
#   - checks if logged in
#   - if not links device
# - run bot
# - tests endpoint in make
# - tests runs tests
# - 
