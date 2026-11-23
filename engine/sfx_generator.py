"""
Meras Studio Procedural Audio Engine
Synthesizes ultra-soft, organic Kurzgesagt-style foley SFX and continuous ambient synth beds.
Enforces scipy low-pass filtering (cutoff < 2500Hz), smooth exponential envelopes, and zero digital clicks.
"""

import os
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter

SAMPLE_RATE = 48000

def apply_lowpass(data: np.ndarray, cutoff_hz: float, fs: int = SAMPLE_RATE, order: int = 2) -> np.ndarray:
    """Applies a smooth Butterworth low-pass filter to eliminate harsh high-frequency screeches."""
    nyq = 0.5 * fs
    norm_cutoff = min(0.95, max(0.01, cutoff_hz / nyq))
    b, a = butter(order, norm_cutoff, btype='low')
    return lfilter(b, a, data)

def apply_bandpass(data: np.ndarray, lowcut: float, highcut: float, fs: int = SAMPLE_RATE, order: int = 2) -> np.ndarray:
    """Applies a smooth Butterworth bandpass filter."""
    nyq = 0.5 * fs
    low = max(20.0, lowcut) / nyq
    high = min(nyq - 20.0, highcut) / nyq
    if low >= high:
        return data
    b, a = butter(order, [low, high], btype='band')
    return lfilter(b, a, data)

def normalize_and_convert(signal: np.ndarray, peak_db: float = -3.0) -> np.ndarray:
    """Safely normalizes signal to peak_db and converts to 16-bit PCM without clipping."""
    peak = np.max(np.abs(signal))
    if peak > 1e-6:
        target_amp = 10.0 ** (peak_db / 20.0)
        signal = signal * (target_amp / peak)
    signal = np.clip(signal, -1.0, 1.0)
    return (signal * 32767).astype(np.int16)

def generate_soft_pop(filepath: str):
    """
    Ultra-soft muted bubble pop (80ms).
    Kurzgesagt visual cue for pill badges, checkmarks, and micro-bubble appearances.
    """
    duration = 0.08  # 80ms
    n_samples = int(SAMPLE_RATE * duration)
    t = np.linspace(0, duration, n_samples, endpoint=False)
    
    # Smooth frequency glide down: 360 Hz -> 110 Hz
    freq = 360.0 * np.exp(-t * 32.0) + 110.0
    phase = 2.0 * np.pi * np.cumsum(freq) / SAMPLE_RATE
    audio = np.sin(phase)
    
    # Warm saturation
    audio = np.tanh(audio * 1.4)
    
    # Smooth attack (4ms raised cosine) to prevent digital click, followed by rapid decay
    attack_len = int(SAMPLE_RATE * 0.005)
    env = np.ones(n_samples)
    env[:attack_len] = 0.5 * (1.0 - np.cos(np.pi * np.linspace(0, 1, attack_len)))
    env[attack_len:] = np.exp(-t[attack_len:] * 48.0)
    
    audio = audio * env
    
    # Low-pass filter at 1600 Hz (strictly < 2500Hz)
    audio = apply_lowpass(audio, 1600.0, SAMPLE_RATE, order=2)
    
    # Centered stereo
    stereo = np.column_stack((audio, audio))
    wavfile.write(filepath, SAMPLE_RATE, normalize_and_convert(stereo, -4.0))
    print(f"[SFX] Generated soft pop -> {filepath}")

