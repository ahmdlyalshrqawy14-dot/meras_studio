"""
Meras Studio Voice Engine
Permanent Broadcast Standards:
- Youthful, sharp, engaging documentary voice: en-US-AndrewMultilingualNeural
- Rate: +5%, Pitch: +1% (+1Hz for edge-tts)
- SSML <emphasis> on core psychological hooks and concepts
- Pronunciation Lock: <phoneme alphabet="ipa" ph="mɪˈrɑːs"><sub alias="Mir-ahs">Meras</sub></phoneme>
- Whisper word-level timestamp alignment with brand name normalization
"""

import os
import sys
import json
import re
import subprocess
from pathlib import Path
from dotenv import load_dotenv

STUDIO_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(STUDIO_ROOT / ".env")

AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY", "").strip()
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION", "").strip()

DEFAULT_VOICE = "en-US-AndrewMultilingualNeural"
DEFAULT_RATE = "+5%"
DEFAULT_PITCH = "+1%"

# High-impact psychological hooks for expressive emphasis
AUTO_EMPHASIS_HOOKS = [
    r"\bcognitive dissonance\b",
    r"\brationalization engine\b",
    r"\bpsychological pain\b",
    r"\bprefrontal cortex\b",
    r"\bdefending a lie\b",
    r"\breality\b",
    r"\blies to you\b",
    r"\blying\b",
    r"\bnever\b",
    r"\bego\b",
    r"\billusion\b",
    r"\bunsettling\b",
    r"\bintellectual plasticity\b",
    r"\bself-justification\b",
    r"\bhumiliation\b",
    r"\bcounter-intuitive\b"
]

def build_ssml(
    text: str,
    voice_name: str = DEFAULT_VOICE,
    style: str = "documentary-narration",
    rate: str = DEFAULT_RATE,
    pitch: str = DEFAULT_PITCH
) -> str:
    """
    Builds documentary storytelling SSML with:
    - Youthful AndrewMultilingualNeural voice
    - Pronunciation lock for 'Meras' using IPA mɪˈrɑːs with fallback sub alias 'Mir-ahs'
    - Expressive emphasis on psychological hooks
    - Strategic curiosity and transition pauses
    """
    processed = text
    
    # 1. Enforce exact clean pronunciation lock for Meras using sub alias 'Miras'
    def _replace_brand(m):
        return '<sub alias="Miras">Meras</sub>'
    
    # Only replace if not already wrapped in sub alias
    processed = re.sub(r'(?<!<sub alias="Miras">)\bMeras\b(?!<\/sub>)', _replace_brand, processed)

    # 2. Transform markdown **bold** into <emphasis level="strong">
    processed = re.sub(r'\*\*(.+?)\*\*', r'<emphasis level="strong">\1</emphasis>', processed)
    # Transform markdown *italic* into <emphasis level="moderate">
    processed = re.sub(r'\*(.+?)\*', r'<emphasis level="moderate">\1</emphasis>', processed)

    # 3. Strategic documentary pauses
    processed = re.sub(r'\.\.\.', ' <break time="320ms"/> ', processed)
    processed = re.sub(r'—|--', ' <break time="200ms"/> ', processed)
    processed = re.sub(r'([;:])\s+', r'\1 <break time="160ms"/> ', processed)

    # 4. Auto-emphasize core psychological keywords
    for hook_pat in AUTO_EMPHASIS_HOOKS:
        def _replace_hook(m):
            matched = m.group(0)
            return f'<emphasis level="moderate">{matched}</emphasis>'
        if f'>{hook_pat}<' not in processed:
            processed = re.sub(hook_pat, _replace_hook, processed, flags=re.IGNORECASE)

    ssml = f"""<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"
       xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">
    <voice name="{voice_name}">
        <mstts:express-as style="{style}">
            <prosody rate="{rate}" pitch="{pitch}">
                {processed}
            </prosody>
        </mstts:express-as>
    </voice>
</speak>"""
    return ssml

def synthesize_azure(ssml: str, wav_path: str, speech_key: str, speech_region: str) -> bool:
    """Synthesize speech using Microsoft Azure Speech SDK with SSML."""
    try:
        import azure.cognitiveservices.speech as speechsdk
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
        speech_config.set_speech_synthesis_output_format(
            speechsdk.SpeechSynthesisOutputFormat.Riff48Khz16BitMonoPcm
        )
        audio_config = speechsdk.audio.AudioOutputConfig(filename=wav_path)
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        
        print(f"[VoiceEngine] Azure Speech Service: Synthesizing ({DEFAULT_VOICE}, rate={DEFAULT_RATE}, pitch={DEFAULT_PITCH})...")
        result = synthesizer.speak_ssml_async(ssml).get()
        
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print(f"[VoiceEngine] Azure synthesis succeeded -> {wav_path}")
            return True
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print(f"[VoiceEngine] Azure Speech Canceled: {cancellation_details.reason}")
            if cancellation_details.error_details:
                print(f"[VoiceEngine] Details: {cancellation_details.error_details}")
            return False
    except Exception as e:
        print(f"[VoiceEngine] Azure Speech SDK Exception: {e}")
        return False
    return False

