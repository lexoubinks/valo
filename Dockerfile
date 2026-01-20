FROM debian:bullseye-slim
RUN apt-get update && apt-get install -y curl default-mysql-client python3
RUN useradd -m toto
COPY index.html /home/toto/index.html
USER toto
CMD ["python3", "-m", "http.server", "8080", "-d", "/home/toto"]
