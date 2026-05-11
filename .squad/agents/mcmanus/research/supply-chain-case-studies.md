# Supply-Chain Case Studies — Speaker Research Dossier

**Prepared by:** McManus  
**Date:** 2026-05-11  
**Scope:** Speaker-grade narrative support for the MITRE ATT&CK for Developers deck. Facts below were checked against primary or high-confidence public sources where available. If a fact is thin, contested, or still evolving, it is flagged.

## Full Case Studies

### Shai-Hulud npm worm (2025)
- **TL;DR:** Shai-Hulud was a self-replicating npm supply-chain worm that used compromised maintainer credentials and npm lifecycle scripts to steal GitHub/npm/cloud secrets, publish infected package versions, and create GitHub-based exfiltration/persistence artifacts.
- **Timeline:** September 14, 2025: GitHub says it was notified of Shai-Hulud; Socket’s timeline shows first observed compromised packages at 17:58 UTC. September 15–16: waves of compromised packages spread, including `@ctrl/tinycolor` and CrowdStrike-scoped packages. September 22: GitHub announced registry hardening after removing 500+ compromised packages and blocking packages containing known IoCs. November 24, 2025: Snyk/Microsoft describe a second-wave “SHA1-Hulud / Shai-Hulud 2.0” using `preinstall`, Bun, GitHub runners, and broader CI/cloud targeting. As of 2026-05-11, first-wave compromised packages were removed from npm, but public reporting treats Shai-Hulud as a family/playbook with later variants; exact maintainer count is not consistently enumerated in public sources.
- **Attack chain mapped to ATT&CK T-IDs:**
  1. **T1195.001 — Supply Chain Compromise: Compromise Software Dependencies:** compromised maintainer/publisher access was used to publish trojanized npm packages.
  2. **T1546.016 — Event Triggered Execution: Installer Packages:** `postinstall` in wave 1, and `preinstall` in later variants, executed malicious payloads during package install.
  3. **T1059.007 — Command and Scripting Interpreter: JavaScript:** `bundle.js`, `setup_bun.js`, or `bun_environment.js` ran the core worm logic.
  4. **T1105 — Ingress Tool Transfer:** the malware downloaded tools such as TruffleHog and runtime components.
  5. **T1555.006 — Credentials from Password Stores: Cloud Secrets Management Stores / T1552 — Unsecured Credentials:** it harvested npm, GitHub, AWS, GCP, Azure, and environment secrets from developer and CI systems.
  6. **T1567.001 — Exfiltration Over Web Service: Exfiltration to Code Repository / T1567.004 — Exfiltration Over Webhook:** stolen data was pushed to public GitHub repos named `Shai-Hulud` or sent to webhook endpoints.
  7. **T1098 — Account Manipulation:** workflows and repositories were modified, including branch/workflow injection and, in later reporting, private repo exposure.
  8. **T1485 — Data Destruction:** later Shai-Hulud 2.0 reporting includes destructive behavior such as shredding/deleting files on Linux hosts.
- **Why it matters to developers:** `npm install` is code execution. If developer laptops and CI runners hold broad tokens, a package install can become a credential-theft and package-publishing event in seconds.
- **Stage moment:** The malware created public GitHub repositories named `Shai-Hulud` containing stolen environment and secret data — the worm used the developer platform itself as the exfiltration channel.
- **Common misconceptions:**
  - It was not just “one bad package”; first-wave public counts reached 500+ packages, and later variants evolved the same playbook.
  - Disabling vulnerable app code would not help if the install had already run on a machine with npm/GitHub/cloud credentials.
- **Sources, 2–4 verified real URLs:**
  - https://github.blog/security/supply-chain-security/our-plan-for-a-more-secure-npm-supply-chain/
  - https://socket.dev/blog/ongoing-supply-chain-attack-targets-crowdstrike-npm-packages
  - https://securelist.com/shai-hulud-worm-infects-500-npm-packages-in-a-supply-chain-attack/117547/
  - https://attack.mitre.org/software/S9008/

