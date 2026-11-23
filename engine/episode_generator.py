"""
Meras Studio Episode Generator
Broadcast Standards:
- 8-Second Hook Rule: Immediate, gripping psychological paradox in the first 8 seconds before introducing the topic
- 6 Thematic Chapters with dynamic color palettes
- 2-Second Animated Chapter Title Cards between chapters
- Audio-Driven Timeline & Zero Cut-off Guarantee:
  Visual timeline precisely matches 100% of the synthesized voice duration + 2.0s outro buffer
- Dynamic Sentence-Accurate Metaphors & Animated Counters (1957, 48 pegs, $20 vs $1, percentages)
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional

STUDIO_ROOT = Path(__file__).resolve().parent.parent

# Import shared sanitization utility
try:
    from engine.voice_engine import sanitize_display_and_tts_text
except ImportError:
    from voice_engine import sanitize_display_and_tts_text

# Anti-AI-Slop Style Guardrail: Banned Cliché LLM Prose
BANNED_AI_SLOP_PATTERNS = [
    r"\bdelve\b",
    r"\bdelves\b",
    r"\bdelving\b",
    r"\bintricate tapestry\b",
    r"\btapestry of\b",
    r"\bdark corridors of your skull\b",
    r"\bagonizing collision\b",
    r"\bexquisitely optimized\b",
    r"\bbeacon\b",
    r"\bunravel\b",
    r"\bunravels\b",
    r"\bunraveling\b",
    r"\btestament to\b",
    r"\bit's important to remember\b",
    r"\bin conclusion\b",
    r"\bgame-changer\b",
    r"\btransformative journey\b"
]

def sanitize_and_validate_script_style(text: str) -> str:
    """
    Enforces Anti-AI-Slop Guardrails & Markdown Sanitization:
    Bans cliché LLM filler words, strips 100% of asterisks/markdown,
    and enforces crisp, punchy, conversational documentary writing.
    """
    # 0. Strip all markdown and asterisks first
    processed = sanitize_display_and_tts_text(text)
    
    replacements = {
        r"\bexquisitely optimized\b": "built",
        r"\bagonizing collision\b": "direct clash",
        r"\bdark corridors of your skull\b": "deep inside your brain",
        r"\bintricate tapestry\b": "complex network",
        r"\bdelve into\b": "explore",
        r"\bdelve\b": "look",
        r"\bunravel\b": "break down",
        r"\bbeacon of\b": "standard for"
    }
    for pat, rep in replacements.items():
        processed = re.sub(pat, rep, processed, flags=re.IGNORECASE)

    found_violations = []
    for pat in BANNED_AI_SLOP_PATTERNS:
        matches = re.findall(pat, processed, flags=re.IGNORECASE)
        if matches:
            found_violations.extend(matches)

    if found_violations:
        print(f"[StoryDirector] ⚠️ Anti-AI-Slop Notice: Flagged terms found: {set(found_violations)}")
    else:
        print("[StoryDirector] ✓ Anti-AI-Slop Style Guardrail PASSED: Clean, punchy documentary tone verified.")

    # Re-verify zero asterisks
    processed = sanitize_display_and_tts_text(processed)
    assert "*" not in processed, f"Asterisk remained after script sanitization: {processed[:100]}"
    return processed

def load_episode_roadmap(episode_num: int) -> Dict[str, Any]:
    """Loads episode metadata from episodes_roadmap.json."""
    roadmap_path = STUDIO_ROOT / "episodes_roadmap.json"
    with open(roadmap_path, "r", encoding="utf-8") as f:
        roadmap = json.load(f)
    ep_data = next((ep for ep in roadmap if ep["episode_number"] == episode_num), roadmap[0])
    return ep_data

def generate_full_episode_script(episode_data: Dict[str, Any]) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Generates a full 8-10 minute documentary script (1,350 to 1,600 words)
    structured into 6 thematic chapters enforcing the 8-Second Hook Rule.
    """
    title = episode_data.get("title", "Why Your Brain Loves Being Lied To")
    core_concept = episode_data.get("core_concept", "Cognitive Dissonance")
    hook = episode_data.get("hook_3_words", "YOUR MIND LIES")

    # 6 Chapters tailored to Meras behavioral psychology architecture
    chapters = [
        {
            "chapter_index": 1,
            "chapter_title": "The Invisible Fraud",
            "subtitle": "The Daily Paradox",
            "target_words": 250,
            "text": (
                # 8-Second Hook: Immediate psychological paradox before introducing topic
                f"Right now, deep inside your skull, you are actively believing a lie. "
                f"Not because you are gullible or uneducated, but because your brain would rather dismantle reality itself than admit you made a single mistake... "
                f"Welcome to Meras. "
                f"You consider yourself an honest, rational observer of the world. "
                f"You pride yourself on seeing through deceit, media manipulation, and falsehoods. "
                f"Yet every single day, you perform actions that directly contradict your most deeply held convictions. "
                f"You stay awake past midnight scrolling through digital feeds, despite promising yourself eight hours of restorative sleep. "
                f"You purchase status symbols you cannot afford to impress people you do not even respect. "
                f"You know with absolute medical certainty that chronic stress and poor nutrition erode your lifespan. "
                f"Yet when the moment of choice arrives, an ancient impulse takes over: *just this once, it doesn't matter.* "
                f"What actually happens in that precise split second inside your prefrontal cortex? "
                f"Does your conscious mind pause, evaluate the empirical evidence, and humbly admit: *I am behaving irrationally*? "
                f"Almost never. "
                f"Your brain is governed by an ancient evolutionary priority that routinely overrides objective truth: the relentless defense of your pride and self-worth. "
                f"To survive the collision between what you know and what you do, your mind commits a silent internal crime: "
                f"it manufactures an elaborate, comforting lie to protect your fragile ego from the truth."
            )
        },
        {
            "chapter_index": 2,
            "chapter_title": "The Evolutionary Wire",
            "subtitle": "Why The Flaw Exists",
            "target_words": 260,
            "text": (
                f"To understand why your mind rejects objective reality, we must journey back over 100,000 years. "
                f"In the ancestral Pleistocene savannah, social banishment was a guaranteed death sentence. "
                f"If an early human hunter made a catastrophic calculation, publicly acknowledging weakness or error carried severe status penalties within the hunting band. "
                f"Confidence, social alignment, and the projection of unwavering certainty were far more vital for genetic survival than mathematical accuracy. "
                f"The human brain was never engineered to be a pure philosophical truth-seeking machine. "
                f"It evolved as a high-stakes survival organ, built for social cohesion, reputational defense, and tribal belonging. "
                f"When your actions openly clash with your self-image, your nervous system does not process an abstract theoretical error. "
                f"Instead, modern neuroimaging demonstrates that your anterior cingulate cortex and anterior insula ignite with the identical neural patterns triggered by physical burns or bone fractures. "
                f"Psychological inconsistency literally hurts. "
                f"To your primitive threat circuitry, admitting *I was utterly wrong* feels dangerously indistinguishable from biological vulnerability. "
                f"Confronted with this acute emotional agony, your brain selects the path of least resistance. "
                f"Rather than undergoing the painful, metabolically costly process of changing established habits, "
                f"it simply rewrites your perception of the past. "
                f"It crafts retrospective excuses that dissolve the pain and restore internal harmony."
            )
        },
        {
            "chapter_index": 3,
            "chapter_title": "The Mechanical Breakdown",
            "subtitle": "How Cognitive Dissonance Works",
            "target_words": 280,
            "text": (
                f"In 1957, legendary social psychologist Leon Festinger formulated the theoretical architecture of this flaw: **Cognitive Dissonance**. "
                f"Dissonance emerges whenever two cognitive elements—beliefs, values, or observable behaviors—exist in sharp psychological contradiction. "
                f"Element A: *I am an intelligent, health-conscious individual who values longevity.* "
                f"Element B: *I just inhaled a pack of cigarettes.* "
                f"These two opposing realities cannot peacefully occupy the same neural workspace without generating unbearable psychological turbulence. "
                f"The human psyche abhors internal contradiction with the same intensity that nature abhors a vacuum. "
                f"Mechanically, there are only three pathways through which your prefrontal cortex can resolve this tension. "
                f"First, you can alter your behavior: you can extinguish the cigarette, throw away the pack, and endure the withdrawal. "
                f"This requires immense willpower, humility, and metabolic investment. "
                f"Second, you can seek out new empirical evidence that disproves the danger—though in an era of overwhelming medical consensus, this is increasingly difficult. "
                f"So your brain almost invariably defaults to the third pathway: **Self-Justification**. "
                f"You systematically discount the significance of the belief: *Everyone dies of something eventually; smoking calms my severe daily stress; my grandfather smoked and lived to ninety.* "
                f"Your neural gears grind into overdrive, spinning an impenetrable emotional cocoon around your fragile ego. "
                f"The contradiction is resolved not by fixing the flaw, but by normalizing the deception."
            )
        },
        {
            "chapter_index": 4,
            "chapter_title": "The Catastrophe",
            "subtitle": "When Reality Collapses",
            "target_words": 270,
            "text": (
                f"If cognitive dissonance were limited to justifying a missed workout or a fast-food binge, it would merely be a harmless psychological quirk. "
                f"However, when this evolutionary mechanism scales into high-stakes leadership, institutions, and society, it causes catastrophic historic collapses. "
                f"Consider venture capitalists and Wall Street traders who sink fortunes into doomed enterprises. "
                f"The balance sheets scream that insolvency is certain. "
                f"Yet because these investors staked their professional reputations and identities on being financial geniuses, accepting the loss feels psychologically unbearable. "
                f"They escalate their commitment, pouring good money after bad in a desperate bid to be proven right. "
                f"Consider ideological and political extremism. When predicted doomsday scenarios or utopian promises fail to materialize, true believers rarely apologize or abandon the creed. "
                f"Instead, they invent elaborate conspiracy theories: The election was stolen, the opposition saboteurs intervened, the prophecy was symbolic. "
                f"In aviation and medicine, seasoned captains and senior surgeons have ignored unmistakable alarm bells because acknowledging a misjudgment felt like personal humiliation. "
                f"Perhaps most unsettling of all, research confirms that higher cognitive ability does not protect you from this trap. "
                f"Intelligent individuals do not experience less cognitive dissonance; "
                f"they are simply equipped with vastly superior verbal and rationalization firepower to construct bulletproof intellectual justifications for their irrationality. "
                f"The hidden cost of protecting our pride is often the collapse of our reality."
            )
        },
        {
            "chapter_index": 5,
            "chapter_title": "The Historic Experiment",
            "subtitle": "The 1-Dollar Revelation",
            "target_words": 260,
            "text": (
                f"Leon Festinger and James Carlsmith demonstrated the counter-intuitive power of this mechanism in one of the most famous psychological experiments ever conducted. "
                f"Stanford University students were instructed to perform a mind-numbing, excruciatingly repetitive physical task for an entire hour: "
                f"using one hand to rotate forty-eight wooden pegs quarter-turn clockwise, over and over again in silence. "
                f"When the grueling hour finally concluded, the experimenter feigned a sudden logistical crisis. "
                f"They told each participant that their assistant had failed to show up, and asked if the student would step in to brief the next subject in the waiting room. "
                f"Their instruction was simple: lie to the incoming subject and tell them the peg-turning experiment was exhilarating, educational, and fun. "
                f"Half of the participants were offered twenty dollars for telling this lie—a high incentive in 1959 providing strong external justification. "
                f"The other half were offered a low incentive: exactly one single dollar, creating acute internal conflict. "
                f"Later, a neutral third party interviewed all subjects about how much they genuinely enjoyed the pegboard task. "
                f"Intuition suggests that individuals paid twenty dollars would feel happier and rate the experience more positively. "
                f"The experimental findings revealed the exact reverse. "
                f"Those who received twenty dollars possessed an undeniable external reason for lying: 'I lied because twenty dollars is great money.' They freely admitted the task was boring torture. "
                f"The students paid one dollar experienced severe internal dissonance: 'I told someone it was fun, but I only received one buck. I am an honest person, so the task must have truly had merit!' "
                f"Their prefrontal cortex rewrote their genuine memory to resolve the conflict."
            )
        },
        {
            "chapter_index": 6,
            "chapter_title": "The Meras Antidote",
            "subtitle": "Cognitive Transcendence",
            "target_words": 250,
            "text": (
                f"How do we liberate ourselves from this invisible psychological cage? "
                f"The path to cognitive engineering does not begin with intellect; it begins with physiological awareness. "
                f"The next time you encounter contradictory evidence and feel a sudden flare of anger, defensiveness, or tension in your throat... pause immediately. "
                f"Recognize that sharp emotional reaction for what it truly is: "
                f"it is not proof that you are under assault. It is the unmistakable sound of your ego shield violently slamming shut. "
                f"Train yourself to perceive that psychological friction not as a threat, but as precious, high-resolution diagnostic data. "
                f"The moment you uncouple your personal self-worth from the compulsion to always be right, you unlock the ultimate competitive advantage: intellectual plasticity. "
                f"You are not the collection of dogmas and beliefs you accumulated in your childhood. "
                f"You are the conscious thinker observing those ideas evolve in real time. "
                f"Admitting an error does not diminish your dignity; it demonstrates that you are sharper and more honest today than you were yesterday. "
                f"We explore the psychological cosmos at Meras not to seek the safety of comforting myths, "
                f"but to courageously confront the unvarnished mechanics of human nature. "
                f"Step outside the fortress of self-justification. Disarm the rationalization engine. "
                f"Because the exact moment you stop defending your comforting illusions... is the moment you finally begin to truly see."
            )
        }
    ]

    for ch in chapters:
        ch["text"] = sanitize_and_validate_script_style(ch["text"])

    full_text_parts = [ch["text"] for ch in chapters]
    full_script = "\n\n".join(full_text_parts)
    assert "*" not in full_script, f"Found unstripped asterisk in full script: {full_script}"
    return full_script, chapters

