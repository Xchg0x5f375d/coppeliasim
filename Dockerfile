# Base Image (Ubuntu 24.04, matching the CoppeliaSim version)
FROM ubuntu:24.04

# Install essential packages including xz-utils
RUN apt-get update -q && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get install -y --no-install-recommends \
        vim \
        tar \
        xz-utils \
        libx11-6 \
        libxcb1 \
        libxau6 \
        libgl1-mesa-dev \
        xvfb \
        dbus-x11 \
        x11-utils \
        libxkbcommon-x11-0 \
        libavcodec-dev \
        libavformat-dev \
        libswscale-dev \
        python3 \
        python3-pip \
        python3-venv \
        libraw1394-11 \
        libmpfr6 \
        libusb-1.0-0 && \
    apt-get autoclean -y && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create a virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv ${VIRTUAL_ENV}

# Activate the virtual environment (add to PATH)
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

# Install Python packages within the virtual environment
RUN pip3 install --no-cache-dir pyzmq cbor2

# Copy CoppeliaSim archive and extract
COPY ./download/CoppeliaSim_Pro_V4_8_0_rev0_Ubuntu24_04.tar.xz /opt/
RUN tar -xf /opt/CoppeliaSim_Pro_V4_8_0_rev0_Ubuntu24_04.tar.xz -C /opt && \
    rm /opt/CoppeliaSim_Pro_V4_8_0_rev0_Ubuntu24_04.tar.xz

# Set environment variables for CoppeliaSim
ENV COPPELIASIM_ROOT_DIR=/opt/CoppeliaSim_Pro_V4_8_0_rev0_Ubuntu24_04
ENV PATH=$COPPELIASIM_ROOT_DIR:$PATH

# Create an entrypoint script to run CoppeliaSim
RUN echo '#!/bin/bash\ncd $COPPELIASIM_ROOT_DIR\n/usr/bin/xvfb-run --server-args "-ac -screen 0, 1024x1024x24" coppeliaSim "$@"' > /entrypoint && \
    chmod a+x /entrypoint

# Expose the required ports for CoppeliaSim
EXPOSE 23000-23500

# Set the entrypoint and default command
ENTRYPOINT ["/entrypoint"]
CMD ["/opt/coppelia/coppeliaSim.sh", "-h"]