### Notepad++ update infrastructure hijack / Chrysalis (2025–2026)
- **TL;DR:** The strongest real Notepad++ supply-chain story is not a plugin compromise or generic typosquat; it is the 2025 compromise of Notepad++ update infrastructure that selectively redirected targeted users to trojanized update installers delivering Cobalt Strike and the Chrysalis backdoor.
- **Timeline:** June 2025: Notepad++ says the incident began. July–October 2025: Kaspersky observed multiple malicious update chains and rotating payloads. September 2, 2025: hosting provider says attackers lost direct server access after maintenance, but retained internal service credentials. November 2025: Kaspersky says it saw no further payloads after November. December 2, 2025: Notepad++ estimates attacker access was definitively terminated after credential rotation and provider fixes. February 2–3, 2026: Notepad++ published disclosure and linked Rapid7/Kaspersky technical research; v8.8.9 added certificate/signature verification, v8.9.1 was recommended for manual update, and v8.9.2 was expected to enforce verification.
- **Attack chain mapped to ATT&CK T-IDs:**
  1. **T1195.002 — Supply Chain Compromise: Compromise Software Supply Chain:** attacker-controlled infrastructure intercepted Notepad++ update traffic.
  2. **T1036 — Masquerading:** malicious `update.exe`/NSIS installers appeared to be legitimate updater artifacts.
  3. **T1105 — Ingress Tool Transfer:** targeted users downloaded malicious update payloads from attacker infrastructure.
  4. **T1574.002 — Hijack Execution Flow: DLL Side-Loading:** a renamed legitimate Bitdefender binary (`BluetoothService.exe`) loaded malicious `log.dll`.
  5. **T1140 — Deobfuscate/Decode Files or Information:** loaders decrypted shellcode/configuration before execution.
  6. **T1071.001 — Application Layer Protocol: Web Protocols:** Chrysalis and Cobalt Strike used HTTP/HTTPS C2 patterns.
  7. **T1059.003 — Command and Scripting Interpreter: Windows Command Shell:** earlier chains collected host data via shell commands such as `whoami`, `tasklist`, `systeminfo`, and `netstat`.
- **Why it matters to developers:** Developer tools are privileged trust anchors. If an editor/updater used on admin jump boxes is hijacked, the attacker inherits the trust of “normal developer workflow.”
- **Stage moment:** The official project says the source code was not the problem; the hosting/update path was. That is the supply-chain lesson: the artifact can be clean while the delivery channel is cursed.
- **Common misconceptions:**
  - This was not a confirmed Notepad++ source-code compromise; public project statements put the compromise at the hosting/update-infrastructure level.
  - “Notepad++ was hacked” does not mean every user got malware; public reporting emphasizes selective targeting.
- **Sources, 2–4 verified real URLs:**
  - https://notepad-plus-plus.org/news/hijacked-incident-info-update/
  - https://securelist.com/notepad-supply-chain-attack/118708/
  - https://www.rapid7.com/blog/post/tr-chrysalis-backdoor-dive-into-lotus-blossoms-toolkit/
  - https://unit42.paloaltonetworks.com/notepad-infrastructure-compromise/

### SolarWinds SUNBURST (2020)
- **TL;DR:** Attackers compromised SolarWinds’ Orion build process so a digitally signed SolarWinds DLL shipped with the SUNBURST backdoor to customers through normal update channels.
- **Timeline:** October 2019: Microsoft reports evidence that attackers were testing code insertion capability. March–June 2020: SolarWinds’ SEC filing says affected Orion updates were released during this period; Mandiant says signed trojanized updates were posted March–May. Spring 2020: Mandiant says the campaign may have begun. December 13–14, 2020: FireEye/Mandiant and CISA published alerts; SolarWinds disclosed fewer than 18,000 customers may have installed affected builds. March 8, 2021: SolarWinds revoked the code-signing certificate used on affected software versions.
- **Attack chain mapped to ATT&CK T-IDs:**
  1. **T1195.002 — Supply Chain Compromise: Compromise Software Supply Chain:** the Orion software build system was compromised and produced affected builds.
  2. **T1554 — Compromise Client Software Binary:** `SolarWinds.Orion.Core.BusinessLayer.dll` was trojanized while still SolarWinds-signed.
  3. **T1027 — Obfuscated Files or Information:** SUNBURST hid strings, blocklists, and logic to evade analysis.
  4. **T1678 — Delay Execution:** Mandiant/Microsoft describe a 12–14 day dormant period before beaconing.
  5. **T1071.004 — Application Layer Protocol: DNS / T1071.001 — Web Protocols:** SUNBURST used DNS-based coordination and HTTP C2 that mimicked SolarWinds traffic.
  6. **T1105 — Ingress Tool Transfer:** follow-on payloads such as TEARDROP/Cobalt Strike were deployed in selected environments.
  7. **T1078 — Valid Accounts / T1021 — Remote Services:** post-compromise activity leaned on legitimate credentials and remote access for lateral movement.
