FROM ubuntu:16.04
# 1. Use any image as your base image, or "scratch"
# 2. Add fwatchdog binary via https://github.com/openfaas/faas/releases/
# 3. Then set fprocess to the process you want to invoke per request - i.e. "cat" or "my_binary"

RUN apt-get update && apt-get install make curl gcc libcurl4-gnutls-dev cmake libboost-all-dev libsctp-dev wget vim g++ libprotobuf-dev net-tools libcurl4-gnutls-dev -y

RUN echo "Pulling watchdog binary from Github." \
    && curl -sSL https://github.com/openfaas/faas/releases/download/0.7.0/fwatchdog > /usr/bin/fwatchdog \
    && chmod +x /usr/bin/fwatchdog

#ENV APP_HOME /opt
#COPY code ${APP_HOME}
#WORKDIR ${APP_HOME}
#RUN make

ENV MCP_HOME /opt/mcp

RUN cd /opt && wget https://tls.mbed.org/download/mbedtls-2.5.1-apache.tgz && \
    tar -xvf mbedtls-2.5.1-apache.tgz

RUN cd /opt/mbedtls-2.5.1 && \
    cmake -DUSE_SHARED_MBEDTLS_LIBRARY=On . && \
    make -j4 && \
    make -j4 install

RUN wget http://downloads.datastax.com/cpp-driver/ubuntu/16.04/dependencies/libuv/v1.18.0/libuv_1.18.0-1_amd64.deb && \
    dpkg -i libuv_1.18.0-1_amd64.deb

RUN wget http://downloads.datastax.com/cpp-driver/ubuntu/16.04/cassandra/v2.4.0/cassandra-cpp-driver_2.4.0-1_amd64.deb && \
    dpkg -i cassandra-cpp-driver_2.4.0-1_amd64.deb

RUN wget http://downloads.datastax.com/cpp-driver/ubuntu/16.04/cassandra/v2.4.0/cassandra-cpp-driver-dev_2.4.0-1_amd64.deb && \
    dpkg -i cassandra-cpp-driver-dev_2.4.0-1_amd64.deb

RUN cd /opt && wget --header <mcp-repository-link> -O mcp.tgz && \
    mkdir -p ${MCP_HOME} && tar -xvzf mcp.tgz -C ${MCP_HOME} --strip-components 1
COPY 0001-MME-FAAS-changes.patch ${MCP_HOME}
RUN cd ${MCP_HOME} && patch -p1 < 0001-MME-FAAS-changes.patch

#RUN mkdir -p ${MCP_HOME}
#ADD MobileControlPlanes ${MCP_HOME}

WORKDIR ${MCP_HOME}
RUN mkdir build && \
    cd build && \
    cmake ../ && \
    make -j4

RUN cp subscriber/LTE_fdd_enodeb.user_db /tmp/

# Populate example here - i.e. "cat", "sha512sum" or "node index.js"
ENV fprocess="xargs /opt/mcp/build/mymme/src/mymme"
# Set to true to see request in function logs
ENV write_debug="true"

#HEALTHCHECK --interval=5s CMD [ -e /tmp/.lock ] || exit 1
CMD [ "fwatchdog" ]
