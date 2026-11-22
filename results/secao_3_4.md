# Seção 3.4 — Resultados Experimentais e Verificação Formal com HermiT

*Nota: Todos os resultados, justificações formais e métricas reportados abaixo foram extraídos exclusivamente dos arquivos gerados em `results/reasoning/`, `results/explanations/`, `results/metrics/` e `results/analises/`.*

---

## 1. Comportamento Inferencial por Cenário (HermiT / ROBOT 1.9.4)

**Cenário A (Aberto — `caso_a_aberto_reasoned.ttl`):** No cenário aberto do Cenário A, em que as cópias de trabalho `oem:Evidencia_Original_1_Work` e `oem:Evidencia_Original_2_Work` resultam de transformações isomórficas (`oem:CopiaForense_video_original_1` e `oem:CopiaForense_Video_original_2`) verificadas por hash SHA-256 (`3abe9633...` e `08945ba4...`) e vinculadas aos respectivos registros de custódia (`oem:RegistroCustodia_video_original_1` e `oem:RegistroCustodia_Video_original_2`), o raciocinador HermiT inferiu que ambas as operações pertencem às classes `oem:TransformacaoPreservadora`, `oem:TransformacaoDeclarada` e `oem:TransformacaoPreservadoraDeclarada`, bem como inferiu a propriedade inversa `oem:sofreu` ligando cada cópia à sua transformação e classificou os exames acústicos (`ENF detectável` em 120 Hz com $\text{SNR} = 8{,}995\text{ dB}$ para o vídeo 1; `ENF não detectável` para o vídeo 2) e de espectrograma como `oem:TransformacaoPreservadoraDeclarada`. Contudo, sob a pressuposição de mundo aberto (OWA), na ausência de um axioma de fechamento universal sobre a propriedade `oem:sofreu`, o HermiT **não inferiu** `oem:EvidenciaIntegra` (nem `oem:EvidenciaComConteudoAlterado` ou `oem:EvidenciaComCadeiaQuebrada`) para `oem:Evidencia_Original_1_Work` ou `oem:Evidencia_Original_2_Work`, mantendo-as apenas como instâncias de `oem:EvidenciaMultimidia`.

**Cenário A (Fechado — `caso_a_fechado_reasoned.ttl`):** Quando se adicionam os axiomas de fechamento pericial de `cases/caso_a/caso_a_fechado.ttl` — que restringem universalmente a propriedade `oem:sofreu` de cada artefato às transformações declaradas em seu percurso documentado —, o HermiT **inferiu** `oem:EvidenciaIntegra` para as cópias de vídeo `oem:Evidencia_Original_1_Work` e `oem:Evidencia_Original_2_Work`, bem como para as trilhas de áudio extraídas sem reamostragem `oem:Evidencia_Audio_Original_1_Stereo` e `oem:Evidencia_Audio_Original_2_Stereo`. Em virtude dos axiomas de disjunção da TBox (`oem:EvidenciaIntegra owl:disjointWith oem:EvidenciaComConteudoAlterado, oem:EvidenciaComCadeiaQuebrada`), o raciocinador também garantiu a consistência lógica de que nenhuma dessas evidências pertence às classes de conteúdo alterado ou de cadeia quebrada, independentemente de o exame de ENF do segundo vídeo ter resultado em `"ENF não detectável"`.

**Cenário B (`caso_b_reasoned.ttl`):** No Cenário B, correspondente às quatro cópias de trabalho dos vídeos sintéticos (`oem:Evidencia_Sintetico_1_1_Work`, `oem:Evidencia_Sintetico_1_2_Work`, `oem:Evidencia_Sintetico_2_1_Work` e `oem:Evidencia_Sintetico_2_2_Work`), cujas aquisições posteriores em laboratório e extrações de áudio/espectrograma foram devidamente registradas na cadeia de custódia e cujos exames de contêiner e GOP (`ffprobe -show_frames`) registraram entre 4 e 5 indivíduos de `oem:IndicioDeRecodificacao` por arquivo, a presença das transformações de origem `oem:SinteseDeepfake_1_1` a `oem:SinteseDeepfake_2_2` (`rdf:type oem:TransformacaoGenerativa`) levou o HermiT a **inferir** a classificação `oem:EvidenciaComConteudoAlterado` para os quatro vídeos. O HermiT **não inferiu** `oem:EvidenciaIntegra` para nenhum dos quatro itens (e, pela disjunção entre `oem:TransformacaoPreservadora` e `oem:TransformacaoGenerativa`, qualquer tentativa de fechar o percurso como inteiramente preservador resultaria em inconsistência lógica), além de **não inferir** conclusões de adulteração a partir da mera ausência de ENF nos arquivos `1_2`, `2_1` e `2_2` (`"ENF não detectável"`).

