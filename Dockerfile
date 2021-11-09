FROM python:3-alpine

ARG protocol
ENV prot="${protocol}"
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 9999/tcp
EXPOSE 9999/udp

CMD python3 ./dnsproxy.py ${prot}
