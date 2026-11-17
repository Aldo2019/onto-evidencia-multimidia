"""
Forensic Multimedia Analysis Pipeline for ISKO-Brasil 2027.

Performs:
1. Spectrogram generation for each extracted .wav file (saved in results/ and results/analises/<caso>/),
   recording parameters as metadata of a HomomorphicTransformation.
2. Electrical Network Frequency (ENF) analysis at 60 Hz and 120 Hz harmonic using parameters from
   analysis/config.yaml. Under Open World Assumption (OWA), if ENF is not detectable above the configured
   SNR threshold, records the Examination with result "ENF não detectável" and generates NO finding.
3. Container & GOP structure comparison (via ffprobe -show_frames) comparing copies against Case A originals,
   generating only evidence indicators (subclasses of IndicioDeEdicao, e.g. IndicioDeRecodificacao),
   never conclusions.
"""

from __future__ import annotations

import csv
import datetime
import hashlib
import json
import math
import pathlib
import subprocess
from typing import Any, Dict, List

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import scipy.io.wavfile as wavfile
import scipy.signal as signal
import yaml


BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "analysis" / "config.yaml"
RESULTS_DIR = BASE_DIR / "results"
SPECTROGRAM_GLOBAL_DIR = RESULTS_DIR / "espectrogramas"
ANALISES_DIR = RESULTS_DIR / "analises"


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest().lower()


def now_iso() -> str:
    return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-3))).isoformat(timespec="seconds")


def load_wav_normalized(wav_path: pathlib.Path) -> tuple[int, np.ndarray, int]:
    """Read WAV file and return (fs, mono_float_signal, n_channels)."""
    fs, data = wavfile.read(str(wav_path))
    if data.ndim == 1:
        n_channels = 1
        sig = data.astype(np.float64)
    else:
        n_channels = data.shape[1]
        sig = np.mean(data.astype(np.float64), axis=1)

    if data.dtype == np.int16:
        sig /= 32768.0
    elif data.dtype == np.int32:
        sig /= 2147483648.0
    elif data.dtype == np.uint8:
        sig = (sig - 128.0) / 128.0
    return fs, sig, n_channels


def generate_spectrogram(
    wav_path: pathlib.Path,
    out_png_case: pathlib.Path,
    out_png_global: pathlib.Path,
    cfg: Dict[str, Any],
) -> Dict[str, Any]:
    """Generate power spectral density spectrogram PNG and return metadata."""
    fs, sig, n_channels = load_wav_normalized(wav_path)
    window_type = cfg["window_type"]
    nperseg = int(cfg["nperseg"])
    noverlap = int(cfg["noverlap"])
    nfft = int(cfg["nfft"])
    scaling = cfg["scaling"]
    cmap = cfg["cmap"]
    dpi = int(cfg["dpi"])
    fmax_display = float(cfg["fmax_display_hz"])

    freqs, times, Sxx = signal.spectrogram(
        sig,
        fs=fs,
        window=window_type,
        nperseg=nperseg,
        noverlap=noverlap,
        nfft=nfft,
        scaling=scaling,
        mode="psd",
    )
    Sxx_db = 10.0 * np.log10(np.maximum(Sxx, 1e-20))

    fig, ax = plt.subplots(figsize=(10, 4.5), dpi=dpi)
    freq_mask = freqs <= min(fmax_display, fs / 2.0)
    pcm = ax.pcolormesh(
        times,
        freqs[freq_mask],
        Sxx_db[freq_mask, :],
        shading="gouraud",
        cmap=cmap,
    )
    ax.axhline(60.0, color="red", linestyle="--", linewidth=0.7, alpha=0.7, label="60 Hz (ENF fundamental)")
    ax.axhline(120.0, color="orange", linestyle=":", linewidth=0.7, alpha=0.7, label="120 Hz (2nd harmonic)")
    ax.set_title(f"Spectrogram (PSD) - {wav_path.name} (fs={fs} Hz, ch={n_channels})")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Frequency (Hz)")
    ax.legend(loc="upper right", fontsize=8)
    cbar = fig.colorbar(pcm, ax=ax)
    cbar.set_label("Power Spectral Density (dB/Hz)")
    fig.tight_layout()

    out_png_case.parent.mkdir(parents=True, exist_ok=True)
    out_png_global.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(str(out_png_case), dpi=dpi)
    fig.savefig(str(out_png_global), dpi=dpi)
    plt.close(fig)

    ts = now_iso()
    png_hash = sha256_file(out_png_case)
    return {
        "input_wav": str(wav_path.relative_to(BASE_DIR)).replace("\\", "/"),
        "input_wav_sha256": sha256_file(wav_path),
        "output_png_case": str(out_png_case.relative_to(BASE_DIR)).replace("\\", "/"),
        "output_png_global": str(out_png_global.relative_to(BASE_DIR)).replace("\\", "/"),
        "output_png_sha256": png_hash,
        "output_png_size_bytes": out_png_case.stat().st_size,
        "sample_rate_hz": fs,
        "channels_input": n_channels,
        "duration_s": round(len(sig) / float(fs), 6),
        "parameters": {
            "window_type": window_type,
            "nperseg": nperseg,
            "noverlap": noverlap,
            "nfft": nfft,
            "scaling": scaling,
            "cmap": cmap,
            "dpi": dpi,
            "fmax_display_hz": fmax_display,
        },
        "timestamp": ts,
    }


