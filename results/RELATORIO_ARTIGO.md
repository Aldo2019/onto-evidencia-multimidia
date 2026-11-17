# Relatório de resultados — ontologia de evidência multimídia

- **Data de geração:** `2026-11-17` [`results/analises/resumo_geral_analises.json`]
- **Commit atual do git (hash curto):** `NÃO ENCONTRADO` (repositório Git não inicializado; `git` ausente no `PATH`, protegido por `.gitignore`) [`.gitignore`]
- **Versões:** Java `OpenJDK 11.0.13+8-LTS` (e `1.8.0_511`), ROBOT `1.9.4` (`tools/robot.jar`), HermiT `1.4.3.456`, Python `3.12.5` (`NumPy 1.26.4`, `SciPy 1.17.1`, `Matplotlib 3.8.4`, `rdflib 7.6.0`, `pytest 7.4.4`), `ffmpeg`/`ffprobe` `8.1.1-full_build-www.gyan.dev`, `exiftool` `13.59` [`results/inventario.md`, `results/secao_3_4.md`, `tests/test_reasoning.py`].

## 1. Corpus de casos

| caso | arquivo (nome) | papel (original/cópia/sintético/recodificado) | contêiner | codec vídeo/áudio | duração | resolução/fps | tem áudio? | SHA-256 (abreviado) |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Caso A** | `video_original_1.mp4` | original (matriz) e cópia (`data/work/caso_a/`) | `mp42` (`mp42isom`) | `h264` (`High@L3.1`) / `aac` (`LC`, `48000 Hz`, `2 ch`) | `7.246688 s` | `478x850` / `30/1` | sim | `3abe96337aefc4c4…` [`results/inventario.csv`] |
| **Caso A** | `Video_original_2.mp4` | original (matriz) e cópia (`data/work/caso_a/`) | `mp42` (`mp42isom`) | `h264` (`High@L3.1`) / `aac` (`LC`, `44100 Hz`, `2 ch`) | `62.566667 s` | `576x1024` / `30/1` | sim | `08945ba4c6ca34b1…` [`results/inventario.csv`] |
| **Caso B** | `video_sintetico_1_1.mp4` | sintético (matriz e cópia em `data/work/caso_b/`) | `mp42` (`mp42isom`) | `h264` (`High@L3.1`) / `aac` (`LC`, `48000 Hz`, `2 ch`) | `10.026667 s` | `848x478` / `24/1` | sim | `11fc8dfd6061cda1…` [`results/inventario.csv`] |
| **Caso B** | `video_sintetico_1_2.mp4` | sintético (matriz e cópia em `data/work/caso_b/`) | `mp42` (`mp42isom`) | `h264` (`High@L3.1`) / `aac` (`LC`, `48000 Hz`, `2 ch`) | `10.026667 s` | `848x478` / `24/1` | sim | `a55dc991a06c7811…` [`results/inventario.csv`] |
| **Caso B** | `video_sintetico_2_1.mp4` | sintético (matriz e cópia em `data/work/caso_b/`) | `mp42` (`mp42isom`) | `h264` (`High@L3.1`) / `aac` (`LC`, `44100 Hz`, `2 ch`) | `16.678563 s` | `478x850` / `30/1` | sim | `843837539c8aa52c…` [`results/inventario.csv`] |
| **Caso B** | `video_sintetico_2_2.mp4` | sintético (matriz e cópia em `data/work/caso_b/`) | `mp42` (`mp42isom`) | `h264` (`High@L3.1`) / `aac` (`LC`, `44100 Hz`, `2 ch`) | `12.985104 s` | `476x848` / `30/1` | sim | `9e361c539f2ae782…` [`results/inventario.csv`] |
| **Caso C** | `video_recodificado_mensageiro_1.mp4` | recodificado sem custódia (`data/work/caso_c/`) | `isom` (`isomiso2avc1mp41`) | `h264` (`Main@L3.1`) / `aac` (`LC`, `44100 Hz`, `2 ch`) | `7.246009 s` | `476x848` / `30/1` | sim | `361fa834338c76bb…` [`results/analises/caso_c/resumo_analises.json`] |

- **`cases/PROTOCOLO.md`:** `NÃO ENCONTRADO`; conforme os registros de custódia, o **Caso A** foi produzido por bloqueio somente leitura das matrizes originais e cópia forense bit a bit [`cases/caso_a/registro_custodia.csv`], o **Caso B** por síntese neural (deepfake de rosto/voz) seguida de cópia forense bit a bit para análise [`cases/caso_b/registro_custodia.csv`], e o **Caso C** por recodificação com perdas (`libx264 Main@L3.1, CRF 28, 476x848, AAC 96k, -map_metadata -1`) sem registro de custódia [`cases/caso_c/registro_custodia.csv`].

## 2. Ontologia (TBox)

