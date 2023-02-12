FROM nginx:stable-alpine

RUN rm /etc/nginx/conf.d/default.conf

COPY ./ci-cd/nginx_balancer/nginx.conf /etc/nginx/conf.d