def analyze_enf_band(
    sig: np.ndarray,
    fs: int,
    target_freq: float,
    cfg: Dict[str, Any],
) -> Dict[str, Any]:
    """Analyze a single ENF harmonic band (60 Hz or 120 Hz)."""
    target_fs = int(cfg["target_fs_hz"])
    decim_factor = max(1, int(round(fs / target_fs)))
    actual_fs = fs / decim_factor
    if decim_factor > 1:
        sig_dec = signal.decimate(sig, decim_factor, ftype="fir", zero_phase=True)
    else:
        sig_dec = sig.copy()

    half_bw = float(cfg["bandpass_half_width_hz"])
    noise_in = float(cfg["noise_band_inner_offset_hz"])
    noise_out = float(cfg["noise_band_outer_offset_hz"])
    win_sec = float(cfg["stft_window_sec"])
    hop_sec = float(cfg["stft_hop_sec"])
    zpad = int(cfg["zero_padding_factor"])
    snr_thresh = float(cfg["snr_threshold_db"])
    min_stable_ratio = float(cfg["min_stable_windows_ratio"])
    max_std_hz = float(cfg["max_freq_std_hz"])
    step_thresh_hz = float(cfg["discontinuity_step_threshold_hz"])

    nperseg = int(round(win_sec * actual_fs))
    nstep = int(round(hop_sec * actual_fs))
    noverlap = max(0, nperseg - nstep)
    nfft = int(2 ** math.ceil(math.log2(nperseg * zpad)))

    if len(sig_dec) < nperseg:
        nperseg = len(sig_dec)
        noverlap = int(nperseg * 0.75)
        nfft = int(2 ** math.ceil(math.log2(max(256, nperseg * zpad))))

    freqs, times, Zxx = signal.stft(
        sig_dec,
        fs=actual_fs,
        window="hann",
        nperseg=nperseg,
        noverlap=noverlap,
        nfft=nfft,
        boundary=None,
        padded=False,
    )
    power = np.abs(Zxx) ** 2

    sig_mask = (freqs >= target_freq - half_bw) & (freqs <= target_freq + half_bw)
    noise_mask = (
        ((freqs >= target_freq - noise_out) & (freqs <= target_freq - noise_in))
        | ((freqs >= target_freq + noise_in) & (freqs <= target_freq + noise_out))
    )

    sig_freqs = freqs[sig_mask]
    sig_power = power[sig_mask, :]
    noise_power = power[noise_mask, :]

    inst_freqs: List[float] = []
    inst_snrs_db: List[float] = []

    for t_idx in range(sig_power.shape[1]):
        col = sig_power[:, t_idx]
        k_max = int(np.argmax(col))
        # Quadratic interpolation around peak bin in log-magnitude
        if 0 < k_max < len(col) - 1:
            y0 = math.log(max(col[k_max - 1], 1e-30))
            y1 = math.log(max(col[k_max], 1e-30))
            y2 = math.log(max(col[k_max + 1], 1e-30))
            denom = 2.0 * (2.0 * y1 - y0 - y2)
            delta = (y0 - y2) / denom if abs(denom) > 1e-12 else 0.0
            delta = max(-0.5, min(0.5, delta))
            bin_df = sig_freqs[1] - sig_freqs[0] if len(sig_freqs) > 1 else 0.0
            f_est = float(sig_freqs[k_max] + delta * bin_df)
        else:
            f_est = float(sig_freqs[k_max])

        peak_p = float(col[k_max])
        median_noise_p = float(np.median(noise_power[:, t_idx])) if noise_power.shape[0] > 0 else 1e-30
        snr_db = 10.0 * math.log10(max(peak_p, 1e-30) / max(median_noise_p, 1e-30))
        inst_freqs.append(round(f_est, 5))
        inst_snrs_db.append(round(snr_db, 3))

    arr_freqs = np.array(inst_freqs, dtype=np.float64)
    arr_snrs = np.array(inst_snrs_db, dtype=np.float64)
    mean_snr_db = float(np.mean(arr_snrs)) if len(arr_snrs) > 0 else -999.0
    median_snr_db = float(np.median(arr_snrs)) if len(arr_snrs) > 0 else -999.0
    above_thresh_ratio = float(np.mean(arr_snrs >= snr_thresh)) if len(arr_snrs) > 0 else 0.0
    freq_std_hz = float(np.std(arr_freqs)) if len(arr_freqs) > 0 else 999.0
    freq_mean_hz = float(np.mean(arr_freqs)) if len(arr_freqs) > 0 else 0.0

    # Normalization to fundamental 60 Hz equivalent for std/step comparison
    harmonic_order = target_freq / 60.0
    norm_freq_std_hz = freq_std_hz / harmonic_order

    is_stable_detected = (
        (mean_snr_db >= snr_thresh)
        and (above_thresh_ratio >= min_stable_ratio)
        and (norm_freq_std_hz <= max_std_hz)
    )

    discontinuities: List[Dict[str, Any]] = []
    if is_stable_detected and len(arr_freqs) >= 3:
        diffs = np.abs(np.diff(arr_freqs)) / harmonic_order
        med_diff = float(np.median(diffs))
        mad_diff = float(np.median(np.abs(diffs - med_diff))) + 1e-9
        for i, d_val in enumerate(diffs):
            z_robust = (d_val - med_diff) / (1.4826 * mad_diff)
            if d_val >= step_thresh_hz and z_robust >= float(cfg["discontinuity_zscore_threshold"]):
                t_inst = float((times[i] + times[i + 1]) / 2.0)
                discontinuities.append({
                    "instant_s": round(t_inst, 3),
                    "delta_freq_norm_hz": round(float(d_val), 5),
                    "robust_zscore": round(float(z_robust), 3),
                    "freq_before_hz": round(float(arr_freqs[i]), 5),
                    "freq_after_hz": round(float(arr_freqs[i + 1]), 5),
                })

    return {
        "target_freq_hz": target_freq,
        "decimated_fs_hz": actual_fs,
        "num_windows": int(len(times)),
        "times_s": [round(float(t), 3) for t in times],
        "instantaneous_freqs_hz": inst_freqs,
        "instantaneous_snr_db": inst_snrs_db,
        "mean_snr_db": round(mean_snr_db, 3),
        "median_snr_db": round(median_snr_db, 3),
        "above_threshold_ratio": round(above_thresh_ratio, 3),
        "freq_mean_hz": round(freq_mean_hz, 5),
        "freq_std_hz": round(freq_std_hz, 5),
        "normalized_freq_std_hz": round(norm_freq_std_hz, 5),
        "detected_stable": bool(is_stable_detected),
        "discontinuities": discontinuities,
    }


