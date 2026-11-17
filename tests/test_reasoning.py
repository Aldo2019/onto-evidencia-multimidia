"""Automated test suite verifying OWL 2 DL profile and HermiT reasoning outputs."""

from __future__ import annotations

import json
import pathlib
import rdflib

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
REASONING_DIR = BASE_DIR / "results" / "reasoning"
METRICS_DIR = BASE_DIR / "results" / "metrics"
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
