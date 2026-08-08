"""
Validate and clean up a script pasted from the ChatGPT UI (see
chatgpt_script_prompt.md) before handing it to inference_from_file.py.

Usage:
    python demo/prepare_chatgpt_script.py --input raw.txt --output demo/text_examples/my_script.txt --speakers 2
    # or pipe from stdin:
    pbpaste | python demo/prepare_chatgpt_script.py --output demo/text_examples/my_script.txt
"""
import argparse
import re
import sys

# Same pattern inference_from_file.py's parse_txt_script uses, kept in sync
# so a script that validates here is guaranteed to parse there too.
SPEAKER_PATTERN = re.compile(r"^Speaker\s+(\d+):\s*(.*)$", re.IGNORECASE)


def parse(text: str):
    lines = text.strip().split("\n")
    scripts, speaker_numbers = [], []
    current_speaker, current_text = None, ""

    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        match = SPEAKER_PATTERN.match(line)
        if match:
            if current_speaker and current_text:
                scripts.append(f"Speaker {current_speaker}: {current_text.strip()}")
                speaker_numbers.append(current_speaker)
            current_speaker = match.group(1).strip()
            current_text = match.group(2).strip()
        else:
            # Unprefixed line: either wrapped continuation of the current
            # turn, or stray text ChatGPT added (preamble/markdown) which we
            # flag separately below.
            if current_speaker is None:
                continue
            current_text = f"{current_text} {line}".strip() if current_text else line

    if current_speaker and current_text:
        scripts.append(f"Speaker {current_speaker}: {current_text.strip()}")
        speaker_numbers.append(current_speaker)

    return scripts, speaker_numbers


def find_stray_lines(text: str):
    stray = []
    for raw_line in text.strip().split("\n"):
        line = raw_line.strip()
        if not line or SPEAKER_PATTERN.match(line):
            continue
        stray.append(line)
    return stray


def clean_line(line: str) -> str:
    line = line.replace("’", "'").replace("‘", "'")
    line = line.replace("“", '"').replace("”", '"')
    line = re.sub(r"\*\*(.*?)\*\*", r"\1", line)  # strip markdown bold
    line = re.sub(r"[*_`]", "", line)  # strip stray markdown chars
    return line.strip()


def clean_and_validate(raw_text: str, expected_speakers: int = None):
    """
    Clean up raw text pasted from the ChatGPT UI and validate it against the
    same 'Speaker N:' format inference_from_file.py expects.

    Returns (cleaned_text, messages) where messages is a list of
    (level, text) tuples with level in {"info", "warning", "error"}.
    """
    messages = []

    cleaned_input = "\n".join(clean_line(l) for l in raw_text.split("\n"))
    stray = find_stray_lines(cleaned_input)
    scripts, speaker_numbers = parse(cleaned_input)

    if not scripts:
        messages.append(("error", "No 'Speaker N:' lines found. Did you paste ChatGPT's raw reply?"))
        return "", messages

    unique_speakers = sorted(set(speaker_numbers), key=int)
    messages.append((
        "info",
        f"Parsed {len(scripts)} turns across {len(unique_speakers)} speaker(s): {', '.join(unique_speakers)}",
    ))

    if expected_speakers is not None and len(unique_speakers) != expected_speakers:
        messages.append((
            "warning",
            f"Expected {expected_speakers} speaker(s) but found {len(unique_speakers)}.",
        ))

    expected_numbers = [str(i) for i in range(1, len(unique_speakers) + 1)]
    if unique_speakers != expected_numbers:
        messages.append((
            "warning",
            f"Speaker numbers are {unique_speakers}, expected contiguous {expected_numbers} starting at 1.",
        ))

    if stray:
        preview = "; ".join(s[:80] for s in stray[:3])
        messages.append((
            "warning",
            f"{len(stray)} line(s) had no 'Speaker N:' prefix and were merged into the previous turn "
            f"(or dropped if before the first speaker): {preview}",
        ))

    return "\n".join(scripts), messages


def main():
    parser = argparse.ArgumentParser(description="Validate/clean a ChatGPT-generated VibeVoice script")
    parser.add_argument("--input", type=str, default=None, help="Raw script file (defaults to stdin)")
    parser.add_argument("--output", type=str, required=True, help="Where to write the cleaned script")
    parser.add_argument("--speakers", type=int, default=None, help="Expected number of unique speakers, for validation")
    args = parser.parse_args()

    if args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            raw_text = f.read()
    else:
        raw_text = sys.stdin.read()

    cleaned_text, messages = clean_and_validate(raw_text, expected_speakers=args.speakers)

    for level, text in messages:
        stream = sys.stderr if level in ("warning", "error") else sys.stdout
        print(f"{level.capitalize()}: {text}" if level != "info" else text, file=stream)

    if not cleaned_text:
        sys.exit(1)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(cleaned_text + "\n")

    print(f"Saved cleaned script to {args.output}")


if __name__ == "__main__":
    main()