**Cenário C (`caso_c_reasoned.ttl`):** No Cenário C, referente ao vídeo recodificado por transmissão de aplicativo de mensageria (`oem:Evidencia_Recodificado_Mensageiro_1_Work`, SHA-256 `361fa834...`), o exame de contêiner/GOP gerou 4 indivíduos de subclasse de `oem:IndicioDeRecodificacao` (mudança de resolução `478x850` $\rightarrow$ `476x848`, inserção de 153 quadros `B`, alteração de `time_base` para `1/15360` e redução de bitrate de vídeo em `41,9%` e de áudio em `70,1%`), e a transformação `oem:TransmissaoMensageiro_video_1` foi declarada com restrição de cardinalidade máxima zero para registros de custódia (`oem:registradaEm max 0 oem:RegistroDeCustodia`). A partir dessa afirmação explícita de ausência de registro, o HermiT **inferiu** que `oem:TransmissaoMensageiro_video_1` pertence a `oem:TransformacaoNaoDeclarada` e classificou `oem:Evidencia_Recodificado_Mensageiro_1_Work` como `oem:EvidenciaComCadeiaQuebrada`. O raciocinador **não inferiu** `oem:EvidenciaIntegra` nem `oem:EvidenciaComConteudoAlterado`, distinguindo formalmente a quebra de cadeia de custódia por recompressão não documentada da síntese generativa do Cenário B.

---

## 2. Justificações Mínimas das Classificações (`results/explanations/`)

### 2.1. Cenário A (Aberto): Classificação da Cópia Forense como `TransformacaoPreservadoraDeclarada` (sem inferir `EvidenciaIntegra` para a evidência)
- **Lógica Descritiva (DL):**
  $$\begin{aligned}
  \mathcal{J}_{A\text{-aberto}} = \{ & \mathsf{CopiaForense\_video\_original\_1} : \mathsf{TransformacaoIsomorfica}, \\
  & (\mathsf{CopiaForense\_video\_original\_1}, \mathsf{RegistroCustodia\_video\_original\_1}) : \mathsf{registradaEm}, \\
  & \mathsf{RegistroCustodia\_video\_original\_1} : \mathsf{RegistroDeCustodia}, \\
  & \mathsf{TransformacaoIsomorfica} \sqsubseteq \mathsf{TransformacaoPreservadora}, \\
  & \top \sqsubseteq \forall \mathsf{registradaEm}^{-}.\mathsf{Transformacao}, \\
  & \mathsf{TransformacaoDeclarada} \equiv \mathsf{Transformacao} \sqcap \exists \mathsf{registradaEm}.\mathsf{RegistroDeCustodia}, \\
  & \mathsf{TransformacaoPreservadoraDeclarada} \equiv \mathsf{TransformacaoPreservadora} \sqcap \mathsf{TransformacaoDeclarada} \} \\
  \models\; & \mathsf{CopiaForense\_video\_original\_1} : \mathsf{TransformacaoPreservadoraDeclarada}
  \end{aligned}$$
  *(Como não há axioma $\mathsf{Evidencia\_Original\_1\_Work} : \forall \mathsf{sofreu}.\mathsf{TransformacaoPreservadoraDeclarada}$, não se deriva $\mathsf{Evidencia\_Original\_1\_Work} : \mathsf{EvidenciaIntegra}$).*