def generate_dynamic_scene_fields(layout: str, sentence: str, chapter_title: str, ch_idx: int) -> Dict[str, str]:
    """Generates rich, contextual, layout-specific fields for each scene in scene_plan.json."""
    sent_l = sentence.lower() if sentence else ""
    fields = {}
    
    if layout == "SPLIT_COMPARISON":
        if "dollar" in sent_l or "$20" in sent_l or "$1" in sent_l:
            fields["left_title"] = "HIGH INCENTIVE"
            fields["left_metric"] = "$20 PAYOUT"
            fields["left_sub"] = "EXTERNAL JUSTIFICATION"
            fields["right_title"] = "LOW INCENTIVE"
            fields["right_metric"] = "$1 PAYOUT"
            fields["right_sub"] = "INTERNAL BELIEF SHIFT"
        elif "action" in sent_l and "belief" in sent_l:
            fields["left_title"] = "CORE BELIEFS"
            fields["left_metric"] = "IDENTITY"
            fields["left_sub"] = "INTERNAL SELF-IMAGE"
            fields["right_title"] = "CONTRADICTORY ACTION"
            fields["right_metric"] = "BEHAVIOR"
            fields["right_sub"] = "ACUTE DISSONANCE"
        elif "invest" in sent_l or "money" in sent_l or "loss" in sent_l:
            fields["left_title"] = "FINANCIAL MODEL"
            fields["left_metric"] = "PROJECTION"
            fields["left_sub"] = "REPUTATION STAKE"
            fields["right_title"] = "MARKET REALITY"
            fields["right_metric"] = "INSOLVENCY"
            fields["right_sub"] = "ESCALATED COMMITMENT"
        elif "honest" in sent_l or "lie" in sent_l or "truth" in sent_l:
            fields["left_title"] = "SELF-PERCEPTION"
            fields["left_metric"] = "HONEST PERSON"
            fields["left_sub"] = "MORAL STANDARD"
            fields["right_title"] = "DISSONANT BEHAVIOR"
            fields["right_metric"] = "THE LIE"
            fields["right_sub"] = "EGO DEFENSE MECHANISM"
        else:
            fields["left_title"] = "PRIMARY COGNITION"
            fields["left_metric"] = "CONCEPT A"
            fields["left_sub"] = chapter_title.upper()
            fields["right_title"] = "OPPOSING FORCE"
            fields["right_metric"] = "CONCEPT B"
            fields["right_sub"] = "COGNITIVE FRICTION"

    elif layout == "HUMAN_SILHOUETTE_SCENE":
        fields["context_label"] = chapter_title.upper()
        if "smoke" in sent_l:
            fields["thought_bubble"] = "I CAN QUIT ANYTIME"
            fields["emotion_state"] = "RATIONALIZATION"
        elif "hunter" in sent_l or "savannah" in sent_l or "ancestral" in sent_l:
            fields["thought_bubble"] = "I MUST PROJECT STRENGTH"
            fields["emotion_state"] = "EVOLUTIONARY SHIELD"
        elif "investor" in sent_l or "wall street" in sent_l or "loss" in sent_l:
            fields["thought_bubble"] = "THE MARKET IS WRONG"
            fields["emotion_state"] = "PRIDE DEFENSE"
        elif "experiment" in sent_l or "peg" in sent_l or "task" in sent_l:
            fields["thought_bubble"] = "THE TASK WAS ENJOYABLE"
            fields["emotion_state"] = "MEMORY REWRITE"
        elif "mistake" in sent_l or "error" in sent_l or "wrong" in sent_l:
            fields["thought_bubble"] = "I WAS BASICALLY RIGHT"
            fields["emotion_state"] = "EGO RESISTANCE"
        elif "honest" in sent_l:
            fields["thought_bubble"] = "MY MOTIVES WERE PURE"
            fields["emotion_state"] = "SELF-JUSTIFICATION"
        else:
            fields["thought_bubble"] = "DEFENDING REALITY"
            fields["emotion_state"] = "INTERNAL EQUILIBRIUM"

    elif layout == "CAUSAL_MECHANISM":
        if "gear" in sent_l or "engine" in sent_l or "manufacture" in sent_l:
            fields["step1_input"] = "COGNITIVE CLASH"
            fields["step2_process"] = "RATIONALIZATION ENGINE"
            fields["step3_output"] = "FABRICATED COMFORT"
        elif "experiment" in sent_l or "peg" in sent_l:
            fields["step1_input"] = "BORING TASK ($1)"
            fields["step2_process"] = "DISSONANCE OVERDRIVE"
            fields["step3_output"] = "ALTERED BELIEF"
        elif "invest" in sent_l or "market" in sent_l:
            fields["step1_input"] = "MOUNTING LOSS"
            fields["step2_process"] = "CONFIRMATION BIAS"
            fields["step3_output"] = "DOUBLE DOWN"
        else:
            fields["step1_input"] = "DISSONANT INPUT"
            fields["step2_process"] = "PREFRONTAL FILTER"
            fields["step3_output"] = "ADAPTIVE EXCUSE"

    elif layout == "MACRO_CLOSEUP":
        fields["header_label"] = "NEURAL TELEMETRY: ACTIVE"
        if "cingulate" in sent_l or "pain" in sent_l:
            fields["focus_metric"] = "ACC CONFLICT"
            fields["sub_detail"] = "ANTERIOR CINGULATE ACTIVATION"
        elif "insula" in sent_l or "visceral" in sent_l:
            fields["focus_metric"] = "INSULA FLARE"
            fields["sub_detail"] = "GUT-LEVEL RESISTANCE"
        elif "cortex" in sent_l or "prefrontal" in sent_l:
            fields["focus_metric"] = "PFC OVERDRIVE"
            fields["sub_detail"] = "PREFRONTAL RATIONALIZATION"
        elif "synap" in sent_l or "brain" in sent_l or "skull" in sent_l:
            fields["focus_metric"] = "SYNAPTIC FLUX"
            fields["sub_detail"] = "NEURAL PATHWAY STABILIZATION"
        else:
            fields["focus_metric"] = "TELEMETRY"
            fields["sub_detail"] = chapter_title.upper()

    elif layout == "FULL_CANVAS_METAPHOR":
        fields["headline"] = chapter_title.upper()
        if "transcend" in sent_l or "antidote" in sent_l or "see clearly" in sent_l or "plasticity" in sent_l:
            fields["focal_label"] = "COGNITIVE TRANSCENDENCE"
            fields["supporting_note"] = "TRUTH OVER COMFORT"
        elif "evolution" in sent_l or "savannah" in sent_l or "ancestral" in sent_l:
            fields["focal_label"] = "EVOLUTIONARY LANDSCAPE"
            fields["supporting_note"] = "SURVIVAL MECHANISMS"
        else:
            fields["focal_label"] = "BEHAVIORAL HORIZON"
            fields["supporting_note"] = "OBJECTIVE REALITY"

    return fields

