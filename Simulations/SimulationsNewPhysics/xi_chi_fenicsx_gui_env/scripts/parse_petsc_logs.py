import os, re, glob, math
def last_float(ms):
    for x in reversed(ms or []):
        try: return float(x)
        except: pass
    return math.nan

rows=[]
for stdout in sorted(glob.glob(os.path.join("logs","poisson3d_*.stdout"))):
    base=os.path.basename(stdout).replace(".stdout","")
    nx=int(re.search(r"_n(\d+)", base).group(1))
    m=re.search(r"_p(\d+)", base)
    procs=int(m.group(1)) if m else 1
    it=math.nan; res=math.nan
    with open(stdout, errors="ignore") as f:
        for ln in f:
            m=re.search(r"KSP.*(?:it|Iteration)?\s*(\d+).*?(?:residual|Residual).*?([0-9.eE+-]+)", ln)
            if m: it=int(m.group(1)); res=float(m.group(2))
            m=re.search(r"CONVERGED.*?iterations?\s+(\d+)", ln)
            if m: it=int(m.group(1))
    t=math.nan
    plog=os.path.join("logs", f"{base}.log")
    if os.path.exists(plog):
        s=open(plog,errors="ignore").read()
        t=last_float(re.findall(r"Time \(sec\)\s*:\s*([0-9.eE+-]+)", s))
        if math.isnan(t): t=last_float(re.findall(r"Total time\s*[:=]\s*([0-9.eE+-]+)", s))
        if math.isnan(t): t=last_float(re.findall(r"\btime\s*=\s*([0-9.eE+-]+)\s*(?:s|sec)\b", s))
    if math.isnan(t):
        pt=os.path.join("logs", f"{base}.time")
        if os.path.exists(pt):
            for ln in open(pt):
                m=re.search(r"ELAPSED\s+([0-9.]+)", ln)
                if m: t=float(m.group(1))
    rows.append((base, procs, nx, it, res, t))

def f(x):
    if x is None or (isinstance(x,float) and math.isnan(x)): return ""
    return f"{x:.6g}" if isinstance(x,float) else str(x)

print("case,procs,n,iter,final_residual,time_s")
for r in rows: print(",".join(f(x) for x in r))

hdr=("case","procs","n","iter","final_res","time_s")
w=[max(len(h), max(len(f(r[i])) for r in rows) if rows else len(h)) for i,h in enumerate(hdr)]
print("\n==== Summary ====")
print("  ".join(hdr[i].ljust(w[i]) for i in range(6)))
for r in rows:
    fres=f"{r[4]:.3e}" if isinstance(r[4],float) and not math.isnan(r[4]) else ""
    tstr=f"{r[5]:.3f}" if isinstance(r[5],float) and not math.isnan(r[5]) else ""
    out=(r[0], r[1], r[2], r[3], fres, tstr)
    print("  ".join(str(out[i]).ljust(w[i]) for i in range(6)))

times={r[1]: r[5] for r in rows if r[2]==64 and isinstance(r[5],float) and not math.isnan(r[5])}
if 1 in times and len(times)>1:
    t1=times[1]
    print("\n==== Strong-scaling (n=64) ====")
    for p in sorted(times):
        sp=t1/times[p] if times[p]>0 else math.nan
        eff=sp/p if p>0 else math.nan
        print(f"p={p}: time={times[p]:.3f}s, speedup={sp:.2f}x, efficiency={eff:.2f}")
else:
    print("\n(no complete n=64 timing data to compute speedup)")
