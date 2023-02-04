FROM hub.docker.com/darshika/diabetes-predictor:0.0.0 AS test

ARG VERSION
ENV VERSION=$VERSION

# Test suite must not be run as root since we create postgres DB instances
RUN useradd -ms /bin/bash testuser
USER testuser
COPY . /home/testuser
RUN cd /home/testuser && \
    bash .conda/run_style.sh && \
    bash .conda/run_test.sh --test-suite unit
