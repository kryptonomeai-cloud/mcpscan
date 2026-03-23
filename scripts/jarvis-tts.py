#!/usr/bin/env python3
"""Generate JARVIS voice briefing using ElevenLabs API."""
import sys
import os
import urllib.request
import json

def main():
    if len(sys.argv) < 3:
        print("Usage: jarvis-tts.py '<text>' <output_path>")
        sys.exit(1)

    text = sys.argv[1]
    output_path = sys.argv[2]

    api_key = os.environ.get("ELEVENLABS_API_KEY", "")
    if not api_key:
        # Try reading from openclaw config
        config_paths = [
            os.path.expanduser("~/.openclaw/openclaw.json"),
            os.path.expanduser("~/.openclaw/.openclaw/openclaw.json"),
        ]
        for cp in config_paths:
            try:
                with open(cp) as f:
                    config = json.load(f)
                api_key = config.get("tts", {}).get("apiKey", "")
                if api_key:
                    break
            except (FileNotFoundError, json.JSONDecodeError):
                continue

    if not api_key:
        print("No ElevenLabs API key found")
        sys.exit(1)

    voice_id = os.environ.get("ELEVENLABS_VOICE_ID", "JBFqnCBsd6RMkjVDRZzb")  # George
    model_id = os.environ.get("ELEVENLABS_MODEL", "eleven_v3")

    payload = json.dumps({
        "text": text,
        "model_id": model_id,
        "voice_settings": {
            "stability": 0.6,
            "similarity_boost": 0.8,
            "style": 0.3,
            "use_speaker_boost": True
        }
    }).encode()

    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "xi-api-key": api_key,
            "Accept": "audio/mpeg"
        }
    )

    try:
        resp = urllib.request.urlopen(req, timeout=30)
        audio_data = resp.read()

        # Convert to ogg if output path ends in .ogg
        if output_path.endswith(".ogg"):
            import subprocess
            mp3_path = output_path.replace(".ogg", ".mp3")
            with open(mp3_path, "wb") as f:
                f.write(audio_data)
            subprocess.run(["ffmpeg", "-y", "-i", mp3_path, "-c:a", "libopus", output_path],
                         capture_output=True, check=True)
            os.remove(mp3_path)
        else:
            with open(output_path, "wb") as f:
                f.write(audio_data)

        print(f"Generated: {output_path} ({len(audio_data)} bytes)")
    except Exception as e:
        print(f"TTS failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