- **Manchester OWL Syntax:**
  ```manchester
  Individual: oem:CopiaForense_video_original_1
      Types: oem:TransformacaoIsomorfica
      Facts: oem:registradaEm oem:RegistroCustodia_video_original_1
  Class: oem:TransformacaoIsomorfica
      SubClassOf: oem:TransformacaoPreservadora
  Class: oem:TransformacaoDeclarada
      EquivalentTo: oem:Transformacao and (oem:registradaEm some oem:RegistroDeCustodia)
  Class: oem:TransformacaoPreservadoraDeclarada
      EquivalentTo: oem:TransformacaoDeclarada and oem:TransformacaoPreservadora
  => Entailment: {oem:CopiaForense_video_original_1} SubClassOf: oem:TransformacaoPreservadoraDeclarada
  ```

### 2.2. Cenário A (Fechado): Inferência de `EvidenciaIntegra` (`explain_caso_a_fechado.md`)
- **Lógica Descritiva (DL):**
  $$\begin{aligned}
  \mathcal{J}_{A\text{-fechado}} = \{ & \mathsf{Evidencia\_Original\_1\_Work} : \mathsf{EvidenciaMultimidia}, \\
  & (\mathsf{CopiaForense\_video\_original\_1}, \mathsf{Evidencia\_Original\_1\_Work}) : \mathsf{temSaida}, \\
  & \mathsf{sofreu} \equiv \mathsf{temSaida}^{-}, \\
  & \mathsf{Evidencia\_Original\_1\_Work} : \forall \mathsf{sofreu}.\{\mathsf{CopiaForense\_video\_original\_1}\}, \\
  & \mathsf{CopiaForense\_video\_original\_1} : \mathsf{TransformacaoIsomorfica}, \\
  & (\mathsf{CopiaForense\_video\_original\_1}, \mathsf{RegistroCustodia\_video\_original\_1}) : \mathsf{registradaEm}, \\
  & \mathsf{RegistroCustodia\_video\_original\_1} : \mathsf{RegistroDeCustodia}, \\
  & \mathsf{TransformacaoIsomorfica} \sqsubseteq \mathsf{TransformacaoPreservadora}, \\
  & \mathsf{TransformacaoDeclarada} \equiv \mathsf{Transformacao} \sqcap \exists \mathsf{registradaEm}.\mathsf{RegistroDeCustodia}, \\
  & \mathsf{TransformacaoPreservadoraDeclarada} \equiv \mathsf{TransformacaoPreservadora} \sqcap \mathsf{TransformacaoDeclarada}, \\
  & \mathsf{EvidenciaIntegra} \equiv \mathsf{EvidenciaMultimidia} \sqcap \exists \mathsf{sofreu}.\mathsf{TransformacaoPreservadoraDeclarada} \\
  & \qquad\qquad\qquad\qquad\quad \sqcap \forall \mathsf{sofreu}.\mathsf{TransformacaoPreservadoraDeclarada} \} \\
  \models\; & \mathsf{Evidencia\_Original\_1\_Work} : \mathsf{EvidenciaIntegra}
  \end{aligned}$$
- **Manchester OWL Syntax:**
  ```manchester
  Individual: oem:Evidencia_Original_1_Work
      Types: oem:EvidenciaMultimidia,
             oem:sofreu only {oem:CopiaForense_video_original_1}
  Individual: oem:CopiaForense_video_original_1
      Types: oem:TransformacaoIsomorfica
      Facts: oem:temSaida oem:Evidencia_Original_1_Work,
             oem:registradaEm oem:RegistroCustodia_video_original_1
  Individual: oem:RegistroCustodia_video_original_1
      Types: oem:RegistroDeCustodia
  ObjectProperty: oem:sofreu
      InverseOf: oem:temSaida
  Class: oem:EvidenciaIntegra
      EquivalentTo: oem:EvidenciaMultimidia
                    and (oem:sofreu some oem:TransformacaoPreservadoraDeclarada)
                    and (oem:sofreu only oem:TransformacaoPreservadoraDeclarada)
  => Entailment: {oem:Evidencia_Original_1_Work} SubClassOf: oem:EvidenciaIntegra
  ```

