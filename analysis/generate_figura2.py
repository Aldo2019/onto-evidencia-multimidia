"""
Generate Figure 2 (results/figuras/figura2_espectrogramas.png):
Three stacked mono spectrograms (video_original_1, video_recodificado_mensageiro_1, video_sintetico_1_1)
using parameters from analysis/config.yaml, shared color scale (common vmin/vmax), 0-8 kHz frequency axis,
Portuguese axis labels, single colorbar, panel labels (a), (b), (c), width 16 cm, height <= 14 cm, 300 dpi,
and no internal panel titles.
"""

from __future__ import annotations

import hashlib
import pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import scipy.io.wavfile as wavfile
import scipy.signal as signal
import yaml


BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "analysis" / "config.yaml"
OUT_PATH = BASE_DIR / "results" / "figuras" / "figura2_espectrogramas.png"


def load_mono_wav(wav_path: pathlib.Path) -> tuple[int, np.ndarray]:
    fs, data = wavfile.read(str(wav_path))
    if data.ndim > 1:
        sig = np.mean(data.astype(np.float64), axis=1)
    else:
        sig = data.astype(np.float64)
    if data.dtype == np.int16:
        sig /= 32768.0
    elif data.dtype == np.int32:
        sig /= 2147483648.0
    elif data.dtype == np.uint8:
        sig = (sig - 128.0) / 128.0
    return fs, sig


def main() -> None:
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)["spectrogram"]

    window_type = cfg["window_type"]
    nperseg = int(cfg["nperseg"])
    noverlap = int(cfg["noverlap"])
    nfft = int(cfg["nfft"])
    scaling = cfg["scaling"]
    cmap = cfg["cmap"]
    fmax_display = float(cfg["fmax_display_hz"])

    items = [
        ("(a)", BASE_DIR / "data" / "work" / "caso_a" / "video_original_1_mono.wav"),
        ("(b)", BASE_DIR / "data" / "work" / "caso_c" / "video_recodificado_mensageiro_1_mono.wav"),
        ("(c)", BASE_DIR / "data" / "work" / "caso_b" / "video_sintetico_1_1_mono.wav"),
    ]

    computed = []
    global_min = float("inf")
    global_max = float("-inf")

    for label, wav_path in items:
        fs, sig = load_mono_wav(wav_path)
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
        freq_mask = freqs <= fmax_display
        freqs_sub = freqs[freq_mask]
        Sxx_db = 10.0 * np.log10(np.maximum(Sxx[freq_mask, :], 1e-20))
        # Use 1st percentile floor to avoid silence-padding -200 dB distorting dynamic range,
        # while strictly sharing the exact same [vmin, vmax] across all three panels
        p1 = float(np.percentile(Sxx_db, 1.0))
        p100 = float(np.max(Sxx_db))
        global_min = min(global_min, p1)
        global_max = max(global_max, p100)
        computed.append((label, freqs_sub, times, Sxx_db))

    vmin = round(global_min, 2)
    vmax = round(global_max, 2)

    # 16 cm width, 13.5 cm height (<= 14 cm) at 300 dpi
    width_in = 16.0 / 2.54
    height_in = 13.5 / 2.54
    dpi = 300

    plt.rcParams.update({
        "font.size": 9,
        "axes.labelsize": 9,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
    })

    fig, axes = plt.subplots(
        3, 1,
        figsize=(width_in, height_in),
        dpi=dpi,
        sharey=True,
        gridspec_kw={"hspace": 0.28, "left": 0.11, "right": 0.86, "top": 0.97, "bottom": 0.09},
    )

    pcm = None
    for idx, (ax, (label, freqs_sub, times, Sxx_db)) in enumerate(zip(axes, computed)):
        pcm = ax.pcolormesh(
            times,
            freqs_sub,
            Sxx_db,
            shading="gouraud",
            cmap=cmap,
            vmin=vmin,
            vmax=vmax,
        )
        ax.set_ylim(0.0, fmax_display)
        ax.set_xlim(float(times[0]), float(times[-1]))
        ax.set_ylabel("Frequência (Hz)")
        if idx == 2:
            ax.set_xlabel("Tempo (s)")
        # Panel label (a), (b), (c) in top-left corner with high-contrast box, no internal title
        ax.text(
            0.015,
            0.88,
            label,
            transform=ax.transAxes,
            fontsize=10,
            fontweight="bold",
            va="top",
            ha="left",
            color="black",
            bbox={"boxstyle": "round,pad=0.2", "facecolor": "white", "edgecolor": "none", "alpha": 0.85},
        )

    cbar_ax = fig.add_axes([0.88, 0.09, 0.022, 0.88])
    cbar = fig.colorbar(pcm, cax=cbar_ax)
    cbar.set_label("Densidade espectral de potência (dB/Hz)", fontsize=9)
    cbar.ax.tick_params(labelsize=8)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(str(OUT_PATH), dpi=dpi)
    plt.close(fig)

    sha = hashlib.sha256(OUT_PATH.read_bytes()).hexdigest().lower()
    size_b = OUT_PATH.stat().st_size
    px_w = int(round(width_in * dpi))
    px_h = int(round(height_in * dpi))
    print(f"SAVED|{OUT_PATH.relative_to(BASE_DIR)}|SIZE={size_b}|SHA256={sha}|VMIN={vmin}|VMAX={vmax}|PX={px_w}x{px_h}")


if __name__ == "__main__":
    main()
