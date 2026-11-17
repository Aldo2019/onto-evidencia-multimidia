# Makefile for OEM (Ontology of Multimedia Evidence) — ISKO-Brasil 2027
# Usage: make all | make figura1 | make figura2 | make test

PYTHON := python
ROBOT  := java -jar tools/robot.jar

.PHONY: all profile reason explain query figura1 figura2 test

all: profile reason explain query figura1 figura2 test

profile:
	$(ROBOT) validate-profile --profile DL --input ontology/oem.ttl --output results/reasoning/profile_tbox.txt

reason:
	$(ROBOT) merge --catalog catalog-v001.xml --input ontology/oem.ttl --input cases/caso_a/caso_a.ttl --output results/reasoning/caso_a_aberto_merged.ttl
	$(ROBOT) reason --catalog catalog-v001.xml --reasoner HermiT --input results/reasoning/caso_a_aberto_merged.ttl --axiom-generators "SubClass EquivalentClass DisjointClasses ClassAssertion PropertyAssertion" --output results/reasoning/caso_a_aberto_reasoned.ttl
	$(ROBOT) merge --catalog catalog-v001.xml --input ontology/oem.ttl --input cases/caso_a/caso_a.ttl --input cases/caso_a/caso_a_fechado.ttl --output results/reasoning/caso_a_fechado_merged.ttl
	$(ROBOT) reason --catalog catalog-v001.xml --reasoner HermiT --input results/reasoning/caso_a_fechado_merged.ttl --axiom-generators "SubClass EquivalentClass DisjointClasses ClassAssertion PropertyAssertion" --output results/reasoning/caso_a_fechado_reasoned.ttl
	$(ROBOT) merge --catalog catalog-v001.xml --input ontology/oem.ttl --input cases/caso_b/caso_b.ttl --output results/reasoning/caso_b_merged.ttl
	$(ROBOT) reason --catalog catalog-v001.xml --reasoner HermiT --input results/reasoning/caso_b_merged.ttl --axiom-generators "SubClass EquivalentClass DisjointClasses ClassAssertion PropertyAssertion" --output results/reasoning/caso_b_reasoned.ttl
	$(ROBOT) merge --catalog catalog-v001.xml --input ontology/oem.ttl --input cases/caso_c/caso_c.ttl --output results/reasoning/caso_c_merged.ttl
	$(ROBOT) reason --catalog catalog-v001.xml --reasoner HermiT --input results/reasoning/caso_c_merged.ttl --axiom-generators "SubClass EquivalentClass DisjointClasses ClassAssertion PropertyAssertion" --output results/reasoning/caso_c_reasoned.ttl

explain:
	$(ROBOT) explain --reasoner HermiT --prefix "oem: http://example.org/oem#" --input results/reasoning/caso_a_aberto_merged.ttl --axiom "{oem:CopiaForense_video_original_1} SubClassOf: oem:TransformacaoPreservadoraDeclarada" --explanation results/explanations/explain_caso_a_aberto.md
	$(ROBOT) explain --reasoner HermiT --prefix "oem: http://example.org/oem#" --input results/reasoning/caso_a_fechado_merged.ttl --axiom "{oem:Evidencia_Original_1_Work} SubClassOf: oem:EvidenciaIntegra" --explanation results/explanations/explain_caso_a_fechado.md
	$(ROBOT) explain --reasoner HermiT --prefix "oem: http://example.org/oem#" --input results/reasoning/caso_b_merged.ttl --axiom "{oem:Evidencia_Sintetico_1_1_Work} SubClassOf: oem:EvidenciaComConteudoAlterado" --explanation results/explanations/explain_caso_b.md
	$(ROBOT) explain --reasoner HermiT --prefix "oem: http://example.org/oem#" --input results/reasoning/caso_c_merged.ttl --axiom "{oem:Evidencia_Recodificado_Mensageiro_1_Work} SubClassOf: oem:EvidenciaComCadeiaQuebrada" --explanation results/explanations/explain_caso_c.md

query:
	$(ROBOT) query --input results/reasoning/caso_a_aberto_reasoned.ttl --query queries/pc1_integridade.rq results/sparql/caso_a_aberto/pc1.csv --query queries/pc2_transformacoes_custodia.rq results/sparql/caso_a_aberto/pc2.csv --query queries/pc3_exames_enf.rq results/sparql/caso_a_aberto/pc3.csv --query queries/pc4_indicios_edicao.rq results/sparql/caso_a_aberto/pc4.csv --query queries/pc5_quebra_custodia_ou_alteracao.rq results/sparql/caso_a_aberto/pc5.csv
	$(ROBOT) query --input results/reasoning/caso_a_fechado_reasoned.ttl --query queries/pc1_integridade.rq results/sparql/caso_a_fechado/pc1.csv --query queries/pc2_transformacoes_custodia.rq results/sparql/caso_a_fechado/pc2.csv --query queries/pc3_exames_enf.rq results/sparql/caso_a_fechado/pc3.csv --query queries/pc4_indicios_edicao.rq results/sparql/caso_a_fechado/pc4.csv --query queries/pc5_quebra_custodia_ou_alteracao.rq results/sparql/caso_a_fechado/pc5.csv
	$(ROBOT) query --input results/reasoning/caso_b_reasoned.ttl --query queries/pc1_integridade.rq results/sparql/caso_b/pc1.csv --query queries/pc2_transformacoes_custodia.rq results/sparql/caso_b/pc2.csv --query queries/pc3_exames_enf.rq results/sparql/caso_b/pc3.csv --query queries/pc4_indicios_edicao.rq results/sparql/caso_b/pc4.csv --query queries/pc5_quebra_custodia_ou_alteracao.rq results/sparql/caso_b/pc5.csv
	$(ROBOT) query --input results/reasoning/caso_c_reasoned.ttl --query queries/pc1_integridade.rq results/sparql/caso_c/pc1.csv --query queries/pc2_transformacoes_custodia.rq results/sparql/caso_c/pc2.csv --query queries/pc3_exames_enf.rq results/sparql/caso_c/pc3.csv --query queries/pc4_indicios_edicao.rq results/sparql/caso_c/pc4.csv --query queries/pc5_quebra_custodia_ou_alteracao.rq results/sparql/caso_c/pc5.csv

figura1:
	$(PYTHON) analysis/make_figura1.py

figura2:
	$(PYTHON) analysis/generate_figura2.py

test:
	$(PYTHON) -m pytest tests/test_reasoning.py -v
