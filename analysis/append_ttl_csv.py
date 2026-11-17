"""Append spectrogram, ENF examination, and container/GOP examination triples and custody rows."""

from __future__ import annotations

import csv
import json
import pathlib
from typing import Any, Dict, List

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
ANALISES_DIR = BASE_DIR / "results" / "analises"
CASES_DIR = BASE_DIR / "cases"

VOCAB_EXTENSION_TTL = """
# =============================================================================
# Extensão de Vocabulário para Análises Periciais (Espectrograma, ENF, GOP)
# =============================================================================

oem:GeracaoDeEspectrograma a owl:Class ;
    rdfs:subClassOf oem:TransformacaoHomomorfica ;
    rdfs:label "Geração de Espectrograma"@pt , "Spectrogram Generation"@en ;
    skos:definition "Transformação homomórfica que projeta um sinal de áudio no domínio tempo-frequência (densidade espectral de potência) sem alterar a evidência de entrada."@pt ,
                    "Homomorphic transformation that projects an audio signal into the time-frequency domain (power spectral density) without altering the input evidence."@en .

oem:ExtracaoDeCurvaENF a owl:Class ;
    rdfs:subClassOf oem:TransformacaoHomomorfica ;
    rdfs:label "Extração de Curva ENF"@pt , "ENF Curve Extraction"@en ;
    skos:definition "Transformação homomórfica que extrai a série temporal da frequência da rede elétrica (60 Hz ou harmônicos) a partir de um sinal de áudio."@pt ,
                    "Homomorphic transformation that extracts the Electrical Network Frequency (60 Hz or harmonics) time series from an audio signal."@en .

oem:ArtefatoAnalitico a owl:Class ;
    rdfs:subClassOf oem:EvidenciaMultimidia ;
    rdfs:label "Artefato Analítico Derivado"@pt , "Derived Analytical Artifact"@en ;
    skos:definition "Representação visual ou numérica (como um espectrograma ou curva de frequência) produzida por uma transformação homomórfica controlada."@pt ,
                    "Visual or numerical representation (such as a spectrogram or frequency curve) produced by a controlled homomorphic transformation."@en .

oem:ExamePericial a owl:Class ;
    rdfs:subClassOf oem:TransformacaoHomomorfica ;
    rdfs:label "Exame Pericial"@pt , "Forensic Examination"@en ;
    skos:definition "Procedimento técnico-pericial documentado que inspeciona propriedades físicas, acústicas ou estruturais de uma evidência multimídia."@pt ,
                    "Documented technical forensic procedure that inspects physical, acoustic, or structural properties of multimedia evidence."@en .

oem:ExameENF a owl:Class ;
    rdfs:subClassOf oem:ExamePericial ;
    rdfs:label "Exame de Frequência da Rede Elétrica (ENF)"@pt , "Electrical Network Frequency (ENF) Examination"@en ;
    skos:definition "Exame pericial que busca a componente da rede elétrica (60 Hz no Brasil e seu harmônico de 120 Hz) para avaliar estabilidade e eventuais descontinuidades de fase ou frequência."@pt ,
                    "Forensic examination that searches for the power grid component (60 Hz in Brazil and its 120 Hz harmonic) to assess stability and potential phase or frequency discontinuities."@en .

oem:ExameMetadadosContainerGOP a owl:Class ;
    rdfs:subClassOf oem:ExamePericial ;
    rdfs:label "Exame de Metadados de Contêiner e Estrutura de GOP"@pt , "Container Metadata and GOP Structure Examination"@en ;
    skos:definition "Exame pericial que compara parâmetros de codificação, contêiner e sequência de quadros (I, P, B) de um vídeo com uma referência conhecida."@pt ,
                    "Forensic examination comparing encoding parameters, container metadata, and frame sequence (I, P, B) of a video against a known reference."@en .

oem:AchadoPericial a owl:Class ;
    rdfs:label "Achado Pericial"@pt , "Forensic Finding"@en ;
    skos:definition "Elemento técnico objetivamente observado durante um exame pericial."@pt ,
                    "Technical element objectively observed during a forensic examination."@en .

oem:IndicioDeEdicao a owl:Class ;
    rdfs:subClassOf oem:AchadoPericial ;
    rdfs:label "Indício de Edição"@pt , "Editing Indicator"@en ;
    skos:definition "Achado técnico que aponta divergência estrutural, acústica ou de codificação compatível com reprocessamento ou edição, sem constituir por si só conclusão de adulteração."@pt ,
                    "Technical finding pointing to structural, acoustic, or encoding divergence compatible with reprocessing or editing, without constituting by itself a conclusion of tampering."@en .

oem:IndicioDeRecodificacao a owl:Class ;
    rdfs:subClassOf oem:IndicioDeEdicao ;
    rdfs:label "Indício de Recodificação"@pt , "Re-encoding Indicator"@en ;
    skos:definition "Indício técnico de que o arquivo de vídeo ou áudio passou por nova etapa de compressão, mudança de resolução, taxa de quadros, estrutura de GOP ou taxa de bits."@pt ,
                    "Technical indicator that the video or audio file underwent a new compression stage, resolution change, frame rate change, GOP structure alteration, or bitrate change."@en .

oem:DescontinuidadeENF a owl:Class ;
    rdfs:subClassOf oem:IndicioDeEdicao ;
    rdfs:label "Descontinuidade de ENF"@pt , "ENF Discontinuity"@en ;
    skos:definition "Salto abrupto estatisticamente significativo na curva da frequência da rede elétrica (ENF) em um instante específico do áudio."@pt ,
                    "Statistically significant abrupt jump in the Electrical Network Frequency (ENF) curve at a specific audio instant."@en .

oem:geraAchado a owl:ObjectProperty ;
    rdfs:label "gera achado"@pt , "generates finding"@en .

oem:comparadoComReferencia a owl:ObjectProperty ;
    rdfs:label "comparado com referência"@pt , "compared with reference"@en .

oem:resultadoExame a owl:DatatypeProperty ;
    rdfs:label "resultado do exame"@pt , "examination result"@en .

oem:snrMedio60Hz_dB a owl:DatatypeProperty ;
    rdfs:label "SNR médio em 60 Hz (dB)"@pt , "mean SNR at 60 Hz (dB)"@en .

oem:snrMedio120Hz_dB a owl:DatatypeProperty ;
    rdfs:label "SNR médio em 120 Hz (dB)"@pt , "mean SNR at 120 Hz (dB)"@en .

oem:limiarSNR_dB a owl:DatatypeProperty ;
    rdfs:label "limiar de SNR configurado (dB)"@pt , "configured SNR threshold (dB)"@en .

oem:desvioPadraoFreqNormalizadoHz a owl:DatatypeProperty ;
    rdfs:label "desvio padrão de frequência normalizado (Hz)"@pt , "normalized frequency standard deviation (Hz)"@en .

oem:instanteSegundos a owl:DatatypeProperty ;
    rdfs:label "instante em segundos"@pt , "instant in seconds"@en .

oem:estruturaGOPResumo a owl:DatatypeProperty ;
    rdfs:label "resumo da estrutura de GOP"@pt , "GOP structure summary"@en .

oem:valorReferencia a owl:DatatypeProperty ;
    rdfs:label "valor na referência"@pt , "reference value"@en .

oem:valorObservado a owl:DatatypeProperty ;
    rdfs:label "valor observado"@pt , "observed value"@en .
"""

