# Network Infrastructure Health & Security Auditor

A lightweight Python-based security auditing tool for assessing the health and security exposure of network hosts.

The tool combines connectivity testing, reverse DNS resolution, Nmap service discovery, SSH exposure checks, firewall assessment, and automated security recommendations.

## Objective

The goal of this proof of concept is to provide a simple and repeatable way to perform an initial security assessment of a network host.

The auditor focuses on practical infrastructure checks rather than performing intrusive penetration testing.

## Features

- Host connectivity testing
- Reverse DNS resolution
- TCP service discovery using Nmap
- Open port identification
- SSH exposure detection
- Host firewall assessment
- Automated security recommendations
- Markdown audit reports
- JSON audit reports

## Architecture

                Target Host
                     |
                     v
        +-------------------------+
        | Network Security Auditor|
        |        Python           |
        +------------+------------+
                     |
        +------------+-------------+
        |            |             |
        v            v             v
     Ping/DNS      Nmap        Local Checks
        |            |             |
        +------------+-------------+
                     |
                     v
            Security Assessment
                     |
          +----------+----------+
          |                     |
          v                     v
    Markdown Report        JSON Report

## Assessment Workflow

The auditor performs the following checks:

### 1. Connectivity

Determines whether the target host is reachable.

### 2. Reverse DNS

Checks whether the target IP can be resolved to a hostname.

### 3. Service Discovery

Uses Nmap service detection against the top 20 TCP ports.

nmap -sV --top-ports 20 <target>

### 4. Port Assessment

Identifies open TCP ports and highlights services that may require additional review.

The current detection logic includes services such as:

- FTP
- Telnet
- SMTP
- POP3
- NetBIOS
- SMB
- RDP
- VNC

### 5. SSH Assessment

Checks whether TCP port 22 is listening on the auditing machine.

### 6. Firewall Assessment

Checks for:

- UFW
- nftables

The tool reports whether firewall rules are detected.

### 7. Security Recommendations

Combines the collected results into actionable recommendations.

## Usage

### Basic audit

python3 scripts/network_auditor.py <target>

### Generate a Markdown report

python3 scripts/network_auditor.py <target> --report

### Generate a JSON report

python3 scripts/network_auditor.py <target> --json

### Generate both reports

python3 scripts/network_auditor.py <target> --report --json

## Example Assessment

The auditor was tested against two hosts on a local network.

### Kali Linux

Target:

192.168.2.76

Observed results:

Connectivity: PASS
Reverse DNS: PASS
Open TCP ports: 0
SSH: Not exposed
Firewall: WARN

The assessment identified no exposed TCP services but detected the absence of active host firewall rules.

### Network Router

Target:

192.168.2.1

Observed results:

Connectivity: PASS
Reverse DNS: PASS
Open TCP ports: 2
SSH: Not exposed
Firewall: WARN

The service discovery identified:

53/tcp  DNS
80/tcp  HTTP

This demonstrated that the auditor produces different findings depending on the target's actual network exposure.

## Project Structure

etis-network-auditor/
│
├── scripts/
│   ├── network_auditor.py
│   └── network_auditor.py.backup
│
├── evidence/
│   ├── audit-192.168.2.1.md
│   ├── audit-192.168.2.1.json
│   ├── audit-192.168.2.76.md
│   └── audit-192.168.2.76.json
│
├── reports/
│   ├── audit-192.168.2.1.md
│   ├── audit-192.168.2.1.json
│   ├── audit-192.168.2.76.md
│   └── audit-192.168.2.76.json
│
├── config/
├── docs/
└── README.md

## Technologies

- Python 3
- Nmap
- Linux
- TCP/IP networking
- UFW
- nftables
- JSON
- Markdown

## Security Considerations

This tool is intended for authorized infrastructure assessment.
Only scan systems that you own or have explicit permission to assess.

The tool performs limited service discovery and does not attempt exploitation, credential attacks, or destructive testing.

## Limitations

The current proof of concept:

- Checks only the top 20 TCP ports
- Performs basic service identification
- Performs basic firewall detection
- Does not perform vulnerability scanning
- Does not assess UDP services
- Does not perform authenticated configuration checks
- Does not exploit identified services

## Future Improvements

Potential future extensions include:

- Configurable port ranges
- UDP service discovery
- CVE and vulnerability database integration
- Configurable security policies
- HTML reporting
- Historical comparison between audits
- Automated network asset inventory
- Integration with monitoring systems

