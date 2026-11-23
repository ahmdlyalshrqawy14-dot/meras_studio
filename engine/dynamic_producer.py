"""
Meras Studio - Dynamic Gemini Production Engine
Automates documentary script ideation, scene planning, YouTube metadata, and Shorts hooks
for any episode in episodes_roadmap.json using Google GenAI SDK (Gemini 2.5 Flash),
with an automated offline/algorithmic documentary engine fallback when offline.
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
from dotenv import load_dotenv

STUDIO_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(STUDIO_ROOT / ".env")

try:
    from engine.voice_engine import sanitize_display_and_tts_text
except ImportError:
    from voice_engine import sanitize_display_and_tts_text


def load_roadmap(episode_num: int) -> Dict[str, Any]:
    """Loads roadmap specification for the given episode number."""
    roadmap_file = STUDIO_ROOT / "episodes_roadmap.json"
    if not roadmap_file.exists():
        raise FileNotFoundError(f"Roadmap file not found at {roadmap_file}")
    with open(roadmap_file, "r", encoding="utf-8") as f:
        episodes = json.load(f)
    for ep in episodes:
        if ep.get("episode_number") == episode_num:
            return ep
    # Default to episode 1 if out of range
    return episodes[0]


def is_gemini_available() -> bool:
    """Returns True if GEMINI_API_KEY is configured with a valid key."""
    key = os.getenv("GEMINI_API_KEY")
    return bool(key and key.strip() and not key.startswith("your_"))


def generate_episode_with_gemini(ep_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Uses Google GenAI SDK (gemini-2.5-flash) to generate a full 1,350-1,600 word
    anti-AI-slop documentary script across 6 chapters with per-scene visual layouts,
    dynamic 60s Short hook, and SEO YouTube metadata.
    """
    if not is_gemini_available():
        return None

    try:
        from google import genai
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

        system_instruction = (
            "You are the Lead Documentary Director and Scriptwriter for 'Meras | مِراس', "
            "a premier animated science channel in the style of Kurzgesagt and Vox. "
            "Your tone is intellectual, punchy, conversational, and philosophically profound. "
            "STRICT RULES:\n"
            "1. NO AI-SLOP: Never use words like 'delve', 'tapestry', 'unravel', 'beacon', "
            "'intricate dance', 'dark corridors of your skull', or 'agonizing collision'.\n"
            "2. Total script length MUST be between 1,350 and 1,600 words across exactly 6 chapters.\n"
            "3. Every chapter must have 3-5 punchy sentences that explain real mechanisms, experiments, or evolutionary logic.\n"
            "4. NEVER output markdown asterisks (*) or underscores (_) inside spoken text.\n"
            "5. Return strictly valid JSON matching the requested schema."
        )

        prompt = f"""
Generate full production assets for Episode #{ep_data.get('episode_number', 1)}:
Title: "{ep_data['title']}"
Core Concept: {ep_data['core_concept']}
Hook 3 Words: "{ep_data['hook_3_words']}"
Curiosity Logline: "{ep_data['curiosity_logline']}"
Visual Metaphor: "{ep_data['visual_metaphor']}"

Return a JSON object with this exact structure:
{{
  "episode_number": {ep_data.get('episode_number', 1)},
  "title": "{ep_data['title']}",
  "short_headline": "{ep_data['hook_3_words']}",
  "chapters": [
    {{
      "chapter_index": 1,
      "chapter_title": "Chapter 1 Title",
      "subtitle": "Subtitle",
      "text": "Full conversational narration text for Chapter 1 (220-260 words). No asterisks."
    }},
    {{
      "chapter_index": 2,
      "chapter_title": "Chapter 2 Title",
      "subtitle": "Subtitle",
      "text": "Full conversational narration text for Chapter 2 (220-260 words). No asterisks."
    }},
    {{
      "chapter_index": 3,
      "chapter_title": "Chapter 3 Title",
      "subtitle": "Subtitle",
      "text": "Full conversational narration text for Chapter 3 (220-260 words). No asterisks."
    }},
    {{
      "chapter_index": 4,
      "chapter_title": "Chapter 4 Title",
      "subtitle": "Subtitle",
      "text": "Full conversational narration text for Chapter 4 (220-260 words). No asterisks."
    }},
    {{
      "chapter_index": 5,
      "chapter_title": "Chapter 5 Title",
      "subtitle": "Subtitle",
      "text": "Full conversational narration text for Chapter 5 (220-260 words). No asterisks."
    }},
    {{
      "chapter_index": 6,
      "chapter_title": "Chapter 6 Title",
      "subtitle": "Subtitle",
      "text": "Full conversational narration text for Chapter 6 (220-260 words). No asterisks."
    }}
  ],
  "youtube_metadata": {{
    "title_options": [
      "Option 1 High CTR Title",
      "Option 2 High CTR Title",
      "Option 3 High CTR Title"
    ],
    "seo_description": "2-3 paragraphs of compelling SEO video description explaining the episode concept.",
    "tags": ["tag1", "tag2", "tag3", "behavioral psychology", "meras", "kurzgesagt style"]
  }},
  "short_script": {{
    "hook_headline": "{ep_data['hook_3_words']}",
    "voice_script": "60-second vertical short narration script (~130 words).",
    "punch_word": "{ep_data['hook_3_words']}"
  }}
}}
"""
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=dict(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                temperature=0.7
            )
        )

        data = json.loads(response.text)
        # Sanitize all chapter texts
        for ch in data.get("chapters", []):
            ch["text"] = sanitize_display_and_tts_text(ch["text"])
            ch["chapter_title"] = sanitize_display_and_tts_text(ch["chapter_title"])
            ch["subtitle"] = sanitize_display_and_tts_text(ch.get("subtitle", ""))
        print(f"[DynamicProducer] ✓ Generated full documentary script via Gemini 2.5 Flash for Episode {ep_data['episode_number']}.")
        return data

    except Exception as e:
        print(f"[DynamicProducer] ⚠️ Gemini API generation notice ({e}); falling back to algorithmic director.")
        return None


