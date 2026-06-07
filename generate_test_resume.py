from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib import colors

OUTPUT = "test_resume_cybersecurity.pdf"

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    rightMargin=2*cm, leftMargin=2*cm,
    topMargin=2*cm, bottomMargin=2*cm
)

styles = getSampleStyleSheet()

name_style = ParagraphStyle("name", fontSize=22, fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=4)
contact_style = ParagraphStyle("contact", fontSize=9, fontName="Helvetica", alignment=TA_CENTER, spaceAfter=12, textColor=colors.grey)
section_style = ParagraphStyle("section", fontSize=11, fontName="Helvetica-Bold", spaceBefore=14, spaceAfter=4, textColor=colors.HexColor("#2c3e50"))
body_style = ParagraphStyle("body", fontSize=9, fontName="Helvetica", spaceAfter=3, leading=13)
job_title_style = ParagraphStyle("job_title", fontSize=10, fontName="Helvetica-Bold", spaceAfter=1)
date_style = ParagraphStyle("date", fontSize=9, fontName="Helvetica-Oblique", spaceAfter=4, textColor=colors.grey)

def section(title):
    return [
        Paragraph(title.upper(), section_style),
        HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#2c3e50"), spaceAfter=6),
    ]

def bullet(text):
    return Paragraph(f"• {text}", body_style)

story = []

story.append(Paragraph("Alex Morgan", name_style))
story.append(Paragraph("Brussels, Belgium &nbsp;|&nbsp; alex.morgan@email.com &nbsp;|&nbsp; +32 470 123 456 &nbsp;|&nbsp; linkedin.com/in/alexmorgan-sec", contact_style))

story += section("Profile")
story.append(Paragraph(
    "Cybersecurity Analyst with 4 years of experience in threat detection, incident response, and vulnerability management. "
    "Skilled in SIEM platforms, penetration testing, and network security monitoring. "
    "Holds CompTIA Security+ and CEH certifications. Passionate about proactive threat hunting and security automation.",
    body_style
))

story += section("Experience")

story.append(Paragraph("Cybersecurity Analyst — SecureNet Belgium", job_title_style))
story.append(Paragraph("March 2022 – Present", date_style))
story += [
    bullet("Monitored and triaged security events using Splunk SIEM, reducing mean time to detect (MTTD) by 35%."),
    bullet("Led incident response for 12 critical security incidents including ransomware and phishing campaigns."),
    bullet("Conducted internal vulnerability assessments using Nessus and OpenVAS across 200+ endpoints."),
    bullet("Developed automated threat hunting scripts in Python, improving detection of lateral movement by 40%."),
    bullet("Collaborated with IT teams to harden Windows and Linux server configurations per CIS benchmarks."),
]

story.append(Spacer(1, 6))
story.append(Paragraph("Junior Security Analyst — DataShield S.A.", job_title_style))
story.append(Paragraph("September 2020 – February 2022", date_style))
story += [
    bullet("Monitored network traffic with Wireshark and Zeek, identifying anomalous behaviour and IOCs."),
    bullet("Assisted in penetration testing engagements using Metasploit and Burp Suite on client web applications."),
    bullet("Maintained and updated firewall rules (pfSense, Cisco ASA) and IDS/IPS signatures (Snort)."),
    bullet("Produced monthly vulnerability reports and remediation recommendations for management."),
]

story += section("Skills")
story += [
    bullet("SIEM: Splunk, IBM QRadar, Microsoft Sentinel"),
    bullet("Penetration Testing: Metasploit, Burp Suite, Nmap, Nikto, Kali Linux"),
    bullet("Network Security: Wireshark, Zeek, Snort, pfSense, Cisco ASA"),
    bullet("Vulnerability Management: Nessus, OpenVAS, Qualys"),
    bullet("Programming: Python (scripting, automation), Bash, PowerShell"),
    bullet("Frameworks: MITRE ATT&CK, NIST CSF, ISO 27001, OWASP Top 10"),
    bullet("Cloud Security: AWS IAM, Azure Security Center, basic GCP"),
    bullet("OS: Windows Server, Ubuntu, CentOS, Active Directory"),
]

story += section("Certifications")
story += [
    bullet("CompTIA Security+ (2021)"),
    bullet("Certified Ethical Hacker (CEH) — EC-Council (2022)"),
    bullet("Splunk Core Certified User (2023)"),
    bullet("AWS Cloud Practitioner (2023)"),
]

story += section("Education")
story.append(Paragraph("Bachelor of Computer Science — Université Libre de Bruxelles", job_title_style))
story.append(Paragraph("2017 – 2020 | Major: Networks & Security", date_style))

story += section("Projects")
story += [
    bullet("Honeypot Network (2023): Deployed a multi-service honeypot using T-Pot to capture and analyse real-world attack patterns. Logged 15,000+ intrusion attempts in 30 days."),
    bullet("Phishing Detection Tool (2022): Built a Python ML classifier using scikit-learn to detect phishing URLs with 94% accuracy, deployed as an internal browser extension."),
]

doc.build(story)
print(f"Generated: {OUTPUT}")
