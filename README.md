# MITRE ATT&CK for Developers — Beyond OWASP

This repository contains the slide deck, demos, and additional resources for the "MITRE ATT&CK for Developers — Beyond OWASP" talk by Chris Ayers, Principal Software Engineer at Microsoft. The talk bridges the gap between threat intelligence and practical development, showing how to apply adversarial thinking to your code.

## Slides

You can access the slides for the talk at [https://chris-ayers.com/mitre-attack-for-devs/](https://chris-ayers.com/mitre-attack-for-devs/).

## Repository Content

This repository provides insights, code samples, and demonstrations for applying the MITRE ATT&CK framework to application development. Topics covered include:

- Understanding the MITRE ATT&CK framework and its 14 tactics
- How ATT&CK complements OWASP — vulnerabilities vs. adversary behavior
- Practical code examples mapping ATT&CK techniques to real development scenarios
- Detection and defense patterns for common attack techniques
- Supply chain security, credential access, and data exfiltration defenses
- Building an adversary-informed development workflow

## Code Samples

The `samples/` directory contains educational code samples in three languages, each demonstrating attack techniques and corresponding defenses mapped to ATT&CK technique IDs:

- **[Python](./samples/python/)** — Credential stuffing detection, command injection, unsafe deserialization, tamper-evident logging, data access monitoring, secrets scanning
- **[.NET/C#](./samples/dotnet/)** — Command injection, session security, tamper-evident logging, secrets management, web shell detection
- **[JavaScript](./samples/javascript/)** — SQL injection, session security, credential stuffing detection, supply chain verification, data exfiltration detection, secrets detection

## Resources

- [MITRE ATT&CK Enterprise Matrix](https://attack.mitre.org/matrices/enterprise/)
- [MITRE ATT&CK Techniques](https://attack.mitre.org/techniques/enterprise/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [MITRE D3FEND](https://d3fend.mitre.org/)
- [ATT&CK Navigator](https://mitre-attack.github.io/attack-navigator/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

## Connect with Chris Ayers

Feel free to connect with Chris Ayers on social media and visit his blog for more information on security and other topics:

- BlueSky: [@chris-ayers.com](https://bsky.app/profile/chris-ayers.com)
- LinkedIn: [chris-l-ayers](https://linkedin.com/in/chris-l-ayers/)
- Blog: [https://chris-ayers.com/](https://chris-ayers.com/)
- GitHub: [Codebytes](https://github.com/codebytes)
- Mastodon: [@Chrisayers@hachyderm.io](https://hachyderm.io/@Chrisayers)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.