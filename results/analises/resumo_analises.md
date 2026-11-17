# Resumo das Análises Periciais (Espectrogramas, ENF 60/120 Hz e Contêiner/GOP)

**Arquivo de configuração utilizado (sem alteração pós-execução):** `analysis/config.yaml`  
**Script de execução:** `analysis/run_analyses.py` (Python 3.12.5, NumPy 1.26.4, SciPy 1.17.1, Matplotlib 3.8.4, FFprobe 8.1.1)

---

## 1. Parâmetros Fixados em `analysis/config.yaml`

- **Espectrograma (`scipy.signal.spectrogram`):**
  - `window_type`: `"hann"`, `nperseg`: `4096`, `noverlap`: `3072`, `nfft`: `4096`, `scaling`: `"density"` (PSD em dB/Hz), `cmap`: `"viridis"`, `dpi`: `150`, `fmax_display_hz`: `8000`.
- **Exame ENF (Rede elétrica brasileira = `60.0 Hz`, harmônicos `[60.0, 120.0] Hz`):**
  - `target_fs_hz`: `1200`, `bandpass_half_width_hz`: `1.0` ($\pm 1\text{ Hz}$), `stft_window_sec`: `4.0`, `stft_hop_sec`: `1.0`, `zero_padding_factor`: `8`, `snr_threshold_db`: `6.0`, `min_stable_windows_ratio`: `0.60`, `max_freq_std_hz`: `0.15` (normalizado para a fundamental de 60 Hz), `discontinuity_step_threshold_hz`: `0.08`, `discontinuity_zscore_threshold`: `3.5`.
- **Comparação de Contêiner e GOP (`ffprobe -show_frames`):**
  - `bitrate_relative_diff_threshold`: `0.15` (15%).

---

## 2. Espectrogramas Gerados (`oem:GeracaoDeEspectrograma`)

Todos os 12 arquivos `.wav` (6 estéreo + 6 mono) tiveram seus espectrogramas PSD gerados e salvos tanto em `results/espectrogramas/` quanto em `results/analises/<caso>/espectrogramas/`:

| Caso | Áudio de Entrada | Espectrograma Gerado (`results/analises/<caso>/espectrogramas/...`) | Tamanho (Bytes) | SHA-256 do PNG |
| :--- | :--- | :--- | :---: | :--- |
| **Caso A** | `video_original_1.wav` | `espectrograma_video_original_1.png` | 876.600 | `1b8aa84ea920ee2604fff5e70b17763e184495fe5e35ed617263e7b120e75025` |
| **Caso A** | `video_original_1_mono.wav` | `espectrograma_video_original_1_mono.png` | 884.477 | `199bfbaf64473791cb960727bdba328169e51e3ba25ac5b7d7abd5bacbed0c51` |
| **Caso A** | `Video_original_2.wav` | `espectrograma_Video_original_2.png` | 1.143.905 | `193f4e0781675ee4fedce9adbe056938221152cd8485edecf32773fa02e8f6c8` |
| **Caso A** | `Video_original_2_mono.wav` | `espectrograma_Video_original_2_mono.png` | 1.143.955 | `efa8f89de63e2ba04ad4f1b0a4da36b53a31e148b8a235da381ecb09c6a367e0` |
| **Caso B** | `video_sintetico_1_1.wav` | `espectrograma_video_sintetico_1_1.png` | 949.785 | `a3127c6fb6e871a32e353c19f3f6962d523bbd867fba719ace9639cce4a07e5a` |
| **Caso B** | `video_sintetico_1_1_mono.wav` | `espectrograma_video_sintetico_1_1_mono.png` | 949.791 | `875029e38d98a235f8c955fc3eb305dbaf97d7c93f467d2226206619e7c8548a` |
| **Caso B** | `video_sintetico_1_2.wav` | `espectrograma_video_sintetico_1_2.png` | 948.062 | `77e1604e2186297f2e0f19073f5217f5c122a4b77cf9512ff20888856680b43f` |
| **Caso B** | `video_sintetico_1_2_mono.wav` | `espectrograma_video_sintetico_1_2_mono.png` | 951.940 | `4ca1401939a273a76a891a499324d8cf8835f64f74ab667aa55aad6a0da225f6` |
| **Caso B** | `video_sintetico_2_1.wav` | `espectrograma_video_sintetico_2_1.png` | 1.109.474 | `6b1118e5ba4b270f584dea031cc4fe05a8ab436dd4145584f0fad73d0bfe463a` |
| **Caso B** | `video_sintetico_2_1_mono.wav` | `espectrograma_video_sintetico_2_1_mono.png` | 1.110.002 | `ead9a566e09bcc140919fe4ce5c32d36e5959c3cb6b6cfc792eaf4cc444637c3` |
| **Caso B** | `video_sintetico_2_2.wav` | `espectrograma_video_sintetico_2_2.png` | 1.050.417 | `7a00ec515b2a9c748483756316b22daf82b11ecb5805ffeebde93f99ae99f4e0` |
| **Caso B** | `video_sintetico_2_2_mono.wav` | `espectrograma_video_sintetico_2_2_mono.png` | 1.049.961 | `7874798d69de7e8f2a59b260c7ec6ad72ef98fc39117309d148c159eed6a9325` |

