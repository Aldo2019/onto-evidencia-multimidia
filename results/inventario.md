# Inventário Forense Preliminar de Arquivos de Vídeo

**Diretórios inspecionados:** `Vídeos/` (6 arquivos, coleta em 2026-11-17) e `data/work/caso_c/` (1 arquivo, acrescentado em 2026-11-22)  
**Modo de operação:** Somente leitura (nenhum arquivo original foi movido, renomeado, convertido ou modificado).

---

## 1. Ferramentas Utilizadas e Versões

- **`ffprobe`**: `8.1.1-full_build-www.gyan.dev` (GCC 15.2.0)
- **`ffmpeg`**: `8.1.1-full_build-www.gyan.dev` (GCC 15.2.0)
- **`exiftool`**: `13.59`

---

## 2. Tabela-Resumo dos Arquivos de Vídeo

| Arquivo | Caminho Relativo | Tamanho (Bytes) | SHA-256 | Contêiner (`major_brand`) | Duração (s) | Vídeo (Codec / Perfil / Nível) | Resolução | FPS | B-Frames | Bitrate Vídeo (bps) | Timebase Vídeo | Áudio (Codec / Perfil) | Sample Rate (Hz) | Canais | Bitrate Áudio (bps) | Timebase Áudio | Encoder |
| :--- | :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `video_original_1.mp4` | `Vídeos/Vídeo_1/video_original_1.mp4` | 1.718.872 | `3abe96337aefc4c4cfb89f24ed6d4bda598b55b0f0d9216245d1dd7fd9984ba3` | `mp42` (`mp42isom`) | 7,246688 | `h264` / High / 31 | 478x850 | 30/1 | 0 | 1.577.083 | `1/90000` | `aac` / LC | 48.000 | 2 (stereo) | 319.352 | `1/48000` | — |
| `video_sintetico_1_1.mp4` | `Vídeos/Vídeo_1/video_sintetico_1_1.mp4` | 2.116.260 | `11fc8dfd6061cda11f308419cd3bb091571521f4976fceaa53f735e3893bd76a` | `mp42` (`mp42isom`) | 10,026667 | `h264` / High / 31 | 848x478 | 24/1 | 0 | 1.560.783 | `1/90000` | `aac` / LC | 48.000 | 2 (stereo) | 128.282 | `1/48000` | — |
| `video_sintetico_1_2.mp4` | `Vídeos/Vídeo_1/video_sintetico_1_2.mp4` | 2.128.149 | `a55dc991a06c7811a4f3b0f18a687db86143dab82390845eac441651b47304b1` | `mp42` (`mp42isom`) | 10,026667 | `h264` / High / 31 | 848x478 | 24/1 | 0 | 1.570.271 | `1/90000` | `aac` / LC | 48.000 | 2 (stereo) | 128.305 | `1/48000` | — |
| `Video_original_2.mp4` | `Vídeos/Vídeo_2/Video_original_2.mp4` | 6.509.060 | `08945ba4c6ca34b15163bba89df473971378b3e658b8ed13a163fa706450ec6e` | `mp42` (`mp42isom`) | 62,566667 | `h264` / High / 31 | 576x1024 | 30/1 | 2 | 699.618 | `1/15360` | `aac` / LC | 44.100 | 2 (stereo) | 128.002 | `1/44100` | — |
| `video_sintetico_2_1.mp4` | `Vídeos/Vídeo_2/video_sintetico_2_1.mp4` | 3.026.983 | `843837539c8aa52c039240016fdfcec1696f301978962004a1e10905498501a6` | `mp42` (`mp42isom`) | 16,678563 | `h264` / High / 31 | 478x850 | 30/1 | 0 | 1.326.996 | `1/90000` | `aac` / LC | 44.100 | 2 (stereo) | 128.041 | `1/48000` | — |
| `video_sintetico_2_2.mp4` | `Vídeos/Vídeo_2/video_sintetico_2_2.mp4` | 2.514.403 | `9e361c539f2ae78207bad6f067e8488dbcf549e9005d5f37dbe3f4daa0ba0969` | `mp42` (`mp42isom`) | 12,985104 | `h264` / High / 31 | 476x848 | 30/1 | 0 | 1.426.896 | `1/90000` | `aac` / LC | 44.100 | 2 (stereo) | 128.282 | `1/48000` | — |
| `video_recodificado_mensageiro_1.mp4` | `data/work/caso_c/video_recodificado_mensageiro_1.mp4` | 925.087 | `361fa834338c76bbc239589c46cc896cd0c524c0fe63a5d5a93f22728a00f3fd` | `isom` (`isomiso2avc1mp41`) | 7,246009 | `h264` / Main / 31 | 476x848 | 30/1 | 2 (`153` quadros B) | 916.790 | `1/15360` | `aac` / LC | 44.100 | 2 (stereo) | 95.586 | `1/44100` | `Lavf62.12.101` |