def analyze_enf_for_wav(
    wav_path: pathlib.Path,
    out_dir: pathlib.Path,
    cfg: Dict[str, Any],
) -> Dict[str, Any]:
    """Run ENF analysis at 60 Hz and 120 Hz for a WAV file."""
    fs, sig, n_channels = load_wav_normalized(wav_path)
    band_60 = analyze_enf_band(sig, fs, 60.0, cfg)
    band_120 = analyze_enf_band(sig, fs, 120.0, cfg)

    any_detected = band_60["detected_stable"] or band_120["detected_stable"]
    if any_detected:
        exam_result = "ENF detectável"
    else:
        exam_result = "ENF não detectável"

    all_discontinuities: List[Dict[str, Any]] = []
    if band_60["detected_stable"]:
        for d in band_60["discontinuities"]:
            all_discontinuities.append({"band_hz": 60.0, **d})
    if band_120["detected_stable"]:
        for d in band_120["discontinuities"]:
            all_discontinuities.append({"band_hz": 120.0, **d})

    # Save ENF diagnostic plot
    fig, axes = plt.subplots(2, 1, figsize=(9, 5.5), dpi=150, sharex=True)
    axes[0].plot(band_60["times_s"], band_60["instantaneous_freqs_hz"], "o-", label="60 Hz peak track", markersize=3)
    axes[0].axhline(60.0, color="gray", linestyle="--", linewidth=0.8)
    axes[0].set_ylabel("Freq around 60 Hz (Hz)")
    axes[0].set_title(
        f"ENF Exam: {wav_path.name} -> {exam_result} "
        f"(SNR60={band_60['mean_snr_db']} dB, SNR120={band_120['mean_snr_db']} dB, Thr={cfg['snr_threshold_db']} dB)"
    )
    axes[0].legend(loc="upper right", fontsize=8)

    axes[1].plot(band_120["times_s"], band_120["instantaneous_freqs_hz"], "s-", color="tab:orange", label="120 Hz peak track", markersize=3)
    axes[1].axhline(120.0, color="gray", linestyle="--", linewidth=0.8)
    axes[1].set_ylabel("Freq around 120 Hz (Hz)")
    axes[1].set_xlabel("Time (s)")
    axes[1].legend(loc="upper right", fontsize=8)
    fig.tight_layout()

    out_dir.mkdir(parents=True, exist_ok=True)
    plot_path = out_dir / f"enf_{wav_path.stem}.png"
    fig.savefig(str(plot_path), dpi=150)
    plt.close(fig)

    # Save curve CSV
    csv_path = out_dir / f"enf_{wav_path.stem}.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["time_s", "freq_60_hz", "snr_60_db", "freq_120_hz", "snr_120_db"])
        for i in range(len(band_60["times_s"])):
            writer.writerow([
                band_60["times_s"][i],
                band_60["instantaneous_freqs_hz"][i],
                band_60["instantaneous_snr_db"][i],
                band_120["instantaneous_freqs_hz"][i],
                band_120["instantaneous_snr_db"][i],
            ])

    return {
        "input_wav": str(wav_path.relative_to(BASE_DIR)).replace("\\", "/"),
        "input_wav_sha256": sha256_file(wav_path),
        "sample_rate_hz": fs,
        "channels": n_channels,
        "snr_threshold_db": cfg["snr_threshold_db"],
        "band_60hz": band_60,
        "band_120hz": band_120,
        "enf_detectable": any_detected,
        "exam_result": exam_result,
        "discontinuities": all_discontinuities,
        "curve_csv": str(csv_path.relative_to(BASE_DIR)).replace("\\", "/"),
        "curve_csv_sha256": sha256_file(csv_path),
        "diagnostic_png": str(plot_path.relative_to(BASE_DIR)).replace("\\", "/"),
        "diagnostic_png_sha256": sha256_file(plot_path),
        "timestamp": now_iso(),
    }


