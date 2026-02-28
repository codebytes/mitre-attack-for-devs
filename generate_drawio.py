"""Generate .drawio.svg diagram files using Graphviz for automatic layout and connectors.
The SVGs include embedded draw.io XML in the content attribute so they can be
opened and edited in draw.io or the VS Code draw.io extension."""
import os
import re
import html
import graphviz


BG = "#1a1a2e"
FONT = "Segoe UI,Helvetica,Arial,sans-serif"


class DiagramBuilder:
    """Wraps graphviz.Digraph and tracks nodes/edges to generate draw.io XML."""

    def __init__(self, name, direction="LR", engine="dot", **kwargs):
        self.g = graphviz.Digraph(name, format="svg", engine=engine)
        attrs = dict(rankdir=direction, bgcolor=BG, pad="0.4", margin="0",
                     fontname=FONT, fontcolor="#999999", fontsize="13",
                     style="rounded", nodesep="0.5", ranksep="0.6",
                     size="10,5!", ratio="fill")
        attrs.update(kwargs)
        self.g.attr(**attrs)
        self.g.attr("node", shape="box", style="filled,rounded,bold",
                    fontname=FONT, fontsize="13", fontcolor="white",
                    width="1.6", height="0.6", penwidth="2.5",
                    fillcolor="#0f3460", color="#333333")
        self.g.attr("edge", arrowsize="0.9", penwidth="2", fontname=FONT,
                    fontsize="11", fontcolor="#cccccc")
        self._cell_id = 1
        self._cells = ['<mxCell id="0" />', '<mxCell id="1" parent="0" />']
        self._node_map = {}  # graphviz id -> mxCell id
        self._clusters = []  # (graphviz_cluster_name, label, cid)

    def _next_id(self):
        self._cell_id += 1
        return str(self._cell_id)

    def cluster(self, name, label, color="#555555"):
        """Register a cluster for draw.io group tracking. Returns a graphviz subgraph context."""
        cid = self._next_id()
        gv_name = f"cluster_{name}"
        self._clusters.append((gv_name, label, cid))
        style = f"rounded=1;whiteSpace=wrap;html=1;fillColor=none;strokeColor={color};fontColor=#999999;fontSize=14;fontStyle=1;verticalAlign=top;spacingTop=5;dashed=1;strokeWidth=1.5;"
        lbl = html.escape(label)
        self._cells.append(
            f'<mxCell id="{cid}" value="{lbl}" style="{style}" vertex="1" parent="1">'
            f'<mxGeometry x="__X_{gv_name}__" y="__Y_{gv_name}__" width="__W_{gv_name}__" height="__H_{gv_name}__" as="geometry" /></mxCell>')
        return self.g.subgraph(name=gv_name)

    def node(self, nid, label, graph=None, **kwargs):
        target = graph if graph is not None else self.g
        target.node(nid, label, **kwargs)
        fill = kwargs.get("fillcolor", "#0f3460")
        stroke = kwargs.get("color", "#333333")
        shape = kwargs.get("shape", "box")
        cid = self._next_id()
        self._node_map[nid] = cid
        style = f"rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};fontColor=#ffffff;fontSize=13;fontStyle=1;"
        if shape == "diamond":
            style = f"rhombus;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};fontColor=#ffffff;fontSize=12;"
        lbl = html.escape(label.replace("\n", "<br>"))
        # Geometry placeholder — will be updated after Graphviz renders
        self._cells.append(
            f'<mxCell id="{cid}" value="{lbl}" style="{style}" vertex="1" parent="1">'
            f'<mxGeometry x="__X_{nid}__" y="__Y_{nid}__" width="__W_{nid}__" height="__H_{nid}__" as="geometry" /></mxCell>')

    def edge(self, src, tgt, **kwargs):
        self.g.edge(src, tgt, **kwargs)
        color = kwargs.get("color", "#888888")
        label = kwargs.get("label", "")
        cid = self._next_id()
        src_cid = self._node_map.get(src, "1")
        tgt_cid = self._node_map.get(tgt, "1")
        style = f"endArrow=block;endFill=1;strokeColor={color};strokeWidth=2;"
        lbl = html.escape(label)
        self._cells.append(
            f'<mxCell id="{cid}" value="{lbl}" style="{style}" edge="1" '
            f'source="{src_cid}" target="{tgt_cid}" parent="1">'
            f'<mxGeometry relative="1" as="geometry" /></mxCell>')

    def subgraph(self, **kwargs):
        return self.g.subgraph(**kwargs)

    def _parse_node_positions(self, svg_content):
        """Extract node and cluster bounding boxes from Graphviz SVG output."""
        import xml.etree.ElementTree as ET
        positions = {}
        clean = re.sub(r'<!DOCTYPE[^>]*>', '', svg_content)
        clean = re.sub(r'<\?xml[^>]*\?>', '', clean)
        try:
            root = ET.fromstring(clean)
        except ET.ParseError:
            return positions

        def _extract_bbox(g_elem):
            """Get bounding box from path or polygon in a <g> element."""
            for tag in ['path', 'polygon']:
                elem = g_elem.find(f'{{http://www.w3.org/2000/svg}}{tag}')
                if elem is not None:
                    attr = 'd' if tag == 'path' else 'points'
                    raw = elem.get(attr, '')
                    coords = [float(x) for x in re.findall(r'[-+]?\d*\.?\d+', raw)]
                    if len(coords) >= 4:
                        xs, ys = coords[0::2], coords[1::2]
                        return {
                            'x': round(min(xs), 1), 'y': round(min(ys), 1),
                            'w': round(max(xs) - min(xs), 1),
                            'h': round(max(ys) - min(ys), 1),
                        }
            return None

        for g_elem in root.iter('{http://www.w3.org/2000/svg}g'):
            cls = g_elem.get('class', '')
            if cls not in ('node', 'cluster'):
                continue
            title_elem = g_elem.find('{http://www.w3.org/2000/svg}title')
            if title_elem is None or not title_elem.text:
                continue
            nid = title_elem.text.strip()
            bbox = _extract_bbox(g_elem)
            if bbox:
                positions[nid] = bbox
        return positions

    def _build_drawio_xml(self, positions):
        cells_str = "".join(self._cells)
        # Replace geometry placeholders with actual positions
        for nid, pos in positions.items():
            cells_str = cells_str.replace(f'__X_{nid}__', str(pos['x']))
            cells_str = cells_str.replace(f'__Y_{nid}__', str(pos['y']))
            cells_str = cells_str.replace(f'__W_{nid}__', str(pos['w']))
            cells_str = cells_str.replace(f'__H_{nid}__', str(pos['h']))
        # Clean any remaining placeholders for nodes not found
        cells_str = re.sub(r'__[XYWH]_\w+__', '0', cells_str)
        return (f'<mxfile host="drawio-gen"><diagram name="Page-1" id="page1">'
                f'<mxGraphModel><root>{cells_str}</root></mxGraphModel>'
                f'</diagram></mxfile>')

    def save(self, outdir, name):
        path = os.path.join(outdir, name)
        self.g.render(path, cleanup=True)
        svg_path = path + ".svg"

        # Read rendered SVG, extract node positions, build draw.io XML
        svg_content = open(svg_path, "r", encoding="utf-8").read()
        positions = self._parse_node_positions(svg_content)
        drawio_xml = self._build_drawio_xml(positions)
        encoded = html.escape(drawio_xml, quote=True)

        # Inject content attr into <svg> tag
        svg_content = re.sub(
            r'<svg\b',
            f'<svg host="drawio-gen" content="{encoded}"',
            svg_content, count=1)

        with open(svg_path, "w", encoding="utf-8") as f:
            f.write(svg_content)
        print(f"Created: {svg_path}")