- **Métricas da TBox (`ontology/oem.ttl`):** `33` classes (`35` nos grafos mesclados), `10` propriedades de objeto (`22` de dados e `2` de anotação), `104` axiomas lógicos (`386` axiomas totais); expressividade DL `RRESTRCUCINTUNIVRESTREIQ(D)` ($\mathcal{ALCRIQ}(\mathbf{D})$) na TBox/Casos A-aberto, B, C e `RRESTRCUCINTUNIVRESTREOIQ(D)` ($\mathcal{ALCOIQ}(\mathbf{D})$) no Caso A-fechado [`results/metrics/oem_tbox_metrics.json`, `results/metrics/caso_a_fechado_metrics.json`].
- **Perfil OWL 2 DL e Consistência:** Válido (`owl2_dl: true`, `0` violações em `results/reasoning/profile_tbox.txt`), consistente sob o HermiT, `0` classes insatisfatíveis [`results/metrics/oem_tbox_metrics.json`, `tests/test_reasoning.py`].
- **Classes acrescentadas (`rdfs:subClassOf oem:TransformacaoHomomorfica` e `oem:IndicioDeEdicao`) com `skos:definition` `@pt` [`ontology/oem.ttl`]:**
  - `oem:ExtracaoDeAudio`: *"Operação homomórfica que separa e decodifica a trilha sonora de um vídeo para áudio PCM sem reamostragem."*
  - `oem:GeracaoDeEspectrograma`: *"Operação homomórfica que calcula e representa graficamente a densidade espectral de potência de um áudio ao longo do tempo."*
  - `oem:ExtracaoDeCurvaENF`: *"Operação homomórfica que isola a variação temporal da frequência da rede elétrica (60 Hz ou 120 Hz) presente no áudio."*
  - `oem:ExameENF`: *"Exame pericial acústico que verifica a presença e a continuidade do zumbido da rede elétrica brasileira (60 Hz e harmônico de 120 Hz)."*
  - `oem:ExameMetadadosContainerGOP`: *"Exame pericial que inspeciona cabeçalhos do arquivo de vídeo e a sequência de quadros I, P e B em comparação com uma referência."*
  - `oem:DescontinuidadeENF`: *"Mudança brusca na frequência da rede elétrica captada na gravação, indicando possível ponto de corte ou inserção no áudio."*
  - `oem:IndicioDeRecodificacao`: *"Divergência nos parâmetros de compressão ou contêiner que aponta que o vídeo ou áudio foi salvo ou comprimido novamente após a captura original."*
  - `oem:DivergenciaDeResolucaoOuOrientacao`: *"Alteração nas dimensões em pixels (largura e altura) ou na orientação espacial do vídeo em comparação com a gravação de referência."*
  - `oem:DivergenciaDeTaxaDeQuadros`: *"Mudança na quantidade de quadros exibidos por segundo (fps) em relação ao vídeo original de referência."*
  - `oem:DivergenciaDeEstruturaGOP`: *"Alteração no padrão de agrupamento de quadros (I, P e B) da compressão de vídeo, indicando que o fluxo visual foi recodificado."*
  - `oem:DivergenciaDeTimeBaseVideo`: *"Diferença na escala de relógio interno usada para marcar o tempo dos quadros de vídeo no contêiner multimídia."*
  - `oem:InconsistenciaSampleRateTimeBaseAudio`: *"Descompasso interno no contêiner em que a escala de tempo da trilha sonora não coincide com a taxa de amostragem do áudio."*
  - `oem:DivergenciaDeBitrate`: *"Variação acentuada no volume de dados por segundo (bitrate) do vídeo ou do áudio em relação à gravação de referência."*

## 3. Cadeia de custódia e transformações declaradas

Registros atestados pelo indivíduo `Agente (perito)` [`cases/caso_a/caso_a.ttl`, `cases/caso_b/caso_b.ttl`, `cases/caso_c/caso_c.ttl`].

| Caso | transformação | tipo (isomórfica/homomórfica/generativa) | declarada? (sim/não) | evidência de verificação (hash antes = depois?) | registro de custódia |
| :--- | :--- | :---: | :---: | :--- | :--- |
| **Caso A** | `oem:CopiaForense_video_original_1` | isomórfica | sim | **Sim:** `3abe96337aefc4c4…` = `3abe96337aefc4c4…` | `oem:RegistroCustodia_video_original_1` [`cases/caso_a/registro_custodia.csv`] |
| **Caso A** | `oem:CopiaForense_Video_original_2` | isomórfica | sim | **Sim:** `08945ba4c6ca34b1…` = `08945ba4c6ca34b1…` | `oem:RegistroCustodia_Video_original_2` [`cases/caso_a/registro_custodia.csv`] |
| **Caso A** | `oem:ExtracaoDeAudio_video_original_1_Stereo` e `_Mono` | homomórfica | sim | derivado (`d27bfdc4192ba097…` / `8b52f679d55902d2…`) | `oem:RegistroCustodia_ExtracaoAudio_video_original_1_Stereo` / `_Mono` [`cases/caso_a/caso_a.ttl`] |
| **Caso A** | `oem:ExtracaoDeAudio_Video_original_2_Stereo` e `_Mono` | homomórfica | sim | derivado (`b6e69d2adea58667…` / `1c412c5fa7fd8fc7…`) | `oem:RegistroCustodia_ExtracaoAudio_Video_original_2_Stereo` / `_Mono` [`cases/caso_a/caso_a.ttl`] |
| **Caso A** | `oem:GeracaoEspectrograma_*` (4), `oem:ExameENF_*` (4), `oem:ExameContainerGOP_*` (2) | homomórfica | sim | derivados verificados (`1b8aa84ea920ee26…`, `193f4e0781675ee4…`, `89090b9968c27973…`, `0a056253877e36d6…`, `9ec75d04a4948440…`) | `oem:RegistroCustodia_Espectrograma_*`, `_ExameENF_*`, `_ExameContainerGOP_*` [`cases/caso_a/caso_a.ttl`] |
| **Caso B** | `oem:SinteseDeepfake_1_1`, `_1_2`, `_2_1`, `_2_2` | **generativa** | **não** | **Divergência face aos originais:** gerou `11fc8dfd6061cda1…`, `a55dc991a06c7811…`, `843837539c8aa52c…`, `9e361c539f2ae782…` | sem registro (`—`) [`cases/caso_b/caso_b.ttl`] |
| **Caso B** | `oem:CopiaForense_video_sintetico_1_1` a `_2_2` (4 cópias) | isomórfica | sim | **Sim (aquisição):** `11fc8dfd6061cda1…`, `a55dc991a06c7811…`, `843837539c8aa52c…`, `9e361c539f2ae782…` (`antes == depois`) | `oem:RegistroCustodia_video_sintetico_1_1` a `_2_2` [`cases/caso_b/registro_custodia.csv`] |
| **Caso B** | `oem:ExtracaoDeAudio_*` (8), `oem:GeracaoEspectrograma_*` (8), `oem:ExameENF_*` (8), `oem:ExameContainerGOP_*` (4) | homomórfica | sim | derivados verificados (`345abd0cf1749f8b…`, `e2c374f1436d12e3…`, `5423b5c5c7fc6826…`, `063409b41b3f4103…`, etc.) | `oem:RegistroCustodia_ExtracaoAudio_*`, `_Espectrograma_*`, `_ExameENF_*`, `_ExameContainerGOP_*` [`cases/caso_b/caso_b.ttl`] |
| **Caso C** | `oem:TransmissaoMensageiro_video_1` | recodificação (`oem:RecodificacaoDeTransmissao`) | **não** (`registradaEm max 0`) | **Divergência de hash:** antes `3abe96337aefc4c4…` $\neq$ depois `361fa834338c76bb…` | **NENHUM** (`oem:TransformacaoNaoDeclarada`) [`cases/caso_c/caso_c.ttl`] |
| **Caso C** | `oem:ExtracaoDeAudio_video_recodificado_1_Stereo`, `oem:ExameENF_*`, `oem:ExameContainerGOP_*` | homomórfica | sim | derivados verificados (`5dd05a685402ef19…`, `53f55af0cd3e73a2…`, `09f7705d69702b73…`) | `oem:RegistroCustodia_ExtracaoAudio_video_recodificado_1_Stereo`, `_ExameENF_*`, `_ExameGOP_caso_c` [`cases/caso_c/caso_c.ttl`] |