def analyze_video_gop_and_container(video_path: pathlib.Path) -> Dict[str, Any]:
    """Run ffprobe -show_format -show_streams and -show_frames (video) to extract GOP & container structure."""
    cmd_meta = [
        "ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        str(video_path),
    ]
    res_meta = subprocess.run(cmd_meta, capture_output=True, text=True, check=True)
    meta_json = json.loads(res_meta.stdout)

    cmd_frames = [
        "ffprobe",
        "-v", "quiet",
        "-select_streams", "v:0",
        "-show_entries", "frame=pict_type,key_frame,pkt_pts_time,pkt_size",
        "-print_format", "json",
        str(video_path),
    ]
    res_frames = subprocess.run(cmd_frames, capture_output=True, text=True, check=True)
    frames_json = json.loads(res_frames.stdout).get("frames", [])

    pict_types = [f.get("pict_type", "?") for f in frames_json]
    i_count = pict_types.count("I")
    p_count = pict_types.count("P")
    b_count = pict_types.count("B")

    # Compute GOP sizes (distance between consecutive key_frame==1 or pict_type=='I')
    key_indices = [idx for idx, f in enumerate(frames_json) if f.get("key_frame") == 1 or f.get("pict_type") == "I"]
    gop_lengths: List[int] = []
    for k in range(len(key_indices)):
        start = key_indices[k]
        end = key_indices[k + 1] if k + 1 < len(key_indices) else len(frames_json)
        gop_lengths.append(end - start)

    v_stream = next((s for s in meta_json.get("streams", []) if s.get("codec_type") == "video"), {})
    a_stream = next((s for s in meta_json.get("streams", []) if s.get("codec_type") == "audio"), {})
    fmt = meta_json.get("format", {})

    return {
        "video_path": str(video_path.relative_to(BASE_DIR)).replace("\\", "/"),
        "sha256": sha256_file(video_path),
        "size_bytes": int(fmt.get("size", 0)),
        "duration_s": float(fmt.get("duration", 0.0)),
        "total_bitrate_bps": int(fmt.get("bit_rate", 0)),
        "major_brand": fmt.get("tags", {}).get("major_brand"),
        "compatible_brands": fmt.get("tags", {}).get("compatible_brands"),
        "encoder": fmt.get("tags", {}).get("encoder") or v_stream.get("tags", {}).get("encoder"),
        "video_codec": v_stream.get("codec_name"),
        "video_profile": v_stream.get("profile"),
        "video_level": v_stream.get("level"),
        "width": v_stream.get("width"),
        "height": v_stream.get("height"),
        "fps": v_stream.get("r_frame_rate"),
        "video_time_base": v_stream.get("time_base"),
        "has_b_frames": v_stream.get("has_b_frames"),
        "video_bitrate_bps": int(v_stream.get("bit_rate", 0)),
        "extradata_size": v_stream.get("extradata_size"),
        "audio_codec": a_stream.get("codec_name"),
        "audio_profile": a_stream.get("profile"),
        "audio_sample_rate_hz": int(a_stream.get("sample_rate", 0)),
        "audio_time_base": a_stream.get("time_base"),
        "audio_bitrate_bps": int(a_stream.get("bit_rate", 0)),
        "gop": {
            "total_frames": len(frames_json),
            "I_frames": i_count,
            "P_frames": p_count,
            "B_frames": b_count,
            "num_gops": len(gop_lengths),
            "gop_lengths": gop_lengths,
            "min_gop": min(gop_lengths) if gop_lengths else 0,
            "max_gop": max(gop_lengths) if gop_lengths else 0,
            "mean_gop": round(float(np.mean(gop_lengths)), 2) if gop_lengths else 0.0,
            "pattern_prefix": "".join(pict_types[:20]),
        },
        "timestamp": now_iso(),
    }


