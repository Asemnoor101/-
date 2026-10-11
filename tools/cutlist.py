import re, sys, json, subprocess
STARTS = r'(من قالها|من قال |يقولها|يقول ذلك|يقال|تقال|قال النبي|قال عليه|قال رسول|قال صلى|كان صلى الله عليه وسلم إذا|موقع|موطع|يقدم لكم|قدما لكم|بصوت فضيلة)'
CONT = r"(فمات من|كفته|كفاه|كفره|من امر|من أمر|^والآخرة$|^وثلاث|سبع مرات|سبق مرات|لم يضره|لم تضره|حقا على الله|يرضيه|لم يأت|إلا أحد قال|أدركته|تدركته|دخل الجنة|أعتقه|أدى شكر|أجير|وجير|حتى يمسي|حتى يصبح|حتى يسبح|من صلى علي|وحين يمسي|وحين يصبح|عشر رقاب|بأفضل|^وحين|^ومن قالها|أربع مرات|ثلاث مرات|مئة مرة|عشر مرات|شفاعة يوم القيام|كتبت له|محيت عنه|حرزا من الشيطان)"
MANUAL = {
 'afasy-morning': [(0, 4.2), (767.9, 781.9)],
 'afasy-evening': [(0, 'pause')],
 'abbad-morning': [(0, 2.0)],
 'abbad-evening': [(0, 2.0), (1153.3, 'end')],
 'abkar-both':    [(0, 19.2), (890.0, 'end')],
 'rifai-both':    [(0, 87.0)],
}
def segs(name):
    out=[]; seen=set()
    for l in open(f"transcripts/{name}.txt", encoding="utf-8"):
        m=re.match(r'\s*([\d.]+)\s+([\d.]+)\s+(.*)', l)
        if not m or l in seen: continue
        seen.add(l)
        txt=re.sub(r'^[\d\-\.]+\s*','',m.group(3)).strip()
        out.append((float(m.group(1)), float(m.group(2)), txt))
    return out
def pauses(path):
    r=subprocess.run(['ffmpeg','-nostdin','-hide_banner','-i',path,'-af','silencedetect=n=-32dB:d=0.08','-f','null','-'],capture_output=True,text=True).stderr
    s=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',r)]; e=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',r)]
    dur=float(re.search(r'Duration: (\d+):(\d+):([\d.]+)',r).groups()[2]) + 60*int(re.search(r'Duration: (\d+):(\d+)',r).group(2)) + 3600*int(re.search(r'Duration: (\d+)',r).group(1))
    return [((a+b)/2) for a,b in zip(s,e)], dur
def snap(t, P, win=1.2):
    c=[p for p in P if abs(p-t)<=win]
    return min(c, key=lambda p:abs(p-t)) if c else t
name=sys.argv[1]; path=f"audio/{name}.mp3"
P,dur=pauses(path); S=segs(name)
cuts=[]; prev=False
for a,b,t in S:
    hit = bool(re.match(STARTS,t)) or (prev and bool(re.search(CONT,t)))
    if hit: cuts.append((a,b,t))
    prev=hit
for a,b in MANUAL.get(name,[]):
    if b=='end': b=dur
    if b=='pause': b=next((p for p in P if p>1.0), 2.0)
    cuts.append((a,b,'[manual]'))
res=[]
for a,b,t in sorted(cuts):
    a2=0.0 if a<0.5 else snap(a,P); b2=dur if b>=dur-0.5 else snap(b,P)
    if b2-a2<0.4: continue
    res.append([round(a2,2),round(b2,2),t])
# merge overlapping/adjacent
kept=[(a,b) for a,b,t in S if not any(c[0]<=a and b<=c[1]+0.01 for c in cuts)]
m=[]
for r in res:
    if m:
        g0,g1=m[-1][1],r[0]
        empty=not any(a<g1 and b>g0 and (min(b,g1)-max(a,g0))>0.5 for a,b in kept)
        if g1<=g0+0.3 or (g1-g0<2.5 and empty):
            m[-1][1]=max(m[-1][1],r[1]); m[-1][2]+=' | '+r[2]; continue
    m.append(r)
json.dump({'dur':dur,'cuts':m},open(f"/tmp/claude-0/cut/{name}.json","w"),ensure_ascii=False)
tot=sum(b-a for a,b,_ in m)
print(f"## {name}: {len(m)} cuts, {tot:.0f}s of {dur:.0f}s")
for a,b,t in m: print(f"  {a:7.1f}-{b:7.1f}  {t[:90]}")
