"""Generate .drawio.svg diagram files using Graphviz for automatic layout and connectors."""
import os
import graphviz


BG = "#1a1a2e"
FONT = "Segoe UI,Helvetica,Arial,sans-serif"


def make_graph(name, direction="LR", engine="dot", **kwargs):
    """Create a styled Graphviz Digraph."""
    g = graphviz.Digraph(name, format="svg", engine=engine)
    attrs = dict(rankdir=direction, bgcolor=BG, pad="0.4", margin="0",
                 fontname=FONT, fontcolor="#999999", fontsize="13",
                 style="rounded", nodesep="0.5", ranksep="0.6",
                 size="10,5!", ratio="fill")
    attrs.update(kwargs)
    g.attr(**attrs)
    g.attr("node", shape="box", style="filled,rounded,bold",
           fontname=FONT, fontsize="13", fontcolor="white",
           width="1.6", height="0.6", penwidth="2.5",
           fillcolor="#0f3460", color="#333333")
    g.attr("edge", arrowsize="0.9", penwidth="2", fontname=FONT,
           fontsize="11", fontcolor="#cccccc")
    return g


def save(g, outdir, name):
    path = os.path.join(outdir, name)
    g.render(path, cleanup=True)
    print(f"Created: {path}.svg")


# ── Diagram 1: MITRE Cybersecurity Ecosystem ──
def diagram_01_ecosystem(outdir):
    g = make_graph("ecosystem")
    with g.subgraph(name="cluster_offense") as c:
        c.attr(label="Offense", style="dashed,rounded", color="#555555",
               fontcolor="#999999", penwidth="1.5")
        c.node("CVE", "CVE\nVulnerabilities", fillcolor="#0f3460", color="#e67e22")
        c.node("CWE", "CWE\nWeaknesses", fillcolor="#0f3460", color="#e67e22")
        c.node("CAPEC", "CAPEC\nAttack Patterns", fillcolor="#0f3460", color="#e67e22")
    with g.subgraph(name="cluster_core") as c:
        c.attr(label="Core", style="dashed,rounded", color="#555555",
               fontcolor="#999999", penwidth="1.5")
        c.node("ATTACK", "ATT&CK\nAdversary Behavior", fillcolor="#0f3460", color="#e94560")
    with g.subgraph(name="cluster_defense") as c:
        c.attr(label="Defense", style="dashed,rounded", color="#555555",
               fontcolor="#999999", penwidth="1.5")
        c.node("D3FEND", "D3FEND\nCountermeasures", fillcolor="#0f3460", color="#16a085")
        c.node("ATLAS", "ATLAS\nAI/ML Threats", fillcolor="#0f3460", color="#9b59b6")
    g.edge("CWE", "CVE", color="#e67e22")
    g.edge("CWE", "CAPEC", color="#e67e22")
    g.edge("CAPEC", "ATTACK", color="#e94560")
    g.edge("CVE", "ATTACK", color="#e94560")
    g.edge("ATTACK", "D3FEND", color="#16a085")
    g.edge("ATTACK", "ATLAS", color="#9b59b6")
    save(g, outdir, "mitre-ecosystem.drawio")