---

## 3. Resultados Reais do Exame de ENF (60 Hz e 120 Hz) (`oem:ExameENF`)

| Caso | Arquivo `.wav` | Janelas STFT | 60 Hz: SNR Médio (dB) | 60 Hz: Freq Média $\pm$ DP Norm (Hz) | 60 Hz Estável? | 120 Hz: SNR Médio (dB) | 120 Hz: Freq Média $\pm$ DP Norm (Hz) | 120 Hz Estável? | Resultado do Exame (`oem:resultadoExame`) | Descontinuidades (`oem:DescontinuidadeENF`) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Caso A** | `video_original_1.wav` | 4 | 3,928 | $59,79515 \pm 0,47330$ | Não | **8,995** | $119,98579 \pm \mathbf{0,02238}$ | **Sim (100%)** | **`ENF detectável`** (em 120 Hz) | `0` |
| **Caso A** | `video_original_1_mono.wav` | 4 | 3,932 | $59,79512 \pm 0,47334$ | Não | **8,994** | $119,98579 \pm \mathbf{0,02238}$ | **Sim (100%)** | **`ENF detectável`** (em 120 Hz) | `0` |
| **Caso A** | `Video_original_2.wav` | 59 | 12,493 | $59,69775 \pm 0,25759$ | Não ($\sigma > 0,15$) | 10,577 | $119,63638 \pm 0,17494$ | Não ($\sigma > 0,15$) | **`ENF não detectável`** | Nenhuma gerada (OWA) |
| **Caso A** | `Video_original_2_mono.wav` | 59 | 12,493 | $59,69775 \pm 0,25759$ | Não ($\sigma > 0,15$) | 10,577 | $119,63638 \pm 0,17494$ | Não ($\sigma > 0,15$) | **`ENF não detectável`** | Nenhuma gerada (OWA) |
| **Caso B** | `video_sintetico_1_1.wav` | 7 | 7,913 | $59,91881 \pm 0,93162$ | Não ($\sigma > 0,15$) | **10,418** | $120,07911 \pm \mathbf{0,05290}$ | **Sim (100%)** | **`ENF detectável`** (em 120 Hz) | `0` |
| **Caso B** | `video_sintetico_1_1_mono.wav` | 7 | 7,905 | $59,91882 \pm 0,93166$ | Não ($\sigma > 0,15$) | **10,419** | $120,07912 \pm \mathbf{0,05290}$ | **Sim (100%)** | **`ENF detectável`** (em 120 Hz) | `0` |
| **Caso B** | `video_sintetico_1_2.wav` | 7 | 11,160 | $59,57500 \pm 0,58230$ | Não ($\sigma > 0,15$) | 4,778 | $120,46957 \pm 0,17987$ | Não ($\text{SNR} < 6\text{ dB}$) | **`ENF não detectável`** | Nenhuma gerada (OWA) |
| **Caso B** | `video_sintetico_1_2_mono.wav` | 7 | 11,162 | $59,57498 \pm 0,58231$ | Não ($\sigma > 0,15$) | 4,769 | $120,46968 \pm 0,17985$ | Não ($\text{SNR} < 6\text{ dB}$) | **`ENF não detectável`** | Nenhuma gerada (OWA) |
| **Caso B** | `video_sintetico_2_1.wav` | 13 | 10,313 | $59,68125 \pm 0,20448$ | Não ($\sigma > 0,15$) | 8,049 | $119,86654 \pm 0,29619$ | Não ($\sigma > 0,15$) | **`ENF não detectável`** | Nenhuma gerada (OWA) |
| **Caso B** | `video_sintetico_2_1_mono.wav` | 13 | 10,313 | $59,68125 \pm 0,20448$ | Não ($\sigma > 0,15$) | 8,049 | $119,86654 \pm 0,29620$ | Não ($\sigma > 0,15$) | **`ENF não detectável`** | Nenhuma gerada (OWA) |
| **Caso B** | `video_sintetico_2_2.wav` | 9 | 9,579 | $60,01572 \pm 0,40557$ | Não ($\sigma > 0,15$) | 5,485 | $119,93954 \pm 0,37689$ | Não ($\text{SNR} < 6\text{ dB}$) | **`ENF não detectável`** | Nenhuma gerada (OWA) |
| **Caso B** | `video_sintetico_2_2_mono.wav` | 9 | 9,579 | $60,01573 \pm 0,40557$ | Não ($\sigma > 0,15$) | 5,485 | $119,93954 \pm 0,37689$ | Não ($\text{SNR} < 6\text{ dB}$) | **`ENF não detectável`** | Nenhuma gerada (OWA) |

