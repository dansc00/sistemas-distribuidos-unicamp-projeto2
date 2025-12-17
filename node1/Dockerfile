FROM python:3.10-alpine
WORKDIR /node1
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
EXPOSE 8001
ENTRYPOINT ["/entrypoint.sh"]