- **Destaque de divergência de hash:** Todas as cópias forenses em `data/work/` preservaram exatamente o SHA-256 (`hash_antes == hash_depois`), enquanto a recodificação de mensageiro no Caso C alterou o hash de `3abe96337aefc4c4…` para `361fa834338c76bb…` e os vídeos sintéticos do Caso B diferem integralmente dos hashes das matrizes do Caso A [`cases/caso_a/registro_custodia.csv`, `cases/caso_b/registro_custodia.csv`, `cases/caso_c/registro_custodia.csv`].

## 4. Análises de sinal e de metadados

### 4.1 Espectrogramas — parâmetros usados e caminho dos PNGs

- **Parâmetros (`analysis/config.yaml`):** `window_type="hann"`, `nperseg=4096`, `noverlap=3072`, `nfft=4096`, `scaling="density"`, `cmap="viridis"`, `dpi=150`, `fmax_display_hz=8000.0` [`analysis/config.yaml`].
- **Caminhos relativos e SHA-256 abreviados (`results/analises/<caso>/espectrogramas/` e `results/espectrogramas/`):** [`results/analises/resumo_geral_analises.json`]
  - Caso A: `results/analises/caso_a/espectrogramas/espectrograma_video_original_1.png` (`1b8aa84ea920ee26…`), `..._video_original_1_mono.png` (`199bfbaf64473791…`), `..._Video_original_2.png` (`193f4e0781675ee4…`), `..._Video_original_2_mono.png` (`efa8f89de63e2ba0…`).
  - Caso B: `results/analises/caso_b/espectrogramas/espectrograma_video_sintetico_1_1.png` (`a3127c6fb6e871a3…`), `..._1_1_mono.png` (`875029e38d98a235…`), `..._1_2.png` (`77e1604e2186297f…`), `..._1_2_mono.png` (`4ca1401939a273a7…`), `..._2_1.png` (`6b1118e5ba4b270f…`), `..._2_1_mono.png` (`ead9a566e09bcc14…`), `..._2_2.png` (`7a00ec515b2a9c74…`), `..._2_2_mono.png` (`7874798d69de7e8f…`).
  - Caso C: `results/analises/caso_c/espectrogramas/espectrograma_video_recodificado_mensageiro_1.png` (`dd2ec5a3bb764516…`), `..._1_mono.png` (`5a5ed92134361157…`).

### 4.2 ENF — por caso: detectável? (sim/não), SNR medida, nº de descontinuidades, instantes (s), limiar usado

- **Limiar usado (`analysis/config.yaml`):** `snr_threshold_db = 6.0`, `min_stable_windows_ratio = 0.60`, `max_freq_std_hz = 0.15` (normalizado para 60 Hz), `discontinuity_step_threshold_hz = 0.08`, `discontinuity_zscore_threshold = 3.5` [`analysis/config.yaml`].

| Caso | Arquivo `.wav` (estéreo e `_mono`) | Detectável? | SNR 60 Hz / 120 Hz (dB) | DP norm. 60 / 120 Hz (Hz) | Nº descontinuidades | Instantes (s) | Limiar (dB) | Registro / Achados |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Caso A** | `video_original_1.wav` | **sim** (120 Hz) | `3.928` (`3.932`) / **`8.995`** (`8.994`) | `0.4733` / **`0.02238`** | `0` | `—` | `6.0` | `"ENF detectável"`, `0` descontinuidades [`results/analises/caso_a/resumo_analises.json`] |
| **Caso A** | `Video_original_2.wav` | **não** | `12.493` / `10.577` | `0.25759` / `0.17494` | `0` | `—` | `6.0` | `"ENF não detectável"` — **nenhum achado gerado** [`results/analises/caso_a/resumo_analises.json`] |
| **Caso B** | `video_sintetico_1_1.wav` | **sim** (120 Hz) | `7.913` (`7.905`) / **`10.418`** (`10.419`) | `0.93162` / **`0.0529`** | `0` | `—` | `6.0` | `"ENF detectável"`, `0` descontinuidades [`results/analises/caso_b/resumo_analises.json`] |
| **Caso B** | `video_sintetico_1_2.wav` | **não** | `11.16` (`11.162`) / `4.778` (`4.769`) | `0.5823` / `0.17987` | `0` | `—` | `6.0` | `"ENF não detectável"` — **nenhum achado gerado** [`results/analises/caso_b/resumo_analises.json`] |
| **Caso B** | `video_sintetico_2_1.wav` | **não** | `10.313` / `8.049` | `0.20448` / `0.29619` | `0` | `—` | `6.0` | `"ENF não detectável"` — **nenhum achado gerado** [`results/analises/caso_b/resumo_analises.json`] |
| **Caso B** | `video_sintetico_2_2.wav` | **não** | `9.579` / `5.485` | `0.40557` / `0.37689` | `0` | `—` | `6.0` | `"ENF não detectável"` — **nenhum achado gerado** [`results/analises/caso_b/resumo_analises.json`] |
| **Caso C** | `video_recodificado_mensageiro_1.wav` | **sim** (120 Hz) | `4.292` (`4.287`) / **`8.966`** | `0.38102` / **`0.02633`** | `0` | `—` | `6.0` | `"ENF detectável"`, `0` descontinuidades [`results/analises/caso_c/resumo_analises.json`] |

- Nos 4 vídeos em que o exame retornou `"ENF não detectável"`, **nenhum achado foi gerado**: sob mundo aberto (OWA), a ausência de ENF não permite inferir nem autenticidade nem adulteração [`results/analises/resumo_analises.md`].

### 4.3 Metadados de contêiner — comparação com o original do caso A

