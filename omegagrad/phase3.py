"""Phase 3 runner. Ground truth remains in the evaluator."""
import time,math,json
from pathlib import Path
import numpy as np
from scipy.stats import ks_2samp
from .universe import ToyUniverse
from .radar import OmegaRadar,miller_rabin_base2
from .phase2 import score,roots
from .detrending import Background,Residual
from .experiments import write_json,write_csv,regression_metrics

def extended(bits,samples=4097):
    u=ToyUniverse(bits);u=ToyUniverse(bits,1e-6*(61/u.p_omega)**2);bg=Background(u.p_omega,u.epsilon,samples);res=Residual(u,bg)
    # Batched bisection on central gap brackets; explicitly reports missing barriers.
    a=u.normalized_primes[:-1];b=u.normalized_primes[1:];lo=a+.05*(b-a);hi=b-.05*(b-a)
    valid=(res.field(lo,1)>0)&(res.field(hi,1)<0)
    for _ in range(40):
        mid=(lo+hi)/2;g=res.field(mid,1);lo=np.where(g>0,mid,lo);hi=np.where(g<=0,mid,hi)
    z=(lo+hi)/2;h=res.field(z,2);valid&=h<0
    original_lo=a+.05*(b-a);original_hi=b-.05*(b-a)
    for _ in range(40):
        m=(original_lo+original_hi)/2;g=u.field(m,1);original_lo=np.where(g>0,m,original_lo);original_hi=np.where(g<=0,m,original_hi)
    original=(original_lo+original_hi)/2
    rows=[]
    for k in range(1,len(z)):
        if valid[k]:rows.append([math.log((z[k]-a[k])/(b[k]-z[k])),math.log(abs(h[k])),(z[k]-original[k])*u.p_omega,int(u.primes[k]-u.primes[k-1])])
    arr=np.array(rows[::-1]);n=int(.7*len(arr));x=arr[:,:3];y=arr[:,3];mean=x[:n].mean(0);sd=x[:n].std(0);sd[sd==0]=1;X=np.column_stack([np.ones(len(x)),(x-mean)/sd]);pred=X[n+1:]@np.linalg.lstsq(X[:n],y[:n],rcond=None)[0]
    # Widths only where neighboring barriers both exist; deterministic-flow basins.
    widths=[(z[k]-z[k-1])*u.p_omega/((u.primes[k+1]-u.primes[k-1])/2) for k in range(1,len(z)) if valid[k] and valid[k-1]]
    return dict(bits=bits,barriers=int(valid.sum()),missing=int((~valid).sum()),widths=widths,features=rows,model=regression_metrics(y[n+1:],pred),baseline=regression_metrics(y[n+1:],np.repeat(y[:n].mean(),len(y[n+1:]))))

def main():
    out=Path('outputs/phase3');out.mkdir(parents=True,exist_ok=True);results=[]
    for bits in [6,8,10,12,14,16,18]:
        u=ToyUniverse(bits);radar=OmegaRadar(u.p_omega);r=radar.run();truth=[int(p) for p in u.primes if p>math.sqrt(u.p_omega)]
        start=time.perf_counter();verified=[n for n in r['candidates'] if miller_rabin_base2(n)];verify_seconds=time.perf_counter()-start
        integers=range(math.floor(math.sqrt(u.p_omega))+1,u.p_omega+1);start=time.perf_counter();direct=[n for n in integers if miller_rabin_base2(n)];direct_seconds=time.perf_counter()-start
        raw={v['n'] for v in r['features']};result=dict(bits=bits,horizon=u.p_omega,calibration=r['threshold'],phase_locked=score(raw,truth),filtered=score(r['candidates'],truth),hybrid=score(verified,truth),direct_mr=score(direct,truth),modular_calls=len(r['candidates']),integer_baseline_calls=len(integers),phase_locked_baseline_calls=sum(n%6 in (1,5) for n in integers),radar_seconds=r['seconds'],verify_seconds=verify_seconds,direct_mr_seconds=direct_seconds,candidates=r['candidates'])
        write_csv(out/f'{bits}bits_features.csv',r['features']);results.append(result);write_json(out/'radar.json',results);print(bits,result['filtered'],flush=True)
    stats=[]
    for bits in [12,14,16]:
        r=extended(bits);stats.append(r);write_json(out/f'{bits}bits_geometry.json',r);print('geometry',bits,r['model'],flush=True)
    ks=[dict(a=a['bits'],b=b['bits'],ks=float(ks_2samp(a['widths'],b['widths']).statistic)) for a,b in zip(stats,stats[1:])]
    write_json(out/'results.json',dict(radar=results,geometry=stats,ks=ks))
if __name__=='__main__':main()