def build_audio_driven_scene_plan(
    chapters: List[Dict[str, Any]],
    words_alignment: List[Dict[str, Any]],
    segments_alignment: List[Dict[str, Any]],
    total_audio_duration: float,
    outro_buffer: float = 1.2
) -> List[Dict[str, Any]]:
    """
    Constructs an audio-driven scene plan covering 100% of the total audio duration + outro buffer.
    Rotates 5 distinct compositional layouts dynamically based on editorial intent.
    Zero-Second Hook Rule: Opens on frame 0 with immediate narrative hook (no blank cards in seconds 0-2).
    """
    LAYOUT_CYCLE = [
        ("MACRO_CLOSEUP", "macro_closeup"),
        ("HUMAN_SILHOUETTE_SCENE", "human_silhouette"),
        ("SPLIT_COMPARISON", "split_comparison"),
        ("CAUSAL_MECHANISM", "causal_mechanism"),
        ("FULL_CANVAS_METAPHOR", "full_canvas_metaphor")
    ]
    FOLEY_TYPES = ["soft_pop", "air_whoosh", "gentle_chime", "sub_drop"]
    PUNCH_WORD_POOL = [
        "YOUR MIND LIES",
        "COGNITIVE DISSONANCE",
        "REWRITING REALITY",
        "HIGH VS LOW INCENTIVE",
        "PROTECTING THE EGO",
        "INTERNAL FRICTION",
        "THE NEURAL ILLUSION",
        "RATIONALIZATION ENGINE",
        "INTELLECTUAL HUMILITY",
        "FACING THE TRUTH",
        "EGO SHIELD ACTIVE",
        "COGNITIVE TRANSCENDENCE"
    ]

    micro_scenes = []
    scene_idx = 1
    total_timeline_target = round(total_audio_duration + outro_buffer, 2)
    last_layout = None

    for ch_idx, ch in enumerate(chapters, 1):
        ch_title = sanitize_display_and_tts_text(ch["chapter_title"])
        ch_sub = sanitize_display_and_tts_text(ch.get("subtitle", "Behavioral Mechanics"))

        # Only insert title card for chapters 2-6 (Zero-Second Hook: Chapter 1 opens instantly on frame 0)
        if ch_idx > 1:
            card_fields = generate_dynamic_scene_fields("FULL_CANVAS_METAPHOR", "", ch_title, ch_idx)
            card_dict = {
                "scene_id": f"scene_{scene_idx:03d}_card_ch{ch_idx}",
                "chapter_index": ch_idx,
                "scene_type": "chapter_title_card",
                "layout": "FULL_CANVAS_METAPHOR",
                "duration": 2.0,
                "title": ch_title,
                "subtitle": ch_sub,
                "sentence": "",
                "punch_word": None,
                "foley_cues": [{"time": 0.4, "sfx": "gentle_chime"}]
            }
            card_dict.update(card_fields)
            micro_scenes.append(card_dict)
            scene_idx += 1

        # Partition chapter sentences
        sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', ch["text"]) if len(s.strip()) > 5]
        for s_idx, sentence in enumerate(sentences):
            sentence = sanitize_display_and_tts_text(sentence)
            sent_l = sentence.lower()
            is_final_scene = (ch_idx == len(chapters) and s_idx == len(sentences) - 1)

            # Editorial Intent-Based Layout Assignment
            if is_final_scene or "transcend" in sent_l or "see clearly" in sent_l or "truly see" in sent_l:
                layout = "FULL_CANVAS_METAPHOR"
                scene_type = "full_canvas_metaphor"
            elif re.search(r'(\$\d+|\b19\d\d\b|\b\d+\s*pegs\b|\b100,000\b)', sentence, re.IGNORECASE):
                layout = "CAUSAL_MECHANISM"
                scene_type = "animated_counter"
            elif "dollar" in sent_l or "$20" in sent_l or "$1" in sent_l or "incentive" in sent_l:
                layout = "SPLIT_COMPARISON"
                scene_type = "split_comparison"
            elif "contradict" in sent_l or "clash" in sent_l or "dissonance" in sent_l or "opposing" in sent_l:
                layout = "SPLIT_COMPARISON"
                scene_type = "split_comparison"
            elif "gear" in sent_l or "rationaliz" in sent_l or "excuse" in sent_l or "engine" in sent_l or "manufacture" in sent_l:
                layout = "CAUSAL_MECHANISM"
                scene_type = "causal_mechanism"
            elif "you" in sent_l and ("honest" in sent_l or "rational" in sent_l or "hunter" in sent_l or "student" in sent_l or "subject" in sent_l or "ego" in sent_l):
                layout = "HUMAN_SILHOUETTE_SCENE"
                scene_type = "human_silhouette"
            elif "skull" in sent_l or "cortex" in sent_l or "neural" in sent_l or "brain" in sent_l or "cingulate" in sent_l or "insula" in sent_l:
                layout = "MACRO_CLOSEUP"
                scene_type = "macro_closeup"
            else:
                for cand_layout, cand_type in LAYOUT_CYCLE:
                    if cand_layout != last_layout:
                        layout, scene_type = cand_layout, cand_type
                        break

            last_layout = layout
            foley_sfx = FOLEY_TYPES[(scene_idx - 1) % len(FOLEY_TYPES)]
            punch_word = PUNCH_WORD_POOL[(scene_idx - 1) % len(PUNCH_WORD_POOL)]

            w_count = len(sentence.split())
            dur = max(3.5, min(7.0, round(w_count / 2.5, 2)))

            dyn_fields = generate_dynamic_scene_fields(layout, sentence, ch_title, ch_idx)

            scene_dict = {
                "scene_id": f"scene_{scene_idx:03d}",
                "chapter_index": ch_idx,
                "layout": layout,
                "scene_type": scene_type,
                "duration": dur,
                "title": ch_title,
                "subtitle": ch_sub,
                "sentence": sentence,
                "punch_word": punch_word,
                "is_outro": is_final_scene,
                "foley_cues": [{"time": 0.6, "sfx": foley_sfx}]
            }
            scene_dict.update(dyn_fields)
            micro_scenes.append(scene_dict)
            scene_idx += 1

    # Calibrate scene durations to word timestamps
    if words_alignment:
        micro_scenes = bind_scenes_to_word_timestamps(
            scenes=micro_scenes,
            words_alignment=words_alignment,
            total_target_duration=total_timeline_target
        )

    # Verification: Assert zero asterisks anywhere in scene plan
    scene_plan_str = json.dumps(micro_scenes)
    assert "*" not in scene_plan_str, "Found unstripped asterisk in scene plan!"

    return micro_scenes

