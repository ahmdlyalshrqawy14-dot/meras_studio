"""
Meras Studio - Master CLI & Production Orchestrator
Automates end-to-end broadcast-grade Kurzgesagt-style vector animation for "Meras | مِراس".

Architectural Upgrades:
- Dynamic Gemini 2.5 Flash Production Engine with offline algorithmic director fallback
- Base64 font embedding (Montserrat-Bold, Inter-Regular) with zero font pop
- Youthful AndrewMultilingualNeural voice (rate=+2%, pitch=0%) with Meras pronunciation lock
- Audio-Driven Timeline & Zero Cut-off Guarantee (100% audio coverage + 1.2s outro buffer)
- 48kHz float32 audio pipeline with YouTube broadcast loudness normalization (-14 LUFS, -1 dBTP)
- Deterministic 30fps motion rendering with fast JPEG piping and adaptive concurrency (2 workers)
- Exact ffprobe stream duration validation on checkpoint auto-resume
- Iterative zero-drift crossfade video stitching with fail-fast sync checkpoints

Usage:
  python run_studio.py --episode 1         # Full 8-10 minute master production
  python run_studio.py --verify            # 25-second multi-scene broadcast verification test
"""

import os
import sys
import json
import shutil
import argparse
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dotenv import load_dotenv

# Add engine to Python path
STUDIO_ROOT = Path(__file__).resolve().parent
load_dotenv(STUDIO_ROOT / ".env")
sys.path.insert(0, str(STUDIO_ROOT / "engine"))

from voice_engine import generate_voice
from motion_renderer import render_scene_plan
from compositor import composite_video, get_media_duration
from thumbnail_gen import generate_thumbnail
from sfx_generator import build_all_sfx
from episode_generator import (
    load_episode_roadmap,
    generate_full_episode_script,
    build_audio_driven_scene_plan,
    bind_scenes_to_word_timestamps,
    generate_verification_script
)
from dynamic_producer import produce_dynamic_episode, is_gemini_available

class UnbufferedTeeLogger:
    """Streams stdout/stderr in unbuffered real-time to both console and a live log file."""
    def __init__(self, filepath: Path, original_stream):
        self.filepath = filepath
        self.original_stream = original_stream
        self.file = open(filepath, "a", encoding="utf-8", buffering=1)

    def write(self, data):
        self.original_stream.write(data)
        self.original_stream.flush()
        try:
            self.file.write(data)
            self.file.flush()
        except Exception:
            pass

    def flush(self):
        self.original_stream.flush()
        try:
            self.file.flush()
        except Exception:
            pass


def run_preflight_checks(sfx_dir: Path):
    """
    Validates all critical runtime dependencies before executing production:
    - FFmpeg and FFprobe binaries
    - Playwright Chromium headless engine
    - Speech API (Azure or cross-platform fallback)
    - Dynamic LLM Generator (Gemini or offline algorithmic director)
    - Procedural Soft SFX assets (auto-builds if missing)
    """
    print("\n" + "="*60)
    print("🔍 RUNNING MERAS STUDIO PREFLIGHT SYSTEM CHECKS")
    print("="*60)

    # 1. FFmpeg & FFprobe
    ffmpeg_bin = shutil.which("ffmpeg")
    ffprobe_bin = shutil.which("ffprobe")
    if not ffmpeg_bin or not ffprobe_bin:
        raise RuntimeError(f"FFmpeg/FFprobe missing from PATH! ffmpeg: {ffmpeg_bin}, ffprobe: {ffprobe_bin}")
    print(f"✓ FFmpeg & FFprobe detected: {ffmpeg_bin}")

    # 2. Playwright Chromium
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            browser.close()
        print("✓ Playwright Chromium browser initialized successfully")
    except Exception as e:
        raise RuntimeError(f"Playwright Chromium check failed: {e}. Run 'playwright install chromium' to fix.")

    # 3. Speech API
    azure_key = os.getenv("AZURE_SPEECH_KEY")
    if azure_key and azure_key.strip() and not azure_key.startswith("your_"):
        print("✓ Azure Speech synthesis configured (Neural Andrew voice active)")
    else:
        print("ℹ️ Azure Speech key not set or placeholder; will use cross-platform edge-tts fallback")

    # 4. Dynamic LLM Generator
    if is_gemini_available():
        print("✓ Gemini 2.5 Flash API configured (Dynamic AI documentary generation enabled)")
    else:
        print("ℹ️ GEMINI_API_KEY not configured; using high-fidelity offline algorithmic documentary director")

    # 5. SFX assets
    required_sfx = ["ambient_bed.wav", "air_whoosh.wav", "gentle_chime.wav", "soft_pop.wav", "sub_drop.wav"]
    missing = [f for f in required_sfx if not (sfx_dir / f).exists()]
    if missing:
        print(f"[Preflight] Synthesizing missing procedural SFX ({missing})...")
        build_all_sfx(str(sfx_dir))
    print(f"✓ All procedural SFX assets verified in {sfx_dir}")
    print("="*60 + "\n")


