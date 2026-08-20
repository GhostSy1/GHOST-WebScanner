import os
class Reporter:
    def __init__(self, target, recon_results, vulnerabilities):
        self.target = target
        self.recon = recon_results
        self.vulns = vulnerabilities
    def generate_txt_report(self):
        filename = f"reports/report_{self.target.replace('https://', '').replace('http://', '').replace('/', '_')}.txt"
        os.makedirs("reports", exist_ok=True)
        with open(filename, "w") as f:
            f.write("="*50 + "\n")
            f.write(f"GHOST SECURITY SUITE - SCAN REPORT\n")
            f.write(f"Target: {self.target}\n")
            f.write("="*50 + "\n\n")
            f.write("[+] RECONNAISSANCE RESULTS\n")
            f.write(f"IP Address: {self.recon.get('ip')}\n")
            f.write(f"Open Ports: {', '.join(map(str, self.recon.get('ports')))}\n")
            f.write("-" * 30 + "\n\n")
            f.write("[+] VULNERABILITY FINDINGS\n")
            if not self.vulns:
                f.write("No major vulnerabilities found.\n")
            for vuln in self.vulns:
                f.write(f"Type: {vuln['type']}\n")
                f.write(f"Finding: {vuln['finding']}\n")
                f.write(f"Severity: {vuln['severity']}\n")
                f.write("-" * 20 + "\n")
        return filename