| Caso / Vídeo | Referência (Caso A) | `encoder` | Perfil/Nível | Resolução / FPS | `time_base` (V / A) | Bitrate V / A (bps) | Estrutura de GOP (`I/P/B`, `maxGOP`, padrão) | Indivíduos de achado gerados |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Caso A:** `video_original_1.mp4` | *(Ref. Conj. 1)* | `null` | `High/31` | `478x850` / `30/1` | `1/90000` / `1/48000` | `1577083` / `319352` | `1/216/0`, `217`, `IPPPPPPPPP…` | Nenhum (`0`) [`results/analises/caso_a/resumo_analises.json`] |
| **Caso A:** `Video_original_2.mp4` | *(Ref. Conj. 2)* | `null` | `High/31` | `576x1024` / `30/1` | `1/15360` / `1/44100` | `699618` / `128002` | `8/547/1322`, `250`, `IBPBBPBBPB…` | Nenhum (`0`) [`results/analises/caso_a/resumo_analises.json`] |
| **Caso B:** `video_sintetico_1_1.mp4` | `video_original_1.mp4` | `null` | `High/31` | `848x478` / `24/1` | `1/90000` / `1/48000` | `1560783` / `128282` | `1/239/0`, `240`, `IPPPPPPPPP…` | `oem:IndicioRecodificacao_video_sintetico_1_1_1_*` a `_4_*` [`cases/caso_b/caso_b.ttl`] |
| **Caso B:** `video_sintetico_1_2.mp4` | `video_original_1.mp4` | `null` | `High/31` | `848x478` / `24/1` | `1/90000` / `1/48000` | `1570271` / `128305` | `1/239/0`, `240`, `IPPPPPPPPP…` | `oem:IndicioRecodificacao_video_sintetico_1_2_1_*` a `_4_*` [`cases/caso_b/caso_b.ttl`] |
| **Caso B:** `video_sintetico_2_1.mp4` | `Video_original_2.mp4` | `null` | `High/31` | `478x850` / `30/1` | `1/90000` / `1/48000` (`44.1k`) | `1326996` / `128041` | `2/496/0`, `300`, `IPPPPPPPPP…` | `oem:IndicioRecodificacao_video_sintetico_2_1_1_*` a `_5_*` [`cases/caso_b/caso_b.ttl`] |
| **Caso B:** `video_sintetico_2_2.mp4` | `Video_original_2.mp4` | `null` | `High/31` | `476x848` / `30/1` | `1/90000` / `1/48000` (`44.1k`) | `1426896` / `128282` | `2/385/0`, `300`, `IPPPPPPPPP…` | `oem:IndicioRecodificacao_video_sintetico_2_2_1_*` a `_5_*` [`cases/caso_b/caso_b.ttl`] |
| **Caso C:** `video_recodificado_mensageiro_1.mp4` | `video_original_1.mp4` | `Lavf62.12.101` | `Main/31` | `476x848` / `30/1` | `1/15360` / `1/44100` | `916790` / `95586` | `1/63/153`, `217`, `IBBBPBBBPB…` | `oem:IndicioRecodificacao_caso_c_1_*` a `_4_*` [`cases/caso_c/caso_c.ttl`] |

### 4.4 Achados gerados

