ARG VERSION
FROM public.ecr.aws/z7k9f6z0/diabetes-predictor:${VERSION} AS test

RUN useradd -ms /bin/bash testuser
USER testuser
COPY . /home/testuser
RUN cd /home/testuser && \
    bash .conda/run_style.sh && \
    bash .conda/run_test.sh --test-suite unit && \
    bash .conda/run_test.sh --test-suite integration
