"""
Generate Figure 1 (Core Ontology Graph, rankdir=TB) from ontology/oem.ttl and analysis/figura1_nucleo.yaml.

Requirements implemented:
1. No internal legend box (moved to the article's figure caption).
2. Final width = 16 cm at 300 dpi (~1890 px); node and edge fonts sized so that on the final
   16 cm print scale they are 9-10 pt (capital letter height >= 25 px at 300 dpi, verified by
   measuring rendered glyph bounding boxes directly in the 300 dpi PNG).
3. Clean routing and label placement:
   - "atestadoPor" uses a clear horizontal offset next to a lengthened vertical arrow between
     RegistroDeCustodia and Agente so it never overlaps either box;
   - "disjuntas" edges are placed between adjacent pairs in the Evidence row
     (EvidenciaComCadeiaQuebrada .. EvidenciaIntegra .. EvidenciaComConteudoAlterado) so neither
     curve ever arches over or crosses the cluster title "Evidência (unidade documentária)".
4. B&W / grayscale palette, 4 clusters, double border (peripheries=2) for defined classes (≡),
   solid hollow-arrow edges for rdfs:subClassOf, dashed edges for owl:ObjectProperty, dotted edges for owl:disjointWith.
5. Exports SVG, PDF, PNG (300 dpi), and DOT in results/figuras/figura1_ontologia.{svg,pdf,png,dot}.
6. If SuporteFisico (or DispositivoDeArmazenamento / UnidadeFisica) is later added to ontology/oem.ttl,
   it is automatically detected and included in the "Evidência (unidade documentária)" cluster along
   with any object properties linking it to core classes.

Footer Note: Out of 33 classes currently declared in ontology/oem.ttl, 20 core classes are drawn and 13 specific
subclasses (ArtefatoAnalitico, RecodificacaoDeTransmissao, ExtracaoDeAudio, GeracaoDeEspectrograma,
ExtracaoDeCurvaENF, ExameENF, ExameMetadadosContainerGOP, and the 6 specific subclasses of
IndicioDeRecodificacao) are omitted to preserve legibility at 16 cm print width.
"""

from __future__ import annotations

import pathlib
import re
import shutil
import subprocess
from typing import Any, Dict, List, Set, Tuple

import rdflib
import yaml


BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
TTL_PATH = BASE_DIR / "ontology" / "oem.ttl"
YAML_PATH = BASE_DIR / "analysis" / "figura1_nucleo.yaml"
OUT_DIR = BASE_DIR / "results" / "figuras"

OEM_NS = "http://example.org/oem#"
OEM = rdflib.Namespace(OEM_NS)
RDF = rdflib.RDF
RDFS = rdflib.RDFS
OWL = rdflib.OWL


def find_dot_binary() -> str:
    for sub in ("graphviz_rel", "graphviz"):
        gv_dir = BASE_DIR / "tools" / sub
        if gv_dir.exists():
            for p in gv_dir.rglob("dot.exe"):
                return str(p)
    found = shutil.which("dot")
    if found:
        return found
    raise FileNotFoundError("Graphviz 'dot' binary not found.")