# ── Diagram 1: MITRE Cybersecurity Ecosystem ──
def diagram_01_ecosystem(outdir):
    b = DiagramBuilder("ecosystem")
    with b.cluster("offense", "Offense") as c:
        c.attr(label="Offense", style="dashed,rounded", color="#555555", fontcolor="#999999", penwidth="1.5")
        b.node("CVE", "CVE\nVulnerabilities", graph=c, fillcolor="#0f3460", color="#e67e22")
        b.node("CWE", "CWE\nWeaknesses", graph=c, fillcolor="#0f3460", color="#e67e22")
        b.node("CAPEC", "CAPEC\nAttack Patterns", graph=c, fillcolor="#0f3460", color="#e67e22")
    with b.cluster("core", "Core") as c:
        c.attr(label="Core", style="dashed,rounded", color="#555555", fontcolor="#999999", penwidth="1.5")
        b.node("ATTACK", "ATT&CK\nAdversary Behavior", graph=c, fillcolor="#0f3460", color="#e94560")
    with b.cluster("defense", "Defense") as c:
        c.attr(label="Defense", style="dashed,rounded", color="#555555", fontcolor="#999999", penwidth="1.5")
        b.node("D3FEND", "D3FEND\nCountermeasures", graph=c, fillcolor="#0f3460", color="#16a085")
        b.node("ATLAS", "ATLAS\nAI/ML Threats", graph=c, fillcolor="#0f3460", color="#9b59b6")
    b.edge("CWE", "CVE", color="#e67e22")
    b.edge("CWE", "CAPEC", color="#e67e22")
    b.edge("CAPEC", "ATTACK", color="#e94560")
    b.edge("CVE", "ATTACK", color="#e94560")
    b.edge("ATTACK", "D3FEND", color="#16a085")
    b.edge("ATTACK", "ATLAS", color="#9b59b6")
    b.save(outdir, "mitre-ecosystem.drawio")