def compare_with_reference(
    target_info: Dict[str, Any],
    ref_info: Dict[str, Any],
    bitrate_rel_thresh: float,
) -> List[Dict[str, Any]]:
    """Compare target video container/GOP metadata against its Case A reference and return IndicioDeEdicao items."""
    indicios: List[Dict[str, Any]] = []

    if (target_info["width"], target_info["height"]) != (ref_info["width"], ref_info["height"]):
        indicios.append({
            "type": "oem:IndicioDeRecodificacao",
            "subtype": "DivergenciaDeResolucaoOuOrientacao",
            "description_pt": (
                f"Mudança de resolução/orientação em relação à referência ({ref_info['width']}x{ref_info['height']} "
                f"-> {target_info['width']}x{target_info['height']})."
            ),
            "description_en": (
                f"Resolution/orientation change relative to reference ({ref_info['width']}x{ref_info['height']} "
                f"-> {target_info['width']}x{target_info['height']})."
            ),
            "ref_value": f"{ref_info['width']}x{ref_info['height']}",
            "target_value": f"{target_info['width']}x{target_info['height']}",
        })

    if target_info["fps"] != ref_info["fps"]:
        indicios.append({
            "type": "oem:IndicioDeRecodificacao",
            "subtype": "DivergenciaDeTaxaDeQuadros",
            "description_pt": f"Taxa de quadros divergente da referência ({ref_info['fps']} -> {target_info['fps']} fps).",
            "description_en": f"Frame rate diverges from reference ({ref_info['fps']} -> {target_info['fps']} fps).",
            "ref_value": str(ref_info["fps"]),
            "target_value": str(target_info["fps"]),
        })

    if (
        target_info["gop"]["B_frames"] != ref_info["gop"]["B_frames"]
        or target_info["has_b_frames"] != ref_info["has_b_frames"]
        or target_info["gop"]["max_gop"] != ref_info["gop"]["max_gop"]
    ):
        indicios.append({
            "type": "oem:IndicioDeRecodificacao",
            "subtype": "DivergenciaDeEstruturaGOP",
            "description_pt": (
                f"Alteração na estrutura de GOP (Referência: I={ref_info['gop']['I_frames']}, "
                f"P={ref_info['gop']['P_frames']}, B={ref_info['gop']['B_frames']}, maxGOP={ref_info['gop']['max_gop']}, "
                f"padrão='{ref_info['gop']['pattern_prefix']}' vs Alvo: I={target_info['gop']['I_frames']}, "
                f"P={target_info['gop']['P_frames']}, B={target_info['gop']['B_frames']}, maxGOP={target_info['gop']['max_gop']}, "
                f"padrão='{target_info['gop']['pattern_prefix']}')."
            ),
            "description_en": (
                f"GOP structure alteration (Reference: I={ref_info['gop']['I_frames']}, "
                f"P={ref_info['gop']['P_frames']}, B={ref_info['gop']['B_frames']}, maxGOP={ref_info['gop']['max_gop']}, "
                f"pattern='{ref_info['gop']['pattern_prefix']}' vs Target: I={target_info['gop']['I_frames']}, "
                f"P={target_info['gop']['P_frames']}, B={target_info['gop']['B_frames']}, maxGOP={target_info['gop']['max_gop']}, "
                f"pattern='{target_info['gop']['pattern_prefix']}')."
            ),
            "ref_value": f"B={ref_info['gop']['B_frames']},maxGOP={ref_info['gop']['max_gop']},pat={ref_info['gop']['pattern_prefix'][:10]}",
            "target_value": f"B={target_info['gop']['B_frames']},maxGOP={target_info['gop']['max_gop']},pat={target_info['gop']['pattern_prefix'][:10]}",
        })

    if target_info["video_time_base"] != ref_info["video_time_base"]:
        indicios.append({
            "type": "oem:IndicioDeRecodificacao",
            "subtype": "DivergenciaDeTimeBaseVideo",
            "description_pt": (
                f"Mudança de time_base da stream de vídeo ({ref_info['video_time_base']} -> {target_info['video_time_base']})."
            ),
            "description_en": (
                f"Video stream time_base change ({ref_info['video_time_base']} -> {target_info['video_time_base']})."
            ),
            "ref_value": str(ref_info["video_time_base"]),
            "target_value": str(target_info["video_time_base"]),
        })

    expected_tb = f"1/{target_info['audio_sample_rate_hz']}"
    if target_info["audio_time_base"] != expected_tb:
        indicios.append({
            "type": "oem:IndicioDeRecodificacao",
            "subtype": "InconsistenciaSampleRateTimeBaseAudio",
            "description_pt": (
                f"Inconsistência interna na trilha de áudio: sample_rate={target_info['audio_sample_rate_hz']} Hz, "
                f"mas time_base={target_info['audio_time_base']} (na referência: {ref_info['audio_time_base']})."
            ),
            "description_en": (
                f"Internal audio stream inconsistency: sample_rate={target_info['audio_sample_rate_hz']} Hz, "
                f"but time_base={target_info['audio_time_base']} (in reference: {ref_info['audio_time_base']})."
            ),
            "ref_value": str(ref_info["audio_time_base"]),
            "target_value": str(target_info["audio_time_base"]),
        })

    v_diff_rel = abs(target_info["video_bitrate_bps"] - ref_info["video_bitrate_bps"]) / max(1.0, float(ref_info["video_bitrate_bps"]))
    a_diff_rel = abs(target_info["audio_bitrate_bps"] - ref_info["audio_bitrate_bps"]) / max(1.0, float(ref_info["audio_bitrate_bps"]))
    if v_diff_rel >= bitrate_rel_thresh or a_diff_rel >= bitrate_rel_thresh:
        indicios.append({
            "type": "oem:IndicioDeRecodificacao",
            "subtype": "DivergenciaDeBitrate",
            "description_pt": (
                f"Variação acentuada de taxa de bits em relação à referência "
                f"(Vídeo: {ref_info['video_bitrate_bps']} -> {target_info['video_bitrate_bps']} bps [{v_diff_rel*100:.1f}%]; "
                f"Áudio: {ref_info['audio_bitrate_bps']} -> {target_info['audio_bitrate_bps']} bps [{a_diff_rel*100:.1f}%])."
            ),
            "description_en": (
                f"Marked bitrate variation relative to reference "
                f"(Video: {ref_info['video_bitrate_bps']} -> {target_info['video_bitrate_bps']} bps [{v_diff_rel*100:.1f}%]; "
                f"Audio: {ref_info['audio_bitrate_bps']} -> {target_info['audio_bitrate_bps']} bps [{a_diff_rel*100:.1f}%])."
            ),
            "ref_value": f"v={ref_info['video_bitrate_bps']},a={ref_info['audio_bitrate_bps']}",
            "target_value": f"v={target_info['video_bitrate_bps']},a={target_info['audio_bitrate_bps']}",
        })

    return indicios


