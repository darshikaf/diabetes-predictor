ARG VERSION
FROM darshika/diabetes-predictor:${VERSION} AS test

# Test suite must not be run as root since we create postgres DB instances
RUN useradd -ms /bin/bash testuser
USER testuser
COPY . /home/testuser
RUN cd /home/testuser && \
    bash .conda/run_style.sh && \
    bash .conda/run_test.sh --test-suite unit \
    bash .conda/run_test.sh --test-suite integration