# ── Diagram 2: 14 ATT&CK Tactics ──
def diagram_02_14tactics(outdir):
    g = make_graph("tactics", ranksep="0.4", nodesep="0.3")
    phases = [
        ("Pre-Attack", "#3498db", [("RECON", "Reconnaissance"), ("RESDEV", "Resource\nDevelopment")]),
        ("Get In", "#e74c3c", [("IA", "Initial\nAccess"), ("EXEC", "Execution"),
                               ("PERS", "Persistence"), ("PE", "Privilege\nEscalation")]),
        ("Stay In", "#e67e22", [("DE", "Defense\nEvasion"), ("CA", "Credential\nAccess"),
                                ("DISC", "Discovery"), ("LM", "Lateral\nMovement")]),
        ("Act", "#9b59b6", [("COLL", "Collection"), ("C2", "Command &\nControl"),
                            ("EXFIL", "Exfiltration"), ("IMP", "Impact")]),
    ]
    prev_last = None
    for label, color, nodes in phases:
        with g.subgraph(name=f"cluster_{label.replace(' ','')}") as c:
            c.attr(label=label, style="dashed,rounded", color="#555555",
                   fontcolor="#999999", penwidth="1.5")
            for i, (nid, nlabel) in enumerate(nodes):
                c.node(nid, nlabel, fillcolor=color, color=color)
            for i in range(len(nodes) - 1):
                g.edge(nodes[i][0], nodes[i + 1][0], color=color)
        if prev_last:
            g.edge(prev_last, nodes[0][0], color="white", style="bold")
        prev_last = nodes[-1][0]
    save(g, outdir, "14-attack-tactics.drawio")


# ── Diagram 3: Attack Chain (Supply Chain) ──
def diagram_03_attack_chain(outdir):
    g = make_graph("attack_chain")
    nodes = [
        ("T1195", "T1195\nSupply Chain\nCompromise", "#e74c3c"),
        ("T1059", "T1059\nExecution", "#e67e22"),
        ("T1552", "T1552\nUnsecured\nCredentials", "#f39c12"),
        ("T1078", "T1078\nValid Accounts", "#2ecc71"),
        ("T1098", "T1098\nAccount\nManipulation", "#3498db"),
        ("T1567", "T1567\nExfiltration", "#9b59b6"),
    ]
    for nid, label, color in nodes:
        g.node(nid, label, fillcolor=color, color=color)
    for i in range(len(nodes) - 1):
        g.edge(nodes[i][0], nodes[i + 1][0], color="#cccccc")
    save(g, outdir, "attack-chain-supply.drawio")


# ── Diagram 4: Upload to Ransomware ──
def diagram_04_ransomware(outdir):
    g = make_graph("ransomware", direction="TB")
    nodes = [
        ("A", "T1190\nUnrestricted\nFile Upload", "#e74c3c"),
        ("B", "T1505.003\nWeb Shell\nDeployed", "#e74c3c"),
        ("C", "T1059\nRemote Command\nExecution", "#e67e22"),
        ("D", "T1552\nExtract DB\nCredentials", "#f39c12"),
        ("E", "T1078\nDirect Database\nAccess", "#2ecc71"),
        ("F", "T1565\nData\nManipulation", "#9b59b6"),
        ("G", "T1485\nRansomware\nDeployment", "#1a1a2e"),
    ]
    for nid, label, color in nodes:
        stroke = "#e94560" if nid == "G" else color
        g.node(nid, label, fillcolor=color, color=stroke)
    for i in range(len(nodes) - 1):
        g.edge(nodes[i][0], nodes[i + 1][0], color="#cccccc")
    save(g, outdir, "ransomware-chain.drawio")


# ── Diagram 5: Crooked Line ──
def diagram_05_crooked_line(outdir):
    g = make_graph("crooked", nodesep="0.3", ranksep="0.4")
    data = [
        ("IA", "Initial\nAccess", "#e74c3c"),
        ("EX", "Execution", "#e67e22"),
        ("D1", "Discovery", "#3498db"),
        ("CA1", "Credential\nAccess", "#f39c12"),
        ("LM1", "Lateral\nMovement", "#2ecc71"),
        ("D2", "Discovery\n(new segment)", "#3498db"),
        ("CA2", "Credential\nAccess", "#f39c12"),
        ("LM2", "Lateral\nMovement", "#2ecc71"),
        ("COL", "Collection", "#9b59b6"),
        ("XF", "Exfiltration", "#1a1a2e"),
    ]
    for nid, label, color in data:
        stroke = "#e94560" if nid == "XF" else color
        g.node(nid, label, fillcolor=color, color=stroke)
    g.edge("IA", "EX", color="#cccccc")
    g.edge("EX", "D1", color="#cccccc")
    g.edge("D1", "CA1", color="#cccccc")
    g.edge("CA1", "D1", color="#e94560", penwidth="3", constraint="false")
    g.edge("CA1", "LM1", color="#cccccc")
    g.edge("LM1", "D1", color="#e94560", penwidth="3", constraint="false")
    g.edge("LM1", "D2", color="#cccccc")
    g.edge("D2", "CA2", color="#cccccc")
    g.edge("CA2", "LM2", color="#cccccc")
    g.edge("LM2", "COL", color="#cccccc")
    g.edge("COL", "XF", color="#cccccc")
    save(g, outdir, "crooked-line.drawio")


