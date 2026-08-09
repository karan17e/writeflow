import re
from typing import Dict, Any

EMOJI_REGEX = re.compile(
    r"[\U00010000-\U0010ffff\u2600-\u27ff\u2300-\u23ff\u2b00-\u2bff\u2190-\u21ff]"
)


def count_emojis(text: str) -> int:
    if not text:
        return 0
    return len(EMOJI_REGEX.findall(text))


def count_hashtags(text: str) -> int:
    if not text:
        return 0
    return len(re.findall(r"#\w+", text))


def parse_user_style_instructions(style_text: str) -> Dict[str, Any]:
    if not style_text or not style_text.strip():
        return {}
    
    style_lower = style_text.lower().strip()
    parsed = {}

    # Emoji count parsing
    if "no emoji" in style_lower or "zero emoji" in style_lower or "without emoji" in style_lower or "0 emoji" in style_lower:
        parsed["emoji_count"] = 0
    else:
        emoji_match = re.search(r"(\d+)\s*emoji", style_lower)
        if emoji_match:
            parsed["emoji_count"] = int(emoji_match.group(1))

    # Hashtag count parsing
    if "no hashtag" in style_lower or "zero hashtag" in style_lower or "without hashtag" in style_lower or "0 hashtag" in style_lower:
        parsed["hashtag_count"] = 0
    else:
        hashtag_match = re.search(r"(\d+)\s*hashtag", style_lower)
        if hashtag_match:
            parsed["hashtag_count"] = int(hashtag_match.group(1))

    # Max words parsing
    word_match = re.search(r"(under|less than|max|within)\s*(\d+)\s*word", style_lower)
    if word_match:
        parsed["max_words"] = int(word_match.group(2))

    return parsed


def validate_style_requirements(post_content: str, requirements: Dict[str, Any]) -> Dict[str, Any]:
    actual_emojis = count_emojis(post_content)
    actual_hashtags = count_hashtags(post_content)
    actual_words = len(post_content.strip().split()) if post_content else 0

    report = {
        "valid": True,
        "details": {}
    }

    if "emoji_count" in requirements:
        req_emojis = requirements["emoji_count"]
        # Allow +/- 1 tolerance for non-zero emoji requests, exact match for 0
        passed = (actual_emojis == 0) if req_emojis == 0 else (abs(actual_emojis - req_emojis) <= 1)
        report["details"]["emoji_count"] = {
            "requested": req_emojis,
            "actual": actual_emojis,
            "passed": passed
        }
        if not passed:
            report["valid"] = False

    if "hashtag_count" in requirements:
        req_hashtags = requirements["hashtag_count"]
        passed = (actual_hashtags == 0) if req_hashtags == 0 else (abs(actual_hashtags - req_hashtags) <= 1)
        report["details"]["hashtag_count"] = {
            "requested": req_hashtags,
            "actual": actual_hashtags,
            "passed": passed
        }
        if not passed:
            report["valid"] = False

    if "max_words" in requirements:
        req_max_words = requirements["max_words"]
        passed = actual_words <= (req_max_words + 15)
        report["details"]["max_words"] = {
            "requested": req_max_words,
            "actual": actual_words,
            "passed": passed
        }
        if not passed:
            report["valid"] = False

    return report