WAV_INDIVIDUAL_MAP = {
    "video_original_1.wav": "oem:Evidencia_Audio_Original_1_Stereo",
    "video_original_1_mono.wav": "oem:Evidencia_Audio_Original_1_Mono",
    "Video_original_2.wav": "oem:Evidencia_Audio_Original_2_Stereo",
    "Video_original_2_mono.wav": "oem:Evidencia_Audio_Original_2_Mono",
    "video_sintetico_1_1.wav": "oem:Evidencia_Audio_Sintetico_1_1_Stereo",
    "video_sintetico_1_1_mono.wav": "oem:Evidencia_Audio_Sintetico_1_1_Mono",
    "video_sintetico_1_2.wav": "oem:Evidencia_Audio_Sintetico_1_2_Stereo",
    "video_sintetico_1_2_mono.wav": "oem:Evidencia_Audio_Sintetico_1_2_Mono",
    "video_sintetico_2_1.wav": "oem:Evidencia_Audio_Sintetico_2_1_Stereo",
    "video_sintetico_2_1_mono.wav": "oem:Evidencia_Audio_Sintetico_2_1_Mono",
    "video_sintetico_2_2.wav": "oem:Evidencia_Audio_Sintetico_2_2_Stereo",
    "video_sintetico_2_2_mono.wav": "oem:Evidencia_Audio_Sintetico_2_2_Mono",
}