### 2.3. Cenário B: Inferência de `EvidenciaComConteudoAlterado` (`explain_caso_b.md`)
- **Lógica Descritiva (DL):**
  $$\begin{aligned}
  \mathcal{J}_{B} = \{ & \mathsf{SinteseDeepfake\_1\_1} : \mathsf{TransformacaoGenerativa}, \\
  & (\mathsf{SinteseDeepfake\_1\_1}, \mathsf{Evidencia\_Sintetico\_1\_1\_Work}) : \mathsf{temSaida}, \\
  & \mathsf{sofreu} \equiv \mathsf{temSaida}^{-}, \quad \top \sqsubseteq \forall \mathsf{sofreu}^{-}.\mathsf{EvidenciaMultimidia}, \\
  & \mathsf{EvidenciaComConteudoAlterado} \equiv \mathsf{EvidenciaMultimidia} \sqcap \exists \mathsf{sofreu}.\mathsf{TransformacaoGenerativa} \} \\
  \models\; & \mathsf{Evidencia\_Sintetico\_1\_1\_Work} : \mathsf{EvidenciaComConteudoAlterado}
  \end{aligned}$$
- **Manchester OWL Syntax:**
  ```manchester
  Individual: oem:SinteseDeepfake_1_1
      Types: oem:TransformacaoGenerativa
      Facts: oem:temSaida oem:Evidencia_Sintetico_1_1_Work
  ObjectProperty: oem:sofreu
      InverseOf: oem:temSaida
      Domain: oem:EvidenciaMultimidia
  Class: oem:EvidenciaComConteudoAlterado
      EquivalentTo: oem:EvidenciaMultimidia and (oem:sofreu some oem:TransformacaoGenerativa)
  => Entailment: {oem:Evidencia_Sintetico_1_1_Work} SubClassOf: oem:EvidenciaComConteudoAlterado
  ```

### 2.4. Cenário C: Inferência de `EvidenciaComCadeiaQuebrada` (`explain_caso_c.md`)
- **Lógica Descritiva (DL):**
  $$\begin{aligned}
  \mathcal{J}_{C} = \{ & \mathsf{Evidencia\_Recodificado\_Mensageiro\_1\_Work} : \mathsf{EvidenciaMultimidia}, \\
  & (\mathsf{Evidencia\_Recodificado\_Mensageiro\_1\_Work}, \mathsf{TransmissaoMensageiro\_video\_1}) : \mathsf{sofreu}, \\
  & \top \sqsubseteq \forall \mathsf{sofreu}.\mathsf{Transformacao}, \\
  & \mathsf{TransmissaoMensageiro\_video\_1} : (\leqslant 0\,\mathsf{registradaEm}.\mathsf{RegistroDeCustodia}), \\
  & \mathsf{TransformacaoNaoDeclarada} \equiv \mathsf{Transformacao} \sqcap (\leqslant 0\,\mathsf{registradaEm}.\mathsf{RegistroDeCustodia}), \\
  & \mathsf{EvidenciaComCadeiaQuebrada} \equiv \mathsf{EvidenciaMultimidia} \sqcap \exists \mathsf{sofreu}.\mathsf{TransformacaoNaoDeclarada} \} \\
  \models\; & \mathsf{Evidencia\_Recodificado\_Mensageiro\_1\_Work} : \mathsf{EvidenciaComCadeiaQuebrada}
  \end{aligned}$$
- **Manchester OWL Syntax:**
  ```manchester
  Individual: oem:Evidencia_Recodificado_Mensageiro_1_Work
      Types: oem:EvidenciaMultimidia
      Facts: oem:sofreu oem:TransmissaoMensageiro_video_1
  Individual: oem:TransmissaoMensageiro_video_1
      Types: oem:registradaEm max 0 oem:RegistroDeCustodia
  ObjectProperty: oem:sofreu
      Range: oem:Transformacao
  Class: oem:TransformacaoNaoDeclarada
      EquivalentTo: oem:Transformacao and (oem:registradaEm max 0 oem:RegistroDeCustodia)
  Class: oem:EvidenciaComCadeiaQuebrada
      EquivalentTo: oem:EvidenciaMultimidia and (oem:sofreu some oem:TransformacaoNaoDeclarada)
  => Entailment: {oem:Evidencia_Recodificado_Mensageiro_1_Work} SubClassOf: oem:EvidenciaComCadeiaQuebrada
  ```

