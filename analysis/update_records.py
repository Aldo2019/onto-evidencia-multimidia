"""Update TTL and custody CSV files with spectrogram, ENF, and container/GOP analysis records."""

from __future__ import annotations

import csv
import json
import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
ANALISES_DIR = BASE_DIR / "results" / "analises"
CASES_DIR = BASE_DIR / "cases"


def fix_indicios_and_save() -> None:
    """Ensure container_indicios in resumo_analises.json use exact prefix matching without re-running heavy DSP."""
    from run_analyses import compare_with_reference
    import yaml

    with (BASE_DIR / "analysis" / "config.yaml").open("r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    rel_thr = float(cfg["container_comparison"]["bitrate_relative_diff_threshold"])

    with (ANALISES_DIR / "caso_a" / "resumo_analises.json").open("r", encoding="utf-8") as f:
        caso_a = json.load(f)
    with (ANALISES_DIR / "caso_b" / "resumo_analises.json").open("r", encoding="utf-8") as f:
        caso_b = json.load(f)

    ref_map = {
        "conjunto_1": caso_a["container_gop"][0],
        "conjunto_2": caso_a["container_gop"][1],
    }

    for case_data in (caso_a, caso_b):
        new_indicios = []
        for c_info in case_data["container_gop"]:
            stem = pathlib.Path(c_info["video_path"]).stem
            ref_key = "conjunto_1" if (stem.startswith("video_original_1") or stem.startswith("video_sintetico_1_")) else "conjunto_2"
            ref_info = ref_map[ref_key]
            inds = compare_with_reference(c_info, ref_info, rel_thr)
            new_indicios.append({
                "target_video": c_info["video_path"],
                "reference_video": ref_info["video_path"],
                "indicios_count": len(inds),
                "indicios": inds,
                "timestamp": c_info["timestamp"],
            })
        case_data["container_indicios"] = new_indicios

    with (ANALISES_DIR / "caso_a" / "resumo_analises.json").open("w", encoding="utf-8") as f:
        json.dump(caso_a, f, indent=2, ensure_ascii=False)
    with (ANALISES_DIR / "caso_b" / "resumo_analises.json").open("w", encoding="utf-8") as f:
        json.dump(caso_b, f, indent=2, ensure_ascii=False)
    with (ANALISES_DIR / "resumo_geral_analises.json").open("w", encoding="utf-8") as f:
        json.dump({"config_used": cfg, "cases": {"caso_a": caso_a, "caso_b": caso_b}}, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    fix_indicios_and_save()
    print("UPDATED_JSON_SUCCESSFULLY")