*Observação metodológica (OWA):* Nos arquivos onde a energia espectral em torno de 60/120 Hz é dominada pelos formantes/fundamental da fala (causando flutuação $\sigma_{\text{norm}} > 0{,}15\text{ Hz}$) ou possui SNR abaixo de $6{,}0\text{ dB}$, o exame é registrado com `oem:resultadoExame "ENF não detectável"` e **nenhum** indivíduo de achado é instanciado. Em `video_original_1` e `video_sintetico_1_1`, o 2º harmônico (`120 Hz`) apresentou componente estável ($\text{SNR} \approx 9{,}0\text{ a }10{,}4\text{ dB}$, $\sigma_{\text{norm}} \le 0{,}053\text{ Hz}$), sem saltos abruptos acima do limiar (`0` indivíduos `oem:DescontinuidadeENF`).

---

## 4. Exame de Metadados de Contêiner e Estrutura de GOP (`ffprobe -show_frames`)

### 4.1. Estrutura de Quadros e GOP Extraída

| Caso | Vídeo (`data/work/...`) | Resolução | FPS | `time_base` Vídeo | `time_base` Áudio (`sample_rate`) | Total de Quadros | Quadros `I` / `P` / `B` | Nº de GOPs | Tamanhos de GOP (`gop_lengths`) | Prefixo do Padrão de Quadros |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Caso A** | `video_original_1.mp4` | `478x850` | `30/1` | `1/90000` | `1/48000` (`48000 Hz`) | 217 | `1 / 216 / 0` | 1 | `[217]` | `IPPPPPPPPPPPPPPPPPPP` |
| **Caso A** | `Video_original_2.mp4` | `576x1024` | `30/1` | `1/15360` | `1/44100` (`44100 Hz`) | 1877 | `8 / 547 / 1322` | 8 | `[250, 250, 250, 250, 250, 250, 250, 127]` | `IBPBBPBBPBBBPBBBPBBB` |
| **Caso B** | `video_sintetico_1_1.mp4` | `848x478` | `24/1` | `1/90000` | `1/48000` (`48000 Hz`) | 240 | `1 / 239 / 0` | 1 | `[240]` | `IPPPPPPPPPPPPPPPPPPP` |
| **Caso B** | `video_sintetico_1_2.mp4` | `848x478` | `24/1` | `1/90000` | `1/48000` (`48000 Hz`) | 240 | `1 / 239 / 0` | 1 | `[240]` | `IPPPPPPPPPPPPPPPPPPP` |
| **Caso B** | `video_sintetico_2_1.mp4` | `478x850` | `30/1` | `1/90000` | `1/48000` (`44100 Hz`) | 498 | `2 / 496 / 0` | 2 | `[300, 198]` | `IPPPPPPPPPPPPPPPPPPP` |
| **Caso B** | `video_sintetico_2_2.mp4` | `476x848` | `30/1` | `1/90000` | `1/48000` (`44100 Hz`) | 387 | `2 / 385 / 0` | 2 | `[300, 87]` | `IPPPPPPPPPPPPPPPPPPP` |