def generate_vertical_short(
    input_video: str,
    output_short: str,
    duration: float = 60.0,
    headline: str = "WHY YOUR BRAIN LIES"
):
    """
    Produces a 60-second 9:16 vertical Short from the master cut.
    Uses blurred background + center foreground + branded typography.
    """
    print(f"[Shorts] Generating 60s 9:16 vertical Short cut from master (headline: '{headline}')...")
    creationflags = subprocess.BELOW_NORMAL_PRIORITY_CLASS if hasattr(subprocess, "BELOW_NORMAL_PRIORITY_CLASS") else 0
    safe_headline = headline.replace("\\", "\\\\").replace("'", "").replace(":", "\\:").upper()
    cmd = [
        "ffmpeg", "-y",
        "-threads", "2",
        "-ss", "00:00:00",
        "-t", str(duration),
        "-i", input_video,
        "-vf", (
            "split[v1][v2];"
            "[v1]scale=1080:1920:force_original_aspect_ratio=increase,"
            "crop=1080:1920,"
            "boxblur=15:3,"
            "eq=brightness=-0.15[bg];"
            "[v2]scale=1080:608:force_original_aspect_ratio=decrease[fg];"
            "[bg][fg]overlay=(W-w)/2:(H-h)/2[v_composed];"
            f"[v_composed]drawtext=text='{safe_headline}':fontcolor=white:fontsize=48:font='Montserrat':x=(w-text_w)/2:y=240:shadowcolor=black:shadowx=2:shadowy=2,"
            "drawtext=text='MERAS STUDIO':fontcolor=#00E5FF:fontsize=32:font='Montserrat':x=(w-text_w)/2:y=1680"
        ),
        "-c:v", "libx264",
        "-crf", "16",
        "-maxrate", "10M",
        "-bufsize", "20M",
        "-preset", "fast",
        "-r", "30",
        "-ac", "2",
        "-c:a", "aac",
        "-b:a", "320k",
        output_short
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, creationflags=creationflags)
    if res.returncode != 0:
        fallback_cmd = [
            "ffmpeg", "-y",
            "-threads", "2",
            "-ss", "00:00:00",
            "-t", str(duration),
            "-i", input_video,
            "-vf", (
                "split[v1][v2];"
                "[v1]scale=1080:1920:force_original_aspect_ratio=increase,"
                "crop=1080:1920,"
                "boxblur=15:3[bg];"
                "[v2]scale=1080:608[fg];"
                "[bg][fg]overlay=(W-w)/2:(H-h)/2"
            ),
            "-c:v", "libx264",
            "-crf", "16",
            "-maxrate", "10M",
            "-bufsize", "20M",
            "-preset", "fast",
            "-r", "30",
            "-ac", "2",
            "-c:a", "aac",
            "-b:a", "320k",
            output_short
        ]
        subprocess.run(fallback_cmd, check=True, creationflags=creationflags)
    print(f"[Shorts] YouTube Short rendered -> {output_short} ({os.path.getsize(output_short)} bytes)")


