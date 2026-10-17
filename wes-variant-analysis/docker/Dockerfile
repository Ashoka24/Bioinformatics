FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip samtools fastqc bwa \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace
COPY scripts/ /workspace/scripts/

ENTRYPOINT ["/bin/bash"]
