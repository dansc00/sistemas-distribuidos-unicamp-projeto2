FROM python:3.10-alpine
WORKDIR /node3
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
EXPOSE 8003
ENTRYPOINT ["/entrypoint.sh"]