| achado | classe | evidência | exame | técnica | valor/instante |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `oem:IndicioRecodificacao_video_sintetico_1_1_1_DivergenciaDeResolucaoOuOrientacao` | `oem:IndicioDeRecodificacao` | `oem:Evidencia_Sintetico_1_1_Work` | `oem:ExameContainerGOP_video_sintetico_1_1` | `ffprobe -show_frames` | `478x850 -> 848x478` [`cases/caso_b/caso_b.ttl`] |
| `oem:IndicioRecodificacao_video_sintetico_1_1_2_DivergenciaDeTaxaDeQuadros` | `oem:IndicioDeRecodificacao` | `oem:Evidencia_Sintetico_1_1_Work` | `oem:ExameContainerGOP_video_sintetico_1_1` | `ffprobe -show_frames` | `30/1 -> 24/1` [`cases/caso_b/caso_b.ttl`] |
| `oem:IndicioRecodificacao_video_sintetico_1_1_3_DivergenciaDeEstruturaGOP` | `oem:IndicioDeRecodificacao` | `oem:Evidencia_Sintetico_1_1_Work` | `oem:ExameContainerGOP_video_sintetico_1_1` | `ffprobe -show_frames` | `B=0,maxGOP=217 -> B=0,maxGOP=240` [`cases/caso_b/caso_b.ttl`] |
| `oem:IndicioRecodificacao_video_sintetico_1_1_4_DivergenciaDeBitrate` | `oem:IndicioDeRecodificacao` | `oem:Evidencia_Sintetico_1_1_Work` | `oem:ExameContainerGOP_video_sintetico_1_1` | `ffprobe -show_frames` | `v=1577083,a=319352 -> v=1560783,a=128282` [`cases/caso_b/caso_b.ttl`] |
| `oem:IndicioRecodificacao_video_sintetico_1_2_1_DivergenciaDeResolucaoOuOrientacao` | `oem:IndicioDeRecodificacao` | `oem:Evidencia_Sintetico_1_2_Work` | `oem:ExameContainerGOP_video_sintetico_1_2` | `ffprobe -show_frames` | `478x850 -> 848x478` [`cases/caso_b/caso_b.ttl`] |
| `oem:IndicioRecodificacao_video_sintetico_1_2_2_DivergenciaDeTaxaDeQuadros` | `oem:IndicioDeRecodificacao` | `oem:Evidencia_Sintetico_1_2_Work` | `oem:ExameContainerGOP_video_sintetico_1_2` | `ffprobe -show_frames` | `30/1 -> 24/1` [`cases/caso_b/caso_b.ttl`] |
| `oem:IndicioRecodificacao_video_sintetico_1_2_3_DivergenciaDeEstruturaGOP` | `oem:IndicioDeRecodificacao` | `oem:Evidencia_Sintetico_1_2_Work` | `oem:ExameContainerGOP_video_sintetico_1_2` | `ffprobe -show_frames` | `B=0,maxGOP=217 -> B=0,maxGOP=240` [`cases/caso_b/caso_b.ttl`] |
| `oem:IndicioRecodificacao_video_sintetico_1_2_4_DivergenciaDeBitrate` | `oem:IndicioDeRecodificacao` | `oem:Evidencia_Sintetico_1_2_Work` | `oem:ExameContainerGOP_video_sintetico_1_2` | `ffprobe -show_frames` | `v=1577083,a=319352 -> v=1570271,a=128305` [`cases/caso_b/caso_b.ttl`] |
| `oem:IndicioRecodificacao_video_sintetico_2_1_1_DivergenciaDeResolucaoOuOrientacao` | `oem:IndicioDeRecodificacao` | `oem:Evidencia_Sintetico_2_1_Work` | `oem:ExameContainerGOP_video_sintetico_2_1` | `ffprobe -show_frames` | `576x1024 -> 478x850` [`cases/caso_b/caso_b.ttl`] |
| `oem:IndicioRecodificacao_video_sintetico_2_1_2_DivergenciaDeEstruturaGOP` | `oem:IndicioDeRecodificacao` | `oem:Evidencia_Sintetico_2_1_Work` | `oem:ExameContainerGOP_video_sintetico_2_1` | `ffprobe -show_frames` | `B=1322,maxGOP=250 -> B=0,maxGOP=300` [`cases/caso_b/caso_b.ttl`] |
| `oem:IndicioRecodificacao_video_sintetico_2_1_3_DivergenciaDeTimeBaseVideo` | `oem:IndicioDeRecodificacao` | `oem:Evidencia_Sintetico_2_1_Work` | `oem:ExameContainerGOP_video_sintetico_2_1` | `ffprobe -show_frames` | `1/15360 -> 1/90000` [`cases/caso_b/caso_b.ttl`] |
| `oem:IndicioRecodificacao_video_sintetico_2_1_4_InconsistenciaSampleRateTimeBaseAudio` | `oem:IndicioDeRecodificacao` | `oem:Evidencia_Sintetico_2_1_Work` | `oem:ExameContainerGOP_video_sintetico_2_1` | `ffprobe -show_frames` | `1/44100 -> 1/48000` [`cases/caso_b/caso_b.ttl`] |
| `oem:IndicioRecodificacao_video_sintetico_2_1_5_DivergenciaDeBitrate` | `oem:IndicioDeRecodificacao` | `oem:Evidencia_Sintetico_2_1_Work` | `oem:ExameContainerGOP_video_sintetico_2_1` | `ffprobe -show_frames` | `v=699618,a=128002 -> v=1326996,a=128041` [`cases/caso_b/caso_b.ttl`] |
| `oem:IndicioRecodificacao_video_sintetico_2_2_1_DivergenciaDeResolucaoOuOrientacao` | `oem:IndicioDeRecodificacao` | `oem:Evidencia_Sintetico_2_2_Work` | `oem:ExameContainerGOP_video_sintetico_2_2` | `ffprobe -show_frames` | `576x1024 -> 476x848` [`cases/caso_b/caso_b.ttl`] |
| `oem:IndicioRecodificacao_video_sintetico_2_2_2_DivergenciaDeEstruturaGOP` | `oem:IndicioDeRecodificacao` | `oem:Evidencia_Sintetico_2_2_Work` | `oem:ExameContainerGOP_video_sintetico_2_2` | `ffprobe -show_frames` | `B=1322,maxGOP=250 -> B=0,maxGOP=300` [`cases/caso_b/caso_b.ttl`] |
| `oem:IndicioRecodificacao_video_sintetico_2_2_3_DivergenciaDeTimeBaseVideo` | `oem:IndicioDeRecodificacao` | `oem:Evidencia_Sintetico_2_2_Work` | `oem:ExameContainerGOP_video_sintetico_2_2` | `ffprobe -show_frames` | `1/15360 -> 1/90000` [`cases/caso_b/caso_b.ttl`] |
| `oem:IndicioRecodificacao_video_sintetico_2_2_4_InconsistenciaSampleRateTimeBaseAudio` | `oem:IndicioDeRecodificacao` | `oem:Evidencia_Sintetico_2_2_Work` | `oem:ExameContainerGOP_video_sintetico_2_2` | `ffprobe -show_frames` | `1/44100 -> 1/48000` [`cases/caso_b/caso_b.ttl`] |
| `oem:IndicioRecodificacao_video_sintetico_2_2_5_DivergenciaDeBitrate` | `oem:IndicioDeRecodificacao` | `oem:Evidencia_Sintetico_2_2_Work` | `oem:ExameContainerGOP_video_sintetico_2_2` | `ffprobe -show_frames` | `v=699618,a=128002 -> v=1426896,a=128282` [`cases/caso_b/caso_b.ttl`] |
| `oem:IndicioRecodificacao_caso_c_1_DivergenciaDeResolucaoOuOrientacao` | `oem:DivergenciaDeResolucaoOuOrientacao` | `oem:Evidencia_Recodificado_Mensageiro_1_Work` | `oem:ExameContainerGOP_video_recodificado_mensageiro_1` | `ffprobe -show_frames` | `478x850 -> 476x848` [`cases/caso_c/caso_c.ttl`] |
| `oem:IndicioRecodificacao_caso_c_2_DivergenciaDeEstruturaGOP` | `oem:DivergenciaDeEstruturaGOP` | `oem:Evidencia_Recodificado_Mensageiro_1_Work` | `oem:ExameContainerGOP_video_recodificado_mensageiro_1` | `ffprobe -show_frames` | `B=0,maxGOP=217 -> B=153,maxGOP=217` [`cases/caso_c/caso_c.ttl`] |
| `oem:IndicioRecodificacao_caso_c_3_DivergenciaDeTimeBaseVideo` | `oem:DivergenciaDeTimeBaseVideo` | `oem:Evidencia_Recodificado_Mensageiro_1_Work` | `oem:ExameContainerGOP_video_recodificado_mensageiro_1` | `ffprobe -show_frames` | `1/90000 -> 1/15360` [`cases/caso_c/caso_c.ttl`] |
| `oem:IndicioRecodificacao_caso_c_4_DivergenciaDeBitrate` | `oem:DivergenciaDeBitrate` | `oem:Evidencia_Recodificado_Mensageiro_1_Work` | `oem:ExameContainerGOP_video_recodificado_mensageiro_1` | `ffprobe -show_frames` | `v=1577083,a=319352 -> v=916790,a=95586` [`cases/caso_c/caso_c.ttl`] |

## 5. Raciocínio (HermiT)

### 5.1 Tabela-síntese

| caso | classificação prevista (`cases/EXPECTED.md`) | obtida? (sim/não) | nº de justificações | tempo de classificação |
| :--- | :--- | :---: | :---: | :---: |
| **Caso A (Aberto)** | `oem:EvidenciaMultimidia` (não `oem:EvidenciaIntegra`); cópias em `oem:TransformacaoPreservadoraDeclarada` [`cases/EXPECTED.md`] | **sim** [`results/reasoning/caso_a_aberto_reasoned.ttl`] | `1` (`8` axiomas) [`results/explanations/explain_caso_a_aberto.md`] | `1234 ms` [`results/secao_3_4.md`] |
| **Caso A (Fechado)** | `oem:EvidenciaIntegra` para vídeos e áudios fechados [`cases/EXPECTED.md`] | **sim** [`results/reasoning/caso_a_fechado_reasoned.ttl`] | `1` (`13` axiomas) [`results/explanations/explain_caso_a_fechado.md`] | `2836 ms` [`results/secao_3_4.md`] |
| **Caso B** | `oem:EvidenciaComConteudoAlterado` (não `oem:EvidenciaIntegra`) [`cases/EXPECTED.md`] | **sim** [`results/reasoning/caso_b_reasoned.ttl`] | `1` (`5` axiomas) [`results/explanations/explain_caso_b.md`] | `1476 ms` [`results/secao_3_4.md`] |
| **Caso C** | `oem:EvidenciaComCadeiaQuebrada` (não `oem:EvidenciaIntegra`) [`cases/EXPECTED.md`] | **sim** [`results/reasoning/caso_c_reasoned.ttl`] | `1` (`6` axiomas) [`results/explanations/explain_caso_c.md`] | `1119 ms` [`results/secao_3_4.md`] |