---

## 3. Quadro-Resumo para o Artigo

| Cenário | Transformações no Percurso | Fechamento / Custódia | Inferência do HermiT | NÃO Inferido pelo HermiT |
| :--- | :--- | :--- | :--- | :--- |
| **Cenário A (Aberto)** | Isomórfica (SHA-256) + Homomórficas (WAV, PSD, ENF, GOP) | `registradaEm` presente; sem fechamento $\forall \mathsf{sofreu}$ (OWA) | `EvidenciaMultimidia`; transformações em `TransformacaoPreservadoraDeclarada` | `EvidenciaIntegra`, `EvidenciaComConteudoAlterado`, `EvidenciaComCadeiaQuebrada` |
| **Cenário A (Fechado)** | Isomórfica (SHA-256) + Homomórficas (WAV, PSD, ENF, GOP) | `registradaEm` presente + axioma $\forall \mathsf{sofreu}.\{t_1,\dots,t_n\}$ | **`EvidenciaIntegra`** (`video_original_1`, `Video_original_2` e `.wav` estéreo) | `EvidenciaComConteudoAlterado`, `EvidenciaComCadeiaQuebrada` |
| **Cenário B (Deepfake)** | Generativa (`TransformacaoGenerativa`) + Aquisição/Exames | Síntese generativa no percurso (`SinteseDeepfake_*`) | **`EvidenciaComConteudoAlterado`** (`video_sintetico_1_1` a `2_2`) | `EvidenciaIntegra` (disjunta de conteúdo alterado) |
| **Cenário C (Mensageiro)** | Recodificação com perdas (`RecodificacaoDeTransmissao`) | Sem registro explícito (`registradaEm max 0 RegistroDeCustodia`) | **`EvidenciaComCadeiaQuebrada`** (`video_recodificado_mensageiro_1`) | `EvidenciaIntegra`, `EvidenciaComConteudoAlterado` |
| **Cenário D1 (Contradição)** | Isomórfica (`CopiaForense_video_original_1`) + Generativa (`t_g`, registro de terceiro) | Fechamento original $\forall \mathsf{sofreu}.\{\mathsf{CopiaForense\_video\_original\_1}\}$ (sem `t_g`) | **INCONSISTENTE** ($\top \sqsubseteq \bot$; 6 axiomas em `saidas/D1_explicacao.md`) | Classificação inviável por contradição lógica |
| **Cenário D2 (Controle)** | Isomórfica (`CopiaForense_video_original_1`) + Generativa (`t_g`, registro de terceiro) | Sem fechamento (OWA) | **Consistente**; **`EvidenciaComConteudoAlterado`** (`Evidencia_Original_1_Work`) | `EvidenciaIntegra` |

---

## 4. Números Citáveis da Ontologia e da Execução (`results/metrics/`)

- **Métricas da TBox (`ontology/oem.ttl` — `oem_tbox_metrics.json`):**
  - **Perfil OWL 2 DL:** Válido (`owl2_dl: true`, `0` violações de perfil)
  - **Número de classes (`class_count`):** `33` classes na TBox (`35` nos grafos mesclados com `owl:Thing` e tipos auxiliares)
  - **Número de propriedades de objeto (`obj_property_count`):** `10`
  - **Número de propriedades de dados (`dataproperty_count`):** `22`
  - **Número de propriedades de anotação (`annotation_property_count`):** `2` (`rdfs:label`, `skos:definition`)
  - **Total de propriedades:** `34` (`10` de objeto + `22` de dados + `2` de anotação)
  - **Axiomas lógicos na TBox (`logical_axiom_count`):** `104` (`102` axiomas de TBox + `2` axiomas de RBox; `386` axiomas totais incluindo `216` anotações e `66` declarações)
