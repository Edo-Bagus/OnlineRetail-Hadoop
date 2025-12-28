FROM bde2020/hadoop-namenode:2.0.0-hadoop3.2.1-java8

# Update sources.list to use Debian archive and remove security repo
RUN sed -i 's/deb.debian.org/archive.debian.org/g' /etc/apt/sources.list && \
    sed -i '/security/d' /etc/apt/sources.list && \
    sed -i '/stretch-updates/d' /etc/apt/sources.list

RUN apt-get update && apt-get install -y --allow-unauthenticated python3 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONIOENCODING=utf-8