### 5.2 Justificação mínima de cada classificação obtida, em Manchester e em notação DL

- **Caso A (Aberto)** [`results/explanations/explain_caso_a_aberto.md`]:
```manchester
TransformacaoIsomorfica SubClassOf: TransformacaoPreservadora
TransformacaoDeclarada EquivalentTo: Transformacao and (registradaEm some RegistroDeCustodia)
TransformacaoPreservadoraDeclarada EquivalentTo: TransformacaoDeclarada and TransformacaoPreservadora
documentaTransformacao InverseOf: registradaEm
registradaEm Domain: Transformacao
documentaTransformacao Domain: RegistroDeCustodia
CopiaForense_video_original_1 Type: TransformacaoIsomorfica
CopiaForense_video_original_1 registradaEm RegistroCustodia_video_original_1
=> {CopiaForense_video_original_1} SubClassOf: TransformacaoPreservadoraDeclarada
```
Notação DL: $\{\mathsf{CopiaForense\_video\_original\_1} : \mathsf{TransformacaoIsomorfica},\; (\mathsf{CopiaForense\_video\_original\_1}, \mathsf{RegistroCustodia\_video\_original\_1}) : \mathsf{registradaEm},\; \mathsf{TransformacaoIsomorfica} \sqsubseteq \mathsf{TransformacaoPreservadora},\; \top \sqsubseteq \forall \mathsf{registradaEm}^{-}.\mathsf{Transformacao},\; \mathsf{TransformacaoDeclarada} \equiv \mathsf{Transformacao} \sqcap \exists \mathsf{registradaEm}.\mathsf{RegistroDeCustodia},\; \mathsf{TransformacaoPreservadoraDeclarada} \equiv \mathsf{TransformacaoPreservadora} \sqcap \mathsf{TransformacaoDeclarada}\} \models \mathsf{CopiaForense\_video\_original\_1} : \mathsf{TransformacaoPreservadoraDeclarada}$.

- **Caso A (Fechado)** [`results/explanations/explain_caso_a_fechado.md`]:
```manchester
EvidenciaIntegra EquivalentTo: EvidenciaMultimidia
    and (sofreu some TransformacaoPreservadoraDeclarada)
    and (sofreu only TransformacaoPreservadoraDeclarada)
TransformacaoPreservadoraDeclarada EquivalentTo: TransformacaoDeclarada and TransformacaoPreservadora
TransformacaoDeclarada EquivalentTo: Transformacao and (registradaEm some RegistroDeCustodia)
TransformacaoIsomorfica SubClassOf: TransformacaoPreservadora
sofreu InverseOf: temSaida
registradaEm Domain: Transformacao
tamanhoBytes Domain: EvidenciaMultimidia
Evidencia_Original_1_Work tamanhoBytes 1718872
Evidencia_Original_1_Work Type: sofreu only {CopiaForense_video_original_1}
CopiaForense_video_original_1 Type: TransformacaoIsomorfica
CopiaForense_video_original_1 temSaida Evidencia_Original_1_Work
CopiaForense_video_original_1 registradaEm RegistroCustodia_video_original_1
RegistroCustodia_video_original_1 Type: RegistroDeCustodia
=> {Evidencia_Original_1_Work} SubClassOf: EvidenciaIntegra
```
Notação DL: $\{\mathsf{Evidencia\_Original\_1\_Work} : \mathsf{EvidenciaMultimidia},\; (\mathsf{CopiaForense\_video\_original\_1}, \mathsf{Evidencia\_Original\_1\_Work}) : \mathsf{temSaida},\; \mathsf{sofreu} \equiv \mathsf{temSaida}^{-},\; \mathsf{Evidencia\_Original\_1\_Work} : \forall \mathsf{sofreu}.\{\mathsf{CopiaForense\_video\_original\_1}\},\; \mathsf{CopiaForense\_video\_original\_1} : \mathsf{TransformacaoPreservadoraDeclarada},\; \mathsf{EvidenciaIntegra} \equiv \mathsf{EvidenciaMultimidia} \sqcap \exists \mathsf{sofreu}.\mathsf{TransformacaoPreservadoraDeclarada} \sqcap \forall \mathsf{sofreu}.\mathsf{TransformacaoPreservadoraDeclarada}\} \models \mathsf{Evidencia\_Original\_1\_Work} : \mathsf{EvidenciaIntegra}$.

- **Caso B** [`results/explanations/explain_caso_b.md`]:
```manchester
EvidenciaComConteudoAlterado EquivalentTo: EvidenciaMultimidia and (sofreu some TransformacaoGenerativa)
sofreu InverseOf: temSaida
sofreu Domain: EvidenciaMultimidia
SinteseDeepfake_1_1 Type: TransformacaoGenerativa
SinteseDeepfake_1_1 temSaida Evidencia_Sintetico_1_1_Work
=> {Evidencia_Sintetico_1_1_Work} SubClassOf: EvidenciaComConteudoAlterado
```
Notação DL: $\{\mathsf{SinteseDeepfake\_1\_1} : \mathsf{TransformacaoGenerativa},\; (\mathsf{SinteseDeepfake\_1\_1}, \mathsf{Evidencia\_Sintetico\_1\_1\_Work}) : \mathsf{temSaida},\; \mathsf{sofreu} \equiv \mathsf{temSaida}^{-},\; \top \sqsubseteq \forall \mathsf{sofreu}^{-}.\mathsf{EvidenciaMultimidia},\; \mathsf{EvidenciaComConteudoAlterado} \equiv \mathsf{EvidenciaMultimidia} \sqcap \exists \mathsf{sofreu}.\mathsf{TransformacaoGenerativa}\} \models \mathsf{Evidencia\_Sintetico\_1\_1\_Work} : \mathsf{EvidenciaComConteudoAlterado}$.

