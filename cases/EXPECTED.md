# Previsões Formais de Classificação (HermiT / OWL 2 DL)

| Cenário | Indivíduo Avaliado | Deve ser inferido (`rdf:type`) | NÃO deve ser inferido (`rdf:type`) |
| :--- | :--- | :--- | :--- |
| **Caso A (Aberto)** | `oem:Evidencia_Original_1_Work`, `oem:Evidencia_Original_2_Work` | `oem:EvidenciaMultimidia` (e `oem:CopiaForense_*` $\in$ `oem:TransformacaoPreservadoraDeclarada`) | `oem:EvidenciaIntegra`, `oem:EvidenciaComConteudoAlterado`, `oem:EvidenciaComCadeiaQuebrada` |
| **Caso A (Fechado)** | `oem:Evidencia_Original_1_Work`, `oem:Evidencia_Original_2_Work`, `oem:Evidencia_Audio_Original_1_Stereo`, `oem:Evidencia_Audio_Original_2_Stereo` | `oem:EvidenciaIntegra`, `oem:EvidenciaMultimidia` | `oem:EvidenciaComConteudoAlterado`, `oem:EvidenciaComCadeiaQuebrada` |
| **Caso B** | `oem:Evidencia_Sintetico_1_1_Work`, `oem:Evidencia_Sintetico_1_2_Work`, `oem:Evidencia_Sintetico_2_1_Work`, `oem:Evidencia_Sintetico_2_2_Work` | `oem:EvidenciaComConteudoAlterado`, `oem:EvidenciaMultimidia` | `oem:EvidenciaIntegra` |
| **Caso C** | `oem:Evidencia_Recodificado_Mensageiro_1_Work` | `oem:EvidenciaComCadeiaQuebrada`, `oem:EvidenciaMultimidia` (e `oem:TransmissaoMensageiro_video_1` $\in$ `oem:TransformacaoNaoDeclarada`) | `oem:EvidenciaIntegra` |
