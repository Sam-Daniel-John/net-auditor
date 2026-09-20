# Network Infrastructure Audit

Target: 192.168.2.1
Date: 2026-09-20 21:17:42

## Executive Summary

- Connectivity: PASS
- Reverse DNS: PASS
- Open TCP ports: 2 detected
- SSH exposure: PASS
- Firewall: WARN

## Service Discovery

```text
Starting Nmap 7.95 ( https://nmap.org ) at 2026-09-20 21:17 CEST
Nmap scan report for speedport.ip (192.168.2.1)
Host is up (0.048s latency).

PORT     STATE  SERVICE       VERSION
21/tcp   closed ftp
22/tcp   closed ssh
23/tcp   closed telnet
25/tcp   closed smtp
53/tcp   open   domain        (unknown banner: dns)
80/tcp   open   http          Apache httpd
110/tcp  closed pop3
111/tcp  closed rpcbind
135/tcp  closed msrpc
139/tcp  closed netbios-ssn
143/tcp  closed imap
443/tcp  closed https
445/tcp  closed microsoft-ds
993/tcp  closed imaps
995/tcp  closed pop3s
1723/tcp closed pptp
3306/tcp closed mysql
3389/tcp closed ms-wbt-server
5900/tcp closed vnc
8080/tcp closed http-proxy
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port53-TCP:V=7.95%I=7%D=9/20%Time=6AB03151%P=x86_64-pc-linux-gnu%r(DNSV
SF:ersionBindReqTCP,30,"\0\.\0\x06\x81\x80\0\x01\0\x01\0\0\0\0\x07version\
SF:x04bind\0\0\x10\0\x03\xc0\x0c\0\x10\0\x03\0\0P\xdd\0\x04\x03dns");
MAC Address: 4C:22:F3:8B:0C:1C (Arcadyan)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 16.64 seconds
```

## Open Port Assessment

- 53/tcp - domain
- 80/tcp - http

## SSH Assessment

SSH is not listening on TCP port 22.

## Firewall Assessment

Detected status: nftables installed but no rules detected

## Security Recommendations

- [WARN] Review exposed TCP services: 53/domain, 80/http
- [PASS] SSH is not exposed. No SSH hardening required.
- [HIGH] No active host firewall rules detected. Configure a host-based firewall.

## Methodology

The auditor performs connectivity testing, reverse DNS resolution, TCP service discovery, SSH exposure checking, firewall assessment, and security recommendation generation.