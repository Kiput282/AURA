"""Isolated local STT/TTS worker for Sprint 271 voice daily use."""

from __future__ import annotations

import argparse
import json
import os
import time
import wave
from pathlib import Path
from typing import Any


def _wav_metadata(path: Path) -> dict[str, Any]:
    with wave.open(str(path), "rb") as wav_file:
        sample_rate = wav_file.getframerate()
        frames = wav_file.getnframes()
        return {
            "channels": wav_file.getnchannels(),
            "sample_width": wav_file.getsampwidth(),
            "sample_rate": sample_rate,
            "frames": frames,
            "duration_seconds": (
                frames / sample_rate if sample_rate else 0.0
            ),
            "size_bytes": path.stat().st_size,
        }


def _transcribe(args: argparse.Namespace) -> dict[str, Any]:
    from faster_whisper import WhisperModel

    input_path = Path(args.input).resolve(strict=True)
    model_dir = Path(args.model_dir).resolve(strict=True)

    started = time.monotonic()
    model = WhisperModel(
        str(model_dir),
        device="cpu",
        compute_type="int8",
        cpu_threads=max(1, min(int(args.cpu_threads), os.cpu_count() or 1)),
    )
    segments, info = model.transcribe(
        str(input_path),
        language=args.language,
        beam_size=1,
        best_of=1,
        condition_on_previous_text=False,
        vad_filter=False,
    )
    materialized = list(segments)
    transcript = " ".join(
        segment.text.strip()
        for segment in materialized
        if segment.text.strip()
    ).strip()
    return {
        "status": "ok",
        "operation": "transcribe",
        "transcript": transcript,
        "language": getattr(info, "language", args.language),
        "language_probability": getattr(
            info,
            "language_probability",
            None,
        ),
        "segment_count": len(materialized),
        "elapsed_seconds": round(time.monotonic() - started, 6),
    }


def _synthesize(args: argparse.Namespace) -> dict[str, Any]:
    from piper import PiperVoice

    model_path = Path(args.model).resolve(strict=True)
    config_path = Path(args.config).resolve(strict=True)
    text_path = Path(args.text_file).resolve(strict=True)
    output_path = Path(args.output).resolve()
    text = text_path.read_text(encoding="utf-8")

    started = time.monotonic()
    voice = PiperVoice.load(
        str(model_path),
        config_path=str(config_path),
    )
    with wave.open(str(output_path), "wb") as wav_file:
        voice.synthesize_wav(text, wav_file)

    return {
        "status": "ok",
        "operation": "synthesize",
        "elapsed_seconds": round(time.monotonic() - started, 6),
        "wav": _wav_metadata(output_path),
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    transcribe = subparsers.add_parser("transcribe")
    transcribe.add_argument("--input", required=True)
    transcribe.add_argument("--model-dir", required=True)
    transcribe.add_argument("--language", default="id")
    transcribe.add_argument("--cpu-threads", type=int, default=6)

    synthesize = subparsers.add_parser("synthesize")
    synthesize.add_argument("--text-file", required=True)
    synthesize.add_argument("--output", required=True)
    synthesize.add_argument("--model", required=True)
    synthesize.add_argument("--config", required=True)
    return parser


def main() -> int:
    args = _parser().parse_args()
    if args.command == "transcribe":
        payload = _transcribe(args)
    else:
        payload = _synthesize(args)
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
