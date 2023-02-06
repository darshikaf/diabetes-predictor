ARG VERSION
ARG AWS_ECR

FROM ${AWS_ECR}/diabetes-predictor:${VERSION} AS test

RUN useradd -ms /bin/bash testuser
USER testuser
COPY . /home/testuser
RUN cd /home/testuser && \
    bash .conda/run_style.sh && \
    bash .conda/run_test.sh --test-suite unit && \
    bash .conda/run_test.sh --test-suite integration