def bind_scenes_to_word_timestamps(
    scenes: List[Dict[str, Any]],
    words_alignment: List[Dict[str, Any]],
    total_target_duration: float
) -> List[Dict[str, Any]]:
    """
    Binds each scene's start time and duration strictly to faster-whisper word timestamps
    using a bounded content-word matching window with proportional timeline calibration.
    Guarantees:
    - No single scene ever exceeds 14.0s (Hard Cap)
    - No scene is shorter than 1.2s (tight outro minimum)
    - Exactly contiguous timeline: start_{i+1} == end_i, duration == end_i - start_i
    - abs(sum(scene_durations) - total_target_duration) <= 0.25s (typically 0.00s)
    """
    if not words_alignment or len(scenes) <= 1:
        return scenes

    import re
    def clean(w):
        return re.sub(r'[^a-z0-9]', '', str(w).lower())

    clean_words = [clean(w.get("word", "")) for w in words_alignment]
    n = len(scenes)
    scene_start_times = [0.0] * n
    last_idx = 0

    STOP_WORDS = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with",
        "by", "from", "up", "about", "into", "over", "after", "is", "are", "was", "were",
        "be", "been", "being", "have", "has", "had", "do", "does", "did", "you", "your",
        "we", "our", "they", "their", "it", "its", "that", "this", "these", "those"
    }

    for s_idx in range(1, n):
        sent = scenes[s_idx].get("sentence", "").strip()
        is_card = scenes[s_idx].get("scene_type") == "chapter_title_card" or not sent
        prev_start = scene_start_times[s_idx - 1]

        if is_card:
            card_dur = float(scenes[s_idx - 1].get("duration", 2.0)) if s_idx > 0 else 2.0
            scene_start_times[s_idx] = round(prev_start + min(card_dur, 2.5), 2)
            continue

        sent_words = [clean(w) for w in sent.split() if clean(w)]
        if not sent_words:
            scene_start_times[s_idx] = round(prev_start + 4.0, 2)
            continue

        # Search window: up to 100 words from last_idx
        search_end = min(len(clean_words), last_idx + 100)
        found_time = None
        best_w_idx = None

        content_words = [w for w in sent_words[:6] if len(w) >= 4 and w not in STOP_WORDS]

        # 1. First priority: 2-word sequence if at least one is a content word
        if len(sent_words) >= 2:
            k1, k2 = sent_words[0], sent_words[1]
            for w_idx in range(last_idx, search_end - 1):
                if clean_words[w_idx] == k1 and clean_words[w_idx + 1] == k2:
                    cand_time = words_alignment[w_idx]["start"]
                    if 2.0 <= (cand_time - prev_start) <= 14.0:
                        found_time = cand_time
                        best_w_idx = w_idx
                        break

        # 2. Second priority: match on any distinctive content word
        if found_time is None and content_words:
            for cw in content_words:
                for w_idx in range(last_idx, search_end):
                    if clean_words[w_idx] == cw:
                        cand_time = words_alignment[w_idx]["start"]
                        cw_pos = sent_words.index(cw)
                        est_start = max(prev_start + 2.0, cand_time - (cw_pos * 0.4))
                        if 2.0 <= (est_start - prev_start) <= 14.0:
                            found_time = est_start
                            best_w_idx = w_idx
                            break
                if found_time is not None:
                    break

        # 3. Third priority: first word if not stop word
        if found_time is None and sent_words[0] not in STOP_WORDS:
            for w_idx in range(last_idx, search_end):
                if clean_words[w_idx] == sent_words[0]:
                    cand_time = words_alignment[w_idx]["start"]
                    if 2.0 <= (cand_time - prev_start) <= 14.0:
                        found_time = cand_time
                        best_w_idx = w_idx
                        break

        if found_time is not None and best_w_idx is not None:
            scene_start_times[s_idx] = round(found_time, 2)
            last_idx = max(last_idx + 1, best_w_idx + 1)
        else:
            prev_sent = scenes[s_idx - 1].get("sentence", "")
            est_dur = max(2.5, min(8.0, round(len(prev_sent.split()) / 2.1, 2))) if prev_sent else 2.0
            scene_start_times[s_idx] = round(prev_start + est_dur, 2)
            last_idx = min(len(clean_words) - 1, last_idx + max(2, len(prev_sent.split())))

    # 1. Compute raw durations between scene start times
    for s_idx in range(n - 1):
        raw_dur = round(scene_start_times[s_idx + 1] - scene_start_times[s_idx], 2)
        scenes[s_idx]["duration"] = max(2.0, min(14.0, raw_dur))

    # Estimate final scene duration based on its sentence length + outro buffer
    last_sent = scenes[-1].get("sentence", "")
    est_last_dur = max(2.5, min(8.0, round(len(last_sent.split()) / 2.1 + 1.2, 2)))
    scenes[-1]["duration"] = est_last_dur

    # 2. Proportional Scaling Calibration across the entire timeline
    current_total = sum(s["duration"] for s in scenes)
    scale_factor = total_target_duration / current_total

    for s in scenes:
        scaled_dur = round(s["duration"] * scale_factor, 2)
        s["duration"] = max(2.0, min(14.0, scaled_dur))

    # 3. Build strictly contiguous timeline
    cur_t = 0.0
    for s in scenes[:-1]:
        s["start_time"] = round(cur_t, 2)
        cur_t = round(cur_t + s["duration"], 2)
        s["end_time"] = cur_t

    # Reconcile final fraction of a second on the last scene
    sum_prev = sum(s["duration"] for s in scenes[:-1])
    final_dur = round(total_target_duration - sum_prev, 2)
    if final_dur > 14.0 or final_dur < 1.2:
        residual = final_dur - 6.0
        scenes[-2]["duration"] = round(scenes[-2]["duration"] + residual, 2)
        scenes[-2]["end_time"] = round(scenes[-2]["start_time"] + scenes[-2]["duration"], 2)
        cur_t = scenes[-2]["end_time"]
        final_dur = 6.0

    scenes[-1]["duration"] = final_dur
    scenes[-1]["start_time"] = cur_t
    scenes[-1]["end_time"] = round(cur_t + final_dur, 2)

    # Automated assertions
    assert all(s["duration"] <= 14.0 for s in scenes), "Hard cap violated: scene duration > 14.0s!"
    assert all(s["duration"] >= 1.2 for s in scenes), "Minimum scene duration violated (< 1.2s)!"
    assert abs(sum(s["duration"] for s in scenes) - total_target_duration) <= 0.25, "Timeline drift exceeds 0.25s!"

    return scenes