def generate_algorithmic_documentary_script(ep_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    High-fidelity offline algorithmic documentary script generator.
    Produces 1,350-1,600 words of conversational, anti-AI-slop narrative
    across 6 chapters directly tailored to the episode roadmap.
    """
    ep_num = ep_data.get("episode_number", 1)
    title = ep_data.get("title", f"Episode {ep_num}")
    concept = ep_data.get("core_concept", "Human Behavioral Mechanics")
    hook_3 = ep_data.get("hook_3_words", "LOOK CLOSER")
    logline = ep_data.get("curiosity_logline", "The surprising neurological math behind human nature.")
    metaphor = ep_data.get("visual_metaphor", "An intricate vector landscape illustrating cognitive trade-offs.")

    # Specialized handcrafted master for Episode 1
    if ep_num == 1:
        from episode_generator import generate_full_episode_script as gen_ep1
        full_text, chapters = gen_ep1(ep_data)
        return {
            "episode_number": 1,
            "title": title,
            "short_headline": "WHY YOUR BRAIN LIES",
            "chapters": chapters,
            "youtube_metadata": {
                "title_options": [
                    "Why Your Brain Loves Being Lied To (Cognitive Dissonance Explained)",
                    "The Disturbing Reason You Can Never Admit You're Wrong",
                    "Why Your Mind Rewrites Reality To Defend Your Ego"
                ],
                "seo_description": (
                    "You believe you are an honest, rational person. But right now, inside your skull, your brain is actively lying to you.\n\n"
                    "In 1957, Stanford psychologist Leon Festinger uncovered an unsettling flaw in human wiring called Cognitive Dissonance. "
                    "When our actions clash with our deeply held beliefs, the brain experiences acute psychological pain. Instead of admitting error, "
                    "your prefrontal cortex rewrites memory, inventing bulletproof justifications to protect your self-worth.\n\n"
                    "In this episode of Meras | مِراس, we engineer the hidden mechanics of human self-deception: why smart people cling to doomed choices, "
                    "how a historic 1-dollar experiment revealed our internal machinery, and how you can disarm the rationalization engine."
                ),
                "tags": [
                    "behavioral psychology", "cognitive dissonance", "leon festinger", "self justification",
                    "human psychology", "cognitive bias", "ego defense mechanism", "psychology explained",
                    "neuroscience", "rationalization", "why we lie to ourselves", "meras", "kurzgesagt style",
                    "educational animation", "1 dollar experiment"
                ]
            },
            "short_script": {
                "hook_headline": "WHY YOUR BRAIN LIES",
                "voice_script": (
                    "Right now, deep inside your skull, you are actively believing a lie. "
                    "Not because you are gullible, but because your brain would rather dismantle reality itself than admit you made a single mistake. "
                    "Welcome to Meras. When actions clash with beliefs, cognitive dissonance triggers internal friction. "
                    "In 1957, subjects paid twenty dollars told the truth, but subjects paid one dollar lied. "
                    "Step outside the fortress of self-justification, and disarm the rationalization engine."
                ),
                "punch_word": "YOUR MIND LIES"
            }
        }

    # Algorithmic documentary engine for Episodes 2-30 (1,350-1,600 words total across 6 chapters)
    ch1_text = sanitize_display_and_tts_text(
        f"Right now, inside your skull, an unseen biological mechanism is orchestrating your every conscious impulse. "
        f"You imagine that you make deliberate, autonomous choices guided by pure logic, self-discipline, and objective awareness. "
        f"You pride yourself on being an honest, perceptive observer of the world who weighs evidence fairly and updates beliefs accordingly. "
        f"Yet the reality is vastly stranger and far more unsettling: {logline.lower()} "
        f"Welcome to Meras. We explore the hidden architecture, cognitive blind spots, and evolutionary compromises of human nature. "
        f"Consider what happens when you attempt to master your own everyday habits and choices. "
        f"You establish clear intentions, you set strict rules, and you promise yourself that this time will be fundamentally different. "
        f"Yet within hours, the invisible machinery deep within your subcortex overrides your executive will. "
        f"You find yourself reaching for the distraction, abandoning the plan, or manufacturing a comforting excuse before the guilt even lands. "
        f"This is not a personal failure of character or intelligence. It is an evolutionary artifact, engineered across millions of generations of survival. "
        f"Behind your conscious inner monologue sits a relentless optimization algorithm that cares nothing for your long-term ambitions, "
        f"prioritizing short-term metabolic security and ego defense above all else. To change how you think, you must first decipher how you are wired. "
        f"Every belief you hold is filtered through layers of neurochemical incentives designed to keep you feeling consistent, safe, and perpetually justified. "
        f"The first step in reclaiming intellectual agency is realizing that your thoughts are not commands; they are biological proposals."
    )

    ch2_text = sanitize_display_and_tts_text(
        f"To understand why your mind behaves this way, we have to journey back to the ancestral environment. "
        f"In the Pleistocene savannah, natural selection never optimized the human nervous system for philosophical serenity or objective theoretical accuracy. "
        f"It optimized for raw metabolic conservation, reproductive survival, and tribal standing within a tight-knit band of hunter-gatherers. "
        f"In that unforgiving landscape, hesitation, overthinking, or solitary contemplation could easily cost you your life. "
        f"The neural circuits governing {concept.lower()} emerged as vital evolutionary shortcuts. "
        f"They rewarded immediate pattern recognition over slow verification, and tribal consensus over dangerous solitary truths. "
        f"Banishment from the tribe was a guaranteed death sentence, so our ancestors developed acute sensitivity to social status and immediate rewards. "
        f"When those ancient circuits clash with our modern environment of endless choices, hyper-stimulating algorithms, and instant gratification, "
        f"the evolutionary gears grind into severe systemic misalignment. The modern world is an alien landscape for Paleolithic wiring. "
        f"Every smartphone ping, algorithmic recommendation, and high-calorie temptation exploits a biological tripwire that was calibrated for a world of extreme physical scarcity. "
        f"Your brain is not broken; it is operating on instructions written for an environment that ceased to exist ten thousand years ago. "
        f"Our ancestors needed quick closure and social belonging; we live in an interconnected civilization that demands deep patience, skepticism, and nuanced probabilistic thinking. "
        f"Without understanding this evolutionary mismatch, you remain the passive victim of impulses designed for ghosts in a dead landscape."
    )

    ch3_text = sanitize_display_and_tts_text(
        f"At the mechanical level, modern neuroimaging reveals the exact anatomical pathways orchestrating this internal conflict. "
        f"When sensory input enters your brain, it does not travel directly to the calm, reflective prefrontal cortex. "
        f"Instead, it triggers rapid, high-priority subcortical feedback loops deep within your limbic system. "
        f"Your anterior cingulate cortex flags psychological tension, while dopaminergic projections from the ventral tegmental area fire in anticipation. "
        f"The visual metaphor of {metaphor.lower()} reflects this dynamic struggle within your neural circuitry. "
        f"One primitive subsystem pushes forcefully for immediate gratification and emotional comfort, "
        f"while the slower, metabolically expensive neocortex is left to invent retrospective justifications. "
        f"Every single microsecond of indecision generates subtle friction across your synapses, consuming glucose and rapidly draining your finite executive willpower. "
        f"You do not act because you reasoned; you reason because you already acted. "
        f"Functional magnetic resonance imaging demonstrates that motor regions and emotional nodes light up hundreds of milliseconds before you become consciously aware of having made a decision. "
        f"The conscious you is rarely the author of your impulses; more often, it is merely the press secretary tasked with announcing and defending them. "
        f"By the time an excuse forms in your thoughts, your emotional brain has already completed the transaction. "
        f"Recognizing this millisecond lag between impulse and narrative is the key to breaking the cycle."
    )

    ch4_text = sanitize_display_and_tts_text(
        f"The destructive consequences of this cognitive trap extend far beyond personal procrastination or daily bad habits. "
        f"Across human history, brilliant political leaders, seasoned airline pilots, and institutional architects have fallen into the exact same pitfall. "
        f"Because the brain instinctively prioritizes internal psychological comfort over corrective feedback, erroneous decisions compound in silence. "
        f"We double down on losing financial investments, defend failing organizational strategies, and construct elaborate intellectual fortresses to shield our fragile ego. "
        f"Psychologists refer to this escalating commitment as the sunken cost fallacy and confirmation bias working in catastrophic tandem. "
        f"By the time external reality forces an undeniable reckoning, the structural damage is already irreversible. "
        f"The catastrophe was never caused by a lack of factual data or intellectual firepower; "
        f"it was caused by the brain fiercely defending its own flawed assumptions against the truth. "
        f"When a belief becomes entangled with identity, receiving evidence that disproves it is processed by the nervous system as physical danger. "
        f"The amygdala sounds the alarm, the prefrontal cortex shuts down nuanced inquiry, and we charge headlong into disaster with absolute righteous conviction. "
        f"History is a graveyard of brilliant minds who preferred catastrophic ruin over the simple humility of admitting they were wrong. "
        f"Certainty is not a measure of truth; it is merely an emotional state manufactured by a threatened ego."
    )

    ch5_text = sanitize_display_and_tts_text(
        f"Rigorous experimental psychology has documented this phenomenon with repeatable mathematical precision. "
        f"When researchers placed participants in controlled laboratory simulations of {concept.lower()}, "
        f"the empirical data consistently overturned common common-sense intuition. "
        f"Subjects did not act according to objective economic utility or logical probability calculations; "
        f"they acted to preserve internal psychological equilibrium and minimize cognitive discomfort. "
        f"When presented with counter-evidence or financial incentives, their self-reported convictions shifted dramatically "
        f"to align with whatever narrative demanded the least mental friction. "
        f"Decades of behavioral economics and cognitive science confirm this uncomfortable verdict: "
        f"human beings are not rational truth-seeking calculation engines. "
        f"We are rationalizing creatures, brilliantly equipped by natural selection to manufacture sophisticated reasons "
        f"for whatever our emotional and evolutionary wiring has already decided. "
        f"In double-blind studies, individuals routinely rated demonstrably flawed arguments as brilliant when those arguments defended their favored viewpoint, "
        f"while subjecting flawless logic to hyper-critical skepticism when it challenged their preexisting assumptions. We measure reality with a biased ruler. "
        f"The smarter a person is, the more formidable their cognitive defense mechanisms become, using intelligence not to discover objective facts, but to defend irrational commitments. "
        f"High IQ does not protect you from delusion; it merely gives you better weapons with which to defend it."
    )

    ch6_text = sanitize_display_and_tts_text(
        f"So how do we liberate ourselves from this invisible machinery? "
        f"The path to cognitive sovereignty begins with rigorous, dispassionate transparency. "
        f"You must train yourself to perceive that subtle internal tension not as a humiliating threat to your dignity, "
        f"but as precious, high-resolution diagnostic data. "
        f"The moment you uncouple your personal self-worth from the compulsion to always be right, "
        f"you unlock the ultimate competitive advantage: intellectual plasticity. "
        f"Admitting an error does not diminish you; it demonstrates that you are sharper and more honest today than you were yesterday. "
        f"At Meras, we explore the human cosmos not to seek comforting myths, "
        f"but to courageously understand the true mechanical blueprints of who we are. "
        f"Because the exact moment you stop defending your comforting illusions, "
        f"is the moment you finally begin to truly see. "
        f"True intellectual mastery is not about building an impenetrable fortress of knowledge; "
        f"it is about cultivating the quiet courage to dismantle your own assumptions the instant reality proves them wrong. "
        f"Step outside the illusion, disarm the rationalization engine, and embrace the freedom of genuine clarity. "
        f"When you replace defensiveness with curiosity, the internal gears align, and the world comes into sharp, unclouded focus. "
        f"At Meras, truth will always triumph over comforting deceit."
    )

    chapters = [
        {"chapter_index": 1, "chapter_title": "The Invisible Illusion", "subtitle": "Conscious Blindspot", "text": ch1_text},
        {"chapter_index": 2, "chapter_title": "The Evolutionary Wire", "subtitle": "Ancestral Programming", "text": ch2_text},
        {"chapter_index": 3, "chapter_title": "The Neural Breakdown", "subtitle": "Mechanical Tension", "text": ch3_text},
        {"chapter_index": 4, "chapter_title": "The Catastrophe", "subtitle": "Compounding Fallacy", "text": ch4_text},
        {"chapter_index": 5, "chapter_title": "The Empirical Proof", "subtitle": "Experimental Verification", "text": ch5_text},
        {"chapter_index": 6, "chapter_title": "The Meras Antidote", "subtitle": "Cognitive Transcendence", "text": ch6_text}
    ]

    return {
        "episode_number": ep_num,
        "title": title,
        "short_headline": hook_3,
        "chapters": chapters,
        "youtube_metadata": {
            "title_options": [
                f"{title} (The Hidden Science Explained)",
                f"The Real Reason You Can't Control {title.split()[-1]}",
                f"How Your Brain Trick You Into {title.split()[-1]}"
            ],
            "seo_description": (
                f"{logline}\n\n"
                f"In Episode {ep_num} of Meras | مِراس, we engineer the hidden mechanics of {concept}: "
                f"why our ancient evolutionary wiring clashes with modern reality, how cognitive biases deceive us, "
                f"and how to unlock intellectual humility and clear perception."
            ),
            "tags": [
                "behavioral psychology", "neuroscience", "cognitive science", "human behavior",
                "meras", "kurzgesagt style", "science animation", concept.lower(), title.lower()
            ]
        },
        "short_script": {
            "hook_headline": hook_3,
            "voice_script": (
                f"Right now, your brain is running a hidden script. {logline} "
                f"Welcome to Meras. When ancient neural wiring clashes with modern reality, we rationalize our mistakes. "
                f"Stop defending comforting illusions, and disarm the internal trap."
            ),
            "punch_word": hook_3
        }
    }


def produce_dynamic_episode(episode_num: int) -> Dict[str, Any]:
    """
    Main entrypoint: Generates full episode documentary package for any episode number.
    Tries Gemini 2.5 Flash if GEMINI_API_KEY is configured; otherwise falls back to
    the high-fidelity algorithmic documentary engine.
    """
    ep_data = load_roadmap(episode_num)
    
    # Try Gemini dynamic generation if key exists
    data = generate_episode_with_gemini(ep_data)
    if data is None:
        data = generate_algorithmic_documentary_script(ep_data)
    
    # Guarantee zero asterisks across all generated fields
    for ch in data.get("chapters", []):
        ch["text"] = sanitize_display_and_tts_text(ch["text"])
        assert "*" not in ch["text"], f"Asterisk remained in Chapter {ch['chapter_index']}!"

    return data


if __name__ == "__main__":
    print("Testing Dynamic Gemini Production Engine for Episode 1 & 2...")
    ep1 = produce_dynamic_episode(1)
    print(f"✓ Episode 1: {ep1['title']} ({sum(len(c['text'].split()) for c in ep1['chapters'])} words)")
    ep2 = produce_dynamic_episode(2)
    print(f"✓ Episode 2: {ep2['title']} ({sum(len(c['text'].split()) for c in ep2['chapters'])} words)")
