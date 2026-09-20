#!/usr/bin/env python3

import argparse
import socket
import subprocess


def check_connectivity(target):
    """Check whether the target responds to a basic network probe."""

    result = subprocess.run(
        ["ping", "-c", "1", "-W", "2", target],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    return result.returncode == 0


def check_dns(target):
    """Check whether reverse DNS resolution is available."""

    try:
        socket.gethostbyaddr(target)
        return True
    except (socket.herror, socket.gaierror):
        return False


def run_nmap(target):
    """Run a basic TCP service discovery scan."""

    result = subprocess.run(
        ["nmap", "-sV", "--top-ports", "20", target],
        capture_output=True,
        text=True
    )

    return result.stdout


def get_open_ports(nmap_output):
    """Extract open TCP ports from Nmap output."""

    open_ports = []

    for line in nmap_output.splitlines():
        parts = line.split()

        if len(parts) >= 3 and "/tcp" in parts[0]:
            port = parts[0].split("/")[0]
            state = parts[1]
            service = parts[2]

            if state == "open":
                open_ports.append((port, service))

    return open_ports


def assess_ports(nmap_output):
    """Assess discovered ports and identify potential security concerns."""

    risky_services = {
        "21": "FTP",
        "23": "Telnet",
        "25": "SMTP",
        "110": "POP3",
        "139": "NetBIOS",
        "445": "SMB",
        "3389": "RDP",
        "5900": "VNC"
    }

    open_ports = get_open_ports(nmap_output)

    print("\n" + "=" * 60)
    print("PORT SECURITY ASSESSMENT")
    print("=" * 60)

    if not open_ports:
        print("[PASS] No open TCP ports detected")
        return

    print(f"[WARN] {len(open_ports)} open TCP port(s) detected")

    for port, service in open_ports:

        if port in risky_services:
            print(
                f"[WARN] Port {port} ({risky_services[port]}) is exposed"
            )
        else:
            print(
                f"[INFO] Port {port} ({service}) is open"
            )


def check_ssh():
    """Check whether an SSH service is listening locally."""

    result = subprocess.run(
        ["ss", "-lnt"],
        capture_output=True,
        text=True
    )

    for line in result.stdout.splitlines():

        parts = line.split()

        if len(parts) >= 4:
            local_address = parts[3]

            if local_address.endswith(":22"):
                return True

    return False


def check_firewall():
    """Check whether a supported local firewall is active."""

    # Check UFW
    ufw_check = subprocess.run(
        ["bash", "-c", "command -v ufw"],
        capture_output=True,
        text=True
    )

    if ufw_check.returncode == 0:

        status = subprocess.run(
            ["sudo", "ufw", "status"],
            capture_output=True,
            text=True
        )

        if "Status: active" in status.stdout:
            return "UFW active"

        return "UFW installed but inactive"

    # Check nftables
    nft_check = subprocess.run(
        ["bash", "-c", "command -v nft"],
        capture_output=True,
        text=True
    )

    if nft_check.returncode == 0:

        rules = subprocess.run(
            ["sudo", "nft", "list", "ruleset"],
            capture_output=True,
            text=True
        )

        if rules.stdout.strip():
            return "nftables rules detected"

        return "nftables installed but no rules detected"

    return "No supported firewall detected"


def assess_ssh():
    """Assess local SSH exposure."""

    print("\n" + "=" * 60)
    print("SSH SECURITY ASSESSMENT")
    print("=" * 60)

    if check_ssh():

        print("[WARN] SSH is listening on port 22")
        print("[INFO] Verify that SSH access is required")

    else:

        print("[PASS] SSH is not listening on port 22")


def assess_firewall():
    """Assess local firewall configuration."""
#!/usr/bin/env python3

import argparse
import json
import socket
import subprocess
from datetime import datetime
from pathlib import Path


REPORT_DIR = Path.home() / "etis-network-auditor" / "reports"


def check_connectivity(target):
    result = subprocess.run(
        ["ping", "-c", "1", "-W", "2", target],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    return result.returncode == 0


def check_dns(target):
    try:
        socket.gethostbyaddr(target)
        return True
    except (socket.herror, socket.gaierror):
        return False


def run_nmap(target):
    result = subprocess.run(
        ["nmap", "-sV", "--top-ports", "20", target],
        capture_output=True,
        text=True
    )

    return result.stdout


def get_open_ports(nmap_output):
    open_ports = []

    for line in nmap_output.splitlines():
        parts = line.split()

        if len(parts) >= 3 and "/tcp" in parts[0]:
            port = parts[0].split("/")[0]
            state = parts[1]
            service = parts[2]

            if state == "open":
                open_ports.append((port, service))

    return open_ports


def assess_ports(nmap_output):
    risky_services = {
        "21": "FTP",
        "23": "Telnet",
        "25": "SMTP",
        "110": "POP3",
        "139": "NetBIOS",
        "445": "SMB",
        "3389": "RDP",
        "5900": "VNC"
    }

    open_ports = get_open_ports(nmap_output)

    print("\n" + "=" * 60)
    print("PORT SECURITY ASSESSMENT")
    print("=" * 60)

    if not open_ports:
        print("[PASS] No open TCP ports detected")
        return

    print(f"[WARN] {len(open_ports)} open TCP port(s) detected")

    for port, service in open_ports:
        if port in risky_services:
            print(f"[WARN] Port {port} ({risky_services[port]}) is exposed")
        else:
            print(f"[INFO] Port {port} ({service}) is open")


def check_ssh():
    result = subprocess.run(
        ["ss", "-lnt"],
        capture_output=True,
        text=True
    )

    for line in result.stdout.splitlines():
        parts = line.split()

        if len(parts) >= 4:
            local_address = parts[3]

            if local_address.endswith(":22"):
                return True

    return False


def check_firewall():
    ufw_check = subprocess.run(
        ["bash", "-c", "command -v ufw"],
        capture_output=True,
        text=True
    )

    if ufw_check.returncode == 0:
        status = subprocess.run(
            ["sudo", "ufw", "status"],
            capture_output=True,
            text=True
        )

        if "Status: active" in status.stdout:
            return "UFW active"

        return "UFW installed but inactive"

    nft_check = subprocess.run(
        ["bash", "-c", "command -v nft"],
        capture_output=True,
        text=True
    )

    if nft_check.returncode == 0:
        rules = subprocess.run(
            ["sudo", "nft", "list", "ruleset"],
            capture_output=True,
            text=True
        )

        if rules.stdout.strip():
            return "nftables rules detected"

        return "nftables installed but no rules detected"

    return "No supported firewall detected"


def generate_recommendations(nmap_output):
    recommendations = []

    open_ports = get_open_ports(nmap_output)

    if open_ports:
        ports = ", ".join(
            f"{port}/{service}"
            for port, service in open_ports
        )

        recommendations.append(
            f"[WARN] Review exposed TCP services: {ports}"
        )
    else:
        recommendations.append(
            "[PASS] No exposed TCP services detected. "
            "Continue minimizing unnecessary services."
        )

    if check_ssh():
        recommendations.append(
            "[WARN] SSH is exposed. Restrict access to trusted "
            "hosts and use key-based authentication."
        )
    else:
        recommendations.append(
            "[PASS] SSH is not exposed. No SSH hardening required."
        )

    firewall_status = check_firewall()
    if firewall_status == "UFW active":
        recommendations.append(
            "[PASS] UFW is active. Review firewall rules regularly."
        )

    elif firewall_status == "nftables rules detected":
        recommendations.append(
            "[PASS] nftables rules are present. "
            "Review firewall rules regularly."
        )

    elif firewall_status == "UFW installed but inactive":
        recommendations.append(
            "[HIGH] UFW is installed but inactive. "
            "Enable and configure the firewall."
        )

    else:
        recommendations.append(
            "[HIGH] No active host firewall rules detected. "
            "Configure a host-based firewall."
        )

    return recommendations


def create_report(
    target,
    connectivity,
    dns,
    nmap_output,
    open_ports,
    ssh_exposed,
    firewall_status,
    recommendations
):
    """Create a Markdown audit report."""

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    safe_target = target.replace("/", "_")

    report_file = REPORT_DIR / f"audit-{safe_target}.md"

    report = []

    report.append("# Network Infrastructure Audit")
    report.append("")
    report.append(f"Target: {target}")
    report.append(f"Date: {timestamp}")
    report.append("")

    report.append("## Executive Summary")
    report.append("")

    if connectivity:
        report.append("- Connectivity: PASS")
    else:
        report.append("- Connectivity: FAIL")

    if dns:
        report.append("- Reverse DNS: PASS")
    else:
        report.append("- Reverse DNS: WARN")

    if open_ports:
        report.append(
            f"- Open TCP ports: {len(open_ports)} detected"
        )
    else:
        report.append(
            "- Open TCP ports: NONE detected"
        )

    if ssh_exposed:
        report.append("- SSH exposure: WARN")
    else:
        report.append("- SSH exposure: PASS")

    if firewall_status in (
        "UFW active",
        "nftables rules detected"
    ):
        report.append("- Firewall: PASS")
    else:
        report.append("- Firewall: WARN")

    report.append("")

    report.append("## Service Discovery")
    report.append("")
    report.append("```text")
    report.append(nmap_output.rstrip())
    report.append("```")
    report.append("")

    report.append("## Open Port Assessment")
    report.append("")

    if open_ports:
        for port, service in open_ports:
            report.append(
                f"- {port}/tcp - {service}"
            )
    else:
        report.append(
            "No open TCP ports were detected."
        )

    report.append("")

    report.append("## SSH Assessment")
    report.append("")

    if ssh_exposed:
        report.append(
            "SSH is listening on TCP port 22."
        )
    else:
        report.append(
            "SSH is not listening on TCP port 22."
        )

    report.append("")

    report.append("## Firewall Assessment")
    report.append("")
    report.append(
        f"Detected status: {firewall_status}"
    )
    report.append("")

    report.append("## Security Recommendations")
    report.append("")

    for recommendation in recommendations:
        report.append(
            f"- {recommendation}"
        )

    report.append("")

    report.append("## Methodology")
    report.append("")
    report.append(
        "The auditor performs connectivity testing, reverse DNS "
        "resolution, TCP service discovery, SSH exposure checking, "
        "firewall assessment, and security recommendation generation."
    )

    report_file.write_text(
        "\n".join(report),
        encoding="utf-8"
    )

    return report_file


def create_json_report(
    target,
    connectivity,
    dns,
    nmap_output,
    open_ports,
    ssh_exposed,
    firewall_status,
    recommendations
):
    """Create a JSON audit report."""

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    safe_target = target.replace("/", "_")
    report_file = REPORT_DIR / f"audit-{safe_target}.json"

    report_data = {
        "audit": {
            "target": target,
            "timestamp": timestamp
        },
        "connectivity": {
            "reachable": connectivity,
            "status": "PASS" if connectivity else "FAIL"
        },
        "reverse_dns": {
            "available": dns,
            "status": "PASS" if dns else "WARN"
        },
        "service_discovery": {
            "method": "nmap -sV --top-ports 20",
            "raw_output": nmap_output
        },
        "open_ports": [
            {
                "port": port,
                "protocol": "tcp",
                "service": service
            }
            for port, service in open_ports
        ],
        "ssh": {
            "exposed": ssh_exposed,
            "status": "WARN" if ssh_exposed else "PASS"
        },
        "firewall": {
            "status": firewall_status,
            "assessment": (
                "PASS"
                if firewall_status in (
                    "UFW active",
                    "nftables rules detected"
                )
                else "WARN"
            )
        },
        "recommendations": recommendations
    }

    report_file.write_text(
        json.dumps(report_data, indent=4),
        encoding="utf-8"
    )

    return report_file


def main():

    parser = argparse.ArgumentParser(
        description="Network Infrastructure Health & Security Auditor"
    )

    parser.add_argument(
        "target",
        help="Target IP address or hostname to audit"
    )

    parser.add_argument(
        "--report",
        action="store_true",
        help="Generate a Markdown audit report"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Generate a JSON audit report"
    )

    args = parser.parse_args()
    target = args.target

    print("=" * 60)
    print("NETWORK INFRASTRUCTURE AUDIT")
    print("=" * 60)
    print(f"Target: {target}\n")

    # Connectivity

    print("[*] Checking connectivity...")

    connectivity = check_connectivity(target)

    if connectivity:
        print("[PASS] Host reachable")
    else:
        print("[FAIL] Host unreachable")

    # DNS

    print("\n[*] Checking DNS resolution...")

    dns = check_dns(target)

    if dns:
        print("[PASS] Reverse DNS resolution available")
    else:
        print("[WARN] Reverse DNS resolution unavailable")

    # Service discovery

    print("\n[*] Discovering network services...")

    nmap_output = run_nmap(target)

    if nmap_output:
        print("[PASS] Service discovery completed")
    else:
        print("[FAIL] Service discovery failed")

    # Nmap results

    print("\n" + "=" * 60)
    print("SERVICE DISCOVERY")
    print("=" * 60)

    print(nmap_output)

    # Port assessment

    open_ports = get_open_ports(nmap_output)

    assess_ports(nmap_output)

    # SSH assessment

    print("\n" + "=" * 60)
    print("SSH SECURITY ASSESSMENT")
    print("=" * 60)

    ssh_exposed = check_ssh()

    if ssh_exposed:
        print("[WARN] SSH is listening on port 22")
    else:
        print("[PASS] SSH is not listening on port 22")

    # Firewall assessment

    print("\n" + "=" * 60)
    print("FIREWALL ASSESSMENT")
    print("=" * 60)

    firewall_status = check_firewall()

    if firewall_status == "UFW active":
        print("[PASS] UFW firewall is active")

    elif firewall_status == "nftables rules detected":
        print("[PASS] nftables rules detected")

    elif firewall_status == "UFW installed but inactive":
        print("[WARN] UFW is installed but inactive")

    elif firewall_status == "nftables installed but no rules detected":
        print("[WARN] nftables has no active rules")

    else:
        print("[WARN] No supported firewall detected")

    # Recommendations

    recommendations = generate_recommendations(nmap_output)

    print("\n" + "=" * 60)
    print("SECURITY RECOMMENDATIONS")
    print("=" * 60)

    for recommendation in recommendations:
        print(recommendation)
# Markdown report

    if args.report:

        report_file = create_report(
            target,
            connectivity,
            dns,
            nmap_output,
            open_ports,
            ssh_exposed,
            firewall_status,
            recommendations
        )

        print("\n" + "=" * 60)
        print("REPORT")
        print("=" * 60)
        print(f"[PASS] Markdown report created: {report_file}")

    # JSON report

    if args.json:

        json_file = create_json_report(
            target,
            connectivity,
            dns,
            nmap_output,
            open_ports,
            ssh_exposed,
            firewall_status,
            recommendations
        )

        print(f"[PASS] JSON report created: {json_file}")

    # Completion

    print("\n" + "=" * 60)
    print("AUDIT COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