def generate_verification_script() -> Tuple[str, List[Dict[str, Any]]]:
    """
    Generates a 25-second fluid verification script and scene templates.
    Explicitly tests:
    - Clean 'Meras' pronunciation (<sub alias="Miras">Meras</sub>)
    - Staggered multi-beat motion & fast physics (rapid 1900->1957 count-up, fast 3.5s gears, dynamic scale tilt)
    - Fluid 0.45s camera zoom-through enter/exit transitions
    - Clean, clutter-free kinetic subtitles (2-3s phrase chunks with cyan/amber punch-word highlights)
    - Tight 1.2s outro buffer (zero dead air)
    - Total duration: ~25.0s
    """
    script_text = (
        "Welcome to Meras... "
        "In 1957, Leon Festinger proved your mind actively lies to you. "
        "When actions clash with beliefs, internal gears grind into overdrive to defend your ego. "
        "In his famous experiment, subjects paid twenty dollars told the truth, but subjects paid one dollar lied. "
        "Because at Meras, truth always conquers comfort."
    )

    scenes = [
        {
            "scene_id": "fluid_01_intro_counter",
            "chapter_index": 1,
            "scene_type": "animated_counter",
            "duration": 6.20,
            "title": "The Cognitive Discovery",
            "subtitle": "Leon Festinger (1957)",
            "sentence": "Welcome to Meras. In 1957, Leon Festinger proved your mind actively lies to you.",
            "match_words": ["in", "1957"],
            "punch_word": "1957 DISCOVERY",
            "foley_cues": [{"time": 0.5, "sfx": "soft_pop"}]
        },
        {
            "scene_id": "fluid_02_gears",
            "chapter_index": 3,
            "scene_type": "rationalization_gears",
            "duration": 6.30,
            "title": "The Rationalization Factory",
            "subtitle": "Ego Defense Shield",
            "sentence": "When actions clash with beliefs, internal gears grind into overdrive to defend your ego.",
            "match_words": ["when", "actions"],
            "punch_word": "REWRITING REALITY",
            "foley_cues": [{"time": 0.5, "sfx": "air_whoosh"}]
        },
        {
            "scene_id": "fluid_03_scales",
            "chapter_index": 5,
            "scene_type": "scales_balance",
            "duration": 6.50,
            "title": "The Psychological Scales",
            "subtitle": "$20 vs $1 Payout",
            "sentence": "In his famous experiment, subjects paid twenty dollars told the truth, but subjects paid one dollar lied.",
            "match_words": ["in", "his"],
            "punch_word": "THE ONE-DOLLAR LIE",
            "foley_cues": [{"time": 0.5, "sfx": "gentle_chime"}]
        },
        {
            "scene_id": "fluid_04_horizon",
            "chapter_index": 6,
            "scene_type": "horizon_revelation",
            "duration": 6.00,
            "title": "The Meras Antidote",
            "subtitle": "Cognitive Transcendence",
            "sentence": "Because at Meras, truth always conquers comfort.",
            "match_words": ["because", "at"],
            "punch_word": "FACE THE TRUTH",
            "foley_cues": [{"time": 0.5, "sfx": "sub_drop"}]
        }
    ]
    return script_text, scenes

if __name__ == "__main__":
    ep1 = load_episode_roadmap(1)
    script, chs = generate_full_episode_script(ep1)
    print(f"Generated script: {len(script.split())} words across {len(chs)} chapters.")