def main() -> None:
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    cases = {
        "caso_a": [
            BASE_DIR / "data" / "work" / "caso_a" / "video_original_1.mp4",
            BASE_DIR / "data" / "work" / "caso_a" / "Video_original_2.mp4",
        ],
        "caso_b": [
            BASE_DIR / "data" / "work" / "caso_b" / "video_sintetico_1_1.mp4",
            BASE_DIR / "data" / "work" / "caso_b" / "video_sintetico_1_2.mp4",
            BASE_DIR / "data" / "work" / "caso_b" / "video_sintetico_2_1.mp4",
            BASE_DIR / "data" / "work" / "caso_b" / "video_sintetico_2_2.mp4",
        ],
        "caso_c": [
            BASE_DIR / "data" / "work" / "caso_c" / "video_recodificado_mensageiro_1.mp4",
        ],
    }

    summary_all: Dict[str, Any] = {"config_used": config, "cases": {}}

    # First analyze all videos & WAVs
    ref_containers: Dict[str, Dict[str, Any]] = {}

    for case_name, video_list in cases.items():
        case_out_dir = ANALISES_DIR / case_name
        spec_out_dir = case_out_dir / "espectrogramas"
        enf_out_dir = case_out_dir / "enf"
        gop_out_dir = case_out_dir / "container_gop"
        for d in (spec_out_dir, enf_out_dir, gop_out_dir):
            d.mkdir(parents=True, exist_ok=True)

        case_data: Dict[str, Any] = {
            "spectrograms": [],
            "enf_exams": [],
            "container_gop": [],
            "container_indicios": [],
        }

        # 1. Container & GOP for each video in the case
        for v_path in video_list:
            c_info = analyze_video_gop_and_container(v_path)
            gop_json_path = gop_out_dir / f"gop_{v_path.stem}.json"
            with gop_json_path.open("w", encoding="utf-8") as gf:
                json.dump(c_info, gf, indent=2, ensure_ascii=False)
            c_info["gop_json_path"] = str(gop_json_path.relative_to(BASE_DIR)).replace("\\", "/")
            c_info["gop_json_sha256"] = sha256_file(gop_json_path)
            case_data["container_gop"].append(c_info)

            if case_name == "caso_a":
                if "1" in v_path.stem:
                    ref_containers["conjunto_1"] = c_info
                else:
                    ref_containers["conjunto_2"] = c_info

            # 2. Spectrograms & ENF for both stereo (.wav) and mono (_mono.wav)
            for suffix in ["", "_mono"]:
                wav_path = v_path.parent / f"{v_path.stem}{suffix}.wav"
                if not wav_path.exists():
                    continue
                png_case = spec_out_dir / f"espectrograma_{wav_path.stem}.png"
                png_global = SPECTROGRAM_GLOBAL_DIR / f"espectrograma_{wav_path.stem}.png"
                spec_meta = generate_spectrogram(wav_path, png_case, png_global, config["spectrogram"])
                case_data["spectrograms"].append(spec_meta)

                # Run ENF on extracted WAV
                enf_meta = analyze_enf_for_wav(wav_path, enf_out_dir, config["enf"])
                case_data["enf_exams"].append(enf_meta)

        summary_all["cases"][case_name] = case_data

    # 3. Compare Case A and Case B containers against Case A references
    rel_thr = float(config["container_comparison"]["bitrate_relative_diff_threshold"])
    for case_name, case_data in summary_all["cases"].items():
        for c_info in case_data["container_gop"]:
            stem = pathlib.Path(c_info["video_path"]).stem
            ref_key = "conjunto_1" if (
                stem.startswith("video_original_1")
                or stem.startswith("video_sintetico_1_")
                or stem.startswith("video_recodificado_mensageiro_1")
            ) else "conjunto_2"
            ref_info = ref_containers[ref_key]
            indicios = compare_with_reference(c_info, ref_info, rel_thr)
            case_data["container_indicios"].append({
                "target_video": c_info["video_path"],
                "reference_video": ref_info["video_path"],
                "indicios_count": len(indicios),
                "indicios": indicios,
                "timestamp": now_iso(),
            })

        # Save per-case consolidated JSON
        case_summary_path = ANALISES_DIR / case_name / "resumo_analises.json"
        with case_summary_path.open("w", encoding="utf-8") as cf:
            json.dump(case_data, cf, indent=2, ensure_ascii=False)

    # Save global summary JSON
    global_summary_path = ANALISES_DIR / "resumo_geral_analises.json"
    with global_summary_path.open("w", encoding="utf-8") as gf:
        json.dump(summary_all, gf, indent=2, ensure_ascii=False)

    print("ANALYSIS_COMPLETED_SUCCESSFULLY")


if __name__ == "__main__":
    main()
