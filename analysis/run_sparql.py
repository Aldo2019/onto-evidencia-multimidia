"""Create and execute SPARQL Competency Questions (PC1-PC5) over reasoned graphs."""

from __future__ import annotations

import json
import pathlib
import rdflib

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
QUERIES_DIR = BASE_DIR / "queries"
REASONING_DIR = BASE_DIR / "results" / "reasoning"
SPARQL_OUT_DIR = BASE_DIR / "results" / "sparql"

QUERIES_DIR.mkdir(parents=True, exist_ok=True)
SPARQL_OUT_DIR.mkdir(parents=True, exist_ok=True)

QUERIES = {
    "pc1_integridade.rq": """PREFIX oem: <http://example.org/oem#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT DISTINCT ?evidencia ?classeIntegridade
WHERE {
    ?evidencia a oem:EvidenciaMultimidia .
    VALUES ?classeIntegridade {
        oem:EvidenciaIntegra
        oem:EvidenciaComConteudoAlterado
        oem:EvidenciaComCadeiaQuebrada
    }
    ?evidencia a ?classeIntegridade .
}
ORDER BY ?evidencia ?classeIntegridade
""",
    "pc2_transformacoes_custodia.rq": """PREFIX oem: <http://example.org/oem#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT DISTINCT ?evidencia ?transformacao ?tipoDeclaracao ?registro ?hashValor
WHERE {
    ?evidencia oem:sofreu ?transformacao .
    VALUES ?tipoDeclaracao {
        oem:TransformacaoPreservadoraDeclarada
        oem:TransformacaoGenerativa
        oem:TransformacaoNaoDeclarada
    }
    ?transformacao a ?tipoDeclaracao .
    OPTIONAL { ?transformacao oem:registradaEm ?registro . }
    OPTIONAL {
        ?transformacao oem:verificadaPor ?h .
        ?h oem:valorHashHex ?hashValor .
    }
}
ORDER BY ?evidencia ?transformacao
""",
    "pc3_exames_enf.rq": """PREFIX oem: <http://example.org/oem#>

SELECT DISTINCT ?exame ?audioEntrada ?resultado ?snr60 ?snr120 ?limiar
WHERE {
    ?exame a oem:ExameENF ;
           oem:temEntrada ?audioEntrada ;
           oem:resultadoExame ?resultado ;
           oem:snrMedio60Hz_dB ?snr60 ;
           oem:snrMedio120Hz_dB ?snr120 ;
           oem:limiarSNR_dB ?limiar .
}
ORDER BY ?exame
""",
    "pc4_indicios_edicao.rq": """PREFIX oem: <http://example.org/oem#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?evidencia ?exame ?achado ?subclasse ?valorRef ?valorObs
WHERE {
    ?exame oem:temEntrada ?evidencia ;
           oem:geraAchado ?achado .
    ?achado a ?subclasse ;
            oem:valorReferencia ?valorRef ;
            oem:valorObservado ?valorObs .
    FILTER(?subclasse != oem:AchadoPericial && ?subclasse != oem:IndicioDeEdicao && ?subclasse != <http://www.w3.org/2002/07/owl#NamedIndividual> && ?subclasse != <http://www.w3.org/2002/07/owl#Thing>)
}
ORDER BY ?evidencia ?achado ?subclasse
""",
    "pc5_quebra_custodia_ou_alteracao.rq": """PREFIX oem: <http://example.org/oem#>

SELECT DISTINCT ?evidencia ?transformacaoVioladora ?classificacaoEvidencia
WHERE {
    ?evidencia oem:sofreu ?transformacaoVioladora ;
               a ?classificacaoEvidencia .
    VALUES ?classificacaoEvidencia {
        oem:EvidenciaComConteudoAlterado
        oem:EvidenciaComCadeiaQuebrada
    }
    FILTER EXISTS {
        { ?transformacaoVioladora a oem:TransformacaoGenerativa }
        UNION
        { ?transformacaoVioladora a oem:TransformacaoNaoDeclarada }
    }
}
ORDER BY ?evidencia ?transformacaoVioladora
""",
}


def shorten(val: object) -> str:
    if val is None:
        return "—"
    s = str(val)
    s = s.replace("http://example.org/oem#", "oem:")
    if len(s) == 64 and all(c in "0123456789abcdef" for c in s):
        return s[:16] + "…"
    return s


def main() -> None:
    for q_name, q_text in QUERIES.items():
        (QUERIES_DIR / q_name).write_text(q_text, encoding="utf-8")

    scenarios = ["caso_a_aberto", "caso_a_fechado", "caso_b", "caso_c"]
    all_results = {}

    for sc in scenarios:
        g = rdflib.Graph()
        g.parse(str(REASONING_DIR / f"{sc}_reasoned.ttl"), format="turtle")
        sc_res = {}
        for q_name, q_text in QUERIES.items():
            res = g.query(q_text)
            rows = []
            for r in res:
                rows.append([shorten(item) for item in r])
            sc_res[q_name] = rows
        all_results[sc] = sc_res

    out_json = SPARQL_OUT_DIR / "resultados_sparql.json"
    out_json.write_text(json.dumps(all_results, indent=2, ensure_ascii=False), encoding="utf-8")
    print("SPARQL_QUERIES_COMPLETED")


if __name__ == "__main__":
    main()
