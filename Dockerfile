FROM ubuntu:21.10

ARG domain=apps.spiralinc.us
ENV domain=$domain

RUN mkdir -p /opt/nginx/config-manager/
COPY . /opt/nginx/config-manager/

RUN apt-get update -y && \
    apt-get install software-properties-common -y && \
    apt-get update -y && \
    add-apt-repository ppa:certbot/certbot && \
    apt-get install python3 python3-certbot-nginx -y

RUN certbot --nginx -d $domain --non-interactive --agree-tos -m lparker.tpx@gmail.com && \
    certbot renew --dry-run

EXPOSE 80 443