VIDEO_INDIVIDUAL_MAP = {
    "video_original_1.mp4": "oem:Evidencia_Original_1_Work",
    "Video_original_2.mp4": "oem:Evidencia_Original_2_Work",
    "video_sintetico_1_1.mp4": "oem:Evidencia_Sintetico_1_1_Work",
    "video_sintetico_1_2.mp4": "oem:Evidencia_Sintetico_1_2_Work",
    "video_sintetico_2_1.mp4": "oem:Evidencia_Sintetico_2_1_Work",
    "video_sintetico_2_2.mp4": "oem:Evidencia_Sintetico_2_2_Work",
}


def build_case_ttl_additions(case_name: str, data: Dict[str, Any]) -> tuple[str, List[List[str]]]:
    lines: List[str] = [VOCAB_EXTENSION_TTL]
    csv_rows: List[List[str]] = []

    # 1. Spectrograms
    lines.append("# =============================================================================")
    lines.append("# 1. Transformações Homomórficas: Geração de Espectrogramas")
    lines.append("# =============================================================================\n")

    for spec in data["spectrograms"]:
        wav_name = pathlib.Path(spec["input_wav"]).name
        stem = pathlib.Path(spec["input_wav"]).stem
        in_indiv = WAV_INDIVIDUAL_MAP[wav_name]
        art_id = f"oem:Espectrograma_{stem}"
        hash_id = f"oem:Hash_Espectrograma_{stem}"
        trans_id = f"oem:GeracaoEspectrograma_{stem}"
        reg_id = f"oem:RegistroCustodia_Espectrograma_{stem}"
        p = spec["parameters"]
        param_str = (
            f"scipy.signal.spectrogram(window='{p['window_type']}', nperseg={p['nperseg']}, "
            f"noverlap={p['noverlap']}, nfft={p['nfft']}, scaling='{p['scaling']}', mode='psd', "
            f"cmap='{p['cmap']}', dpi={p['dpi']}, fmax_display_hz={p['fmax_display_hz']})"
        )

        lines.append(f"""{art_id} a owl:NamedIndividual , oem:ArtefatoAnalitico ;
    rdfs:label "Espectrograma PSD de {wav_name}"@pt , "PSD Spectrogram of {wav_name}"@en ;
    oem:caminhoArquivo "{spec['output_png_case']}"^^xsd:string ;
    oem:tamanhoBytes {spec['output_png_size_bytes']} ;
    oem:temValorHash {hash_id} .

{hash_id} a owl:NamedIndividual , oem:ValorHash ;
    rdfs:label "Hash SHA-256 de espectrograma_{stem}.png"@pt , "SHA-256 Hash of espectrograma_{stem}.png"@en ;
    oem:algoritmoHash "SHA-256"^^xsd:string ;
    oem:valorHashHex "{spec['output_png_sha256']}"^^xsd:string ;
    oem:dataHora "{spec['timestamp']}"^^xsd:dateTime .

{trans_id} a owl:NamedIndividual , oem:TransformacaoHomomorfica , oem:GeracaoDeEspectrograma ;
    rdfs:label "Geração Homomórfica de Espectrograma - {stem}"@pt , "Homomorphic Spectrogram Generation - {stem}"@en ;
    oem:temEntrada {in_indiv} ;
    oem:temSaida {art_id} ;
    oem:verificadaPor {hash_id} ;
    oem:registradaEm {reg_id} ;
    oem:versaoFerramenta "Python 3.12.5 / SciPy 1.17.1 / Matplotlib 3.8.4"^^xsd:string ;
    oem:parametrosTransformacao "{param_str}"^^xsd:string ;
    oem:dataHora "{spec['timestamp']}"^^xsd:dateTime .

{reg_id} a owl:NamedIndividual , oem:RegistroDeCustodia ;
    rdfs:label "Registro de Custódia - Espectrograma de {wav_name}"@pt , "Custody Record - Spectrogram of {wav_name}"@en ;
    oem:documentaTransformacao {trans_id} ;
    oem:atestadoPor oem:Agente_Perito ;
    oem:verificadaPor {hash_id} ;
    oem:dataHora "{spec['timestamp']}"^^xsd:dateTime .
""")
        csv_rows.append([
            spec["timestamp"],
            "Agente (perito)",
            "geracao_espectrograma_psd",
            spec["input_wav"],
            spec["output_png_case"],
            spec["input_wav_sha256"],
            spec["output_png_sha256"],
            "oem:GeracaoDeEspectrograma",
        ])

    # 2. ENF Examinations
    lines.append("# =============================================================================")
    lines.append("# 2. Exames Periciais de ENF (60 Hz e Harmônico de 120 Hz)")
    lines.append("# =============================================================================\n")

    for enf in data["enf_exams"]:
        wav_name = pathlib.Path(enf["input_wav"]).name
        stem = pathlib.Path(enf["input_wav"]).stem
        in_indiv = WAV_INDIVIDUAL_MAP[wav_name]
        exam_id = f"oem:ExameENF_{stem}"
        reg_id = f"oem:RegistroCustodia_ExameENF_{stem}"
        curve_id = f"oem:CurvaENF_{stem}"
        hash_curve_id = f"oem:Hash_CurvaENF_{stem}"
        b60 = enf["band_60hz"]
        b120 = enf["band_120hz"]

        extra_triples = ""
        if enf["enf_detectable"]:
            # Also register the extracted curve artifact
            extra_triples = f"""    oem:temSaida {curve_id} ;
    oem:verificadaPor {hash_curve_id} ;
    oem:desvioPadraoFreqNormalizadoHz {b120['normalized_freq_std_hz']} ;"""

        lines.append(f"""{curve_id} a owl:NamedIndividual , oem:ArtefatoAnalitico ;
    rdfs:label "Série Temporal ENF (60/120 Hz) de {wav_name}"@pt , "ENF Time Series (60/120 Hz) of {wav_name}"@en ;
    oem:caminhoArquivo "{enf['curve_csv']}"^^xsd:string ;
    oem:temValorHash {hash_curve_id} .

{hash_curve_id} a owl:NamedIndividual , oem:ValorHash ;
    rdfs:label "Hash SHA-256 de enf_{stem}.csv"@pt , "SHA-256 Hash of enf_{stem}.csv"@en ;
    oem:algoritmoHash "SHA-256"^^xsd:string ;
    oem:valorHashHex "{enf['curve_csv_sha256']}"^^xsd:string ;
    oem:dataHora "{enf['timestamp']}"^^xsd:dateTime .

{exam_id} a owl:NamedIndividual , oem:TransformacaoHomomorfica , oem:ExameENF""" + (
            " , oem:ExtracaoDeCurvaENF" if enf["enf_detectable"] else ""
        ) + f""" ;
    rdfs:label "Exame ENF (60/120 Hz) - {stem}"@pt , "ENF Examination (60/120 Hz) - {stem}"@en ;
    oem:temEntrada {in_indiv} ;
{extra_triples}
    oem:registradaEm {reg_id} ;
    oem:resultadoExame "{enf['exam_result']}"^^xsd:string ;
    oem:limiarSNR_dB {enf['snr_threshold_db']} ;
    oem:snrMedio60Hz_dB {b60['mean_snr_db']} ;
    oem:snrMedio120Hz_dB {b120['mean_snr_db']} ;
    oem:parametrosTransformacao "grid=60Hz, harmonics=[60,120]Hz, target_fs=1200Hz, win=4.0s, hop=1.0s, zpad=8x, snr_thr=6.0dB, min_stable_ratio=0.60, max_norm_std=0.15Hz, step_thr=0.08Hz"^^xsd:string ;
    oem:dataHora "{enf['timestamp']}"^^xsd:dateTime .

{reg_id} a owl:NamedIndividual , oem:RegistroDeCustodia ;
    rdfs:label "Registro de Custódia - Exame ENF de {wav_name}"@pt , "Custody Record - ENF Examination of {wav_name}"@en ;
    oem:documentaTransformacao {exam_id} ;
    oem:atestadoPor oem:Agente_Perito ;
    oem:verificadaPor {hash_curve_id} ;
    oem:dataHora "{enf['timestamp']}"^^xsd:dateTime .
""")
        # If discontinuities exist, generate DescontinuidadeENF individuals (none in current data, but strictly supported)
        for idx, disc in enumerate(enf["discontinuities"], start=1):
            disc_id = f"oem:DescontinuidadeENF_{stem}_{idx}"
            lines.append(f"""{disc_id} a owl:NamedIndividual , oem:DescontinuidadeENF ;
    rdfs:label "Descontinuidade ENF #{idx} em {stem} ({disc['instant_s']} s)"@pt ,
               "ENF Discontinuity #{idx} in {stem} ({disc['instant_s']} s)"@en ;
    oem:instanteSegundos {disc['instant_s']} .

{exam_id} oem:geraAchado {disc_id} .
""")

        csv_rows.append([
            enf["timestamp"],
            "Agente (perito)",
            f"exame_enf_60_120hz ({enf['exam_result']})",
            enf["input_wav"],
            enf["curve_csv"],
            enf["input_wav_sha256"],
            enf["curve_csv_sha256"],
            "oem:ExameENF",
        ])

    # 3. Container & GOP Metadata Comparison
    lines.append("# =============================================================================")
    lines.append("# 3. Exame de Metadados de Contêiner e Estrutura de GOP (ffprobe -show_frames)")
    lines.append("# =============================================================================\n")

    gop_by_path = {g["video_path"]: g for g in data["container_gop"]}

    for comp in data["container_indicios"]:
        v_path = comp["target_video"]
        v_name = pathlib.Path(v_path).name
        stem = pathlib.Path(v_path).stem
        ref_path = comp["reference_video"]
        ref_name = pathlib.Path(ref_path).name
        in_indiv = VIDEO_INDIVIDUAL_MAP[v_name]
        ref_indiv = VIDEO_INDIVIDUAL_MAP[ref_name]
        g_info = gop_by_path[v_path]
        gop = g_info["gop"]

        exam_id = f"oem:ExameContainerGOP_{stem}"
        reg_id = f"oem:RegistroCustodia_ExameContainerGOP_{stem}"
        hash_id = f"oem:Hash_RelatorioGOP_{stem}"
        gop_summary_str = (
            f"frames={gop['total_frames']}, I={gop['I_frames']}, P={gop['P_frames']}, B={gop['B_frames']}, "
            f"num_gops={gop['num_gops']}, gop_lengths={gop['gop_lengths']}, pattern_prefix={gop['pattern_prefix']}"
        )

        achados_links = ""
        indicios_blocks: List[str] = []
        for idx, ind in enumerate(comp["indicios"], start=1):
            ind_id = f"oem:IndicioRecodificacao_{stem}_{idx}_{ind['subtype']}"
            achados_links += f"    oem:geraAchado {ind_id} ;\n"
            indicios_blocks.append(f"""{ind_id} a owl:NamedIndividual , oem:IndicioDeRecodificacao , oem:IndicioDeEdicao ;
    rdfs:label "Indício de Recodificação ({ind['subtype']}) em {v_name}"@pt ,
               "Re-encoding Indicator ({ind['subtype']}) in {v_name}"@en ;
    skos:definition "{ind['description_pt']}"@pt , "{ind['description_en']}"@en ;
    oem:valorReferencia "{ind['ref_value']}"^^xsd:string ;
    oem:valorObservado "{ind['target_value']}"^^xsd:string .
""")

        lines.append(f"""{hash_id} a owl:NamedIndividual , oem:ValorHash ;
    rdfs:label "Hash SHA-256 de gop_{stem}.json"@pt , "SHA-256 Hash of gop_{stem}.json"@en ;
    oem:algoritmoHash "SHA-256"^^xsd:string ;
    oem:valorHashHex "{g_info['gop_json_sha256']}"^^xsd:string ;
    oem:dataHora "{g_info['timestamp']}"^^xsd:dateTime .

{exam_id} a owl:NamedIndividual , oem:TransformacaoHomomorfica , oem:ExameMetadadosContainerGOP ;
    rdfs:label "Exame de Contêiner e GOP - {v_name}"@pt , "Container and GOP Examination - {v_name}"@en ;
    oem:temEntrada {in_indiv} ;
    oem:comparadoComReferencia {ref_indiv} ;
{achados_links}    oem:verificadaPor {hash_id} ;
    oem:registradaEm {reg_id} ;
    oem:comandoExecutado "ffprobe -v quiet -select_streams v:0 -show_entries frame=pict_type,key_frame,pkt_pts_time,pkt_size -print_format json {v_path}"^^xsd:string ;
    oem:estruturaGOPResumo "{gop_summary_str}"^^xsd:string ;
    oem:resultadoExame "{comp['indicios_count']} indício(s) de recodificação observado(s)"^^xsd:string ;
    oem:dataHora "{g_info['timestamp']}"^^xsd:dateTime .

{reg_id} a owl:NamedIndividual , oem:RegistroDeCustodia ;
    rdfs:label "Registro de Custódia - Exame de Contêiner e GOP de {v_name}"@pt ,
               "Custody Record - Container and GOP Examination of {v_name}"@en ;
    oem:documentaTransformacao {exam_id} ;
    oem:atestadoPor oem:Agente_Perito ;
    oem:verificadaPor {hash_id} ;
    oem:dataHora "{g_info['timestamp']}"^^xsd:dateTime .
""")
        lines.extend(indicios_blocks)

        csv_rows.append([
            g_info["timestamp"],
            "Agente (perito)",
            f"exame_container_gop ({comp['indicios_count']}_indicios)",
            v_path,
            g_info["gop_json_path"],
            g_info["sha256"],
            g_info["gop_json_sha256"],
            "oem:ExameMetadadosContainerGOP",
        ])

    return "\n".join(lines), csv_rows


