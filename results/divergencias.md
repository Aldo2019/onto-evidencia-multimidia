# Relatório de Divergências entre Previsões (`cases/EXPECTED.md`) e Execução Real

**Data da verificação:** 2026-11-22  
**Raciocinador utilizado:** HermiT (via ROBOT `1.9.4`; Cenários A–C executados com OpenJDK `11.0.13`, Cenário D com OpenJDK `25.0.5`)

---

## 1. Comparação das Inferências Lógicas (OWL 2 DL / HermiT)

| Cenário | Indivíduo(s) | Esperado (`cases/EXPECTED.md`) | Obtido (`results/reasoning/<cenario>_reasoned.ttl`) | Divergência? |
| :--- | :--- | :--- | :--- | :---: |
| **Cenário A (Aberto)** | `Evidencia_Original_1_Work`, `Evidencia_Original_2_Work` | `EvidenciaMultimidia`; **não** `EvidenciaIntegra` | `EvidenciaMultimidia`; **não** `EvidenciaIntegra` | **Nenhuma** |
| **Cenário A (Fechado)** | `Evidencia_Original_1_Work`, `Evidencia_Original_2_Work`, `Evidencia_Audio_Original_1_Stereo`, `Evidencia_Audio_Original_2_Stereo` | `EvidenciaIntegra` | `EvidenciaIntegra` | **Nenhuma** |
| **Cenário B** | `Evidencia_Sintetico_1_1_Work`, `Evidencia_Sintetico_1_2_Work`, `Evidencia_Sintetico_2_1_Work`, `Evidencia_Sintetico_2_2_Work` | `EvidenciaComConteudoAlterado`; **não** `EvidenciaIntegra` | `EvidenciaComConteudoAlterado`; **não** `EvidenciaIntegra` | **Nenhuma** |
| **Cenário C** | `Evidencia_Recodificado_Mensageiro_1_Work` | `EvidenciaComCadeiaQuebrada`; **não** `EvidenciaIntegra` | `EvidenciaComCadeiaQuebrada`; **não** `EvidenciaIntegra` | **Nenhuma** |
| **Cenário D1** | `Evidencia_Original_1_Work` | inconsistente | inconsistente | **Nenhuma** |
| **Cenário D2** | `Evidencia_Original_1_Work` | `EvidenciaComConteudoAlterado`; **não** `EvidenciaIntegra` | idem | **Nenhuma** |

---

## 2. Observações Empíricas nas Análises de Sinal e Metadados

1. **Ausência de `oem:DescontinuidadeENF` nos sinais analisados:**
   - Em `video_original_1` (Cenário A), `video_sintetico_1_1` (Cenário B) e `video_recodificado_mensageiro_1` (Cenário C), o harmônico de `120 Hz` superou o limiar de SNR (`6,0 dB`) com baixa dispersão ($\sigma_{\text{norm}} \le 0{,}0529\text{ Hz}$), mas sem saltos abruptos acima de `0,08 Hz` (`0` indivíduos `oem:DescontinuidadeENF`).
   - Nos demais arquivos (`Video_original_2`, `video_sintetico_1_2`, `video_sintetico_2_1`, `video_sintetico_2_2`), a componente ENF não atingiu estabilidade acima dos limiares configurados e foi registrada como `"ENF não detectável"` sem geração de achados, conforme a regra de mundo aberto.

   | Cenário | Arquivo | SNR média em 120 Hz (estéreo / mono) | Desvio-padrão normalizado (60 Hz eq., estéreo / mono) | Descontinuidades | Fonte JSON |
   | :--- | :--- | :---: | :---: | :---: | :--- |
   | **Cenário A** | `video_original_1` | `8,995 dB` (`8,994 dB`) | `0,02238 Hz` (`0,02238 Hz`) | `0` | `results/analises/caso_a/resumo_analises.json` |
   | **Cenário B** | `video_sintetico_1_1` | `10,418 dB` (`10,419 dB`) | `0,05290 Hz` (`0,05290 Hz`) | `0` | `results/analises/caso_b/resumo_analises.json` |
   | **Cenário C** | `video_recodificado_mensageiro_1` | `8,966 dB` (`8,966 dB`) | `0,02633 Hz` (`0,02634 Hz`) | `0` | `results/analises/caso_c/resumo_analises.json` |
2. **Metadados de origem nos arquivos brutos:**
   - Todos os 6 vídeos fornecidos na pasta `Vídeos/` já apresentavam cabeçalhos MP4 sem tags `Make`, `Model` ou `encoder` e com datas internas `0000:00:00 00:00:00`. Ainda assim, a comparação estrutural quadro a quadro (`ffprobe -show_frames`) entre os vídeos do Cenário B e suas referências do Cenário A identificou de 4 a 5 indícios objetivos de recodificação (`oem:IndicioDeRecodificacao`) por arquivo.
