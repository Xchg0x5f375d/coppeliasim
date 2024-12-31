# Base Image (Ubuntu 24.04)
FROM ubuntu:24.04

# Environment Variables
ENV DEBIAN_FRONTEND=noninteractive \
    COPPELIASIM_VERSION="V4_8_0_rev0" \
    COPPELIASIM_DIR="/opt/CoppeliaSim_Pro_${COPPELIASIM_VERSION}_Ubuntu24_04" \
    VIRTUAL_ENV="/opt/venv"

# Install Essential Packages
RUN apt-get update -q && \
    apt-get install -y --no-install-recommends \
        vim tar xz-utils \
        libx11-6 libxcb1 libxau6 libgl1-mesa-dev \
        xvfb dbus-x11 x11-utils libxkbcommon-x11-0 \
        libavcodec-dev libavformat-dev libswscale-dev \
        python3 python3-pip python3-venv libraw1394-11 libmpfr6 \
        libusb-1.0-0 && \
    apt-get autoclean -y && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create and Activate Virtual Environment
RUN python3 -m venv ${VIRTUAL_ENV}
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

# Install Python Packages
RUN pip3 install --no-cache-dir pyzmq cbor2

# Download and Extract CoppeliaSim
COPY ./download/CoppeliaSim_Pro_${COPPELIASIM_VERSION}_Ubuntu24_04.tar.xz ${COPPELIASIM_DIR}.tar.xz
RUN tar -xf ${COPPELIASIM_DIR}.tar.xz -C /opt && \
    rm ${COPPELIASIM_DIR}.tar.xz

# Set Environment Variables for CoppeliaSim
ENV LD_LIBRARY_PATH="${COPPELIASIM_DIR}:${LD_LIBRARY_PATH}" \
    PATH="${COPPELIASIM_DIR}:${PATH}"

# Create Entrypoint Script for Headless Execution with Xvfb
RUN echo '#!/bin/bash\n\
cd "${COPPELIASIM_DIR}"\n\
/usr/bin/xvfb-run --server-args "-ac -screen 0, 1024x1024x24" coppeliaSim "$@"\n' > /entrypoint && \
    chmod a+x /entrypoint

# Expose Ports for Visualization
EXPOSE 23000-23500

# Set Entrypoint
ENTRYPOINT ["/entrypoint"]

# Default Command to Run CoppeliaSim in Headless Mode
CMD ["-h"]