- **Caso C** [`results/explanations/explain_caso_c.md`]:
```manchester
EvidenciaComCadeiaQuebrada EquivalentTo: EvidenciaMultimidia and (sofreu some TransformacaoNaoDeclarada)
TransformacaoNaoDeclarada EquivalentTo: Transformacao and (registradaEm max 0 RegistroDeCustodia)
sofreu Range: Transformacao
Evidencia_Recodificado_Mensageiro_1_Work Type: EvidenciaMultimidia
Evidencia_Recodificado_Mensageiro_1_Work sofreu TransmissaoMensageiro_video_1
TransmissaoMensageiro_video_1 Type: registradaEm max 0 RegistroDeCustodia
=> {Evidencia_Recodificado_Mensageiro_1_Work} SubClassOf: EvidenciaComCadeiaQuebrada
```
Notação DL: $\{\mathsf{Evidencia\_Recodificado\_Mensageiro\_1\_Work} : \mathsf{EvidenciaMultimidia},\; (\mathsf{Evidencia\_Recodificado\_Mensageiro\_1\_Work}, \mathsf{TransmissaoMensageiro\_video\_1}) : \mathsf{sofreu},\; \top \sqsubseteq \forall \mathsf{sofreu}.\mathsf{Transformacao},\; \mathsf{TransmissaoMensageiro\_video\_1} : (\leqslant 0\,\mathsf{registradaEm}.\mathsf{RegistroDeCustodia}),\; \mathsf{TransformacaoNaoDeclarada} \equiv \mathsf{Transformacao} \sqcap (\leqslant 0\,\mathsf{registradaEm}.\mathsf{RegistroDeCustodia}),\; \mathsf{EvidenciaComCadeiaQuebrada} \equiv \mathsf{EvidenciaMultimidia} \sqcap \exists \mathsf{sofreu}.\mathsf{TransformacaoNaoDeclarada}\} \models \mathsf{Evidencia\_Recodificado\_Mensageiro\_1\_Work} : \mathsf{EvidenciaComCadeiaQuebrada}$.

### 5.3 Caso A com e sem axioma de fechamento

Sem o axioma de fechamento (`results/reasoning/caso_a_aberto_reasoned.ttl`), o HermiT **não inferiu** `oem:EvidenciaIntegra` para nenhuma evidência do Caso A, mantendo-as apenas como `oem:EvidenciaMultimidia`. Com o axioma de fechamento (`cases/caso_a/caso_a_fechado.ttl` $\rightarrow$ `results/reasoning/caso_a_fechado_reasoned.ttl`), o HermiT **inferiu** `oem:EvidenciaIntegra` para `oem:Evidencia_Original_1_Work`, `oem:Evidencia_Original_2_Work`, `oem:Evidencia_Audio_Original_1_Stereo` e `oem:Evidencia_Audio_Original_2_Stereo`. **A previsão central do artigo foi confirmada** [`results/secao_3_4.md`, `tests/test_reasoning.py`].

### 5.4 Classificações previstas e NÃO obtidas, e classificações obtidas e NÃO previstas

- **Classificações previstas e NÃO obtidas:** `Nenhuma` (`0`) [`results/divergencias.md`].
- **Classificações obtidas e NÃO previstas:** `Nenhuma` (`0`) [`results/divergencias.md`].
- **Hipótese em `results/divergencias.md`:** A ausência de indivíduos `oem:DescontinuidadeENF` decorre do fato de que as gravações com 120 Hz estável (`video_original_1`, `video_sintetico_1_1`, `video_recodificado_mensageiro_1`) não possuíam cortes temporais na rede elétrica, e nos demais arquivos a voz sobrepôs a faixa de 60/120 Hz (`"ENF não detectável"`) [`results/divergencias.md`].

## 6. Perguntas de competência (PC1–PC5)

Consultas em `queries/pc1_integridade.rq` a `pc5_quebra_custodia_ou_alteracao.rq` executadas via `robot query` [`results/sparql/`]:

```sparql
# PC1 (queries/pc1_integridade.rq)
PREFIX oem: <http://example.org/oem#>
SELECT DISTINCT ?evidencia ?classeIntegridade WHERE {
  ?evidencia a oem:EvidenciaMultimidia .
  VALUES ?classeIntegridade { oem:EvidenciaIntegra oem:EvidenciaComConteudoAlterado oem:EvidenciaComCadeiaQuebrada }
  ?evidencia a ?classeIntegridade .
} ORDER BY ?evidencia ?classeIntegridade

# PC2 (queries/pc2_transformacoes_custodia.rq)
PREFIX oem: <http://example.org/oem#>
SELECT DISTINCT ?evidencia ?transformacao ?tipoDeclaracao ?registro ?hashValor WHERE {
  ?evidencia oem:sofreu ?transformacao .
  VALUES ?tipoDeclaracao { oem:TransformacaoPreservadoraDeclarada oem:TransformacaoGenerativa oem:TransformacaoNaoDeclarada }
  ?transformacao a ?tipoDeclaracao .
  OPTIONAL { ?transformacao oem:registradaEm ?registro . }
  OPTIONAL { ?transformacao oem:verificadaPor ?h . ?h oem:valorHashHex ?hashValor . }
} ORDER BY ?evidencia ?transformacao

# PC3 (queries/pc3_exames_enf.rq)
PREFIX oem: <http://example.org/oem#>
SELECT DISTINCT ?exame ?audioEntrada ?resultado ?snr60 ?snr120 ?limiar WHERE {
  ?exame a oem:ExameENF ; oem:temEntrada ?audioEntrada ; oem:resultadoExame ?resultado ;
         oem:snrMedio60Hz_dB ?snr60 ; oem:snrMedio120Hz_dB ?snr120 ; oem:limiarSNR_dB ?limiar .
} ORDER BY ?exame

# PC4 (queries/pc4_indicios_edicao.rq)
PREFIX oem: <http://example.org/oem#>
SELECT DISTINCT ?evidencia ?exame ?achado ?subclasse ?valorRef ?valorObs WHERE {
  ?exame oem:temEntrada ?evidencia ; oem:geraAchado ?achado .
  ?achado a ?subclasse ; oem:valorReferencia ?valorRef ; oem:valorObservado ?valorObs .
  FILTER(?subclasse != oem:AchadoPericial && ?subclasse != oem:IndicioDeEdicao && ?subclasse != <http://www.w3.org/2002/07/owl#NamedIndividual> && ?subclasse != <http://www.w3.org/2002/07/owl#Thing>)
} ORDER BY ?evidencia ?achado ?subclasse

# PC5 (queries/pc5_quebra_custodia_ou_alteracao.rq)
PREFIX oem: <http://example.org/oem#>
SELECT DISTINCT ?evidencia ?transformacaoVioladora ?classificacaoEvidencia WHERE {
  ?evidencia oem:sofreu ?transformacaoVioladora ; a ?classificacaoEvidencia .
  VALUES ?classificacaoEvidencia { oem:EvidenciaComConteudoAlterado oem:EvidenciaComCadeiaQuebrada }
  FILTER EXISTS { { ?transformacaoVioladora a oem:TransformacaoGenerativa } UNION { ?transformacaoVioladora a oem:TransformacaoNaoDeclarada } }
} ORDER BY ?evidencia ?transformacaoVioladora
```

