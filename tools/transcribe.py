import sys, traceback
name = sys.argv[1]
out = open(f"{name}.txt", "w", encoding="utf-8")
try:
    from faster_whisper import WhisperModel
    m = WhisperModel("small", device="cpu", compute_type="int8")
    segs, _ = m.transcribe(f"audio/{name}.mp3", language="ar", beam_size=1)
    for s in segs:
        line = f"{s.start:8.1f} {s.end:8.1f}  {s.text.strip()}"
        print(line, flush=True); out.write(line + "\n"); out.flush()
except Exception:
    out.write("ERROR\n" + traceback.format_exc())
    raise