*Nota sobre arquivo auxiliar presente na pasta:* Também foi localizado o arquivo de imagem `Vídeos/Vídeo_1/Frame_video_utilizado.jpeg` (127.613 bytes; arquivo não versionado, mantido pelo perito), não incluído na tabela acima por não pertencer às extensões de vídeo solicitadas.

---

## 3. Metadados de Tags e ExifTool (6 Arquivos Originais + 1 Recodificado no Cenário C)

- **`creation_time` / `CreateDate` / `ModifyDate` (internos ao contêiner MP4):** Ausentes no `ffprobe` e zerados (`0000:00:00 00:00:00`) no `exiftool` para todos os 6 arquivos originais em `Vídeos/`; ausentes também em `video_recodificado_mensageiro_1.mp4` (`-map_metadata -1`).
- **`encoder` / `Software` / `Make` / `Model`:** Ausentes tanto no `ffprobe` quanto no `exiftool` em todos os 6 arquivos originais em `Vídeos/`. Em `data/work/caso_c/video_recodificado_mensageiro_1.mp4`, o `ffprobe` registra `encoder = Lavf62.12.101` (tag gerada pelo muxer do `ffmpeg`).
- **`com.apple.*` / `com.android.*`:** Ausentes em todos os arquivos.
- **`handler_name` / `HandlerType`:** Ausente nas streams do `ffprobe`; reportado como `Audio Track` no `exiftool` para os 6 arquivos em `Vídeos/`.
- **`ZoneIdentifier`:** Reportado como `Exists` pelo `exiftool` nos 6 arquivos em `Vídeos/` (indicando transferência/download no sistema de arquivos Windows).
- **Campos `pix_fmt`, `color_space` e `exif_*` da linha 8 (`data/work/caso_c/video_recodificado_mensageiro_1.mp4`) no `results/inventario.csv`:** Registrados como `n/a`, pois o arquivo de mídia recodificado não é versionado no repositório (conforme `.gitignore`) e não estava presente neste clone para execução do `exiftool`/`ffprobe` sobre o binário (os demais campos da linha 8 provêm de `results/analises/caso_c/container_gop/gop_video_recodificado_mensageiro_1.json`).

---

## 4. Proposta de Correspondência com os Cenários do Artigo e Observações sobre Metadados

*Mapeamento preliminar, anterior à execução. O mapeamento final está em `results/secao_3_4.md`.*

Com base **exclusivamente** nos nomes de arquivo e nos metadados extraídos:

### Proposta de Mapeamento
- **Cenário A (Gravação original + cópia forense):**
  - Candidatos a gravação original: `video_original_1.mp4` (conjunto `Vídeo_1`) e/ou `Video_original_2.mp4` (conjunto `Vídeo_2`).
  - *Nota sobre a cópia forense:* Nenhum dos 6 arquivos possui SHA-256 idêntico a outro; portanto, a cópia forense isomórfica deverá ser gerada de forma controlada durante o experimento ou um dos originais servirá de base para ela.
- **Cenário B (Versão sintética — deepfake de rosto e/ou voz):**
  - Conjunto `Vídeo_1`: `video_sintetico_1_1.mp4` e `video_sintetico_1_2.mp4` (provavelmente gerados a partir do quadro `Frame_video_utilizado.jpeg` ou de `video_original_1.mp4`).
  - Conjunto `Vídeo_2`: `video_sintetico_2_1.mp4` e `video_sintetico_2_2.mp4`.
- **Cenário C (Versão recodificada por aplicativo de mensagem):**
  - *Hipótese 1 (Metadados de recodificação por mensageiro já presentes nos arquivos):* Todos os 6 arquivos apresentam remoção completa de metadados de dispositivo (`Make`, `Model`, `CreateDate=0000:00:00 00:00:00`, ausência de `encoder`) e resoluções reduzidas típicas de transcodificação por aplicativos de mensagens (como WhatsApp: `478x850`, `848x478`, `576x1024`, `476x848`). Em particular, `Video_original_2.mp4` apresenta `time_base = 1/15360`, `has_b_frames = 2`, bitrate total mais baixo (`832.271 bps`) e `TimeScale = 1000`, ou alternativamente um dos pares `video_sintetico_*_1` vs `video_sintetico_*_2` pode representar o par "antes/depois" de envio por aplicativo de mensagem.
  - *Hipótese 2 (Geração controlada para o Cenário C):* Caso os 4 arquivos nomeados `video_sintetico_*` sejam todos variações puramente generativas (Cenário B) e os 2 `video_original_*` sejam os pontos de partida (Cenário A), precisaremos de sua confirmação sobre qual arquivo já passou por aplicativo de mensagem (Cenário C) ou se um arquivo específico será destinado ao Cenário C.

### Diferenças de Metadados Entre os Arquivos (Marcadas Estritamente como Observações)

