FROM python:3-alpine

ARG protocol
ENV prot="${protocol}"
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 53/tcp
EXPOSE 53/udp

CMD python3 ./dnsproxy.py ${prot}