| PC | Caso A (Aberto) | Caso A (Fechado) | Caso B | Caso C |
| :--- | :--- | :--- | :--- | :--- |
| **PC1** | `0` linhas [`results/sparql/caso_a_aberto/pc1.csv`] | `4` indivíduos em `oem:EvidenciaIntegra` [`results/sparql/caso_a_fechado/pc1.csv`] | `8` indivíduos (`Raw` e `Work` de `1_1` a `2_2`) em `oem:EvidenciaComConteudoAlterado` [`results/sparql/caso_b/pc1.csv`] | `1` indivíduo (`Evidencia_Recodificado_Mensageiro_1_Work`) em `oem:EvidenciaComCadeiaQuebrada` [`results/sparql/caso_c/pc1.csv`] |
| **PC2** | `12` transformações em `TransformacaoPreservadoraDeclarada` [`results/sparql/caso_a_aberto/pc2.csv`] | `12` transformações em `TransformacaoPreservadoraDeclarada` [`results/sparql/caso_a_fechado/pc2.csv`] | `18` `TransformacaoPreservadoraDeclarada` + `8` vínculos de `TransformacaoGenerativa` [`results/sparql/caso_b/pc2.csv`] | `1` `TransformacaoNaoDeclarada` (`TransmissaoMensageiro_video_1`) + `2` `TransformacaoPreservadoraDeclarada` [`results/sparql/caso_c/pc2.csv`] |
| **PC3** | `4` exames: `original_1` `"ENF detectável"` (`8.995 dB`); `original_2` `"ENF não detectável"` [`results/sparql/caso_a_aberto/pc3.csv`] | Idêntico ao Caso A-aberto [`results/sparql/caso_a_fechado/pc3.csv`] | `8` exames: `1_1` `"ENF detectável"` (`10.418 dB`); `1_2`, `2_1`, `2_2` `"ENF não detectável"` [`results/sparql/caso_b/pc3.csv`] | `1` exame: `"ENF detectável"` (`snr60=4.292`, `snr120=8.966`, `limiar=6.0`) [`results/sparql/caso_c/pc3.csv`] |
| **PC4** | `0` indícios [`results/sparql/caso_a_aberto/pc4.csv`] | `0` indícios [`results/sparql/caso_a_fechado/pc4.csv`] | `18` indícios de `oem:IndicioDeRecodificacao` [`results/sparql/caso_b/pc4.csv`] | `4` indícios de subclasse de `oem:IndicioDeRecodificacao` [`results/sparql/caso_c/pc4.csv`] |
| **PC5** | `0` linhas [`results/sparql/caso_a_aberto/pc5.csv`] | `0` linhas [`results/sparql/caso_a_fechado/pc5.csv`] | `8` linhas (`SinteseDeepfake_1_1` a `_2_2` $\rightarrow$ `EvidenciaComConteudoAlterado`) [`results/sparql/caso_b/pc5.csv`] | `1` linha (`TransmissaoMensageiro_video_1` $\rightarrow$ `EvidenciaComCadeiaQuebrada`) [`results/sparql/caso_c/pc5.csv`] |

## 7. Testes automatizados

- **Saída resumida do `pytest` (`tests/test_reasoning.py`):** `5` testes executados, `5` aprovados (`PASSED` em `0.31s`), `0` falhos (`FAILED`) [`tests/test_reasoning.py`].
- **Testes que falharam:** `Nenhum` (`0`).

## 8. Limitações observadas na execução

1. **Trilhas sem áudio:** `Nenhuma` (`0`); todos os vídeos continham áudio estéreo `AAC LC` [`results/inventario.csv`].
2. **ENF ausente (`"ENF não detectável"`):** Ocorreu em `Video_original_2`, `video_sintetico_1_2`, `video_sintetico_2_1` e `video_sintetico_2_2` devido à variabilidade espectral da fala ($\sigma_{\text{norm}} > 0.15\text{ Hz}$) ou SNR $< 6.0\text{ dB}$; nenhum achado foi gerado para eles [`results/analises/resumo_analises.md`].
3. **Ferramentas:** `git` e `make` ausentes no `PATH`; `exiftool` exigiu execução fora do sandbox por realocação de DLL no Windows; `ROBOT 1.9.4` executado com `OpenJDK 11.0.13`; consultas SPARQL rodadas via `robot query` devido a incompatibilidade de `pyparsing` com `rdflib.Graph.query()` [`results/sparql/`].
4. **Limiares alterados:** `Nenhum` (`0`) [`analysis/config.yaml`].
5. **Passos manuais:** Recodificação controlada do Caso C executada via `ffmpeg` sobre a cópia de trabalho do Caso A [`cases/caso_c/caso_c.ttl`].

## 9. Pendências para o artigo

- **Figura do grafo da ontologia:** `NÃO GERADA` (apenas os `14` PNGs de espectrogramas em `results/espectrogramas/` e `14` PNGs de ENF em `results/analises/<caso>/enf/` foram gerados).
- **DOI do Zenodo e W3ID:** `NÃO ENCONTRADO` (namespace atual provisório: `http://example.org/oem#`) [`ontology/oem.ttl`].
- **Versão anonimizada:** Pendente substituir a literal nominal do pesquisador nos arquivos `.ttl` e `.csv` por `"Agente (perito)"` antes do envio para revisão cega (já anonimizado neste relatório).
- **Marcadores `TODO-LAB` restantes nos arquivos `.ttl`:** `Nenhum` (`0` linhas em `ontology/oem.ttl` e `cases/*/*.ttl`).