### 4.2. Indícios Gerados (`oem:IndicioDeRecodificacao` $\sqsubseteq$ `oem:IndicioDeEdicao`)

Na comparação com os respectivos originais do Caso A (`video_original_1.mp4` para o Conjunto 1; `Video_original_2.mp4` para o Conjunto 2), foram gerados exclusivamente **indícios** (nunca conclusões):

- **`video_sintetico_1_1.mp4` vs `video_original_1.mp4` (4 indícios):**
  1. `DivergenciaDeResolucaoOuOrientacao`: `478x850` $\rightarrow$ `848x478`
  2. `DivergenciaDeTaxaDeQuadros`: `30/1` $\rightarrow$ `24/1 fps`
  3. `DivergenciaDeEstruturaGOP`: `I=1, P=216, B=0, maxGOP=217` $\rightarrow$ `I=1, P=239, B=0, maxGOP=240`
  4. `DivergenciaDeBitrate`: Áudio reduzido em `59,8%` (`319.352` $\rightarrow$ `128.282 bps`)
- **`video_sintetico_1_2.mp4` vs `video_original_1.mp4` (4 indícios):**
  1. `DivergenciaDeResolucaoOuOrientacao`: `478x850` $\rightarrow$ `848x478`
  2. `DivergenciaDeTaxaDeQuadros`: `30/1` $\rightarrow$ `24/1 fps`
  3. `DivergenciaDeEstruturaGOP`: `I=1, P=216, B=0, maxGOP=217` $\rightarrow$ `I=1, P=239, B=0, maxGOP=240`
  4. `DivergenciaDeBitrate`: Áudio reduzido em `59,8%` (`319.352` $\rightarrow$ `128.305 bps`)
- **`video_sintetico_2_1.mp4` vs `Video_original_2.mp4` (5 indícios):**
  1. `DivergenciaDeResolucaoOuOrientacao`: `576x1024` $\rightarrow$ `478x850`
  2. `DivergenciaDeEstruturaGOP`: Eliminação completa de quadros B e mudança de tamanho de GOP (`I=8, P=547, B=1322, maxGOP=250, padrão=IBPBBPBBPB...` $\rightarrow$ `I=2, P=496, B=0, maxGOP=300, padrão=IPPPPPPPPP...`)
  3. `DivergenciaDeTimeBaseVideo`: `1/15360` $\rightarrow$ `1/90000`
  4. `InconsistenciaSampleRateTimeBaseAudio`: `sample_rate=44100 Hz`, mas `time_base=1/48000` (na referência: `1/44100`)
  5. `DivergenciaDeBitrate`: Vídeo aumentado em `89,7%` (`699.618` $\rightarrow$ `1.326.996 bps`)
- **`video_sintetico_2_2.mp4` vs `Video_original_2.mp4` (5 indícios):**
  1. `DivergenciaDeResolucaoOuOrientacao`: `576x1024` $\rightarrow$ `476x848`
  2. `DivergenciaDeEstruturaGOP`: Eliminação completa de quadros B e mudança de tamanho de GOP (`I=8, P=547, B=1322, maxGOP=250, padrão=IBPBBPBBPB...` $\rightarrow$ `I=2, P=385, B=0, maxGOP=300, padrão=IPPPPPPPPP...`)
  3. `DivergenciaDeTimeBaseVideo`: `1/15360` $\rightarrow$ `1/90000`
  4. `InconsistenciaSampleRateTimeBaseAudio`: `sample_rate=44100 Hz`, mas `time_base=1/48000` (na referência: `1/44100`)
  5. `DivergenciaDeBitrate`: Vídeo aumentado em `104,0%` (`699.618` $\rightarrow$ `1.426.896 bps`)
完美