# ── Diagram 2: 14 ATT&CK Tactics ──
def diagram_02_14tactics(outdir):
    b = DiagramBuilder("tactics", ranksep="0.4", nodesep="0.3")
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
        with b.cluster(label.replace(' ',''), label) as c:
            c.attr(label=label, style="dashed,rounded", color="#555555", fontcolor="#999999", penwidth="1.5")
            for i, (nid, nlabel) in enumerate(nodes):
                b.node(nid, nlabel, graph=c, fillcolor=color, color=color)
            for i in range(len(nodes) - 1):
                b.edge(nodes[i][0], nodes[i + 1][0], color=color)
        if prev_last:
            b.edge(prev_last, nodes[0][0], color="white", style="bold")
        prev_last = nodes[-1][0]
    b.save(outdir, "14-attack-tactics.drawio")


# ── Diagram 3: Attack Chain (Supply Chain) ──
def diagram_03_attack_chain(outdir):
    b = DiagramBuilder("attack_chain")
    nodes = [
        ("T1195", "T1195\nSupply Chain\nCompromise", "#e74c3c"),
        ("T1059", "T1059\nExecution", "#e67e22"),
        ("T1552", "T1552\nUnsecured\nCredentials", "#f39c12"),
        ("T1078", "T1078\nValid Accounts", "#2ecc71"),
        ("T1098", "T1098\nAccount\nManipulation", "#3498db"),
        ("T1567", "T1567\nExfiltration", "#9b59b6"),
    ]
    for nid, label, color in nodes:
        b.node(nid, label, fillcolor=color, color=color)
    for i in range(len(nodes) - 1):
        b.edge(nodes[i][0], nodes[i + 1][0], color="#cccccc")
    b.save(outdir, "attack-chain-supply.drawio")


# ── Diagram 4: Upload to Ransomware ──
def diagram_04_ransomware(outdir):
    b = DiagramBuilder("ransomware", direction="TB")
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
        b.node(nid, label, fillcolor=color, color=stroke)
    for i in range(len(nodes) - 1):
        b.edge(nodes[i][0], nodes[i + 1][0], color="#cccccc")
    b.save(outdir, "ransomware-chain.drawio")


# ── Diagram 5: Crooked Line ──
def diagram_05_crooked_line(outdir):
    b = DiagramBuilder("crooked", nodesep="0.3", ranksep="0.4")
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
        b.node(nid, label, fillcolor=color, color=stroke)
    b.edge("IA", "EX", color="#cccccc")
    b.edge("EX", "D1", color="#cccccc")
    b.edge("D1", "CA1", color="#cccccc")
    b.edge("CA1", "D1", color="#e94560", penwidth="3", constraint="false")
    b.edge("CA1", "LM1", color="#cccccc")
    b.edge("LM1", "D1", color="#e94560", penwidth="3", constraint="false")
    b.edge("LM1", "D2", color="#cccccc")
    b.edge("D2", "CA2", color="#cccccc")
    b.edge("CA2", "LM2", color="#cccccc")
    b.edge("LM2", "COL", color="#cccccc")
    b.edge("COL", "XF", color="#cccccc")
    b.save(outdir, "crooked-line.drawio")


# ── Diagram 6: Immutable Logging ──
def diagram_06_immutable_logging(outdir):
    b = DiagramBuilder("logging")
    b.node("APP", "Application", fillcolor="#2c3e50", color="#3498db")
    b.node("LOG", "Secure Logger", fillcolor="#27ae60", color="#2ecc71")
    b.node("HASH", "Hash\nValidation", fillcolor="#2980b9", color="#3498db")
    b.node("BUF", "Local Buffer", fillcolor="#8e44ad", color="#9b59b6")
    b.node("ENC", "Encrypted\nStorage", fillcolor="#d35400", color="#e67e22")
    b.node("SIEM", "External\nSIEM", fillcolor="#d35400", color="#e67e22")
    b.node("TAMP", "Tamper\nDetection", fillcolor="#c0392b", color="#e74c3c")
    b.node("ALERT", "Alert\nSecurity Team", fillcolor="#e74c3c", color="#c0392b")
    b.edge("APP", "LOG", color="#3498db")
    b.edge("LOG", "HASH", color="#2ecc71")
    b.edge("HASH", "BUF", color="#3498db")
    b.edge("BUF", "ENC", color="#9b59b6")
    b.edge("BUF", "SIEM", color="#9b59b6")
    b.edge("ENC", "TAMP", color="#e67e22")
    b.edge("SIEM", "TAMP", color="#e67e22")
    b.edge("TAMP", "ALERT", color="#e74c3c")
    b.save(outdir, "immutable-logging.drawio")


