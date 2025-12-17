FROM python:3.10-alpine
WORKDIR /node2
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
EXPOSE 8002
ENTRYPOINT ["/entrypoint.sh"]