- **Why it matters to developers:** Code signing proves provenance, not intent. If the build pipeline is compromised before signing, the signature faithfully certifies a malicious artifact.
- **Stage moment:** The malicious DLL was SolarWinds-signed; to many controls, the poisoned artifact looked official because it was official.
- **Common misconceptions:**
  - “18,000 affected” means installations of vulnerable Orion builds, not necessarily 18,000 fully exploited intrusions.
  - This was not a simple source-code review miss; SolarWinds reported the vulnerability was introduced via the software build system, not present in the source repository.
- **Sources, 2–4 verified real URLs:**
  - https://www.mandiant.com/resources/blog/evasive-attacker-leverages-solarwinds-supply-chain-compromises-with-sunburst-backdoor
  - https://www.sec.gov/Archives/edgar/data/1739942/000162828020017451/swi-20201214.htm
  - https://www.microsoft.com/en-us/security/blog/2020/12/18/analyzing-solorigate-the-compromised-dll-file-that-started-a-sophisticated-cyberattack-and-how-microsoft-defender-helps-protect/
  - https://www.solarwinds.com/sa-overview/securityadvisory

### XZ Utils backdoor / CVE-2024-3094 (2024)
- **TL;DR:** A long-running social-engineering and maintainer-trust attack inserted an obfuscated backdoor into XZ Utils 5.6.0/5.6.1 release tarballs that could affect `sshd` through `liblzma` on certain Linux builds.
- **Timeline:** 2021–2023: “Jia Tan”/related accounts built trust in the XZ project through contributions and maintainer pressure (widely reported; exact motive/identity remains unproven). February–March 2024: XZ 5.6.0 and 5.6.1 release tarballs contained the backdoor. March 29, 2024: Andres Freund disclosed the backdoor to oss-security after noticing slow SSH logins, high CPU, and valgrind errors. March 29, 2024: CISA warned about malicious code in XZ Utils 5.6.0/5.6.1 and recommended downgrading to an uncompromised version such as 5.4.6 stable.
- **Attack chain mapped to ATT&CK T-IDs:**
  1. **T1195.001 — Supply Chain Compromise: Compromise Software Dependencies:** upstream XZ release artifacts were backdoored.
  2. **T1027 — Obfuscated Files or Information:** exploit data was hidden in test `.xz/.lzma` files and obfuscated build logic.
  3. **T1059.004 — Command and Scripting Interpreter: Unix Shell:** the malicious build process injected shell script execution through `configure`/Makefile logic.
  4. **T1140 — Deobfuscate/Decode Files or Information:** build-time transformations decoded hidden payload material.
  5. **T1574 — Hijack Execution Flow:** the resulting `liblzma` manipulation redirected `RSA_public_decrypt` behavior in `sshd`-related execution paths on affected systems.
  6. **T1210 — Exploitation of Remote Services:** the suspected objective was unauthorized access/RCE through SSH server authentication paths, though full exploit semantics were still under analysis in the original disclosure.