# ── Diagram 7: Supply Chain Security Flow ──
def diagram_07_supply_chain(outdir):
    b = DiagramBuilder("supplychain", direction="TB")
    b.node("DEV", "Developer", fillcolor="#2c3e50", color="#3498db")
    b.node("DEP", "Dependency\nRequest", fillcolor="#2980b9", color="#3498db")
    b.node("REG", "Package\nRegistry", fillcolor="#8e44ad", color="#9b59b6", shape="diamond")
    b.node("INT", "Integrity\nCheck", fillcolor="#d35400", color="#e67e22")
    b.node("HASH", "Hash Valid?", fillcolor="#f39c12", color="#e67e22", shape="diamond")
    b.node("BLOCK", "Block & Log\nT1195.001", fillcolor="#e74c3c", color="#c0392b")
    b.node("VULN", "Vulnerability\nScan", fillcolor="#27ae60", color="#2ecc71")
    b.node("CLEAN", "Clean?", fillcolor="#f39c12", color="#e67e22", shape="diamond")
    b.node("INST", "Install &\nMonitor", fillcolor="#16a085", color="#1abc9c")
    b.edge("DEV", "DEP", color="#3498db")
    b.edge("DEP", "REG", color="#3498db")
    b.edge("REG", "INT", color="#9b59b6")
    b.edge("INT", "HASH", color="#e67e22")
    b.edge("HASH", "BLOCK", label="No", color="#e74c3c")
    b.edge("HASH", "VULN", label="Yes", color="#2ecc71")
    b.edge("VULN", "CLEAN", color="#2ecc71")
    b.edge("CLEAN", "BLOCK", label="No", color="#e74c3c")
    b.edge("CLEAN", "INST", label="Yes", color="#1abc9c")
    b.save(outdir, "supply-chain-flow.drawio")


# ── Diagram 8: Data Flow Monitoring ──
def diagram_08_data_flow(outdir):
    b = DiagramBuilder("dataflow", direction="TB")
    b.node("REQ", "User Request", fillcolor="#2c3e50", color="#3498db")
    b.node("AUTH", "Auth &\nAuthorization", fillcolor="#2980b9", color="#3498db")
    b.node("MON", "Data Access\nMonitor", fillcolor="#8e44ad", color="#9b59b6")
    b.node("ANOM", "Anomaly?", fillcolor="#f39c12", color="#e67e22", shape="diamond")
    b.node("ALERT", "Alert & Block", fillcolor="#e74c3c", color="#c0392b")
    b.node("QUERY", "Execute Query", fillcolor="#27ae60", color="#2ecc71")
    b.node("BULK", "Bulk Transfer?", fillcolor="#f39c12", color="#e67e22", shape="diamond")
    b.node("RATE", "Rate\nExceeded?", fillcolor="#f39c12", color="#e67e22", shape="diamond")
    b.node("RESP", "Send Response", fillcolor="#16a085", color="#1abc9c")
    b.edge("REQ", "AUTH", color="#3498db")
    b.edge("AUTH", "MON", color="#3498db")
    b.edge("MON", "ANOM", color="#9b59b6")
    b.edge("ANOM", "ALERT", label="Yes", color="#e74c3c")
    b.edge("ANOM", "QUERY", label="No", color="#2ecc71")
    b.edge("QUERY", "BULK", color="#2ecc71")
    b.edge("BULK", "ALERT", label="Yes", color="#e74c3c")
    b.edge("BULK", "RATE", label="No", color="#2ecc71")
    b.edge("RATE", "ALERT", label="Yes", color="#e74c3c")
    b.edge("RATE", "RESP", label="No", color="#1abc9c")
    b.save(outdir, "data-flow-monitoring.drawio")


