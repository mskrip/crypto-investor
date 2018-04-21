FROM python:3.6-alpine3.7

ENV CRYPTO_INVESTOR_VERSION=1.0.0

COPY dist/crypto-investor-${CRYPTO_INVESTOR_VERSION}.tar.gz docker/ /

RUN set -x \
    && apk add --update --no-cache --virtual .build-deps \
        build-base \
        linux-headers \
        pcre-dev \
        python3-dev \
    && apk add --no-cache \
        nginx \
        runit \
    && pip install --upgrade pip setuptools \
    && mkdir -p /srv/cryptoinvestor \
    && pip install crypto-investor-${CRYPTO_INVESTOR_VERSION}.tar.gz \
    && rm crypto-investor-${CRYPTO_INVESTOR_VERSION}.tar.gz \
    # Setup nginx
    && mkdir -p /run/nginx \
    && chown nginx:nginx /run/nginx \
    # Clean up
    && apk del .build-deps \
    && rm -rf /root/.cache /var/cache/apk/*

EXPOSE 5000

CMD [ "/sbin/entrypoint" ]