def generate_air_whoosh(filepath: str):
    """
    Filtered pink-noise breeze (250ms).
    Smooth organic camera zoom / slide transition without tonal screech.
    """
    duration = 0.25  # 250ms
    n_samples = int(SAMPLE_RATE * duration)
    t = np.linspace(0, duration, n_samples, endpoint=False)
    
    # Filtered noise base
    noise = np.random.normal(0, 1.0, n_samples)
    
    # Smooth dynamic bandpass sweep: center sweeps 380Hz -> 1350Hz -> 420Hz
    # Max frequency stays strictly below 1800Hz
    audio = np.zeros_like(noise)
    n_chunks = 12
    chunk_len = n_samples // n_chunks
    for i in range(n_chunks):
        st = i * chunk_len
        en = (i + 1) * chunk_len if i < n_chunks - 1 else n_samples
        p = i / float(n_chunks)
        center_f = 380.0 + 950.0 * np.sin(p * np.pi)
        low_f = max(80.0, center_f * 0.5)
        high_f = min(2200.0, center_f * 1.5)
        filtered_chunk = apply_bandpass(noise[st:en], low_f, high_f, SAMPLE_RATE, order=2)
        audio[st:en] = filtered_chunk
        
    # Raised cosine bell envelope (Hann window) - guaranteed zero start/end clicks
    envelope = (np.sin(np.pi * (t / duration))) ** 2.2
    audio = audio * envelope
    
    # Low-pass filter at 1900 Hz for warm organic feel
    audio = apply_lowpass(audio, 1900.0, SAMPLE_RATE, order=2)
    
    # Subtle stereo pan from left (0.65/0.35) to right (0.35/0.65)
    pan_l = 0.65 - 0.30 * (t / duration)
    pan_r = 0.35 + 0.30 * (t / duration)
    stereo = np.column_stack((audio * pan_l, audio * pan_r))
    wavfile.write(filepath, SAMPLE_RATE, normalize_and_convert(stereo, -3.5))
    print(f"[SFX] Generated air whoosh -> {filepath}")

def generate_gentle_chime(filepath: str):
    """
    Warm marimba / sine harmonic insight chime (300ms).
    Used for psychological insight, cognitive reveals, and explorer discovery cues.
    """
    duration = 0.30  # 300ms
    n_samples = int(SAMPLE_RATE * duration)
    t = np.linspace(0, duration, n_samples, endpoint=False)
    
    # Warm acoustic harmonic progression (C5 fundamental + soft 3rd harmonic G6)
    f0 = 523.25   # C5
    f1 = 1046.50  # C6
    f2 = 1569.75  # G6
    
    tone0 = np.sin(2.0 * np.pi * f0 * t)
    tone1 = np.sin(2.0 * np.pi * f1 * t)
    tone2 = np.sin(2.0 * np.pi * f2 * t)
    
    audio = 0.70 * tone0 + 0.22 * tone1 + 0.08 * tone2
    
    # Attack envelope (8ms smooth cosine attack) and exponential decay
    att_samples = int(SAMPLE_RATE * 0.008)
    env = np.ones(n_samples)
    env[:att_samples] = 0.5 * (1.0 - np.cos(np.pi * np.linspace(0, 1, att_samples)))
    env[att_samples:] = np.exp(-t[att_samples:] * 15.0)
    audio = audio * env
    
    # Low-pass at 2000 Hz to retain warm woody body without piercing treble
    audio = apply_lowpass(audio, 2000.0, SAMPLE_RATE, order=2)
    
    stereo = np.column_stack((audio * 0.95, audio * 1.05))
    wavfile.write(filepath, SAMPLE_RATE, normalize_and_convert(stereo, -3.0))
    print(f"[SFX] Generated gentle chime -> {filepath}")

def generate_sub_drop(filepath: str):
    """
    Smooth sub-bass swell (400ms).
    Gravity revelation cue when an unsettling cognitive flaw or contradiction is stated.
    """
    duration = 0.40  # 400ms
    n_samples = int(SAMPLE_RATE * duration)
    t = np.linspace(0, duration, n_samples, endpoint=False)
    
    # Smooth low descent: 72 Hz -> 36 Hz
    freq = 72.0 * np.exp(-t * 2.8) + 36.0
    phase = 2.0 * np.pi * np.cumsum(freq) / SAMPLE_RATE
    audio = np.sin(phase) + 0.25 * np.sin(phase * 2.0)
    
    # Gentle analog saturation
    audio = np.tanh(audio * 1.5)
    
    # Swell envelope: 25ms attack, smooth exponential decay
    att_samples = int(SAMPLE_RATE * 0.025)
    env = np.ones(n_samples)
    env[:att_samples] = 0.5 * (1.0 - np.cos(np.pi * np.linspace(0, 1, att_samples)))
    env[att_samples:] = np.exp(-t[att_samples:] * 7.5)
    audio = audio * env
    
    # Strictly low-pass below 250 Hz (deep rumble, zero clicks)
    audio = apply_lowpass(audio, 250.0, SAMPLE_RATE, order=2)
    
    stereo = np.column_stack((audio, audio))
    wavfile.write(filepath, SAMPLE_RATE, normalize_and_convert(stereo, -2.5))
    print(f"[SFX] Generated sub drop -> {filepath}")

