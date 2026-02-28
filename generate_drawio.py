"""Generate .drawio.svg files with rendered SVG for all diagrams in Slides.md"""
import html
import math


class DrawioBuilder:
    def __init__(self, bg="#1a1a2e"):
        self._id = 1
        self.bg = bg
        self.nodes = {}
        self.groups = {}
        self.edges = []

    def _next_id(self):
        self._id += 1
        return str(self._id)

    def add_node(self, label, x, y, w=160, h=60, fill="#0f3460", stroke="#333333",
                 font_color="#ffffff", rounded=True, shape=None):
        nid = self._next_id()
        self.nodes[nid] = dict(label=label, x=x, y=y, w=w, h=h, fill=fill,
                               stroke=stroke, font_color=font_color, rounded=rounded, shape=shape)
        return nid

    def add_group(self, label, x, y, w, h, fill="#1a1a2e", stroke="#444444", font_color="#999999"):
        gid = self._next_id()
        self.groups[gid] = dict(label=label, x=x, y=y, w=w, h=h, fill=fill,
                                stroke=stroke, font_color=font_color)
        return gid

    def add_edge(self, src, tgt, label="", color="#888888", dashed=False, thick=False):
        self.edges.append(dict(src=src, tgt=tgt, label=label, color=color,
                               dashed=dashed, thick=thick))

    def _center(self, nid):
        n = self.nodes[nid]
        return n['x'] + n['w'] / 2, n['y'] + n['h'] / 2

    def _edge_points(self, src_id, tgt_id):
        sx, sy = self._center(src_id)
        tx, ty = self._center(tgt_id)
        s, t = self.nodes[src_id], self.nodes[tgt_id]
        dx, dy = tx - sx, ty - sy
        dist = math.hypot(dx, dy) or 1
        ndx, ndy = dx / dist, dy / dist
        # Source exit
        if abs(ndx) * s['h'] > abs(ndy) * s['w']:
            r = (s['w'] / 2) / abs(ndx) if ndx else 0
        else:
            r = (s['h'] / 2) / abs(ndy) if ndy else 0
        x1, y1 = sx + ndx * r, sy + ndy * r
        # Target entry
        nx2, ny2 = -ndx, -ndy
        if abs(nx2) * t['h'] > abs(ny2) * t['w']:
            r2 = (t['w'] / 2) / abs(nx2) if nx2 else 0
        else:
            r2 = (t['h'] / 2) / abs(ny2) if ny2 else 0
        x2, y2 = tx + nx2 * r2, ty + ny2 * r2
        return x1, y1, x2, y2

    def _render(self):
        parts = []
        marker_colors = set()

        # Groups (behind everything)
        for g in self.groups.values():
            parts.append(
                f'  <rect x="{g["x"]}" y="{g["y"]}" width="{g["w"]}" height="{g["h"]}" '
                f'rx="10" ry="10" fill="{g["fill"]}" fill-opacity="0.5" '
                f'stroke="{g["stroke"]}" stroke-width="1.5" stroke-dasharray="8,4" />')
            parts.append(
                f'  <text x="{g["x"] + g["w"]/2}" y="{g["y"] + 22}" text-anchor="middle" '
                f'font-family="Segoe UI,Helvetica,Arial,sans-serif" font-size="13" '
                f'font-weight="600" fill="{g["font_color"]}" letter-spacing="0.5">'
                f'{html.escape(g["label"])}</text>')

        # Edges
        for e in self.edges:
            marker_colors.add(e['color'])
            sw = 3 if e['thick'] else 2
            dash = ' stroke-dasharray="8,4"' if e['dashed'] else ''
            x1, y1, x2, y2 = self._edge_points(e['src'], e['tgt'])
            dx, dy = x2 - x1, y2 - y1
            d = math.hypot(dx, dy) or 1
            x2a, y2a = x2 - (dx / d) * 10, y2 - (dy / d) * 10
            mid = f'ah{e["color"][1:]}'
            parts.append(
                f'  <line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2a:.1f}" y2="{y2a:.1f}" '
                f'stroke="{e["color"]}" stroke-width="{sw}" stroke-linecap="round"{dash} '
                f'marker-end="url(#{mid})" />')
            if e['label']:
                mx, my = (x1 + x2) / 2, (y1 + y2) / 2
                # Label background pill
                parts.append(
                    f'  <rect x="{mx - 16}" y="{my - 14}" width="32" height="18" rx="9" '
                    f'fill="{self.bg}" fill-opacity="0.85" />')
                parts.append(
                    f'  <text x="{mx:.1f}" y="{my - 2:.1f}" text-anchor="middle" '
                    f'font-family="Segoe UI,Helvetica,Arial,sans-serif" font-size="11" '
                    f'font-weight="700" fill="{e["color"]}">{html.escape(e["label"])}</text>')

        # Nodes
        for n in self.nodes.values():
            cx, cy = n['x'] + n['w'] / 2, n['y'] + n['h'] / 2
            if n['shape'] == 'diamond':
                pts = f"{cx},{n['y']} {n['x']+n['w']},{cy} {cx},{n['y']+n['h']} {n['x']},{cy}"
                # shadow
                pts_s = f"{cx},{n['y']+3} {n['x']+n['w']+2},{cy+3} {cx},{n['y']+n['h']+3} {n['x']-2},{cy+3}"
                parts.append(f'  <polygon points="{pts_s}" fill="black" fill-opacity="0.3" />')
                parts.append(
                    f'  <polygon points="{pts}" fill="{n["fill"]}" '
                    f'stroke="{n["stroke"]}" stroke-width="2.5" />')
            else:
                rx = "10" if n['rounded'] else "2"
                # Drop shadow
                parts.append(
                    f'  <rect x="{n["x"]+2}" y="{n["y"]+3}" width="{n["w"]}" height="{n["h"]}" '
                    f'rx="{rx}" ry="{rx}" fill="black" fill-opacity="0.25" />')
                parts.append(
                    f'  <rect x="{n["x"]}" y="{n["y"]}" width="{n["w"]}" height="{n["h"]}" '
                    f'rx="{rx}" ry="{rx}" fill="{n["fill"]}" '
                    f'stroke="{n["stroke"]}" stroke-width="2.5" />')
            # Text
            label = n['label'].replace('&amp;', '&')
            lines = label.split('\n')
            line_h = 17
            total = len(lines) * line_h
            sy = cy - total / 2 + 13
            for i, ln in enumerate(lines):
                parts.append(
                    f'  <text x="{cx}" y="{sy + i * line_h}" text-anchor="middle" '
                    f'font-family="Segoe UI,Helvetica,Arial,sans-serif" font-size="13" '
                    f'font-weight="700" fill="{n["font_color"]}">'
                    f'{html.escape(ln)}</text>')

        return parts, marker_colors

    def save_as_drawio_svg(self, path):
        all_items = list(self.nodes.values()) + list(self.groups.values())
        pad = 25
        min_x = min(n['x'] for n in all_items) - pad
        min_y = min(n['y'] for n in all_items) - pad
        max_x = max(n['x'] + n['w'] for n in all_items) + pad
        max_y = max(n['y'] + n['h'] for n in all_items) + pad
        vw, vh = max_x - min_x, max_y - min_y

        shapes, marker_colors = self._render()

        defs = []
        for c in marker_colors:
            mid = f'ah{c[1:]}'
            defs.append(
                f'    <marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" '
                f'markerWidth="7" markerHeight="7" orient="auto-start-auto">'
                f'<path d="M 0 1 L 8 5 L 0 9 z" fill="{c}" /></marker>')

        svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" version="1.1"
     width="{vw}" height="{vh}" viewBox="{min_x} {min_y} {vw} {vh}">
  <defs>
{chr(10).join(defs)}
  </defs>
  <rect x="{min_x}" y="{min_y}" width="{vw}" height="{vh}" fill="{self.bg}" rx="12" ry="12" />
{chr(10).join(shapes)}
</svg>'''
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg)


def diagram_01_ecosystem():
    b = DrawioBuilder()
    # Offense group
    b.add_group("Offense", 20, 20, 200, 260)
    cve = b.add_node("CVE\nVulnerabilities", 40, 60, 160, 60, fill="#0f3460", stroke="#e67e22")
    cwe = b.add_node("CWE\nWeaknesses", 40, 140, 160, 60, fill="#0f3460", stroke="#e67e22")
    capec = b.add_node("CAPEC\nAttack Patterns", 40, 220, 160, 60, fill="#0f3460", stroke="#e67e22")
    # Core group
    b.add_group("Core", 320, 80, 200, 140)
    attack = b.add_node("ATT&amp;CK\nAdversary Behavior", 340, 120, 160, 60, fill="#0f3460", stroke="#e94560")
    # Defense group
    b.add_group("Defense", 620, 20, 200, 260)
    d3fend = b.add_node("D3FEND\nCountermeasures", 640, 80, 160, 60, fill="#0f3460", stroke="#16a085")
    atlas = b.add_node("ATLAS\nAI/ML Threats", 640, 200, 160, 60, fill="#0f3460", stroke="#9b59b6")
    # Edges
    b.add_edge(cwe, cve, color="#e67e22")
    b.add_edge(cwe, capec, color="#e67e22")
    b.add_edge(capec, attack, color="#e94560")
    b.add_edge(cve, attack, color="#e94560")
    b.add_edge(attack, d3fend, color="#16a085")
    b.add_edge(attack, atlas, color="#9b59b6")
    return b

def diagram_02_14tactics():
    b = DrawioBuilder()
    # Pre-Attack
    b.add_group("Pre-Attack", 20, 20, 300, 100)
    a = b.add_node("Reconnaissance", 40, 40, 120, 60, fill="#2c3e50", stroke="#3498db")
    br = b.add_node("Resource\nDevelopment", 180, 40, 120, 60, fill="#2c3e50", stroke="#3498db")
    # Get In
    b.add_group("Get In", 340, 20, 540, 100)
    c = b.add_node("Initial\nAccess", 360, 40, 110, 60, fill="#c0392b", stroke="#e74c3c")
    d = b.add_node("Execution", 490, 40, 110, 60, fill="#c0392b", stroke="#e74c3c")
    e = b.add_node("Persistence", 620, 40, 110, 60, fill="#c0392b", stroke="#e74c3c")
    f = b.add_node("Privilege\nEscalation", 750, 40, 110, 60, fill="#c0392b", stroke="#e74c3c")
    # Stay In
    b.add_group("Stay In", 20, 150, 540, 100)
    g = b.add_node("Defense\nEvasion", 40, 170, 110, 60, fill="#d35400", stroke="#e67e22")
    h = b.add_node("Credential\nAccess", 170, 170, 110, 60, fill="#d35400", stroke="#e67e22")
    i = b.add_node("Discovery", 300, 170, 110, 60, fill="#d35400", stroke="#e67e22")
    j = b.add_node("Lateral\nMovement", 430, 170, 110, 60, fill="#d35400", stroke="#e67e22")
    # Act
    b.add_group("Act", 580, 150, 540, 100)
    k = b.add_node("Collection", 600, 170, 110, 60, fill="#8e44ad", stroke="#9b59b6")
    l = b.add_node("Command &amp;\nControl", 730, 170, 110, 60, fill="#8e44ad", stroke="#9b59b6")
    m = b.add_node("Exfiltration", 860, 170, 110, 60, fill="#8e44ad", stroke="#9b59b6")
    n = b.add_node("Impact", 990, 170, 110, 60, fill="#8e44ad", stroke="#9b59b6")
    # Edges
    b.add_edge(a, br, color="#3498db")
    b.add_edge(c, d, color="#e74c3c")
    b.add_edge(d, e, color="#e74c3c")
    b.add_edge(e, f, color="#e74c3c")
    b.add_edge(g, h, color="#e67e22")
    b.add_edge(h, i, color="#e67e22")
    b.add_edge(i, j, color="#e67e22")
    b.add_edge(k, l, color="#9b59b6")
    b.add_edge(l, m, color="#9b59b6")
    b.add_edge(m, n, color="#9b59b6")
    b.add_edge(br, c, color="#ffffff")
    b.add_edge(f, g, color="#ffffff")
    b.add_edge(j, k, color="#ffffff")
    return b

def diagram_03_attack_chain():
    b = DrawioBuilder()
    sx = 20
    nodes = [
        ("T1195\nSupply Chain\nCompromise", "#e74c3c", "#c0392b"),
        ("T1059\nExecution", "#e67e22", "#d35400"),
        ("T1552\nUnsecured\nCredentials", "#f39c12", "#e67e22"),
        ("T1078\nValid Accounts", "#2ecc71", "#27ae60"),
        ("T1098\nAccount\nManipulation", "#3498db", "#2980b9"),
        ("T1567\nExfiltration", "#9b59b6", "#8e44ad"),
    ]
    nids = []
    for i, (label, fill, stroke) in enumerate(nodes):
        nid = b.add_node(label, sx + i * 170, 60, 150, 70, fill=fill, stroke=stroke)
        nids.append(nid)
    for i in range(len(nids) - 1):
        b.add_edge(nids[i], nids[i + 1], color="#cccccc")
    return b

def diagram_04_ransomware_chain():
    b = DrawioBuilder()
    nodes = [
        ("T1190\nUnrestricted\nFile Upload", "#e74c3c", "#c0392b"),
        ("T1505.003\nWeb Shell\nDeployed", "#e74c3c", "#c0392b"),
        ("T1059\nRemote Command\nExecution", "#e67e22", "#d35400"),
        ("T1552\nExtract DB\nCredentials", "#f39c12", "#e67e22"),
        ("T1078\nDirect Database\nAccess", "#2ecc71", "#27ae60"),
        ("T1565\nData\nManipulation", "#9b59b6", "#8e44ad"),
        ("T1485\nRansomware\nDeployment", "#1a1a2e", "#e94560"),
    ]
    nids = []
    cx = 350
    for i, (label, fill, stroke) in enumerate(nodes):
        nid = b.add_node(label, cx, 20 + i * 90, 160, 70, fill=fill, stroke=stroke)
        nids.append(nid)
    for i in range(len(nids) - 1):
        b.add_edge(nids[i], nids[i + 1], color="#cccccc")
    return b

def diagram_05_crooked_line():
    b = DrawioBuilder()
    nodes_data = [
        ("Initial\nAccess", 20, 100, "#e74c3c", "#c0392b"),
        ("Execution", 200, 100, "#e67e22", "#d35400"),
        ("Discovery", 380, 100, "#3498db", "#2980b9"),
        ("Credential\nAccess", 560, 100, "#f39c12", "#e67e22"),
        ("Lateral\nMovement", 740, 100, "#2ecc71", "#27ae60"),
        ("Discovery\n(new segment)", 380, 250, "#3498db", "#2980b9"),
        ("Credential\nAccess", 560, 250, "#f39c12", "#e67e22"),
        ("Lateral\nMovement", 740, 250, "#2ecc71", "#27ae60"),
        ("Collection", 920, 250, "#9b59b6", "#8e44ad"),
        ("Exfiltration", 1100, 250, "#1a1a2e", "#e94560"),
    ]
    nids = []
    for label, x, y, fill, stroke in nodes_data:
        nid = b.add_node(label, x, y, 150, 60, fill=fill, stroke=stroke)
        nids.append(nid)
    # Linear connections
    b.add_edge(nids[0], nids[1], color="#cccccc")
    b.add_edge(nids[1], nids[2], color="#cccccc")
    b.add_edge(nids[2], nids[3], color="#cccccc")
    b.add_edge(nids[4], nids[5], color="#cccccc")
    b.add_edge(nids[5], nids[6], color="#cccccc")
    b.add_edge(nids[6], nids[7], color="#cccccc")
    b.add_edge(nids[7], nids[8], color="#cccccc")
    b.add_edge(nids[8], nids[9], color="#cccccc")
    # Loop-back edges (the "crooked" part)
    b.add_edge(nids[3], nids[2], color="#e94560", thick=True)  # Credential Access -> Discovery
    b.add_edge(nids[3], nids[4], color="#cccccc")  # Credential Access -> Lateral Movement
    b.add_edge(nids[4], nids[2], color="#e94560", thick=True)  # Lateral Movement -> Discovery (loop)
    return b

def diagram_06_immutable_logging():
    b = DrawioBuilder()
    app = b.add_node("Application", 20, 120, 140, 60, fill="#2c3e50", stroke="#3498db")
    logger = b.add_node("Secure Logger", 200, 120, 140, 60, fill="#27ae60", stroke="#2ecc71")
    hashv = b.add_node("Hash\nValidation", 380, 120, 140, 60, fill="#2980b9", stroke="#3498db")
    buf = b.add_node("Local Buffer", 560, 120, 140, 60, fill="#8e44ad", stroke="#9b59b6")
    enc = b.add_node("Encrypted\nStorage", 740, 40, 140, 60, fill="#d35400", stroke="#e67e22")
    siem = b.add_node("External\nSIEM", 740, 200, 140, 60, fill="#d35400", stroke="#e67e22")
    tamper = b.add_node("Tamper\nDetection", 920, 120, 140, 60, fill="#c0392b", stroke="#e74c3c")
    alert = b.add_node("Alert\nSecurity Team", 1100, 120, 140, 60, fill="#e74c3c", stroke="#c0392b")
    b.add_edge(app, logger, color="#3498db")
    b.add_edge(logger, hashv, color="#2ecc71")
    b.add_edge(hashv, buf, color="#3498db")
    b.add_edge(buf, enc, color="#9b59b6")
    b.add_edge(buf, siem, color="#9b59b6")
    b.add_edge(enc, tamper, color="#e67e22")
    b.add_edge(siem, tamper, color="#e67e22")
    b.add_edge(tamper, alert, color="#e74c3c")
    return b

def diagram_07_supply_chain_flow():
    b = DrawioBuilder()
    cx = 350
    dev = b.add_node("Developer", cx, 20, 160, 50, fill="#2c3e50", stroke="#3498db")
    dep = b.add_node("Dependency\nRequest", cx, 100, 160, 50, fill="#2980b9", stroke="#3498db")
    reg = b.add_node("Package\nRegistry", cx, 180, 160, 60, fill="#8e44ad", stroke="#9b59b6", shape="diamond")
    integ = b.add_node("Integrity\nCheck", cx, 270, 160, 50, fill="#d35400", stroke="#e67e22")
    hashq = b.add_node("Hash Valid?", cx, 350, 160, 60, fill="#f39c12", stroke="#e67e22", shape="diamond")
    block = b.add_node("Block &amp; Log\nT1195.001", 100, 350, 160, 50, fill="#e74c3c", stroke="#c0392b")
    vuln = b.add_node("Vulnerability\nScan", cx, 440, 160, 50, fill="#27ae60", stroke="#2ecc71")
    clean = b.add_node("Clean?", cx, 520, 160, 60, fill="#f39c12", stroke="#e67e22", shape="diamond")
    install = b.add_node("Install &amp;\nMonitor", cx, 610, 160, 50, fill="#16a085", stroke="#1abc9c")
    b.add_edge(dev, dep, color="#3498db")
    b.add_edge(dep, reg, color="#3498db")
    b.add_edge(reg, integ, color="#9b59b6")
    b.add_edge(integ, hashq, color="#e67e22")
    b.add_edge(hashq, block, label="No", color="#e74c3c")
    b.add_edge(hashq, vuln, label="Yes", color="#2ecc71")
    b.add_edge(vuln, clean, color="#2ecc71")
    b.add_edge(clean, block, label="No", color="#e74c3c")
    b.add_edge(clean, install, label="Yes", color="#1abc9c")
    return b

def diagram_08_data_flow():
    b = DrawioBuilder()
    cx = 350
    req = b.add_node("User Request", cx, 20, 160, 50, fill="#2c3e50", stroke="#3498db")
    auth = b.add_node("Auth &amp;\nAuthorization", cx, 100, 160, 50, fill="#2980b9", stroke="#3498db")
    monitor = b.add_node("Data Access\nMonitor", cx, 180, 160, 50, fill="#8e44ad", stroke="#9b59b6")
    anomaly = b.add_node("Anomaly?", cx, 260, 160, 60, fill="#f39c12", stroke="#e67e22", shape="diamond")
    alert = b.add_node("Alert &amp; Block", 100, 260, 160, 50, fill="#e74c3c", stroke="#c0392b")
    query = b.add_node("Execute Query", cx, 350, 160, 50, fill="#27ae60", stroke="#2ecc71")
    bulk = b.add_node("Bulk Transfer?", cx, 430, 160, 60, fill="#f39c12", stroke="#e67e22", shape="diamond")
    rate = b.add_node("Rate\nExceeded?", cx, 520, 160, 60, fill="#f39c12", stroke="#e67e22", shape="diamond")
    resp = b.add_node("Send Response", cx, 610, 160, 50, fill="#16a085", stroke="#1abc9c")
    b.add_edge(req, auth, color="#3498db")
    b.add_edge(auth, monitor, color="#3498db")
    b.add_edge(monitor, anomaly, color="#9b59b6")
    b.add_edge(anomaly, alert, label="Yes", color="#e74c3c")
    b.add_edge(anomaly, query, label="No", color="#2ecc71")
    b.add_edge(query, bulk, color="#2ecc71")
    b.add_edge(bulk, alert, label="Yes", color="#e74c3c")
    b.add_edge(bulk, rate, label="No", color="#2ecc71")
    b.add_edge(rate, alert, label="Yes", color="#e74c3c")
    b.add_edge(rate, resp, label="No", color="#1abc9c")
    return b

def diagram_09_threat_modeling():
    b = DrawioBuilder()
    cx = 350
    ident = b.add_node("Identify Feature", cx, 20, 180, 50, fill="#2c3e50", stroke="#3498db")
    mapn = b.add_node("Map to ATT&amp;CK\nTechniques", cx, 100, 180, 55, fill="#2980b9", stroke="#3498db")
    assess = b.add_node("Assess Risk\n&amp; Impact", cx, 185, 180, 55, fill="#d35400", stroke="#e67e22")
    design = b.add_node("Design\nDetections", cx, 270, 180, 55, fill="#8e44ad", stroke="#9b59b6")
    impl = b.add_node("Implement\n&amp; Monitor", cx, 355, 180, 55, fill="#27ae60", stroke="#2ecc71")
    test = b.add_node("Test &amp;\nIterate", cx, 440, 180, 55, fill="#e74c3c", stroke="#c0392b")
    b.add_edge(ident, mapn, color="#3498db")
    b.add_edge(mapn, assess, color="#3498db")
    b.add_edge(assess, design, color="#e67e22")
    b.add_edge(design, impl, color="#9b59b6")
    b.add_edge(impl, test, color="#2ecc71")
    b.add_edge(test, mapn, color="#e74c3c")  # cycle back
    return b

def diagram_10_defense_depth():
    b = DrawioBuilder()
    nodes = [
        ("Input\nValidation", "#27ae60", "#2ecc71"),
        ("Authentication", "#2980b9", "#3498db"),
        ("Authorization", "#8e44ad", "#9b59b6"),
        ("Data Access\nControls", "#d35400", "#e67e22"),
        ("Behavioral\nAnalytics", "#c0392b", "#e74c3c"),
        ("Anomaly\nDetection", "#e74c3c", "#c0392b"),
        ("Threat\nIntelligence", "#f39c12", "#e67e22"),
        ("Automated\nBlocking", "#2c3e50", "#3498db"),
        ("Alert &amp;\nRemediation", "#1a1a2e", "#e94560"),
    ]
    # Prevention | Detection | Response labels
    b.add_group("Prevention", 15, 10, 600, 110)
    b.add_group("Detection", 635, 10, 460, 110)
    b.add_group("Response", 1115, 10, 310, 110)
    nids = []
    for i, (label, fill, stroke) in enumerate(nodes):
        nid = b.add_node(label, 30 + i * 155, 40, 135, 60, fill=fill, stroke=stroke)
        nids.append(nid)
    for i in range(len(nids) - 1):
        b.add_edge(nids[i], nids[i + 1], color="#cccccc")
    return b

def diagram_11_owasp_integration():
    b = DrawioBuilder()
    # Left column - practices
    sc = b.add_node("Secure Coding", 20, 40, 150, 50, fill="#27ae60", stroke="#2ecc71")
    bm = b.add_node("Behavioral\nMonitoring", 20, 120, 150, 50, fill="#2980b9", stroke="#3498db")
    vt = b.add_node("Vulnerability\nTesting", 20, 200, 150, 50, fill="#d35400", stroke="#e67e22")
    tc = b.add_node("Technique\nCorrelation", 20, 280, 150, 50, fill="#8e44ad", stroke="#9b59b6")
    sr = b.add_node("Security\nReviews", 20, 360, 150, 50, fill="#c0392b", stroke="#e74c3c")
    th = b.add_node("Threat\nHunting", 20, 440, 150, 50, fill="#e74c3c", stroke="#c0392b")
    # Right column - outcomes
    sbd = b.add_node("Secure\nby Design", 350, 80, 170, 55, fill="#16a085", stroke="#1abc9c")
    mbb = b.add_node("Monitor\nby Behavior", 350, 240, 170, 55, fill="#16a085", stroke="#1abc9c")
    rbi = b.add_node("Respond by\nIntelligence", 350, 400, 170, 55, fill="#16a085", stroke="#1abc9c")
    # Practice -> outcome edges
    b.add_edge(sc, sbd, color="#2ecc71")
    b.add_edge(bm, sbd, color="#3498db")
    b.add_edge(vt, mbb, color="#e67e22")
    b.add_edge(tc, mbb, color="#9b59b6")
    b.add_edge(sr, rbi, color="#e74c3c")
    b.add_edge(th, rbi, color="#c0392b")
    # Chain outcomes
    b.add_edge(sbd, mbb, color="#1abc9c")
    b.add_edge(mbb, rbi, color="#1abc9c")
    return b


if __name__ == "__main__":
    import os
    outdir = os.path.join("slides", "img")
    os.makedirs(outdir, exist_ok=True)

    diagrams = {
        "mitre-ecosystem": diagram_01_ecosystem,
        "14-attack-tactics": diagram_02_14tactics,
        "attack-chain-supply": diagram_03_attack_chain,
        "ransomware-chain": diagram_04_ransomware_chain,
        "crooked-line": diagram_05_crooked_line,
        "immutable-logging": diagram_06_immutable_logging,
        "supply-chain-flow": diagram_07_supply_chain_flow,
        "data-flow-monitoring": diagram_08_data_flow,
        "threat-modeling-cycle": diagram_09_threat_modeling,
        "defense-in-depth": diagram_10_defense_depth,
        "owasp-attack-integration": diagram_11_owasp_integration,
    }

    for name, builder_fn in diagrams.items():
        builder = builder_fn()
        drawio_path = os.path.join(outdir, f"{name}.drawio.svg")
        builder.save_as_drawio_svg(drawio_path)
        print(f"Created: {drawio_path}")

    print(f"\nGenerated {len(diagrams)} .drawio.svg files in {outdir}/")
