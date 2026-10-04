"""
Sound Engine for Arcana Tarot.
Uses native Windows sound synthesis via winsound with automatic silent fallback.
"""
import sys
import time
import threading

SOUND_ENABLED = True

def is_windows() -> bool:
    return sys.platform == "win32"

def toggle_sound() -> bool:
    global SOUND_ENABLED
    SOUND_ENABLED = not SOUND_ENABLED
    return SOUND_ENABLED

def set_sound(enabled: bool):
    global SOUND_ENABLED
    SOUND_ENABLED = enabled

def _play_async(fn, *args):
    if not SOUND_ENABLED or not is_windows():
        return
    t = threading.Thread(target=fn, args=args, daemon=True)
    t.start()

def _card_flip_sync():
    try:
        import winsound
        winsound.Beep(880, 25)
        winsound.Beep(1200, 35)
    except Exception:
        pass

def play_card_flip():
    _play_async(_card_flip_sync)

def _shuffle_sync():
    try:
        import winsound
        freqs = [320, 360, 420, 380, 460, 520, 440]
        for f in freqs:
            winsound.Beep(f, 20)
            time.sleep(0.01)
    except Exception:
        pass

def play_shuffle():
    _play_async(_shuffle_sync)

def _reveal_sync():
    try:
        import winsound
        # Solfeggio 528Hz -> 639Hz chime
        winsound.Beep(528, 90)
        winsound.Beep(660, 110)
        winsound.Beep(880, 160)
    except Exception:
        pass

def play_reveal():
    _play_async(_reveal_sync)

def _shadow_reveal_sync():
    try:
        import winsound
        # Deep mystery omen tone
        winsound.Beep(320, 120)
        winsound.Beep(240, 140)
        winsound.Beep(180, 220)
    except Exception:
        pass

def play_shadow_reveal():
    _play_async(_shadow_reveal_sync)

def _omen_bell_sync():
    try:
        import winsound
        # Sacred geometry chord progression
        chords = [(528, 80), (660, 80), (792, 100), (1056, 200)]
        for f, d in chords:
            winsound.Beep(f, d)
            time.sleep(0.02)
    except Exception:
        pass

def play_omen_bell():
    _play_async(_omen_bell_sync)

def _victory_fanfare_sync():
    try:
        import winsound
        melody = [(440, 70), (554, 70), (659, 70), (880, 220)]
        for f, d in melody:
            winsound.Beep(f, d)
            time.sleep(0.02)
    except Exception:
        pass

def play_victory():
    _play_async(_victory_fanfare_sync)

def _clash_sync():
    try:
        import winsound
        winsound.Beep(220, 80)
        winsound.Beep(440, 50)
        winsound.Beep(180, 120)
    except Exception:
        pass

def play_clash():
    _play_async(_clash_sync)