def generate_ambient_bed(filepath: str, duration: float = 60.0):
    """
    Continuous warm cosmic ambient synth bed (Kurzgesagt aesthetic).
    D-minor / A-modal ethereal progression with slow undulating filter modulation.
    """
    n_samples = int(SAMPLE_RATE * duration)
    t = np.linspace(0, duration, n_samples, endpoint=False)
    
    # Warm modal chord frequencies: D2 (73.42), A2 (110.0), F3 (174.61), C4 (261.63), E4 (329.63)
    chord = [
        (73.42, 0.32, 0.0),
        (73.85, 0.24, 0.35),   # subtle chorus detune
        (110.00, 0.24, -0.25),
        (174.61, 0.18, 0.20),
        (261.63, 0.14, -0.20),
        (329.63, 0.10, 0.25)
    ]
    
    left = np.zeros(n_samples)
    right = np.zeros(n_samples)
    
    # Very slow breathing LFO (0.08 Hz and 0.05 Hz)
    lfo1 = 0.5 + 0.5 * np.sin(2.0 * np.pi * 0.08 * t)
    lfo2 = 0.5 + 0.5 * np.cos(2.0 * np.pi * 0.05 * t)
    
    for base_freq, amp, pan in chord:
        # Subtle vibrato
        vib = np.sin(2.0 * np.pi * 0.2 * t) * 0.3
        phase = 2.0 * np.pi * np.cumsum(base_freq + vib) / SAMPLE_RATE
        sig = np.sin(phase) + 0.15 * np.sin(phase * 2.0)
        sig = sig * amp * (0.85 + 0.15 * lfo1)
        
        pan_l = np.clip(0.5 - pan * 0.5, 0.1, 0.9)
        pan_r = np.clip(0.5 + pan * 0.5, 0.1, 0.9)
        left += sig * pan_l
        right += sig * pan_r
        
    # Ethereal cosmic dust (filtered warm soft noise)
    dust = np.random.normal(0, 0.012, n_samples)
    dust_filtered = apply_bandpass(dust, 180.0, 1800.0, SAMPLE_RATE, order=2)
    left += dust_filtered * (0.6 + 0.4 * lfo2)
    right += dust_filtered * (0.4 + 0.6 * lfo2)
    
    # Low-pass filter overall mix below 2200 Hz for warm velvety tone
    left = apply_lowpass(left, 2200.0, SAMPLE_RATE, order=2)
    right = apply_lowpass(right, 2200.0, SAMPLE_RATE, order=2)
    
    # 2.0 second smooth fade in and fade out
    fade_samples = int(SAMPLE_RATE * 2.0)
    fade_in = 0.5 * (1.0 - np.cos(np.pi * np.linspace(0, 1, fade_samples)))
    fade_out = 0.5 * (1.0 + np.cos(np.pi * np.linspace(0, 1, fade_samples)))
    left[:fade_samples] *= fade_in
    right[:fade_samples] *= fade_in
    left[-fade_samples:] *= fade_out
    right[-fade_samples:] *= fade_out
    
    stereo = np.column_stack((left, right))
    wavfile.write(filepath, SAMPLE_RATE, normalize_and_convert(stereo, -4.5))
    print(f"[SFX] Generated continuous ambient bed ({duration:.1f}s) -> {filepath}")

def build_all_sfx(output_dir: str):
    """Generates all soft foley SFX and continuous ambient bed."""
    os.makedirs(output_dir, exist_ok=True)
    generate_soft_pop(os.path.join(output_dir, "soft_pop.wav"))
    generate_air_whoosh(os.path.join(output_dir, "air_whoosh.wav"))
    generate_gentle_chime(os.path.join(output_dir, "gentle_chime.wav"))
    generate_sub_drop(os.path.join(output_dir, "sub_drop.wav"))
    generate_ambient_bed(os.path.join(output_dir, "ambient_bed.wav"), duration=60.0)

if __name__ == "__main__":
    import sys
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join("assets", "sfx")
    build_all_sfx(out_dir)
