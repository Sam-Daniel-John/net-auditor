# Network Infrastructure Audit

Target: 192.168.2.76
Date: 2026-09-20 20:50:14

## Executive Summary

- Connectivity: PASS
- Reverse DNS: PASS
- Open TCP ports: NONE detected
- SSH exposure: PASS
- Firewall: WARN

## Service Discovery

```text
Starting Nmap 7.95 ( https://nmap.org ) at 2026-09-20 20:50 CEST
Nmap scan report for kali (192.168.2.76)
Host is up (0.0000040s latency).

PORT     STATE  SERVICE       VERSION
21/tcp   closed ftp
22/tcp   closed ssh
23/tcp   closed telnet
25/tcp   closed smtp
53/tcp   closed domain
80/tcp   closed http
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

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 0.30 seconds
```

## Open Port Assessment

No open TCP ports were detected.

## SSH Assessment

SSH is not listening on TCP port 22.

## Firewall Assessment

Detected status: nftables installed but no rules detected

## Security Recommendations

- [PASS] No exposed TCP services detected. Continue minimizing unnecessary services.
- [PASS] SSH is not exposed. No SSH hardening required.
- [HIGH] No active host firewall rules detected. Configure a host-based firewall.

## Methodology

The auditor performs connectivity testing, reverse DNS resolution, TCP service discovery, SSH exposure checking, firewall assessment, and security recommendation generation.