- **Métricas por Cenário Raciocinado (`*_metrics.json`) e Tempos Reais de Classificação (HermiT via ROBOT 1.9.4):**
  - **Ambiente Java:** Cenários A–C executados com OpenJDK `11.0.13`; Cenário D com OpenJDK `25.0.5`.
  - **Expressividade em Lógica Descritiva:**
    - TBox, Cenário A (Aberto), Cenário B e Cenário C: $\mathcal{ALCIQ}(\mathbf{D})$ (reportado pelo OWLAPI/ROBOT como `RRESTRCUCINTUNIVRESTREIQ(D)`; o código `RRESTR` do OWLAPI indica restrições de domínio/imagem, não composição de papéis ($\mathcal{R}$))
    - Cenário A (Fechado) e Cenário D1 (com nominais `owl:oneOf` no axioma de fechamento): $\mathcal{ALCOIQ}(\mathbf{D})$ (reportado pelo OWLAPI/ROBOT como `RRESTRCUCINTUNIVRESTREOIQ(D)`)
  - **Cenário A (Aberto):** `65` indivíduos, `564` axiomas lógicos (`1.077` totais), tempo de classificação = **`1.234 ms`** (`1,23 s`)
  - **Cenário A (Fechado):** `65` indivíduos, `572` axiomas lógicos (`1.085` totais), tempo de classificação = **`2.836 ms`** (`2,84 s`)
  - **Cenário B:** `153` indivíduos, `1.076` axiomas lógicos (`1.885` totais), tempo de classificação = **`1.476 ms`** (`1,48 s`)
  - **Cenário C:** `15` indivíduos, `237` axiomas lógicos (`564` totais), tempo de classificação = **`1.119 ms`** (`1,12 s`)
  - **Cenário D1 (com fechamento):** detecção de inconsistência em **`1.690 ms`** (`robot reason`) e justificação mínima em **`2.124 ms`** (`robot explain --mode inconsistency`)
  - **Cenário D2 (controle, sem fechamento):** classificação consistente em **`2.034 ms`** (`robot reason`)

---

## 5. Testes de conformidade

Nos cenários avaliados, as classificações obtidas coincidiram com as deduzidas dos axiomas (`cases/EXPECTED.md`). Esses resultados verificam a coerência do modelo com suas definições; não constituem validação empírica da classificação.

---

## 6. Cenário D (Detecção de Contradição — D1 e D2)

O **Cenário D** avalia o comportamento da ontologia diante de uma transformação generativa declarada por terceiro (`oem:t_g`, `rdf:type oem:TransformacaoGenerativa`, `oem:temSaida oem:Evidencia_Original_1_Work`, `oem:registradaEm oem:RegistroCustodia_Terceiro`) aplicada sobre a evidência única `oem:Evidencia_Original_1_Work` (`video_original_1.mp4`), sem alteração de `ontology/oem.ttl` nem das ABoxes dos Cenários A–C:

- **Variante D1 (com fechamento — `abox/caso_D1.ttl` → `saidas/D1_explicacao.md`):** mantém o axioma de fechamento original ($\forall \mathsf{sofreu}.\{\mathsf{CopiaForense\_video\_original\_1}\}$), sem incluir `oem:t_g`. O HermiT detectou **ontologia inconsistente** ($\top \sqsubseteq \bot$, `1.690 ms`), com justificação mínima composta por exatamente **6 axiomas**: `t_g Type TransformacaoGenerativa`, `sofreu InverseOf temSaida`, `CopiaForense_video_original_1 Type TransformacaoIsomorfica`, `Evidencia_Original_1_Work Type sofreu only ({CopiaForense_video_original_1})`, `t_g temSaida Evidencia_Original_1_Work` e `DisjointClasses(TransformacaoGenerativa, TransformacaoHomomorfica, TransformacaoIsomorfica)`.
- **Variante D2 (controle, sem fechamento — `abox/caso_D2.ttl` → `saidas/D2_classificacao.ttl`):** idêntica a D1, porém sem o axioma de fechamento. A ontologia permaneceu **consistente** (`2.034 ms`), e o HermiT classificou `oem:Evidencia_Original_1_Work` como **`oem:EvidenciaComConteudoAlterado`** (e **não** como `oem:EvidenciaIntegra`).
