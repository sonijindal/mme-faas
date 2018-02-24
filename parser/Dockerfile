FROM ubuntu:16.04
# 1. Use any image as your base image, or "scratch"
# 2. Add fwatchdog binary via https://github.com/openfaas/faas/releases/
# 3. Then set fprocess to the process you want to invoke per request - i.e. "cat" or "my_binary"

#ADD https://github.com/openfaas/faas/releases/download/0.7.0/fwatchdog /usr/bin
#RUN chmod +x /usr/bin/fwatchdog
RUN apt-get update && apt-get install make curl gcc libcurl4-gnutls-dev -y

RUN echo "Pulling watchdog binary from Github." \
    && curl -sSL https://github.com/openfaas/faas/releases/download/0.7.0/fwatchdog > /usr/bin/fwatchdog \
    && chmod +x /usr/bin/fwatchdog

ENV APP_HOME /opt
COPY code ${APP_HOME}
WORKDIR ${APP_HOME}
RUN make

# Populate example here - i.e. "cat", "sha512sum" or "node index.js"
ENV fprocess="/opt/parser"
# Set to true to see request in function logs
ENV write_debug="false"

HEALTHCHECK --interval=5s CMD [ -e /tmp/.lock ] || exit 1
CMD [ "fwatchdog" ]