- **Why it matters to developers:** Release artifacts are not automatically equivalent to source repository contents. Reproducible builds, maintainer governance, and artifact verification are security controls, not bureaucracy.
- **Stage moment:** This was caught because Andres Freund noticed SSH was roughly 500ms slower — a performance anomaly exposed a near-catastrophic supply-chain backdoor.
- **Common misconceptions:**
  - The malicious line was not simply sitting in the normal GitHub-generated source snapshot; Andres called out that part of the backdoor was only in distributed tarballs.
  - This did not broadly compromise all Linux systems; CISA and distributions focused on XZ 5.6.0/5.6.1, many of which were in pre-release/rolling distributions.
- **Sources, 2–4 verified real URLs:**
  - https://www.openwall.com/lists/oss-security/2024/03/29/4
  - https://www.cisa.gov/news-events/alerts/2024/03/29/reported-supply-chain-compromise-affecting-xz-utils-data-compression-library-cve-2024-3094
  - https://access.redhat.com/security/cve/CVE-2024-3094

### event-stream / flatmap-stream (2018)
- **TL;DR:** A new maintainer added the malicious `flatmap-stream` dependency to the popular `event-stream` npm package, targeting Copay wallet builds to steal cryptocurrency private keys.
- **Timeline:** September 9, 2018: npm says `flatmap-stream@0.1.1` was added as a direct dependency of `event-stream@3.3.6` by a new maintainer. September–November 2018: the malicious dependency remained present for about 2.5 months. November 20, 2018: GitHub issue #116 flagged the suspicious dependency/obfuscated code. November 26, 2018: npm was notified, removed `flatmap-stream` and `event-stream@3.3.6`, and took ownership of the package. Copay later confirmed affected app versions 5.0.2–5.1.0 were deployed.
- **Attack chain mapped to ATT&CK T-IDs:**
  1. **T1195.001 — Supply Chain Compromise: Compromise Software Dependencies:** a trusted package dependency was poisoned.
  2. **T1098 — Account Manipulation:** maintainership/publishing authority changed hands through social engineering.
  3. **T1059.007 — Command and Scripting Interpreter: JavaScript:** malicious npm package code executed in the JavaScript build environment.
  4. **T1027 — Obfuscated Files or Information:** encrypted/obfuscated payload data was hidden in what looked like test fixture data.
  5. **T1552 — Unsecured Credentials:** the payload targeted Copay account/private key material.
  6. **T1041 — Exfiltration Over C2 Channel:** stolen account/private-key data was sent to an attacker-controlled collection service.
- **Why it matters to developers:** Maintainer handoff is a supply-chain event. A tiny dependency added to an old, trusted package can land in millions of installs before anyone reviews the diff.
- **Stage moment:** The malicious code only activated in a specific Copay build environment — for most users it looked inert, which helped it hide.
- **Common misconceptions:**
  - It was not a generic malware blast against every `event-stream` user; it was narrowly targeted at Copay’s build chain.
  - The risk was not only “developer machine got hacked”; npm reported malicious code made it into Copay versions 5.0.2 through 5.1.0.
- **Sources, 2–4 verified real URLs:**
  - https://blog.npmjs.org/post/180565383195/details-about-the-event-stream-incident.html
  - https://snyk.io/blog/malicious-code-found-in-npm-package-event-stream/
  - https://github.com/dominictarr/event-stream/issues/116

