# Relatório de Divergências entre Previsões (`cases/EXPECTED.md`) e Execução Real

**Data da verificação:** 2026-11-17  
**Raciocinador utilizado:** HermiT (via ROBOT `1.9.4` / OpenJDK `11.0.13`)

---

## 1. Comparação das Inferências Lógicas (OWL 2 DL / HermiT)

| Cenário | Indivíduo(s) | Esperado (`cases/EXPECTED.md`) | Obtido (`results/reasoning/<cenario>_reasoned.ttl`) | Divergência? |
| :--- | :--- | :--- | :--- | :---: |
| **Caso A (Aberto)** | `Evidencia_Original_1_Work`, `Evidencia_Original_2_Work` | `EvidenciaMultimidia`; **não** `EvidenciaIntegra` | `EvidenciaMultimidia`; **não** `EvidenciaIntegra` | **Nenhuma** |
| **Caso A (Fechado)** | `Evidencia_Original_1_Work`, `Evidencia_Original_2_Work`, `Evidencia_Audio_Original_1_Stereo`, `Evidencia_Audio_Original_2_Stereo` | `EvidenciaIntegra` | `EvidenciaIntegra` | **Nenhuma** |
| **Caso B** | `Evidencia_Sintetico_1_1_Work`, `Evidencia_Sintetico_1_2_Work`, `Evidencia_Sintetico_2_1_Work`, `Evidencia_Sintetico_2_2_Work` | `EvidenciaComConteudoAlterado`; **não** `EvidenciaIntegra` | `EvidenciaComConteudoAlterado`; **não** `EvidenciaIntegra` | **Nenhuma** |
| **Caso C** | `Evidencia_Recodificado_Mensageiro_1_Work` | `EvidenciaComCadeiaQuebrada`; **não** `EvidenciaIntegra` | `EvidenciaComCadeiaQuebrada`; **não** `EvidenciaIntegra` | **Nenhuma** |

---

## 2. Observações Empíricas nas Análises de Sinal e Metadados (Prompts 12–14)

1. **Ausência de `oem:DescontinuidadeENF` nos sinais analisados:**
   - Em `video_original_1` (Caso A), `video_sintetico_1_1` (Caso B) e `video_recodificado_mensageiro_1` (Caso C), o harmônico de `120 Hz` superou o limiar de SNR (`6,0 dB`) com baixa dispersão ($\sigma_{\text{norm}} \le 0{,}0529\text{ Hz}$), mas sem saltos abruptos acima de `0,08 Hz` (`0` indivíduos `oem:DescontinuidadeENF`).
   - Nos demais arquivos (`Video_original_2`, `video_sintetico_1_2`, `video_sintetico_2_1`, `video_sintetico_2_2`), a componente ENF não atingiu estabilidade acima dos limiares configurados e foi registrada como `"ENF não detectável"` sem geração de achados, conforme a regra de mundo aberto.
2. **Metadados de origem nos arquivos brutos:**
   - Todos os 6 vídeos fornecidos na pasta `Vídeos/` já apresentavam cabeçalhos MP4 sem tags `Make`, `Model` ou `encoder` e com datas internas `0000:00:00 00:00:00`. Ainda assim, a comparação estrutural quadro a quadro (`ffprobe -show_frames`) entre os vídeos do Caso B e suas referências do Caso A identificou de 4 a 5 indícios objetivos de recodificação (`oem:IndicioDeRecodificacao`) por arquivo.
