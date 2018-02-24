FROM python:3.6-alpine3.7

ENV CRYPTO_INVESTOR_VERSION=1.0.0

COPY dist/crypto-investor-${CRYPTO_INVESTOR_VERSION}.tar.gz /

RUN set -x \
    && apk add --update --no-cache --virtual .build-deps \
        build-base \
        libxml2-dev \
        libxslt-dev \
        linux-headers \
    && pip install --upgrade setuptools \
    && pip install crypto-investor-${CRYPTO_INVESTOR_VERSION}.tar.gz \
    && rm crypto-investor-${CRYPTO_INVESTOR_VERSION}.tar.gz \
    # Clean up
    && apk del .build-deps \
    && rm -rf /root/.cache /var/cache/apk/*

EXPOSE 8050