# ── Diagram 6: Immutable Logging ──
def diagram_06_immutable_logging(outdir):
    g = make_graph("logging")
    g.node("APP", "Application", fillcolor="#2c3e50", color="#3498db")
    g.node("LOG", "Secure Logger", fillcolor="#27ae60", color="#2ecc71")
    g.node("HASH", "Hash\nValidation", fillcolor="#2980b9", color="#3498db")
    g.node("BUF", "Local Buffer", fillcolor="#8e44ad", color="#9b59b6")
    g.node("ENC", "Encrypted\nStorage", fillcolor="#d35400", color="#e67e22")
    g.node("SIEM", "External\nSIEM", fillcolor="#d35400", color="#e67e22")
    g.node("TAMP", "Tamper\nDetection", fillcolor="#c0392b", color="#e74c3c")
    g.node("ALERT", "Alert\nSecurity Team", fillcolor="#e74c3c", color="#c0392b")
    g.edge("APP", "LOG", color="#3498db")
    g.edge("LOG", "HASH", color="#2ecc71")
    g.edge("HASH", "BUF", color="#3498db")
    g.edge("BUF", "ENC", color="#9b59b6")
    g.edge("BUF", "SIEM", color="#9b59b6")
    g.edge("ENC", "TAMP", color="#e67e22")
    g.edge("SIEM", "TAMP", color="#e67e22")
    g.edge("TAMP", "ALERT", color="#e74c3c")
    save(g, outdir, "immutable-logging.drawio")


# ── Diagram 7: Supply Chain Security Flow ──
def diagram_07_supply_chain(outdir):
    g = make_graph("supplychain", direction="TB")
    g.node("DEV", "Developer", fillcolor="#2c3e50", color="#3498db")
    g.node("DEP", "Dependency\nRequest", fillcolor="#2980b9", color="#3498db")
    g.node("REG", "Package\nRegistry", fillcolor="#8e44ad", color="#9b59b6", shape="diamond")
    g.node("INT", "Integrity\nCheck", fillcolor="#d35400", color="#e67e22")
    g.node("HASH", "Hash Valid?", fillcolor="#f39c12", color="#e67e22", shape="diamond")
    g.node("BLOCK", "Block & Log\nT1195.001", fillcolor="#e74c3c", color="#c0392b")
    g.node("VULN", "Vulnerability\nScan", fillcolor="#27ae60", color="#2ecc71")
    g.node("CLEAN", "Clean?", fillcolor="#f39c12", color="#e67e22", shape="diamond")
    g.node("INST", "Install &\nMonitor", fillcolor="#16a085", color="#1abc9c")
    g.edge("DEV", "DEP", color="#3498db")
    g.edge("DEP", "REG", color="#3498db")
    g.edge("REG", "INT", color="#9b59b6")
    g.edge("INT", "HASH", color="#e67e22")
    g.edge("HASH", "BLOCK", label="No", color="#e74c3c")
    g.edge("HASH", "VULN", label="Yes", color="#2ecc71")
    g.edge("VULN", "CLEAN", color="#2ecc71")
    g.edge("CLEAN", "BLOCK", label="No", color="#e74c3c")
    g.edge("CLEAN", "INST", label="Yes", color="#1abc9c")
    save(g, outdir, "supply-chain-flow.drawio")


