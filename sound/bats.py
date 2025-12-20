import numpy as np
import wave

MORSE = {
    "A": ".-",   "B": "-...", "C": "-.-.", "D": "-..",  "E": ".",
    "F": "..-.", "G": "--.",  "H": "....", "I": "..",   "J": ".---",
    "K": "-.-",  "L": ".-..", "M": "--",   "N": "-.",   "O": "---",
    "P": ".--.", "Q": "--.-", "R": ".-.",  "S": "...",  "T": "-",
    "U": "..-",  "V": "...-", "W": ".--",  "X": "-..-", "Y": "-.--",
    "Z": "--..",
    "0": "-----","1": ".----","2": "..---","3": "...--","4": "....-",
    "5": ".....","6": "-....","7": "--...","8": "---..","9": "----.",
}

def tone(freq_hz: float, duration_s: float, sr: int, amp: float = 0.3, fade_ms: float = 2.0):
    """Sine-Ton mit kurzem Fade-in/out gegen Knackser."""
    n = int(duration_s * sr)
    t = np.arange(n) / sr
    x = amp * np.sin(2 * np.pi * freq_hz * t)

    fade_n = int((fade_ms / 1000.0) * sr)
    fade_n = min(fade_n, n // 2)
    if fade_n > 0:
        fade = np.linspace(0, 1, fade_n)
        x[:fade_n] *= fade
        x[-fade_n:] *= fade[::-1]
    return x

def silence(duration_s: float, sr: int):
    return np.zeros(int(duration_s * sr), dtype=np.float32)

def text_to_morse(text: str):
    words = text.upper().split()
    morse_words = []
    for w in words:
        chars = []
        for ch in w:
            if ch in MORSE:
                chars.append(MORSE[ch])
        if chars:
            morse_words.append(chars)
    return morse_words  # Liste von Wörtern, jedes Wort: Liste von Zeichen-Morse

def morse_audio(text: str, freq_hz: float = 30000.0, wpm: float = 20.0, sr: int = 192000, amp: float = 0.3):
    """
    Morse-Timing:
      dot = 1 unit
      dash = 3 units
      gap innerhalb Buchstabe = 1 unit
      gap zwischen Buchstaben = 3 units
      gap zwischen Wörtern = 7 units
    Einheit aus WPM: dot_len = 1.2 / WPM Sekunden
    """
    unit = 1.2 / wpm

    morse_words = text_to_morse(text)
    parts = []

    for wi, word in enumerate(morse_words):
        for ci, code in enumerate(word):
            for si, sym in enumerate(code):
                if sym == ".":
                    parts.append(tone(freq_hz, 1 * unit, sr, amp))
                elif sym == "-":
                    parts.append(tone(freq_hz, 3 * unit, sr, amp))

                # Abstand zwischen Symbolen innerhalb eines Buchstabens (außer nach letztem)
                if si != len(code) - 1:
                    parts.append(silence(1 * unit, sr))

            # Abstand zwischen Buchstaben (außer nach letztem im Wort)
            if ci != len(word) - 1:
                parts.append(silence(3 * unit, sr))

        # Abstand zwischen Wörtern (außer nach letztem Wort)
        if wi != len(morse_words) - 1:
            parts.append(silence(7 * unit, sr))

    if not parts:
        return np.array([], dtype=np.float32), sr

    audio = np.concatenate(parts).astype(np.float32)
    # Hard limit (falls amp zu hoch)
    audio = np.clip(audio, -1.0, 1.0)
    return audio, sr

def write_wav(path: str, audio_f32: np.ndarray, sr: int):
    """Schreibt 16-bit PCM WAV."""
    pcm = (audio_f32 * 32767.0).astype(np.int16)
    with wave.open(path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(sr)
        wf.writeframes(pcm.tobytes())

if __name__ == "__main__":
    text = "N 52 15 789 E 13 08 460"
    audio, sr = morse_audio(text, freq_hz=30000.0, wpm=18.0, sr=192000, amp=0.2)
    write_wav("17-morse_30khz.wav", audio, sr)
    print("WAV geschrieben: morse_30khz.wav", "Samplerate:", sr, "Dauer(s):", len(audio)/sr)