def synthesize_azure_edge(
    text: str,
    wav_path: str,
    voice_name: str = DEFAULT_VOICE,
    rate: str = DEFAULT_RATE,
    pitch: str = "+1Hz"
) -> bool:
    """
    Direct cloud neural synthesis via Microsoft Azure Neural AndrewMultilingualNeural.
    Applies pronunciation lock ('Mir-ahs' for 'Meras') so it is NEVER mispronounced as 'Moras'.
    """
    import asyncio
    import edge_tts
    
    # Process text for edge_tts:
    # 1. First extract alias if SSML tags present: <sub alias="([^"]+)">.*?</sub>
    clean_text = text
    clean_text = re.sub(r'<sub alias="([^"]+)">.*?</sub>', r'\1', clean_text)
    clean_text = re.sub(r'<phoneme[^>]*>(.*?)</phoneme>', r'\1', clean_text)
    
    # 2. Phonetic pronunciation lock for brand: 'Meras' -> 'Miras'
    # Andrew pronounces 'Miras' naturally and smoothly without spelling letters
    clean_text = re.sub(r'\bMeras\b', 'Miras', clean_text)
    
    # 3. Clean remaining tags
    clean_text = re.sub(r'\.\.\.', '... ', clean_text)
    clean_text = re.sub(r'<[^>]+>', ' ', clean_text)
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    
    temp_mp3 = wav_path + ".tmp.mp3"
    print(f"[VoiceEngine] Neural Cloud TTS: {voice_name} (rate={rate}, pitch={pitch}, pronunciation lock='Miras')...")
    
    async def _synth():
        comm = edge_tts.Communicate(
            text=clean_text,
            voice=voice_name,
            rate=rate,
            pitch=pitch
        )
        await comm.save(temp_mp3)

    try:
        asyncio.run(_synth())
        if os.path.exists(temp_mp3) and os.path.getsize(temp_mp3) > 0:
            creationflags = subprocess.BELOW_NORMAL_PRIORITY_CLASS if hasattr(subprocess, "BELOW_NORMAL_PRIORITY_CLASS") else 0
            subprocess.run([
                "ffmpeg", "-y", "-i", temp_mp3,
                "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le",
                wav_path
            ], check=True, capture_output=True, creationflags=creationflags)
            if os.path.exists(temp_mp3):
                os.remove(temp_mp3)
            print(f"[VoiceEngine] Studio 48kHz PCM WAV generated -> {wav_path}")
            return True
    except Exception as e:
        print(f"[VoiceEngine] Neural TTS error: {e}")
        if os.path.exists(temp_mp3):
            os.remove(temp_mp3)
    return False

def synthesize_fallback(text: str, wav_path: str):
    """Fallback local speech synthesis."""
    print(f"[VoiceEngine] Falling back to local speech synthesis...")
    clean_text = re.sub(r'<[^>]+>', ' ', text)
    clean_text = clean_text.replace("'", "''").strip()
    
    ps_cmd = f"""
    Add-Type -AssemblyName System.Speech;
    $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer;
    $synth.Rate = 1;
    $synth.SetOutputToWaveFile('{wav_path}');
    $synth.Speak('{clean_text}');
    $synth.Dispose();
    """
    creationflags = subprocess.BELOW_NORMAL_PRIORITY_CLASS if hasattr(subprocess, "BELOW_NORMAL_PRIORITY_CLASS") else 0
    res = subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True, text=True, creationflags=creationflags)
    if res.returncode == 0 and os.path.exists(wav_path) and os.path.getsize(wav_path) > 0:
        tmp_converted = wav_path + ".tmp.wav"
        subprocess.run([
            "ffmpeg", "-y", "-i", wav_path,
            "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le",
            tmp_converted
        ], capture_output=True, creationflags=creationflags)
        if os.path.exists(tmp_converted):
            os.replace(tmp_converted, wav_path)
        print(f"[VoiceEngine] Local fallback generated -> {wav_path}")
        return True
    return False

def normalize_transcription_text(text: str) -> str:
    """Normalizes phonetic variations of 'Meras' back to clean brand casing."""
    normalized = re.sub(
        r'\b(mehr-ahs|meh-rahs|mehrahs|meh ahais|marry h\.s\.|maryhs|mary hs|mirror h\'s|mirror hs|mirror h|mirror ahs|mirror ahss|mirror hia|mirror|maras|moras|meeras|miras)\b',
        'Meras',
        text,
        flags=re.IGNORECASE
    )
    # Also clean up greeting misheard by Whisper
    normalized = re.sub(r'\b(they come to my eyes|vetcom to meh eyes)\b', 'Welcome to Meras', normalized, flags=re.IGNORECASE)
    return normalized