### Axios npm compromise (2026)
- **TL;DR:** Axios’ official npm package was briefly poisoned via a compromised maintainer account, adding a phantom `plain-crypto-js@4.2.1` dependency whose `postinstall` hook deployed a cross-platform RAT.
- **Timeline:** About two weeks before March 31, 2026: Axios’ postmortem says a social-engineering campaign began against the lead maintainer. March 30, 2026 05:57 UTC: `plain-crypto-js@4.2.0` clean decoy was published. March 30 23:59: malicious `plain-crypto-js@4.2.1` was published. March 31 00:21: `axios@1.14.1` was published with `plain-crypto-js` injected. Around 01:00: `axios@0.30.4` was published and community detections began; attacker deleted some reports using the compromised account. March 31 03:15–03:29: malicious axios/plain-crypto-js versions were removed. April 20, 2026: CISA alert linked to the Axios postmortem, Microsoft, and Socket.
- **Attack chain mapped to ATT&CK T-IDs:**
  1. **T1078 — Valid Accounts:** attacker used a compromised maintainer/npm account to publish official package versions.
  2. **T1195.001 — Supply Chain Compromise: Compromise Software Dependencies:** official `axios` releases were poisoned on npm.
  3. **T1546.016 — Event Triggered Execution: Installer Packages:** `plain-crypto-js` executed `postinstall: node setup.js`.
  4. **T1059.007 — Command and Scripting Interpreter: JavaScript:** the setup script/dropper executed during install.
  5. **T1105 — Ingress Tool Transfer:** the dropper contacted C2 and downloaded platform-specific second-stage payloads.
  6. **T1219 — Remote Access Software / T1071.001 — Web Protocols:** the payload behaved as a cross-platform remote access trojan using network C2.
  7. **T1027 — Obfuscated Files or Information:** the payload was obfuscated and self-erased/replaced package metadata after execution.
  8. **T1041 — Exfiltration Over C2 Channel:** systems that ran the RAT should be treated as capable of credential/data exfiltration.
- **Why it matters to developers:** This is verified and stronger than a hypothetical. It shows that even a top-tier package can be compromised without malicious code appearing in the project’s source repo: one added dependency in `package.json` was enough.
- **Stage moment:** StepSecurity found exactly one Axios file changed: `package.json`; the weapon was a dependency nobody imported, added only to trigger `postinstall`.
- **Common misconceptions:**
  - This is not unverifiable; the Axios GitHub postmortem, CISA alert, StepSecurity, and Snyk all document it.
  - Axios source code was not broadly rewritten; the compromise was a malicious npm publication/dependency injection.
- **Sources, 2–4 verified real URLs:**
  - https://github.com/axios/axios/issues/10636
  - https://www.cisa.gov/news-events/alerts/2026/04/20/supply-chain-compromise-impacts-axios-node-package-manager
  - https://www.stepsecurity.io/blog/axios-compromised-on-npm-malicious-versions-drop-remote-access-trojan
  - https://snyk.io/blog/axios-npm-package-compromised-supply-chain-attack-delivers-cross-platform/

### Log4Shell / CVE-2021-44228 (2021)
- **TL;DR:** Log4Shell was a critical remote code execution flaw in the widely embedded Log4j dependency, turning ordinary logged strings into attacker-controlled JNDI lookups that could execute code on vulnerable systems.
- **Timeline:** December 10, 2021: CISA says Log4Shell/CVE-2021-44228 was disclosed publicly and affected Log4j 2.0-beta9 through 2.14.1; Apache released mitigations/updates beginning with 2.15.0. December 13–17: additional related Log4j CVEs and versions followed, including 2.16.0 and 2.17.0 guidance. December 22, 2021: joint CISA/FBI/NSA/international CSA provided mitigation guidance and warned sophisticated actors were scanning/exploiting vulnerable systems. Longer term: CISA assessed exploitation would continue over an extended period.
- **Attack chain mapped to ATT&CK T-IDs:**
  1. **T1190 — Exploit Public-Facing Application:** attackers sent crafted strings to internet-facing apps that logged attacker-controlled input.
  2. **T1210 — Exploitation of Remote Services:** vulnerable services were coerced into JNDI/LDAP/DNS lookups and code execution.
  3. **T1059 — Command and Scripting Interpreter:** successful exploitation commonly enabled attacker-controlled commands or scripts.
  4. **T1105 — Ingress Tool Transfer:** follow-on payloads such as miners, botnet malware, or ransomware tooling could be downloaded.
  5. **T1046 — Network Service Discovery / T1083 — File and Directory Discovery:** post-exploitation activity often involved discovery before lateral movement or payload deployment.