def update_all_cases() -> None:
    for case_name in ("caso_a", "caso_b"):
        json_path = ANALISES_DIR / case_name / "resumo_analises.json"
        ttl_path = CASES_DIR / case_name / f"{case_name}.ttl"
        csv_path = CASES_DIR / case_name / "registro_custodia.csv"

        with json_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        ttl_additions, new_csv_rows = build_case_ttl_additions(case_name, data)

        # Read original TTL up to the marker if already appended, or full file
        ttl_text = ttl_path.read_text(encoding="utf-8")
        marker = "# =============================================================================\n# Extensão de Vocabulário para Análises Periciais"
        if marker in ttl_text:
            ttl_text = ttl_text.split(marker)[0].rstrip() + "\n"

        ttl_path.write_text(ttl_text + "\n" + ttl_additions, encoding="utf-8")

        # Update CSV (keep initial 8 or 16 rows before spectrogram/enf/gop)
        with csv_path.open("r", encoding="utf-8", newline="") as f:
            existing_rows = list(csv.reader(f))

        header = existing_rows[0]
        base_rows = [
            r for r in existing_rows[1:]
            if r[2] in (
                "bloqueio_somente_leitura_original",
                "copia_forense_bit_a_bit",
                "extracao_audio_pcm_s16le_original_stereo",
                "extracao_audio_pcm_s16le_downmix_mono",
            )
        ]

        with csv_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(base_rows)
            writer.writerows(new_csv_rows)


if __name__ == "__main__":
    update_all_cases()
    print("TTL_AND_CSV_UPDATED_SUCCESSFULLY")