# ── Diagram 8: Data Flow Monitoring ──
def diagram_08_data_flow(outdir):
    g = make_graph("dataflow", direction="TB")
    g.node("REQ", "User Request", fillcolor="#2c3e50", color="#3498db")
    g.node("AUTH", "Auth &\nAuthorization", fillcolor="#2980b9", color="#3498db")
    g.node("MON", "Data Access\nMonitor", fillcolor="#8e44ad", color="#9b59b6")
    g.node("ANOM", "Anomaly?", fillcolor="#f39c12", color="#e67e22", shape="diamond")
    g.node("ALERT", "Alert & Block", fillcolor="#e74c3c", color="#c0392b")
    g.node("QUERY", "Execute Query", fillcolor="#27ae60", color="#2ecc71")
    g.node("BULK", "Bulk Transfer?", fillcolor="#f39c12", color="#e67e22", shape="diamond")
    g.node("RATE", "Rate\nExceeded?", fillcolor="#f39c12", color="#e67e22", shape="diamond")
    g.node("RESP", "Send Response", fillcolor="#16a085", color="#1abc9c")
    g.edge("REQ", "AUTH", color="#3498db")
    g.edge("AUTH", "MON", color="#3498db")
    g.edge("MON", "ANOM", color="#9b59b6")
    g.edge("ANOM", "ALERT", label="Yes", color="#e74c3c")
    g.edge("ANOM", "QUERY", label="No", color="#2ecc71")
    g.edge("QUERY", "BULK", color="#2ecc71")
    g.edge("BULK", "ALERT", label="Yes", color="#e74c3c")
    g.edge("BULK", "RATE", label="No", color="#2ecc71")
    g.edge("RATE", "ALERT", label="Yes", color="#e74c3c")
    g.edge("RATE", "RESP", label="No", color="#1abc9c")
    save(g, outdir, "data-flow-monitoring.drawio")


# ── Diagram 9: Threat Modeling Cycle ──
def diagram_09_threat_modeling(outdir):
    g = make_graph("threat_model", engine="circo", mindist="2.0")
    g.attr("node", width="1.8", height="0.7")
    items = [
        ("ID", "Identify\nFeature", "#2c3e50", "#3498db"),
        ("MAP", "Map to ATT&CK\nTechniques", "#2980b9", "#3498db"),
        ("ASSESS", "Assess Risk\n& Impact", "#d35400", "#e67e22"),
        ("DESIGN", "Design\nDetections", "#8e44ad", "#9b59b6"),
        ("IMPL", "Implement\n& Monitor", "#27ae60", "#2ecc71"),
        ("TEST", "Test &\nIterate", "#e74c3c", "#c0392b"),
    ]
    for nid, label, fill, stroke in items:
        g.node(nid, label, fillcolor=fill, color=stroke)
    colors = ["#3498db", "#3498db", "#e67e22", "#9b59b6", "#2ecc71", "#e74c3c"]
    for i in range(len(items)):
        g.edge(items[i][0], items[(i + 1) % len(items)][0], color=colors[i])
    save(g, outdir, "threat-modeling-cycle.drawio")