def generate_youtube_metadata(
    ep_data: dict,
    scene_plan: list,
    output_path: str,
    chapters: Optional[list] = None,
    metadata_info: Optional[dict] = None
):
    """
    Generates 3 high-CTR titles, SEO description with chapter timestamps, and tags.
    Dynamically adapts to any episode in the roadmap.
    """
    chapter_timestamps = {}
    current_time = 0.0
    for scene in scene_plan:
        ch_idx = scene.get("chapter_index", 1)
        if ch_idx not in chapter_timestamps:
            m = int(current_time // 60)
            s = int(current_time % 60)
            chapter_timestamps[ch_idx] = f"{m:02d}:{s:02d}"
        current_time += float(scene.get("duration", 5.0))

    # Map dynamic chapter titles
    chapter_titles_map = {}
    if chapters:
        for ch in chapters:
            c_idx = ch.get("chapter_index")
            c_title = ch.get("chapter_title")
            if c_idx and c_title:
                chapter_titles_map[c_idx] = c_title

    chapters_str = []
    for idx in sorted(chapter_timestamps.keys()):
        ch_title = chapter_titles_map.get(idx, f"Chapter {idx}")
        ts = chapter_timestamps[idx]
        chapters_str.append(f"{ts} - {ch_title}")

    # Dynamic or fallback metadata content
    title_options = []
    seo_desc = ""
    tags_list = []
    if metadata_info:
        title_options = metadata_info.get("title_options", [])
        seo_desc = metadata_info.get("seo_description", "")
        tags_list = metadata_info.get("tags", [])

    if not title_options:
        t_base = ep_data.get("title", "Episode")
        title_options = [
            f"{t_base} (The Hidden Science Explained)",
            f"The Real Reason We Struggle With {t_base.split()[-1]}",
            f"How Your Brain Distorts {t_base.split()[-1]}"
        ]
    if not seo_desc:
        seo_desc = ep_data.get("curiosity_logline", "A deep dive into behavioral psychology and neuroscience.")
    if not tags_list:
        tags_list = ["behavioral psychology", "neuroscience", "cognitive science", "meras", "kurzgesagt style"]

    titles_formatted = "\n".join(f"{i+1}. {opt}" for i, opt in enumerate(title_options))
    tags_formatted = ", ".join(tags_list)

    content = f"""======================================================================
MERAS | مِراس - YOUTUBE METADATA FOR EPISODE {ep_data.get('episode_number', 1):02d}
======================================================================

🎯 HIGH-CTR TITLE OPTIONS:
{titles_formatted}

----------------------------------------------------------------------
📝 SEO VIDEO DESCRIPTION:
{seo_desc}

⏱️ CHAPTERS:
{chr(10).join(chapters_str)}

----------------------------------------------------------------------
🏷️ TAGS:
{tags_formatted}

#Psychology #CognitiveScience #Brain #Meras #BehavioralMechanics #Neuroscience
======================================================================
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[Metadata] Generated YouTube metadata -> {output_path}")


def run_production_pipeline(
    episode_num: int = 1,
    is_verification: bool = False,
    sample_duration: Optional[float] = None,
    fps: int = 30
) -> dict:
    """
    Executes the broadcast-grade production pipeline end-to-end.
    """
    print("\n" + "="*70)
    if is_verification:
        mode_label = "25-SECOND FLUID MULTI-SCENE VERIFICATION TEST"
    elif sample_duration:
        mode_label = f"EPISODE {episode_num:02d} ({int(sample_duration)}-SECOND BROADCAST PRODUCTION SAMPLE)"
    else:
        mode_label = f"EPISODE {episode_num:02d} (8-10 MINUTE BROADCAST MASTER)"
    print(f"🎬 MERAS STUDIO | PRODUCTION PIPELINE: {mode_label}")
    print("="*70)

    ep_data = load_episode_roadmap(episode_num)
    print(f"📌 Title:        {ep_data['title']}")
    print(f"🎯 Core Concept: {ep_data['core_concept']}")
    print(f"💥 3-Word Hook:  {ep_data['hook_3_words']}")

    # Setup directories
    if is_verification:
        out_dirname = "verification_25s"
        temp_dirname = "verification_25s_work"
    elif sample_duration:
        out_dirname = f"EP_{episode_num:02d}_sample_{int(sample_duration)}s"
        temp_dirname = f"ep{episode_num:02d}_sample_{int(sample_duration)}s_work"
    else:
        out_dirname = f"EP_{episode_num}"
        temp_dirname = f"ep{episode_num}_work"

    ep_out_dir = STUDIO_ROOT / "output" / out_dirname
    temp_dir = STUDIO_ROOT / "temp" / temp_dirname
    os.makedirs(ep_out_dir, exist_ok=True)
    os.makedirs(temp_dir, exist_ok=True)

    # Attach live unbuffered progress logging to pipeline_live.log
    live_log = ep_out_dir / "pipeline_live.log"
    sys.stdout = UnbufferedTeeLogger(live_log, sys.__stdout__)
    sys.stderr = UnbufferedTeeLogger(live_log, sys.__stderr__)
    print(f"[Pipeline] Streaming unbuffered live log -> {live_log}")

    # Ensure procedural soft SFX suite and verify system dependencies
    sfx_dir = STUDIO_ROOT / "assets" / "sfx"
    ambient_file = sfx_dir / "ambient_bed.wav"
    run_preflight_checks(sfx_dir)

    # STAGE 1: VOICE ENGINE & WHISPER ALIGNMENT
    print("\n" + "-"*50)
    print("🎙️ STAGE 1: SIGNATURE YOUTHFUL VOICE SYNTHESIS (Andrew, rate=+2%, pitch=0%)")
    print("-"*50)

    sample_sentences = []
    short_headline = ep_data.get("hook_3_words", "MERAS STUDIO")
    metadata_info = None

    if is_verification:
        script_text, verification_scenes = generate_verification_script()
        chapters = []
        short_headline = "THE 1957 DISCOVERY"
        voice_base_name = f"ep{episode_num:02d}_verif"
    elif sample_duration:
        sample_sentences = [
            ("Right now, deep inside your skull, you are actively believing a lie.", "MACRO_CLOSEUP", "macro_closeup", "The Invisible Fraud", "Neural Telemetry"),
            ("Not because you are gullible or uneducated, but because your brain would rather dismantle reality itself than admit you made a single mistake.", "HUMAN_SILHOUETTE_SCENE", "human_silhouette", "Ego Defense Shield", "Internal Conflict"),
            ("Welcome to Meras.", "FULL_CANVAS_METAPHOR", "full_canvas_metaphor", "Meras Architecture", "Behavioral Mechanics"),
            ("You consider yourself an honest, rational observer of the world.", "HUMAN_SILHOUETTE_SCENE", "human_silhouette", "Self-Perception", "The Rational Mind"),
            ("Yet every single day, you perform actions that directly contradict your most deeply held convictions.", "SPLIT_COMPARISON", "split_comparison", "Cognitive Friction", "Belief vs Action"),
            ("In 1957, legendary social psychologist Leon Festinger formulated the theoretical architecture of this flaw: Cognitive Dissonance.", "CAUSAL_MECHANISM", "animated_counter", "Historic Formulation", "Leon Festinger (1957)"),
            ("Your prefrontal cortex manufactures an elaborate, comforting lie to protect your fragile ego from the truth.", "CAUSAL_MECHANISM", "causal_mechanism", "The Rationalization Factory", "Input -> Engine -> Excuse"),
            ("Step outside the fortress of self-justification, and disarm the rationalization engine.", "FULL_CANVAS_METAPHOR", "full_canvas_metaphor", "Cognitive Transcendence", "Truth Over Comfort")
        ]
        script_text = " ".join(s[0] for s in sample_sentences)
        chapters = []
        short_headline = "WHY YOUR BRAIN LIES"
        voice_base_name = f"ep{episode_num:02d}_sample_{int(sample_duration)}s"
    else:
        # Dynamic documentary package (Gemini 2.5 Flash with Algorithmic Director fallback)
        dynamic_package = produce_dynamic_episode(episode_num)
        chapters = dynamic_package.get("chapters", [])
        script_text = " ".join(c["text"] for c in chapters)
        short_headline = dynamic_package.get("short_headline", ep_data.get("hook_3_words", "MERAS STUDIO"))
        metadata_info = dynamic_package.get("youtube_metadata")
        voice_base_name = f"ep{episode_num:02d}_master"

    voice_wav, alignment_json = generate_voice(
        text=script_text,
        output_dir=str(temp_dir),
        base_name=voice_base_name,
        voice_name="en-US-AndrewMultilingualNeural",
        rate="+2%",
        pitch="0%"
    )

    with open(alignment_json, "r", encoding="utf-8") as f:
        alignment = json.load(f)
    voice_dur = alignment.get("duration", 28.0)
    words = alignment.get("words", [])
    segments = alignment.get("segments", [])
    print(f"✓ Voice Track Generated: {voice_wav} ({voice_dur:.2f}s, {len(words)} words)")

    # STAGE 2: AUDIO-DRIVEN SCENE PLANNING
    print("\n" + "-"*50)
    print("🎨 STAGE 2: EXACT WORD-TIMESTAMP SCENE ALIGNMENT (Zero Cut-off Guarantee)")
    print("-"*50)

    # Tight 1.2s Outro Buffer (Zero dead air after final spoken word)
    outro_buffer = 1.2
    total_timeline_target = round(voice_dur + outro_buffer, 2)

    if is_verification:
        scene_plan = bind_scenes_to_word_timestamps(
            scenes=verification_scenes,
            words_alignment=words,
            total_target_duration=total_timeline_target
        )
    elif sample_duration:
        sample_scenes = []
        for s_i, (sent, lay, stype, stitle, ssub) in enumerate(sample_sentences, 1):
            is_last = (s_i == len(sample_sentences))
            ch_idx_map = 1 if s_i <= 3 else (2 if s_i <= 5 else (3 if s_i <= 7 else 6))
            sample_scenes.append({
                "scene_id": f"ep1_sample_{s_i:02d}_{stype}",
                "chapter_index": ch_idx_map,
                "layout": lay,
                "scene_type": stype,
                "duration": 5.0,
                "title": stitle,
                "subtitle": ssub,
                "sentence": sent,
                "punch_word": "YOUR MIND LIES",
                "is_outro": is_last,
                "foley_cues": [{"time": 0.5, "sfx": "gentle_chime" if s_i % 2 == 0 else "soft_pop"}]
            })
        scene_plan = bind_scenes_to_word_timestamps(
            scenes=sample_scenes,
            words_alignment=words,
            total_target_duration=total_timeline_target
        )
    else:
        scene_plan = build_audio_driven_scene_plan(
            chapters=chapters,
            words_alignment=words,
            segments_alignment=segments,
            total_audio_duration=voice_dur,
            outro_buffer=outro_buffer
        )

    planned_dur = sum(s["duration"] for s in scene_plan)
    print(f"✓ Scene Plan: {len(scene_plan)} dynamic scenes | Audio: {voice_dur:.2f}s + Buffer: {outro_buffer:.1f}s -> Timeline: {planned_dur:.2f}s")

    scene_plan_file = temp_dir / "scene_plan.json"
    with open(scene_plan_file, "w", encoding="utf-8") as f:
        json.dump(scene_plan, f, indent=2)

    # STAGE 3: 30FPS DETERMINISTIC MOTION RENDERING (FAST JPEG PIPING)
    print("\n" + "-"*50)
    print(f"🎥 STAGE 3: 30FPS DETERMINISTIC MOTION RENDERING (Safe Adaptive Concurrency, Fast JPEG Piping)")
    print("-"*50)

    trans_dur = 0.35  # 0.35s zero-drift xfade transition
    rendered_clips_dir = temp_dir / "temp_scenes"
    clips = render_scene_plan(
        scene_plan_path=str(scene_plan_file),
        output_dir=str(rendered_clips_dir),
        temp_dir=str(temp_dir / "html_staging"),
        fps=fps,
        words_alignment=words,
        overlap_sec=trans_dur
    )
    print(f"✓ Rendered {len(clips)} deterministic {fps}fps clips with zero-drift tail compensation")

    # Consolidate timeline-shifted Foley cues (Exact Millisecond Alignment)
    all_foley_cues = []
    current_offset = 0.0
    for scene in scene_plan:
        dur = float(scene["duration"])
        for cue in scene.get("foley_cues", []):
            all_foley_cues.append({
                "time": round(cue["time"] + current_offset, 3),
                "sfx": cue["sfx"]
            })
        current_offset += dur

    # STAGE 4: MASTER COMPOSITION, SHORT & THUMBNAIL
    print("\n" + "-"*50)
    print("🎛️ STAGE 4: MASTER COMPOSITION & BROADCAST EXPORT")
    print("-"*50)

    final_video_path = str(ep_out_dir / "final_video.mp4")
    thumbnail_path = str(ep_out_dir / "thumbnail.png")
    watermark_path = str(STUDIO_ROOT / "assets" / "watermark.png")

    composite_video(
        scene_clips=clips,
        voice_path=voice_wav,
        ambient_path=str(ambient_file),
        sfx_cues=all_foley_cues,
        output_video=final_video_path,
        watermark_path=watermark_path,
        sfx_dir=str(sfx_dir),
        transition_duration=trans_dur,
        words_alignment=words,
        target_total_duration=total_timeline_target
    )

    generate_thumbnail(
        hook_3_words=ep_data["hook_3_words"],
        output_path=thumbnail_path,
        episode_num=episode_num,
        category="BEHAVIORAL MECHANICS"
    )

    metadata_path = str(ep_out_dir / "youtube_metadata.txt")
    generate_youtube_metadata(ep_data, scene_plan, metadata_path, chapters=chapters, metadata_info=metadata_info)

    short_path = str(ep_out_dir / "short_video.mp4")
    short_dur = min(60.0, get_media_duration(final_video_path))
    generate_vertical_short(final_video_path, short_path, duration=short_dur, headline=short_headline)

    # Save scene plan and voice alignment to output directory
    shutil.copyfile(str(scene_plan_file), str(ep_out_dir / "scene_plan.json"))
    shutil.copyfile(str(alignment_json), str(ep_out_dir / "voice_alignment.json"))

    test_fluid_clip = None
    if is_verification:
        test_fluid_clip = str(ep_out_dir / "test_fluid.mp4")
        shutil.copyfile(final_video_path, test_fluid_clip)
        shutil.copyfile(final_video_path, str(STUDIO_ROOT / "output" / "test_fluid.mp4"))
        shutil.copyfile(final_video_path, str(ep_out_dir / "test_40s.mp4"))
        print(f"✓ Verification Test Clip saved -> {test_fluid_clip}")
    elif sample_duration:
        sample_filename = f"sample_ep{episode_num}_{int(sample_duration)}s.mp4"
        sample_path_out = ep_out_dir / sample_filename
        sample_path_root = STUDIO_ROOT / "output" / sample_filename
        shutil.copyfile(final_video_path, str(sample_path_out))
        shutil.copyfile(final_video_path, str(sample_path_root))
        alt_sample_name = f"sample_ep{episode_num:02d}_{int(sample_duration)}s.mp4"
        if alt_sample_name != sample_filename:
            shutil.copyfile(final_video_path, str(ep_out_dir / alt_sample_name))
            shutil.copyfile(final_video_path, str(STUDIO_ROOT / "output" / alt_sample_name))
        print(f"✓ Broadcast Production Sample saved -> {sample_path_out}")
        print(f"✓ Mirrored to -> {sample_path_root}")

    # Mirror for episode numbering if producing full episode
    alt_out_dirs = [
        STUDIO_ROOT / "output" / f"EP_{episode_num:02d}",
        STUDIO_ROOT / "output" / f"EP_[{episode_num}]"
    ]
    if not is_verification and not sample_duration:
        for a_dir in alt_out_dirs:
            if ep_out_dir != a_dir:
                os.makedirs(a_dir, exist_ok=True)
                for item in ep_out_dir.glob("*"):
                    if item.is_file():
                        shutil.copyfile(str(item), str(a_dir / item.name))

    print("\n" + "="*70)
    print("✨ BROADCAST PRODUCTION COMPLETE: READY FOR YOUTUBE EXPORT")
    print("="*70)
    print(f"📁 Output Directory:   {ep_out_dir}")
    print(f"📹 Master Video:       {final_video_path} ({os.path.getsize(final_video_path)} bytes)")
    print(f"📱 YouTube Short:      {short_path} ({os.path.getsize(short_path)} bytes)")
    print(f"🖼️ Vector Thumbnail:   {thumbnail_path} ({os.path.getsize(thumbnail_path)} bytes)")
    print(f"📋 YouTube Metadata:   {metadata_path}")
    print(f"🎙️ Voice Track:        {voice_wav}")

    return {
        "episode_number": episode_num,
        "mode": mode_label,
        "video": final_video_path,
        "short": short_path,
        "thumbnail": thumbnail_path,
        "metadata": metadata_path,
        "voice": voice_wav,
        "alignment": alignment_json
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Meras Studio Vector Animation Production Pipeline")
    parser.add_argument("--episode", type=int, default=1, help="Episode number (1-30)")
    parser.add_argument("--verify", action="store_true", help="Run 25-second broadcast verification test")
    parser.add_argument("--test", action="store_true", help="Alias for --verify")
    parser.add_argument("--sample", type=float, default=None, help="Render authentic broadcast sample of specified duration in seconds (e.g. 40)")
    parser.add_argument("--fps", type=int, default=30, help="Framerate (default: 30)")

    args = parser.parse_args()
    is_verif = args.verify or args.test
    run_production_pipeline(episode_num=args.episode, is_verification=is_verif, sample_duration=args.sample, fps=args.fps)