def extract_word_timestamps(wav_path: str, alignment_path: str, model_size: str = "tiny.en") -> dict:
    """
    Extracts high-precision word-level and segment-level timestamps using Faster-Whisper.
    Normalizes brand name occurrences back to 'Meras'.
    """
    from faster_whisper import WhisperModel
    import wave

    with wave.open(wav_path, 'rb') as wf:
        frames = wf.getnframes()
        rate = wf.getframerate()
        duration = frames / float(rate)

    print(f"[VoiceEngine] Aligning word timestamps via Faster-Whisper ({model_size}, duration={duration:.2f}s)...")
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments_gen, info = model.transcribe(wav_path, word_timestamps=True)
    
    words_list = []
    segments_list = []
    
    for seg in segments_gen:
        cleaned_seg_text = normalize_transcription_text(seg.text.strip())
        segments_list.append({
            "id": seg.id,
            "start": round(seg.start, 3),
            "end": round(seg.end, 3),
            "text": cleaned_seg_text
        })
        if seg.words:
            for w in seg.words:
                raw_w = w.word.strip()
                normalized_w = normalize_transcription_text(raw_w)
                words_list.append({
                    "word": normalized_w,
                    "start": round(w.start, 3),
                    "end": round(w.end, 3),
                    "probability": round(w.probability, 3)
                })

    alignment_data = {
        "audio_file": os.path.basename(wav_path),
        "duration": round(duration, 3),
        "language": info.language,
        "language_probability": round(info.language_probability, 3),
        "word_count": len(words_list),
        "words": words_list,
        "segments": segments_list
    }

    with open(alignment_path, "w", encoding="utf-8") as f:
        json.dump(alignment_data, f, indent=2, ensure_ascii=False)

    print(f"[VoiceEngine] Alignment extracted: {len(words_list)} words, duration: {duration:.2f}s -> {alignment_path}")
    return alignment_data

def generate_voice(
    text: str,
    output_dir: str,
    base_name: str = "voice",
    voice_name: str = DEFAULT_VOICE,
    rate: str = DEFAULT_RATE,
    pitch: str = DEFAULT_PITCH
) -> tuple[str, str]:
    """
    Master method:
    1. Compiles SSML with documentary pacing & Meras pronunciation lock
    2. Synthesizes voice.wav via Azure (or Azure Edge Neural en-US-AndrewMultilingualNeural)
    3. Runs Whisper to produce voice_alignment.json
    Returns (wav_path, alignment_path).
    """
    os.makedirs(output_dir, exist_ok=True)
    wav_path = os.path.join(output_dir, f"{base_name}.wav")
    alignment_path = os.path.join(output_dir, f"{base_name}_alignment.json")
    
    if os.path.exists(wav_path) and os.path.getsize(wav_path) > 1000 and os.path.exists(alignment_path) and os.path.getsize(alignment_path) > 100:
        print(f"[VoiceEngine] ⏭️ Checkpoint resume: using existing {wav_path} and {alignment_path}")
        return wav_path, alignment_path

    ssml = build_ssml(text, voice_name=voice_name, rate=rate, pitch=pitch)
    
    azure_configured = (
        AZURE_SPEECH_KEY and 
        AZURE_SPEECH_KEY != "your_azure_speech_key_here" and
        len(AZURE_SPEECH_KEY) >= 20
    )

    success = False
    if azure_configured:
        success = synthesize_azure(ssml, wav_path, AZURE_SPEECH_KEY, AZURE_SPEECH_REGION)
    
    if not success:
        pitch_edge = "+1Hz" if pitch == "+1%" else pitch
        success = synthesize_azure_edge(text, wav_path, voice_name=voice_name, rate=rate, pitch=pitch_edge)
    
    if not success:
        synthesize_fallback(text, wav_path)

    # Extract word timestamps
    extract_word_timestamps(wav_path, alignment_path)
    return wav_path, alignment_path

if __name__ == "__main__":
    test_text = (
        "Welcome to Meras... "
        "Your brain is actively lying to you right now. "
        "At Meras, we explore the hidden mechanics of human cognition."
    )
    test_out = STUDIO_ROOT / "temp"
    print("--- Testing Upgraded Meras Voice Engine (Andrew, rate=+5%, pitch=+1%) ---")
    wav, align = generate_voice(test_text, str(test_out), "test_andrew_voice")
    print(f"Test Voice Output: {wav}")
    print(f"Test Alignment Output: {align}")