# ── Diagram 9: Threat Modeling Cycle ──
def diagram_09_threat_modeling(outdir):
    b = DiagramBuilder("threat_model", engine="circo", mindist="2.0")
    b.g.attr("node", width="1.8", height="0.7")
    items = [
        ("ID", "Identify\nFeature", "#2c3e50", "#3498db"),
        ("MAP", "Map to ATT&CK\nTechniques", "#2980b9", "#3498db"),
        ("ASSESS", "Assess Risk\n& Impact", "#d35400", "#e67e22"),
        ("DESIGN", "Design\nDetections", "#8e44ad", "#9b59b6"),
        ("IMPL", "Implement\n& Monitor", "#27ae60", "#2ecc71"),
        ("TEST", "Test &\nIterate", "#e74c3c", "#c0392b"),
    ]
    for nid, label, fill, stroke in items:
        b.node(nid, label, fillcolor=fill, color=stroke)
    colors = ["#3498db", "#3498db", "#e67e22", "#9b59b6", "#2ecc71", "#e74c3c"]
    for i in range(len(items)):
        b.edge(items[i][0], items[(i + 1) % len(items)][0], color=colors[i])
    b.save(outdir, "threat-modeling-cycle.drawio")


# ── Diagram 10: Defense in Depth ──
def diagram_10_defense_depth(outdir):
    b = DiagramBuilder("defense", direction="TB", ranksep="0.4")
    with b.cluster("prevent", "Prevention") as c:
        c.attr(label="Prevention", style="dashed,rounded", color="#555555", fontcolor="#999999", penwidth="1.5")
        b.node("IV", "Input\nValidation", graph=c, fillcolor="#27ae60", color="#2ecc71")
        b.node("AUTHN", "Authentication", graph=c, fillcolor="#2980b9", color="#3498db")
        b.node("AUTHZ", "Authorization", graph=c, fillcolor="#8e44ad", color="#9b59b6")
        b.node("DAC", "Data Access\nControls", graph=c, fillcolor="#d35400", color="#e67e22")
    with b.cluster("detect", "Detection") as c:
        c.attr(label="Detection", style="dashed,rounded", color="#555555", fontcolor="#999999", penwidth="1.5")
        b.node("BA", "Behavioral\nAnalytics", graph=c, fillcolor="#c0392b", color="#e74c3c")
        b.node("AD", "Anomaly\nDetection", graph=c, fillcolor="#e74c3c", color="#c0392b")
        b.node("TI", "Threat\nIntelligence", graph=c, fillcolor="#f39c12", color="#e67e22")
    with b.cluster("respond", "Response") as c:
        c.attr(label="Response", style="dashed,rounded", color="#555555", fontcolor="#999999", penwidth="1.5")
        b.node("AB", "Automated\nBlocking", graph=c, fillcolor="#2c3e50", color="#3498db")
        b.node("AR", "Alert &\nRemediation", graph=c, fillcolor="#1a1a2e", color="#e94560")
    edges = [("IV","AUTHN"),("AUTHN","AUTHZ"),("AUTHZ","DAC"),
             ("DAC","BA"),("BA","AD"),("AD","TI"),("TI","AB"),("AB","AR")]
    for s, t in edges:
        b.edge(s, t, color="#cccccc")
    b.save(outdir, "defense-in-depth.drawio")


# ── Diagram 11: OWASP + ATT&CK Integration ──
def diagram_11_owasp_integration(outdir):
    b = DiagramBuilder("owasp", ranksep="0.6")
    # Practices
    b.node("SC", "Secure Coding", fillcolor="#27ae60", color="#2ecc71")
    b.node("BM", "Behavioral\nMonitoring", fillcolor="#2980b9", color="#3498db")
    b.node("VT", "Vulnerability\nTesting", fillcolor="#d35400", color="#e67e22")
    b.node("TC", "Technique\nCorrelation", fillcolor="#8e44ad", color="#9b59b6")
    b.node("SR", "Security\nReviews", fillcolor="#c0392b", color="#e74c3c")
    b.node("TH", "Threat\nHunting", fillcolor="#e74c3c", color="#c0392b")
    # Outcomes
    b.node("SBD", "Secure\nby Design", fillcolor="#16a085", color="#1abc9c")
    b.node("MBB", "Monitor\nby Behavior", fillcolor="#16a085", color="#1abc9c")
    b.node("RBI", "Respond by\nIntelligence", fillcolor="#16a085", color="#1abc9c")
    b.edge("SC", "SBD", color="#2ecc71")
    b.edge("BM", "SBD", color="#3498db")
    b.edge("VT", "MBB", color="#e67e22")
    b.edge("TC", "MBB", color="#9b59b6")
    b.edge("SR", "RBI", color="#e74c3c")
    b.edge("TH", "RBI", color="#c0392b")
    b.edge("SBD", "MBB", color="#1abc9c")
    b.edge("MBB", "RBI", color="#1abc9c")
    b.save(outdir, "owasp-attack-integration.drawio")


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
