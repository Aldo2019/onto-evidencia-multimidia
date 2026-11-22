# Ontologia de Evidências Multimídia (OEM) — ISKO Brasil 2027

[![OWL 2 DL](https://img.shields.io/badge/OWL_2-DL_Valid-brightgreen)](#)
[![Reasoner](https://img.shields.io/badge/Reasoner-HermiT_1.4.3-blue)](#)
[![License: CC BY 4.0](https://img.shields.io/badge/Ontology_%26_Cases-CC_BY_4.0-lightgrey)](#licen%C3%A7as--licenses)
[![License: MIT](https://img.shields.io/badge/Code_%26_Tests-MIT-yellow)](#licen%C3%A7as--licenses)

---

## Português (PT-BR)

### 1. Visão Geral e Tese Central

Este repositório acompanha o artigo submetido ao **ISKO Brasil 2027 (Organização do Conhecimento)** e apresenta a **Ontologia de Evidências Multimídia (OEM)**, formalizada em **OWL 2 DL** (sintaxe Turtle, `.ttl`).

A tese central modelada e verificada formalmente na ontologia estabelece que:

1. **Preservação vs. Alteração Semântica:** Uma evidência multimídia (áudio, imagem ou vídeo) só pode ser inferida como **íntegra** (`oem:EvidenciaIntegra`) se todas as transformações pelas quais passou forem **declaradas** (registradas formalmente na cadeia de custódia por um `oem:Agente`) e de natureza **preservadora**:
   - **Transformação Isomórfica (`oem:TransformacaoIsomorfica`):** cópia forense bit a bit verificada pela igualdade do valor de hash criptográfico (`SHA-256`);
   - **Transformação Homomórfica (`oem:TransformacaoHomomorfica`):** redução analítica controlada que projeta propriedades do sinal sem introduzir conteúdo sintético (extração de áudio PCM sem reamostragem, geração de espectrograma PSD, extração de curva de Frequência da Rede Elétrica — ENF a `60 Hz` / `120 Hz` — e inspeção de estrutura de GOP).
2. **Transformações Generativas (`oem:TransformacaoGenerativa`):** operações de edição ou síntese neural (como *deepfakes* de voz ou rosto) alteram o conteúdo informacional que a evidência afirma, classificando o item em `oem:EvidenciaComConteudoAlterado` (disjunta de `oem:EvidenciaIntegra`).
3. **Pressuposição de Mundo Aberto (OWA) e Axioma de Fechamento:** Sob a semântica de mundo aberto da OWL 2 DL, o raciocinador **HermiT** **não** infere integridade a partir do silêncio ou da mera ausência de registros de adulteração. A classificação como `oem:EvidenciaIntegra` exige um **axioma de fechamento** ($\forall \mathsf{sofreu}.\{t_1, \dots, t_n\}$), que representa formalmente a atestação pericial de que o percurso documentado na cadeia de custódia está completo. Analogamente, a ausência de componente ENF detectável no áudio (`"ENF não detectável"`) não gera achado pericial nem conclusão de manipulação.

---

### 2. Estrutura do Repositório

```text
├── ontology/
│   └── oem.ttl                       # TBox principal (OWL 2 DL, rótulos @pt/@en e skos:definition)
├── cases/
│   ├── EXPECTED.md                   # Previsões formais de classificação por cenário
│   ├── caso_a/
│   │   ├── caso_a.ttl                # ABox do Caso A (mundo aberto: cópias isomórficas e exames)
│   │   ├── caso_a_fechado.ttl        # Axiomas de fechamento pericial do Caso A
│   │   └── registro_custodia.csv     # Registro tabular da cadeia de custódia (Caso A)
│   ├── caso_b/
│   │   ├── caso_b.ttl                # ABox do Caso B (vídeos sintéticos / deepfake e exames)
│   │   └── registro_custodia.csv     # Registro tabular da cadeia de custódia (Caso B)
│   └── caso_c/
│       ├── caso_c.ttl                # ABox do Caso C (recodificação sem custódia: registradaEm max 0)
│       └── registro_custodia.csv     # Registro tabular da cadeia de custódia (Caso C)
├── analysis/
│   ├── config.yaml                   # Parâmetros fixos de espectrograma, ENF (60/120 Hz) e GOP
│   ├── run_analyses.py               # Pipeline de processamento de sinal e metadados (SciPy / FFprobe)
│   ├── append_ttl_csv.py             # Conversão de resultados e custódia para instâncias RDF/Turtle
│   └── run_sparql.py                 # Gerador das consultas SPARQL (PC1–PC5)
├── queries/
│   ├── pc1_integridade.rq            # PC1: Classificação de integridade das evidências
│   ├── pc2_transformacoes_custodia.rq# PC2: Transformações sofridas, registros e hashes
│   ├── pc3_exames_enf.rq             # PC3: Resultados e SNR dos exames de ENF (60/120 Hz)
│   ├── pc4_indicios_edicao.rq        # PC4: Indícios de edição/recodificação (GOP/contêiner)
│   └── pc5_quebra_custodia_ou_alteracao.rq # PC5: Transformações violadoras de integridade
├── results/
│   ├── RELATORIO_ARTIGO.md           # Relatório técnico completo consolidado para o artigo
│   ├── secao_3_4.md                  # Síntese analítica da Seção 3.4, justificações DL/Manchester e quadro
│   ├── inventario.csv / inventario.md# Inventário preliminar de hashes SHA-256 e metadados
│   ├── inventario_ffprobe/           # Saídas brutas JSON do ffprobe
│   ├── inventario_exif/              # Saídas brutas JSON do exiftool
│   ├── analises/                     # Relatórios JSON, CSVs de curvas ENF e PNGs do Conjunto 1
│   ├── reasoning/                    # Grafos mesclados e raciocinados pelo HermiT (*_reasoned.ttl)
│   ├── explanations/                 # Justificações formais mínimas geradas via robot explain
│   ├── metrics/                      # Métricas OWL 2 DL e expressividade DL via robot measure
│   └── sparql/                       # Respostas reais em CSV para as questões PC1–PC5
├── tests/
│   └── test_reasoning.py             # Suíte automatizada pytest verificando OWL 2 DL e inferências
└── catalog-v001.xml                  # Catálogo XML OASIS para resolução local de owl:imports
```

> **Política de Privacidade e Não-Versionamento de Mídia Bruta:** Conforme configurado em `.gitignore`, **nenhum arquivo de vídeo, áudio ou imagem bruta** (`Vídeos/`, `data/raw/`, `data/work/`, `*.mp4`, `*.wav`, `*.jpeg`) e nenhum artefato visual derivado de vídeo de plataforma de terceiros (Conjunto 2) é versionado no Git. Apenas a ontologia, hashes criptográficos `SHA-256`, metadados estruturais, séries numéricas e asserções RDF derivadas são publicados.

---

### 3. Quadro-Resumo dos Resultados Experimentais (HermiT)

| Cenário / Caso | Transformações no Percurso | Fechamento / Custódia | Inferência do HermiT | NÃO Inferido pelo HermiT | Tempo |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **Caso A (Aberto)** | Isomórfica (`SHA-256`) + Homomórficas (`WAV`, `PSD`, `ENF`, `GOP`) | `registradaEm` presente; sem fechamento $\forall \mathsf{sofreu}$ (OWA) | `oem:EvidenciaMultimidia`; cópias em `oem:TransformacaoPreservadoraDeclarada` | `oem:EvidenciaIntegra`, `oem:EvidenciaComConteudoAlterado`, `oem:EvidenciaComCadeiaQuebrada` | `1234 ms` |
| **Caso A (Fechado)** | Isomórfica (`SHA-256`) + Homomórficas (`WAV`, `PSD`, `ENF`, `GOP`) | `registradaEm` presente + axioma $\forall \mathsf{sofreu}.\{t_1,\dots,t_n\}$ | **`oem:EvidenciaIntegra`** (`video_original_1`, `Video_original_2` e `.wav` estéreo) | `oem:EvidenciaComConteudoAlterado`, `oem:EvidenciaComCadeiaQuebrada` | `2836 ms` |
| **Caso B (Deepfake)** | Generativa (`oem:TransformacaoGenerativa`) + Aquisição/Exames | Síntese generativa no percurso (`oem:SinteseDeepfake_*`) | **`oem:EvidenciaComConteudoAlterado`** (`video_sintetico_1_1` a `2_2`) | `oem:EvidenciaIntegra` (disjunta de conteúdo alterado) | `1476 ms` |
| **Caso C (Mensageiro)** | Recodificação com perdas (`oem:RecodificacaoDeTransmissao`) | Sem registro explícito (`registradaEm max 0 RegistroDeCustodia`) | **`oem:EvidenciaComCadeiaQuebrada`** (`video_recodificado_mensageiro_1`) | `oem:EvidenciaIntegra`, `oem:EvidenciaComConteudoAlterado` | `1119 ms` |
| **Cenário D1 (Contradição)** | Isomórfica (`CopiaForense_video_original_1`) + Generativa (`oem:t_g`, registro de terceiro) | Fechamento original $\forall \mathsf{sofreu}.\{\mathsf{CopiaForense\_video\_original\_1}\}$ (sem `t_g`) | **INCONSISTENTE** ($\top \sqsubseteq \bot$; 6 axiomas na justificação mínima) | Classificação inviável por contradição formal | `1690 ms` (reason) / `2124 ms` (explain) |
| **Cenário D2 (Controle)** | Isomórfica (`CopiaForense_video_original_1`) + Generativa (`oem:t_g`, registro de terceiro) | Sem axioma de fechamento (OWA) | **Consistente**; **`oem:EvidenciaComConteudoAlterado`** (`Evidencia_Original_1_Work`) | `oem:EvidenciaIntegra` | `2034 ms` |

---

### Cenário D (Detecção de Contradição)

O **Cenário D** avalia o comportamento da ontologia quando uma transformação generativa registrada por terceiro (`oem:t_g`, vinculada a `oem:RegistroCustodia_Terceiro`, `"Registro de terceiro"`) é asserida sobre uma evidência única (`oem:Evidencia_Original_1_Work`, vídeo original do Conjunto 1), em duas variantes sem alteração da TBox (`ontology/oem.ttl`) nem das ABoxes anteriores:

- **D1 — Com fechamento (`abox/caso_D1.ttl` → `saidas/D1_explicacao.md`):** mantém o axioma de fechamento original do Caso A ($\forall \mathsf{sofreu}.\{\mathsf{CopiaForense\_video\_original\_1}\}$), sem incluir `oem:t_g`. O HermiT detectou **inconsistência lógica** (`1690 ms` no `robot reason`; `2124 ms` no `robot explain --mode inconsistency`). Como o fechamento restringe toda transformação sofrida pela evidência ao conjunto unitário da cópia isomórfica e `oem:sofreu` é inversa de `oem:temSaida`, a asserção de `oem:t_g` como `oem:TransformacaoGenerativa` entra em conflito direto com a disjunção entre transformações isomórficas, homomórficas e generativas.
- **D2 — Controle, sem fechamento (`abox/caso_D2.ttl` → `saidas/D2_classificacao.ttl`):** idêntica a D1, porém removendo o axioma de fechamento. A ontologia permaneceu **consistente** (`2034 ms` no `robot reason`), e o HermiT inferiu `oem:Evidencia_Original_1_Work` como **`oem:EvidenciaComConteudoAlterado`** (e **não** como `oem:EvidenciaIntegra`), além de classificar `oem:t_g` em `oem:TransformacaoDeclarada`.

#### Axiomas exatos na justificação mínima de inconsistência de D1 (`saidas/D1_explicacao.md`)

Entailment explicado: `owl:Thing SubClassOf owl:Nothing` (6 axiomas):

1. `[Third-Party Generative Transformation (t_g)](http://example.org/oem#t_g) Type [Transformação Generativa](http://example.org/oem#TransformacaoGenerativa)`
2. `[underwent transformation](http://example.org/oem#sofreu) InverseOf [tem saída](http://example.org/oem#temSaida)`
3. `[Isomorphic Forensic Copy of video_original_1.mp4](http://example.org/oem#CopiaForense_video_original_1) Type [Transformação Isomórfica](http://example.org/oem#TransformacaoIsomorfica)`
4. `[Original Video 1 ( Working Forensic Copy - Case A )](http://example.org/oem#Evidencia_Original_1_Work) Type [underwent transformation](http://example.org/oem#sofreu) only ({[Isomorphic Forensic Copy of video_original_1.mp4](http://example.org/oem#CopiaForense_video_original_1)})`
5. `[Third-Party Generative Transformation (t_g)](http://example.org/oem#t_g) [tem saída](http://example.org/oem#temSaida) [Original Video 1 ( Working Forensic Copy - Case A )](http://example.org/oem#Evidencia_Original_1_Work)`
6. `DisjointClasses: [Transformação Generativa](http://example.org/oem#TransformacaoGenerativa), [Homomorphic Transformation](http://example.org/oem#TransformacaoHomomorfica), [Transformação Isomórfica](http://example.org/oem#TransformacaoIsomorfica)`

---

### 4. Como Reproduzir os Experimentos

#### Pré-requisitos
- **Java 11+** e **ROBOT 1.9.4+** (`tools/robot.jar`: `https://github.com/ontodev/robot/releases/download/v1.9.4/robot.jar`)
- **Python 3.12+** com `numpy`, `scipy`, `matplotlib`, `pyyaml`, `rdflib`, `pytest`
- **FFmpeg / FFprobe** e **ExifTool** (para reexecução sobre arquivos de mídia em `data/work/`)

#### Comandos Principais
```bash
# 1. Validar perfil OWL 2 DL da TBox
java -jar tools/robot.jar validate-profile --profile DL --input ontology/oem.ttl

# 2. Mesclar e executar o raciocinador HermiT (exemplo: Caso A Fechado)
java -jar tools/robot.jar merge --catalog catalog-v001.xml \
  --input ontology/oem.ttl \
  --input cases/caso_a/caso_a.ttl \
  --input cases/caso_a/caso_a_fechado.ttl \
  --output results/reasoning/caso_a_fechado_merged.ttl

java -jar tools/robot.jar reason --catalog catalog-v001.xml --reasoner HermiT \
  --input results/reasoning/caso_a_fechado_merged.ttl \
  --axiom-generators "SubClass EquivalentClass DisjointClasses ClassAssertion PropertyAssertion" \
  --output results/reasoning/caso_a_fechado_reasoned.ttl

# 3. Gerar justificação formal mínima (robot explain)
java -jar tools/robot.jar explain --reasoner HermiT --prefix "oem: http://example.org/oem#" \
  --input results/reasoning/caso_a_fechado_merged.ttl \
  --axiom "{oem:Evidencia_Original_1_Work} SubClassOf: oem:EvidenciaIntegra" \
  --explanation results/explanations/explain_caso_a_fechado.md

# 4. Executar a suíte de testes automatizados
pytest tests/test_reasoning.py -v
```

---

## English (EN)

### 1. Overview and Core Thesis

This repository accompanies the paper submitted to **ISKO Brazil 2027 (Knowledge Organization)** and introduces the **Ontology of Multimedia Evidence (OEM)**, formalized in **OWL 2 DL** (Turtle syntax, `.ttl`).

The core thesis modeled and formally verified by the ontology states that:

1. **Preservation vs. Semantic Alteration:** A piece of multimedia evidence (audio, image, or video) can only be inferred as **intact** (`oem:EvidenciaIntegra`) if all transformations it underwent are **declared** (formally recorded in the chain of custody by an `oem:Agente`) and are **preserving** in nature:
   - **Isomorphic Transformation (`oem:TransformacaoIsomorfica`):** bit-by-bit forensic copy verified by cryptographic hash equality (`SHA-256`);
   - **Homomorphic Transformation (`oem:TransformacaoHomomorfica`):** controlled analytical reduction projecting signal properties without introducing synthetic content (unresampled PCM audio extraction, PSD spectrogram generation, Electrical Network Frequency — ENF at `60 Hz` / `120 Hz` — curve extraction, and GOP structure inspection).
2. **Generative Transformations (`oem:TransformacaoGenerativa`):** editing or neural synthesis operations (such as voice or face *deepfakes*) alter the informational content asserted by the evidence, classifying it under `oem:EvidenciaComConteudoAlterado` (disjoint with `oem:EvidenciaIntegra`).
3. **Open World Assumption (OWA) and Closure Axiom:** Under OWL 2 DL open-world semantics, the **HermiT** reasoner **cannot** infer integrity from silence or from the mere absence of tampering records. Classification under `oem:EvidenciaIntegra` requires an explicit **closure axiom** ($\forall \mathsf{sofreu}.\{t_1, \dots, t_n\}$), representing the forensic expert's attestation that the documented chain-of-custody path is complete. Likewise, the absence of a detectable ENF component (`"ENF não detectável"`) generates neither a forensic finding nor a conclusion of tampering.

---

## Licenças / Licenses

Este repositório adota licenciamento duplo conforme a natureza dos artefatos:

- **Ontologia e Casos (`ontology/` e `cases/`):** Licenciados sob **Creative Commons Atribuição 4.0 Internacional (CC BY 4.0)** ([https://creativecommons.org/licenses/by/4.0/](https://creativecommons.org/licenses/by/4.0/)).
- **Código-Fonte de Análise e Testes (`analysis/` e `tests/`):** Licenciados sob a **Licença MIT (MIT License)** ([https://opensource.org/licenses/MIT](https://opensource.org/licenses/MIT)).

*(English)* This repository is dual-licensed according to artifact type:
- **Ontology and Cases (`ontology/` and `cases/`):** Licensed under **Creative Commons Attribution 4.0 International (CC BY 4.0)**.
- **Analysis Source Code and Tests (`analysis/` and `tests/`):** Licensed under the **MIT License**.

---

## Como citar / How to cite

[Referência do artigo omitida durante a avaliação cega — será incluída após a publicação nos anais do ISKO Brasil 2027.]

---

## Referências fundamentais

BAADER, Franz; McGUINNESS, Deborah L.; NARDI, Daniele; PATEL-SCHNEIDER, Peter F. (ed.). The description logic handbook: theory, implementation, and applications. Cambridge: Cambridge University Press, 2003.

BUCKLAND, Michael K. Information as thing. Journal of the American Society for Information Science, v. 42, n. 5, p. 351-360, jun. 1991.

GRÜNINGER, Michael; FOX, Mark S. Methodology for the design and evaluation of ontologies. In: WORKSHOP ON BASIC ONTOLOGICAL ISSUES IN KNOWLEDGE SHARING, IJCAI-95, 1995, Montreal. Proceedings [...]. Montreal, 1995.

KALYANPUR, Aditya et al. Finding all justifications of OWL DL entailments. In: ABERER, Karl et al. (ed.). The Semantic Web: ISWC 2007 + ASWC 2007. Berlin: Springer, 2007. p. 267-280. (Lecture Notes in Computer Science, 4825).

NOY, Natalya F.; McGUINNESS, Deborah L. Ontology development 101: a guide to creating your first ontology. Stanford: Stanford Knowledge Systems Laboratory, 2001. (Technical Report KSL-01-05).

ORTEGA, Cristina Dotta. Organizar para socializar: a função social da mediação documentária. Marília: Oficina Universitária; São Paulo: Cultura Acadêmica, 2024.

WARDLE, Claire; DERAKHSHAN, Hossein. Information disorder: toward an interdisciplinary framework for research and policy making. Estrasburgo: Council of Europe Publishing, 2017.

WELLISCH, Hans H. A cibernética do controle bibliográfico: para uma teoria dos sistemas de recuperação da informação. Tradução de Tarcísio Zandonade. Brasília: IBICT, 1987.

WILKINSON, Mark D. et al. The FAIR guiding principles for scientific data management and stewardship. Scientific Data, v. 3, 160018, 2016.
