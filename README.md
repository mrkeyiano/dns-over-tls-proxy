# DNS over TLS proxy



## Implementation



Tool Listens for DNS queries on port 53/tcp and proxies them to Cloudfare's 1.0.0.1 nameserver through DNS over TLS, then sends the response back to the client.



## Support

* Sends DNS queries over an encrypted (TLS) connection

* Allows multiple incoming requests at the same time

* Handles TCP & UDP requests, while still querying TCP on the other side (Cloudflare)





## DNS security concerns



Traditional DNS queries and responses are sent over UDP or TCP without encryption, connection is prone to eavesdropping and spoofing.



DNS over TLS mitigates this security concern.



There are concerns around Clients sending DNS queries from a remote source which makes the connection open to sniffing attacks.



This proxy only ensures connection between DNSproxy and DNS server is encrypted, the connection from Client to DNSProxy is unencrypted unless the implementation is made to ensure a secure connection from Client to DNSproxy





## Usage in microservice-oriented and containerized architecture



Configure dnsmasq's nameserver on every microservice's host to point to the dnsproxy service.





## Possible improvements



- Add support for other nameservers i.e Google

- Improve logging of errors and request tracing for use in real-time monitoring and alerting systems.





## Installation Procedure



1. Build the Docker image:



```

docker build -t dnsproxy .

```



2. Run the container:



```

docker run -p 8989:53/tcp dnsproxy

```



3. Or simple run below command to build & run





```

docker-compose up --build

```



For testing purposes it is bound to port 8989 by default; it can be published on any other port if desired.



It can be tested with a query to localhost:8989 nameserver:



```

$ dig @localhost -p 8989 n26.com



; <<>> DiG 9.10.6 <<>> @127.0.0.1 -p 8989 +tcp n26.com

; (1 server found)

;; global options: +cmd

;; Got answer:

;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 56119

;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1



;; OPT PSEUDOSECTION:

; EDNS: version: 0, flags:; udp: 1232

; PAD: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ("............................................................................................................................................................................................................................................................................................................................................................................................................................")

;; QUESTION SECTION:

;n26.com. IN A



;; ANSWER SECTION:

n26.com. 32 IN A 128.65.211.162



;; Query time: 860 msec

;; SERVER: 127.0.0.1#8989(127.0.0.1)

;; WHEN: Tue Nov 09 22:29:30 WAT 2021

;; MSG SIZE rcvd: 468



```