- **Why it matters to developers:** This is not a supply-chain compromise in the SolarWinds sense; it is a dependency-trust failure mode. You can be vulnerable because a transitive library feature is reachable through something as mundane as logging a header.
- **Stage moment:** A string in a log line could become code execution; the dangerous input did not need to be in a “business logic” parameter.
- **Common misconceptions:**
  - Log4Shell was not caused by a malicious maintainer or poisoned Log4j release.
  - Patching the app code alone was not enough; organizations needed asset inventories/SBOM-style visibility to find every embedded copy of Log4j.
- **Sources, 2–4 verified real URLs:**
  - https://www.cisa.gov/news-events/cybersecurity-advisories/aa21-356a
  - https://www.cisa.gov/news-events/news/statement-cisa-director-easterly-log4j-vulnerability
  - https://logging.apache.org/log4j/2.x/security.html
  - https://nvd.nist.gov/vuln/detail/CVE-2021-44228

## Bonus Roster — Swap-In Options

- **Codecov Bash Uploader (2021):** Attackers modified Codecov’s Bash Uploader beginning January 31, 2021, causing CI environments to leak env vars/secrets to a third-party server; source: https://about.codecov.io/security-update/
- **3CX Desktop App (2023):** A trojanized Trading Technologies X_TRADER installer led to compromise of 3CX’s build environment, producing a cascading software supply-chain attack against 3CX Desktop App; source: https://www.mandiant.com/resources/blog/3cx-software-supply-chain-compromise
- **ua-parser-js npm hijack (2021):** Compromised npm versions `0.7.29`, `0.8.0`, and `1.0.0` installed cryptominers and password stealers; source: https://us-cert.cisa.gov/ncas/current-activity/2021/10/22/malware-discovered-popular-npm-package-ua-parser-js
- **ctx PyPI / phpass hijack (2022):** Dormant Python/PHP packages were hijacked to exfiltrate environment variables and AWS credentials, reportedly via expired-domain/account-recovery weaknesses; source: https://www.bleepingcomputer.com/news/security/popular-python-and-php-libraries-hijacked-to-steal-aws-keys/
- **Polyfill.io (2024):** The `cdn.polyfill.io` domain changed hands and was observed serving malicious, dynamically generated JavaScript to sites embedding it, affecting 100K+ sites according to Sansec; source: https://sansec.io/research/polyfill-supply-chain-attack
- **Ledger Connect Kit (2023):** A phished former employee’s npm access allowed malicious Ledger Connect Kit versions `1.1.5`–`1.1.7` to drain DApp users via malicious signing flows; source: https://www.ledger.com/blog/security-incident-report
- **Notepad++ update infrastructure (2025):** Strong candidate for a new deck slide because it is developer-tool specific and shows why update verification matters; sources above.
- **Axios npm compromise (2026):** Keep if the deck wants a very recent npm example; it is now well-documented by project, CISA, StepSecurity, and Snyk.

## Narrative Arc Recommendation

Start familiar and simple: **event-stream** shows how a maintainer handoff plus one dependency can hit real users. Escalate to **Log4Shell** and **XZ** to show that dependency risk is not only npm and not only malicious packages — sometimes the trusted library itself or its release artifact becomes the battlefield. Then hit the developer nervous system with **Shai-Hulud**, **Axios**, and **Notepad++**: package install, CI tokens, and daily developer tools are the attacker’s new beachhead. Close with **SolarWinds** as the enterprise-scale “signed ≠ safe” lesson that ties build pipelines, signing, and detection together.

## Deck-Level Recommendations

1. **Keep Axios, but present it as verified 2026 research, not rumor.** The current deck’s Axios slide is defensible with strong sources.
2. **Add Notepad++ as a short “developer tool supply chain” mini-case or speaker-note sidebar.** It is directly relevant to developers and administrators because the updater path, not the source repo, was abused.
3. **Upgrade Shai-Hulud from a bullet to a narrative beat.** It is the clearest “npm install is code execution” story and should anchor the npm supply-chain section.
4. **Use event-stream as the historical setup, not the climax.** It is excellent for explaining maintainer trust, but Shai-Hulud and Axios are stronger modern developer-stage moments.
5. **Keep Log4Shell framed accurately.** It is dependency trust / transitive exposure, not a malicious supply-chain compromise.