# ── Diagram 10: Defense in Depth ──
def diagram_10_defense_depth(outdir):
    g = make_graph("defense", direction="TB", ranksep="0.4")
    with g.subgraph(name="cluster_prevent") as c:
        c.attr(label="Prevention", style="dashed,rounded", color="#555555",
               fontcolor="#999999", penwidth="1.5")
        c.node("IV", "Input\nValidation", fillcolor="#27ae60", color="#2ecc71")
        c.node("AUTHN", "Authentication", fillcolor="#2980b9", color="#3498db")
        c.node("AUTHZ", "Authorization", fillcolor="#8e44ad", color="#9b59b6")
        c.node("DAC", "Data Access\nControls", fillcolor="#d35400", color="#e67e22")
    with g.subgraph(name="cluster_detect") as c:
        c.attr(label="Detection", style="dashed,rounded", color="#555555",
               fontcolor="#999999", penwidth="1.5")
        c.node("BA", "Behavioral\nAnalytics", fillcolor="#c0392b", color="#e74c3c")
        c.node("AD", "Anomaly\nDetection", fillcolor="#e74c3c", color="#c0392b")
        c.node("TI", "Threat\nIntelligence", fillcolor="#f39c12", color="#e67e22")
    with g.subgraph(name="cluster_respond") as c:
        c.attr(label="Response", style="dashed,rounded", color="#555555",
               fontcolor="#999999", penwidth="1.5")
        c.node("AB", "Automated\nBlocking", fillcolor="#2c3e50", color="#3498db")
        c.node("AR", "Alert &\nRemediation", fillcolor="#1a1a2e", color="#e94560")
    edges = [("IV","AUTHN"),("AUTHN","AUTHZ"),("AUTHZ","DAC"),
             ("DAC","BA"),("BA","AD"),("AD","TI"),("TI","AB"),("AB","AR")]
    for s, t in edges:
        g.edge(s, t, color="#cccccc")
    save(g, outdir, "defense-in-depth.drawio")


# ── Diagram 11: OWASP + ATT&CK Integration ──
def diagram_11_owasp_integration(outdir):
    g = make_graph("owasp", ranksep="0.6")
    # Practices
    g.node("SC", "Secure Coding", fillcolor="#27ae60", color="#2ecc71")
    g.node("BM", "Behavioral\nMonitoring", fillcolor="#2980b9", color="#3498db")
    g.node("VT", "Vulnerability\nTesting", fillcolor="#d35400", color="#e67e22")
    g.node("TC", "Technique\nCorrelation", fillcolor="#8e44ad", color="#9b59b6")
    g.node("SR", "Security\nReviews", fillcolor="#c0392b", color="#e74c3c")
    g.node("TH", "Threat\nHunting", fillcolor="#e74c3c", color="#c0392b")
    # Outcomes
    g.node("SBD", "Secure\nby Design", fillcolor="#16a085", color="#1abc9c")
    g.node("MBB", "Monitor\nby Behavior", fillcolor="#16a085", color="#1abc9c")
    g.node("RBI", "Respond by\nIntelligence", fillcolor="#16a085", color="#1abc9c")
    g.edge("SC", "SBD", color="#2ecc71")
    g.edge("BM", "SBD", color="#3498db")
    g.edge("VT", "MBB", color="#e67e22")
    g.edge("TC", "MBB", color="#9b59b6")
    g.edge("SR", "RBI", color="#e74c3c")
    g.edge("TH", "RBI", color="#c0392b")
    g.edge("SBD", "MBB", color="#1abc9c")
    g.edge("MBB", "RBI", color="#1abc9c")
    save(g, outdir, "owasp-attack-integration.drawio")


if __name__ == "__main__":
    outdir = os.path.join("slides", "img")
    os.makedirs(outdir, exist_ok=True)

    # Add Graphviz to PATH if needed
    gv_bin = r"C:\Program Files\Graphviz\bin"
    if os.path.isdir(gv_bin) and gv_bin not in os.environ.get("PATH", ""):
        os.environ["PATH"] = gv_bin + ";" + os.environ.get("PATH", "")

    diagram_01_ecosystem(outdir)
    diagram_02_14tactics(outdir)
    diagram_03_attack_chain(outdir)
    diagram_04_ransomware(outdir)
    diagram_05_crooked_line(outdir)
    diagram_06_immutable_logging(outdir)
    diagram_07_supply_chain(outdir)
    diagram_08_data_flow(outdir)
    diagram_09_threat_modeling(outdir)
    diagram_10_defense_depth(outdir)
    diagram_11_owasp_integration(outdir)

    print(f"\nGenerated 11 .drawio.svg files in {outdir}/")
