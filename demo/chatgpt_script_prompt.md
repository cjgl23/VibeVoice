# ChatGPT prompt for generating VibeVoice scripts

Paste the block below into the ChatGPT UI (chatgpt.com). Pick whichever model
and thinking level you want — this is just the instruction text, it doesn't
call any API. Fill in the `[bracketed]` fields before sending.

---

You are a scriptwriter for an audio podcast/dialogue generator called
VibeVoice. Write a natural, spoken-language script on the topic below.

Topic: [YOUR TOPIC HERE]
Number of speakers: [N, 1-4]
Speaker roles: [e.g. "Speaker 1 = host named Alice, Speaker 2 = guest expert named Andrew"]
Target length: [e.g. "about 3 minutes of spoken audio" or "short, ~10 turns"]
Tone: [e.g. "casual and curious" / "professional interview" / "playful debate"]

Formatting rules — follow these exactly, the output goes straight into a TTS
engine with no further editing:

1. Every line must start with `Speaker N:` where N is the speaker's number
   (1 through the number of speakers above). No other prefixes, no names in
   the prefix, no timestamps.
2. One turn per line. Do not use markdown, bullet points, headers, asterisks,
   emojis, or stage directions like "(laughs)" or "[pause]".
3. Spell out numbers, dates, and abbreviations as words the way a person
   would say them out loud (e.g. "twenty twenty-five", "seven hundred
   million", "Doctor Smith" instead of "Dr. Smith").
4. Keep sentences conversational — contractions, natural interruptions,
   verbal fillers are fine, but no narration or scene-setting text outside
   the Speaker lines.
5. Use plain straight quotes/apostrophes, not curly ones.
6. Output ONLY the script lines. No preamble, no explanation, no closing
   remarks outside the dialogue itself.

Example of the expected format (2 speakers):

Speaker 1: I heard there's big news in TTS lately?
Speaker 2: Yes! Microsoft Research just open-sourced VibeVoice. The model can generate speech up to ninety minutes long, with smooth delivery and rich emotion.

---

Once ChatGPT replies, save its raw output to a `.txt` file and run it
through the validator before feeding it to VibeVoice:

```bash
python demo/prepare_chatgpt_script.py --input raw_from_chatgpt.txt --output demo/text_examples/my_script.txt --speakers 2
python demo/inference_from_file.py --txt_path demo/text_examples/my_script.txt --speaker_names Alice Andrew
```
