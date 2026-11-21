"""Automated test suite verifying OWL 2 DL profile and HermiT reasoning outputs."""

from __future__ import annotations

import json
import pathlib
import subprocess
import rdflib

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
REASONING_DIR = BASE_DIR / "results" / "reasoning"
METRICS_DIR = BASE_DIR / "results" / "metrics"
ABOX_DIR = BASE_DIR / "abox"
SAIDAS_DIR = BASE_DIR / "saidas"
ROBOT_JAR = BASE_DIR / "tools" / "robot.jar"
OEM = rdflib.Namespace("http://example.org/oem#")
RDF = rdflib.RDF


def load_graph(name: str) -> rdflib.Graph:
    g = rdflib.Graph()
    g.parse(str(REASONING_DIR / f"{name}_reasoned.ttl"), format="turtle")
    return g


def test_owl2_dl_profile_compliance() -> None:
    for m_file in [
        "oem_tbox_metrics.json",
        "caso_a_aberto_metrics.json",
        "caso_a_fechado_metrics.json",
        "caso_b_metrics.json",
        "caso_c_metrics.json",
    ]:
        data = json.loads((METRICS_DIR / m_file).read_text(encoding="utf-8"))
        assert data["metrics"]["owl2_dl"] is True, f"{m_file} violated OWL 2 DL profile"


def test_caso_a_aberto_does_not_infer_integra() -> None:
    g = load_graph("caso_a_aberto")
    for ind in ["Evidencia_Original_1_Work", "Evidencia_Original_2_Work"]:
        types = set(g.objects(OEM[ind], RDF.type))
        assert OEM.EvidenciaMultimidia in types
        assert OEM.EvidenciaIntegra not in types
        assert OEM.EvidenciaComConteudoAlterado not in types
        assert OEM.EvidenciaComCadeiaQuebrada not in types
    # Transformations themselves are inferred as TransformacaoPreservadoraDeclarada
    assert (OEM.CopiaForense_video_original_1, RDF.type, OEM.TransformacaoPreservadoraDeclarada) in g


def test_caso_a_fechado_infers_integra() -> None:
    g = load_graph("caso_a_fechado")
    for ind in [
        "Evidencia_Original_1_Work",
        "Evidencia_Original_2_Work",
        "Evidencia_Audio_Original_1_Stereo",
        "Evidencia_Audio_Original_2_Stereo",
    ]:
        types = set(g.objects(OEM[ind], RDF.type))
        assert OEM.EvidenciaIntegra in types
        assert OEM.EvidenciaComConteudoAlterado not in types
        assert OEM.EvidenciaComCadeiaQuebrada not in types


def test_caso_b_infers_conteudo_alterado_and_not_integra() -> None:
    g = load_graph("caso_b")
    for ind in [
        "Evidencia_Sintetico_1_1_Work",
        "Evidencia_Sintetico_1_2_Work",
        "Evidencia_Sintetico_2_1_Work",
        "Evidencia_Sintetico_2_2_Work",
    ]:
        types = set(g.objects(OEM[ind], RDF.type))
        assert OEM.EvidenciaComConteudoAlterado in types
        assert OEM.EvidenciaIntegra not in types


def test_caso_c_infers_cadeia_quebrada_and_not_integra() -> None:
    g = load_graph("caso_c")
    types = set(g.objects(OEM.Evidencia_Recodificado_Mensageiro_1_Work, RDF.type))
    assert OEM.EvidenciaComCadeiaQuebrada in types
    assert OEM.EvidenciaIntegra not in types
    assert (OEM.TransmissaoMensageiro_video_1, RDF.type, OEM.TransformacaoNaoDeclarada) in g


def test_cenario_d1_inconsistent(tmp_path: pathlib.Path) -> None:
    """D1 (com fechamento + t_g generativa) deve resultar em ontologia inconsistente."""
    expl_path = SAIDAS_DIR / "D1_explicacao.md"
    assert expl_path.exists(), "Arquivo saidas/D1_explicacao.md não encontrado"
    expl_text = expl_path.read_text(encoding="utf-8")
    assert "owl#Thing" in expl_text and "owl#Nothing" in expl_text
    assert "oem#t_g" in expl_text
    assert "oem#TransformacaoGenerativa" in expl_text
    assert "oem#TransformacaoIsomorfica" in expl_text
    assert "oem#Evidencia_Original_1_Work" in expl_text

    if ROBOT_JAR.exists():
        merged = tmp_path / "d1_merged.ttl"
        reasoned = tmp_path / "d1_reasoned.ttl"
        merge_proc = subprocess.run(
            [
                "java", "-jar", str(ROBOT_JAR), "merge",
                "--catalog", str(BASE_DIR / "catalog-v001.xml"),
                "--input", str(BASE_DIR / "ontology" / "oem.ttl"),
                "--input", str(ABOX_DIR / "caso_D1.ttl"),
                "--output", str(merged),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        assert merge_proc.returncode == 0, merge_proc.stderr
        reason_proc = subprocess.run(
            [
                "java", "-jar", str(ROBOT_JAR), "reason",
                "--catalog", str(BASE_DIR / "catalog-v001.xml"),
                "--reasoner", "HermiT",
                "--input", str(merged),
                "--output", str(reasoned),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        combined = f"{reason_proc.stdout}\n{reason_proc.stderr}".lower()
        assert reason_proc.returncode != 0, "D1 deveria falhar por inconsistência no HermiT"
        assert "inconsistent" in combined, f"Saída inesperada do HermiT: {combined}"


def test_cenario_d2_conteudo_alterado_and_not_integra() -> None:
    """D2 (controle, sem fechamento) deve ser consistente e inferir EvidenciaComConteudoAlterado."""
    d2_path = SAIDAS_DIR / "D2_classificacao.ttl"
    assert d2_path.exists(), "Arquivo saidas/D2_classificacao.ttl não encontrado"
    g = rdflib.Graph()
    g.parse(str(d2_path), format="turtle")
    types = set(g.objects(OEM.Evidencia_Original_1_Work, RDF.type))
    assert OEM.EvidenciaComConteudoAlterado in types
    assert OEM.EvidenciaIntegra not in types
    assert (OEM.t_g, RDF.type, OEM.TransformacaoGenerativa) in g
    assert (OEM.t_g, RDF.type, OEM.TransformacaoDeclarada) in g