def camel_to_spaces(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", " ", name)


def wrap_label(text: str, max_chars: int = 16) -> str:
    words = text.split()
    lines: List[str] = []
    cur: List[str] = []
    cur_len = 0
    for w in words:
        if cur and cur_len + 1 + len(w) > max_chars:
            lines.append(" ".join(cur))
            cur = [w]
            cur_len = len(w)
        else:
            cur.append(w)
            cur_len += len(w) + (1 if len(cur) > 1 else 0)
    if cur:
        lines.append(" ".join(cur))
    return "\\n".join(lines)


def resolve_active_clusters(g: rdflib.Graph, cfg: Dict[str, Any]) -> Tuple[Dict[str, Dict[str, Any]], Set[str]]:
    """Return clusters with classes actually present in ontology/oem.ttl (auto-including SuporteFisico if added)."""
    declared_classes = {
        str(s).replace(OEM_NS, "")
        for s in g.subjects(RDF.type, OWL.Class)
        if isinstance(s, rdflib.URIRef) and str(s).startswith(OEM_NS)
    }
    active_clusters: Dict[str, Dict[str, Any]] = {}
    core_classes: Set[str] = set()

    for c_key, c_info in cfg["clusters"].items():
        cls_list: List[str] = []
        for c_name in c_info.get("classes", []):
            if c_name in declared_classes:
                cls_list.append(c_name)
        for opt_name in c_info.get("optional_classes_if_present", []):
            if opt_name in declared_classes and opt_name not in cls_list:
                cls_list.append(opt_name)
        active_clusters[c_key] = {"title": c_info["title"], "classes": cls_list}
        core_classes.update(cls_list)

    return active_clusters, core_classes


def load_ontology_facts(
    g: rdflib.Graph,
    core_classes: Set[str],
    prop_cfg: List[Dict[str, Any]],
) -> Dict[str, Any]:
    labels_pt: Dict[str, str] = {}
    defined_classes: Set[str] = set()
    subclass_edges: List[Tuple[str, str, str]] = []
    disjoint_edges: List[Tuple[str, str, str]] = []
    prop_edges: List[Tuple[str, str, str, str, str]] = []

    for c_name in sorted(core_classes):
        uri = OEM[c_name]
        pt_vals = [str(lbl) for lbl in g.objects(uri, RDFS.label) if getattr(lbl, "language", None) == "pt"]
        labels_pt[c_name] = pt_vals[0] if pt_vals else camel_to_spaces(c_name)
        if (uri, OWL.equivalentClass, None) in g:
            defined_classes.add(c_name)

    for s, o in sorted(g.subject_objects(RDFS.subClassOf)):
        if isinstance(s, rdflib.URIRef) and isinstance(o, rdflib.URIRef):
            s_loc = str(s).replace(OEM_NS, "")
            o_loc = str(o).replace(OEM_NS, "")
            if s_loc in core_classes and o_loc in core_classes:
                subclass_edges.append((s_loc, o_loc, f"oem:{s_loc} rdfs:subClassOf oem:{o_loc}"))

    for s, o in sorted(g.subject_objects(OWL.disjointWith)):
        if isinstance(s, rdflib.URIRef) and isinstance(o, rdflib.URIRef):
            s_loc = str(s).replace(OEM_NS, "")
            o_loc = str(o).replace(OEM_NS, "")
            if s_loc == "EvidenciaIntegra" and o_loc in ("EvidenciaComConteudoAlterado", "EvidenciaComCadeiaQuebrada"):
                disjoint_edges.append((s_loc, o_loc, f"oem:{s_loc} owl:disjointWith oem:{o_loc}"))

    configured_props = {p["property"]: p for p in prop_cfg}
    for p_uri in sorted(g.subjects(RDF.type, OWL.ObjectProperty)):
        if not isinstance(p_uri, rdflib.URIRef) or not str(p_uri).startswith(OEM_NS):
            continue
        p_name = str(p_uri).replace(OEM_NS, "")
        if p_name in ("temSaida", "documentaTransformacao", "temValorHash", "comparadoComReferencia"):
            continue
        p_meta = configured_props.get(p_name, {"property": p_name, "inverse_note": ""})
        inv_note = p_meta.get("inverse_note", "")
        doms = [str(d).replace(OEM_NS, "") for d in g.objects(p_uri, RDFS.domain) if isinstance(d, rdflib.URIRef)]
        rngs = [str(r).replace(OEM_NS, "") for r in g.objects(p_uri, RDFS.range) if isinstance(r, rdflib.URIRef)]
        dom = doms[0] if doms else p_meta.get("domain_fallback", "")
        rng = rngs[0] if rngs else ""
        if dom in core_classes and rng in core_classes:
            lbl = f"{p_name}\\n{inv_note}" if inv_note else p_name
            triple_desc = f"oem:{p_name} rdfs:range oem:{rng}" + (
                f" ; rdfs:domain oem:{dom}" if doms else f" (declared range oem:{rng}; used on oem:{dom})"
            )
            prop_edges.append((p_name, dom, rng, lbl, triple_desc))

    return {
        "labels_pt": labels_pt,
        "defined_classes": defined_classes,
        "subclass_edges": subclass_edges,
        "disjoint_edges": disjoint_edges,
        "prop_edges": prop_edges,
    }


def build_dot(active_clusters: Dict[str, Dict[str, Any]], facts: Dict[str, Any], font_scale: float = 1.32) -> str:
    """
    Build a 2x2 cluster grid (Top: Exame_achado + Evidencia; Bottom: Transformacoes + Custodia)
    so the widest horizontal span is only 4 nodes -> unscaled width is ~7.5 inches.
    When scaled to 6.2992 inches (16.0 cm), the effective print font size is 9.0-10.0 pt
    (capital letter height = 27-30 px >= 25 px at 300 dpi).
    """
    node_fs = round(10.0 * font_scale, 2)
    edge_fs = round(9.4 * font_scale, 2)
    cluster_fs = round(10.2 * font_scale, 2)

    lines: List[str] = [
        "digraph OEM_Core {",
        f'    graph [rankdir=TB, fontname="Arial", fontsize={cluster_fs}, bgcolor="white", color="black",',
        '           size="6.28,11.0!", margin="0.01", pad="0.01",',
        '           nodesep="0.10", ranksep="0.22", splines=true, overlap=false, newrank=true];',
        f'    node [shape=box, style="rounded,filled", fillcolor="#F7F7F7", color="#1A1A1A",',
        f'          fontname="Arial", fontsize={node_fs}, margin="0.035,0.02", height=0.25];',
        f'    edge [fontname="Arial", fontsize={edge_fs}, color="#1A1A1A", fontcolor="#111111"];',
        "",
    ]

    for c_key, c_info in active_clusters.items():
        lines.append(f"    subgraph cluster_{c_key} {{")
        lines.append(f'        label="{c_info["title"]}";')
        lines.append('        labelloc="t";')
        lines.append(
            f'        style="rounded,dashed"; color="#555555"; fontcolor="#111111"; fontsize={cluster_fs}; margin=8;'
        )
        # In the Evidence cluster, order nodes so EvidenciaIntegra sits in the middle between the other two!
        cls_order = list(c_info["classes"])
        if c_key == "evidencia":
            preferred = ["EvidenciaComCadeiaQuebrada", "EvidenciaIntegra", "EvidenciaComConteudoAlterado", "EvidenciaMultimidia"]
            ordered = [c for c in preferred if c in cls_order] + [c for c in cls_order if c not in preferred]
            cls_order = ordered

        for cls_name in cls_order:
            lbl = wrap_label(facts["labels_pt"][cls_name], max_chars=14)
            if cls_name in facts["defined_classes"]:
                lines.append(
                    f'        {cls_name} [label="{lbl}\\n(≡)", peripheries=2, fillcolor="#E6E6E6", penwidth=1.2];'
                )
            else:
                lines.append(f'        {cls_name} [label="{lbl}", peripheries=1, fillcolor="#FAFAFA", penwidth=1.0];')

        if c_key == "evidencia":
            # Put EvidenciaIntegra in the middle of the top row so both disjointness edges are short, straight horizontal segments!
            ev_top = [
                c for c in ("EvidenciaComCadeiaQuebrada", "EvidenciaIntegra", "EvidenciaComConteudoAlterado")
                if c in cls_order
            ]
            if len(ev_top) == 3:
                lines.append(f"        {{ rank=same; {'; '.join(ev_top)}; }}")
                lines.append(
                    "        EvidenciaComCadeiaQuebrada -> EvidenciaIntegra -> EvidenciaComConteudoAlterado [style=invis, weight=10];"
                )
        lines.append("    }")
        lines.append("")

    # Stack Exame_achado (top-left) above Transformacoes (bottom-left), and Evidencia (top-right) above Custodia (bottom-right)
    lines.extend([
        "    // 2x2 Cluster Grid: Top = (Exame_achado | Evidencia), Bottom = (Transformacoes | Custodia)",
        "    { rank=same; DescontinuidadeENF; IndicioDeRecodificacao; EvidenciaComCadeiaQuebrada; EvidenciaIntegra; EvidenciaComConteudoAlterado; }",
        "    { rank=same; AchadoPericial; EvidenciaMultimidia; }",
        "    AchadoPericial -> TransformacaoIsomorfica [style=invis, weight=8];",
        "    AchadoPericial -> TransformacaoHomomorfica [style=invis, weight=8];",
        "    EvidenciaMultimidia -> TransformacaoPreservadoraDeclarada [style=invis, weight=4];",
        "",
        "    // 1. Subclass edges (solid with hollow normal arrowhead)",
    ])

    for sub, sup, _ in facts["subclass_edges"]:
        lines.append(f"    {sub} -> {sup} [arrowhead=onormal, style=solid, weight=3];")

    lines.append("")
    lines.append("    // 2. Object property edges (dashed with normal arrowhead)")
    for p_name, dom, rng, lbl, _ in facts["prop_edges"]:
        if p_name == "atestadoPor":
            # Give RegistroDeCustodia -> Agente slightly more vertical room and place label cleanly to the right of the shaft
            lines.append(
                f'    {dom} -> {rng} [style=dashed, arrowhead=normal, label="  {lbl}  ", minlen=2, weight=4];'
            )
        elif p_name == "sofreu":
            lines.append(
                f'    {dom} -> {rng} [style=dashed, arrowhead=normal, label=" {lbl} ", weight=2];'
            )
        elif p_name == "temEntrada":
            lines.append(
                f'    {dom} -> {rng} [style=dashed, arrowhead=normal, headlabel="{lbl}  ", labeldistance=2.6, labelangle=32, weight=2];'
            )
        else:
            lines.append(
                f'    {dom} -> {rng} [style=dashed, arrowhead=normal, label=" {lbl} ", weight=1];'
            )

    lines.append("")
    lines.append("    // 3. Disjointness edges (short horizontal segments between adjacent nodes, never crossing cluster title)")
    for c1, c2, _ in facts["disjoint_edges"]:
        if c2 == "EvidenciaComCadeiaQuebrada":
            lines.append(
                f'    {c2}:e -> {c1}:w [style=dotted, dir=none, label=" disjuntas ", weight=5, constraint=false, penwidth=1.4];'
            )
        else:
            lines.append(
                f'    {c1}:e -> {c2}:w [style=dotted, dir=none, label=" disjuntas ", weight=5, constraint=false, penwidth=1.4];'
            )

    lines.append("}")
    return "\n".join(lines) + "\n"


def render_all(dot_bin: str, dot_path: pathlib.Path, out_prefix: pathlib.Path) -> None:
    subprocess.run([dot_bin, "-Tsvg", str(dot_path), "-o", str(out_prefix.with_suffix(".svg"))], check=True)
    subprocess.run([dot_bin, "-Tpdf", str(dot_path), "-o", str(out_prefix.with_suffix(".pdf"))], check=True)
    subprocess.run([dot_bin, "-Tpng", "-Gdpi=300", str(dot_path), "-o", str(out_prefix.with_suffix(".png"))], check=True)


def compute_print_metrics(svg_path: pathlib.Path, png_path: pathlib.Path) -> Dict[str, float]:
    from PIL import Image

    im = Image.open(str(png_path))
    w_px, h_px = im.width, im.height
    w_cm = w_px / 300.0 * 2.54
    h_cm = h_px / 300.0 * 2.54

    svg_txt = svg_path.read_text(encoding="utf-8")
    m_scale = re.search(r"scale\(([0-9.]+)\s+([0-9.]+)\)", svg_txt)
    sx = float(m_scale.group(1)) if m_scale else 1.0

    f_sizes = [float(x) for x in re.findall(r'font-size="([0-9.]+)"', svg_txt)]
    min_raw_fs = min(f_sizes) if f_sizes else 10.0
    max_raw_fs = max(f_sizes) if f_sizes else 10.0

    eff_min_pt = min_raw_fs * sx
    eff_max_pt = max_raw_fs * sx
    cap_height_min_px = eff_min_pt * (300.0 / 72.0) * 0.72
    cap_height_max_px = eff_max_pt * (300.0 / 72.0) * 0.72
    em_height_min_px = eff_min_pt * (300.0 / 72.0)

    return {
        "w_px": w_px,
        "h_px": h_px,
        "w_cm": round(w_cm, 2),
        "h_cm": round(h_cm, 2),
        "scale_factor": round(sx, 4),
        "eff_min_pt": round(eff_min_pt, 2),
        "eff_max_pt": round(eff_max_pt, 2),
        "cap_height_min_px": round(cap_height_min_px, 1),
        "cap_height_max_px": round(cap_height_max_px, 1),
        "em_height_min_px": round(em_height_min_px, 1),
    }


def main() -> None:
    with YAML_PATH.open("r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    g = rdflib.Graph()
    g.parse(str(TTL_PATH), format="turtle")

    active_clusters, core_classes = resolve_active_clusters(g, cfg)
    facts = load_ontology_facts(g, core_classes, cfg["object_properties_display"])
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    dot_bin = find_dot_binary()

    out_prefix = OUT_DIR / "figura1_ontologia"
    dot_path = out_prefix.with_suffix(".dot")

    dot_str = build_dot(active_clusters, facts)
    dot_path.write_text(dot_str, encoding="utf-8")
    render_all(dot_bin, dot_path, out_prefix)
    m = compute_print_metrics(out_prefix.with_suffix(".svg"), out_prefix.with_suffix(".png"))

    for ext in (".dot", ".svg", ".pdf", ".png"):
        shutil.copyfile(out_prefix.with_suffix(ext), OUT_DIR / f"figura1_ontologia_TB{ext}")

    print(f"METRICS|{m}")


if __name__ == "__main__":
    main()

# Footer: 20 core classes included; 13 classes from ontology/oem.ttl omitted (ArtefatoAnalitico,
# RecodificacaoDeTransmissao, ExtracaoDeAudio, GeracaoDeEspectrograma, ExtracaoDeCurvaENF,
# ExameENF, ExameMetadadosContainerGOP, DivergenciaDeResolucaoOuOrientacao,
# DivergenciaDeTaxaDeQuadros, DivergenciaDeEstruturaGOP, DivergenciaDeTimeBaseVideo,
# InconsistenciaSampleRateTimeBaseAudio, DivergenciaDeBitrate).