1. **Observação (Resolução e Orientação no Conjunto 1):** `video_original_1.mp4` possui resolução vertical `478x850` (retrato), enquanto `video_sintetico_1_1.mp4` e `video_sintetico_1_2.mp4` possuem resolução horizontal `848x478` (paisagem).
2. **Observação (Taxa de Quadros e Duração no Conjunto 1):** `video_original_1.mp4` tem taxa de quadros de `30/1 fps` e duração de `7,25 s`, enquanto `video_sintetico_1_1.mp4` e `video_sintetico_1_2.mp4` têm taxa de quadros de `24/1 fps` e duração exata de `10,00 s` na trilha de vídeo (`10,026667 s` no contêiner).
3. **Observação (Bitrate de Áudio no Conjunto 1):** `video_original_1.mp4` apresenta bitrate de áudio de `319.352 bps` (AAC LC @ 48 kHz), enquanto `video_sintetico_1_1.mp4` (`128.282 bps`) e `video_sintetico_1_2.mp4` (`128.305 bps`) apresentam bitrate de áudio próximo a 128 kbps.
4. **Observação (Similaridade Estrutural entre `video_sintetico_1_1` e `video_sintetico_1_2`):** Ambos têm exatamente a mesma resolução (`848x478`), duração (`10,026667 s`), FPS (`24/1`), número de quadros (`240` vídeo / `470` áudio) e `MediaDataOffset` (`4500`), diferindo apenas levemente no bitrate de vídeo (`1.560.783` vs `1.570.271 bps`), tamanho (`2.116.260` vs `2.128.149` bytes) e hash SHA-256. Conforme `results/inventario_ffprobe/video_sintetico_1_2.json`, o `audio_time_base` de `video_sintetico_1_2.mp4` é `1/48000` (corrigida a divergência anterior de `1/90000` no `.csv`).
5. **Observação (Estrutura de Codificação de `Video_original_2.mp4`):** É o único arquivo entre os seis originais que utiliza quadros bidirecionais (`has_b_frames: 2`), `time_base` de vídeo `1/15360` (contra `1/90000` nos outros cinco), `TimeScale` de contêiner `1000` (contra `48000` nos outros cinco), resolução `576x1024` (`DAR 9:16`), duração de `62,57 s` e bitrate de vídeo mais baixo (`699.618 bps`).
6. **Observação (Inconsistência entre `sample_rate` e `time_base` de Áudio em `video_sintetico_2_1` e `video_sintetico_2_2`):** Em `video_sintetico_2_1.mp4` e `video_sintetico_2_2.mp4`, a trilha de áudio tem `sample_rate = 44100 Hz`, mas o `time_base` da stream de áudio no contêiner está registrado como `1/48000` (diferente de `Video_original_2.mp4`, onde ambos são `44100`).
7. **Observação (Diferença de Resolução e Duração no Conjunto 2):** Enquanto `Video_original_2.mp4` tem `576x1024` e `62,57 s`, `video_sintetico_2_1.mp4` tem `478x850` e `16,68 s`, e `video_sintetico_2_2.mp4` tem `476x848` (2 pixels menor em largura e altura) e `12,99 s`.
8. **Observação (Ausência de Metadados de Origem e Datas Zeradas):** Todos os 6 arquivos originais em `Vídeos/` apresentam `CreateDate` e `ModifyDate` zerados (`0000:00:00 00:00:00`) no cabeçalho MP4 e ausência de tags `encoder`, `Make`, `Model` ou tags proprietárias (`com.apple.*` / `com.android.*`).
9. **Observação (Comparação de `data/work/caso_c/video_recodificado_mensageiro_1.mp4` com `video_original_1.mp4`):** A recodificação controlada do Cenário C alterou múltiplos parâmetros estruturais e de contêiner em relação à matriz `video_original_1.mp4`: perfil H.264 `High` → `Main` (nível 31 mantido), resolução `478x850` → `476x848`, `has_b_frames` `0` (0 quadros B) → `2` com `153` quadros B (GOP `I=1, P=63, B=153`), `sample_rate` de áudio `48000` → `44100 Hz` (`audio_time_base` `1/48000` → `1/44100`), `time_base` de vídeo `1/90000` → `1/15360`, tag `encoder` ausente → `Lavf62.12.101` (`major_brand` `mp42` → `isom`), e redução dos bitrates em **−41,9%** no vídeo (`1.577.083` → `916.790 bps`) e **−70,1%** no áudio (`319.352` → `95.586 bps`).
10. **Observação (Proveniência dos vídeos sintéticos do Conjunto 1):** Proveniência confirmada pelo perito: `video_sintetico_1_1.mp4` e `video_sintetico_1_2.mp4` foram gerados pelo Gemini (Google), em novembro de 2026, a partir de `Frame_video_utilizado.jpeg` e do comando textual registrado em `cases/caso_b/prompt_gemini.txt`. A trilha de áudio também foi sintetizada; nenhum trecho do sinal de `video_original_1.mp4` foi usado como entrada.
