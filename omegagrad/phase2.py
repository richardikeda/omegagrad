"""Phase 2 reproducible experiments; truth is used only outside blind scanner."""
import json,math,hashlib,platform
from pathlib import Path
import numpy as np
from scipy.optimize import brentq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from .universe import ToyUniverse
from .detrending import Background,Residual
from .blind_sieve import BlindWave
from .experiments import write_json,write_csv,regression_metrics

def roots(field,grid):
    g=field.field(grid,1);out=[]
    for i in np.flatnonzero(np.signbit(g[:-1])!=np.signbit(g[1:])):
        z=brentq(lambda x:float(field.field(x,1)),grid[i],grid[i+1],xtol=1e-14)
        h=float(field.field(z,2));out.append(dict(z=z,hessian=h,kind='minimum' if h>0 else 'maximum',residual=abs(float(field.field(z,1)))))
    return out

def score(pred,truth):
    pred,truth=set(pred),set(truth);tp=len(pred&truth);p=tp/len(pred) if pred else 0;r=tp/len(truth) if truth else 0
    return dict(tp=tp,fp=len(pred-truth),fn=len(truth-pred),precision=p,recall=r,f1=2*p*r/(p+r) if p+r else 0)

def regression(rows):
    rows=list(reversed(rows));n=int(.7*len(rows));test=n+1
    if len(rows)-test<3:return {'status':'insufficient'}
    a=np.array(rows);y=a[:,2];x=a[:,:2];mean=x[:n].mean(0);sd=x[:n].std(0);sd[sd==0]=1
    X=np.column_stack([np.ones(len(a)),(x-mean)/sd]);pred=X[test:]@np.linalg.lstsq(X[:n],y[:n],rcond=None)[0]
    return dict(train=n,test=len(y[test:]),model=regression_metrics(y[test:],pred),baseline=regression_metrics(y[test:],np.repeat(y[:n].mean(),len(y[test:]))))

def main():
    out=Path('outputs/phase2');out.mkdir(parents=True,exist_ok=True);results=[]
    for bits in [6,8,10,12]:
        u=ToyUniverse(bits);u=ToyUniverse(bits,1e-6*(61/u.p_omega)**2)
        bg=Background(u.p_omega,u.epsilon,1025);fine=Background(u.p_omega,u.epsilon,2049);res=Residual(u,fine)
        # Resolve narrow prime wells with local samples plus gap subdivision.
        grid=np.unique(np.r_[np.linspace(0,1,10001),np.clip((u.normalized_primes[:,None]+np.sqrt(u.epsilon)*np.linspace(-4,4,33)).ravel(),0,1)])
        original=roots(u,grid);adjusted=roots(res,grid)
        def features(catalog,field):
            rows=[]
            for k in range(1,len(u.primes)-1):
                a,b=u.normalized_primes[k:k+2];rr=[r for r in catalog if a<r['z']<b and r['kind']=='maximum']
                if len(rr)==1:
                    z=rr[0]['z'];rows.append([math.log((z-a)/(b-z)),math.log(abs(rr[0]['hessian'])),int(u.primes[k]-u.primes[k-1])])
            return rows
        # Matched intervals prevent selection changes from explaining improvement.
        common=[]
        for k in range(1,len(u.primes)-1):
            a,b=u.normalized_primes[k:k+2]
            pair=[[r for r in cat if a<r['z']<b and r['kind']=='maximum'] for cat in [original,adjusted]]
            if all(len(v)==1 for v in pair):common.append((k,pair))
        matched=[[],[]]
        for k,pair in common:
            a,b=u.normalized_primes[k:k+2]
            for j in [0,1]:
                r=pair[j][0];matched[j].append([math.log((r['z']-a)/(b-r['z'])),math.log(abs(r['hessian'])),int(u.primes[k]-u.primes[k-1])])
        wave=BlindWave(u.p_omega);discovery=wave.discover();refined=wave.discover(.025)
        truth=[int(p) for p in u.primes if p>math.sqrt(u.p_omega)]
        # Random internal removal, fixed seed; removed labels used only in evaluation.
        rng=np.random.default_rng(42);hidden=sorted(rng.choice(u.primes[1:-1],max(1,round(.1*(len(u.primes)-2))),replace=False).tolist())
        masked=ToyUniverse(bits,u.epsilon);masked.primes=np.array([p for p in u.primes if p not in hidden]);masked.normalized_primes=masked.primes/u.p_omega
        altered=roots(masked,grid);changes=[]
        for p in masked.primes[1:-1]:
            z=p/u.p_omega;before=min((r for r in original if r['kind']=='minimum'),key=lambda r:abs(r['z']-z));after=min((r for r in altered if r['kind']=='minimum'),key=lambda r:abs(r['z']-z))
            changes.append(dict(prime=int(p),shift_integer=(after['z']-before['z'])*u.p_omega,hessian_before=before['hessian'],hessian_after=after['hessian']))
        # Predeclared gap anomaly heuristic, no hidden labels in candidate construction.
        gaps=np.diff(masked.primes);threshold=2*np.median(gaps)
        guesses=[round((int(a)+int(b))/2) for a,b in zip(masked.primes[:-1],masked.primes[1:]) if b-a>threshold]
        result=dict(bits=bits,horizon=u.p_omega,epsilon=u.epsilon,base=wave.base.tolist(),blind=score(refined['candidates'],truth),blind_grid_stable=discovery['candidates']==refined['candidates'],blind_candidates=refined['candidates'],blind_minima=refined['minima'],original_roots=original,residual_roots=adjusted,detrending_before=regression(matched[0]),detrending_after=regression(matched[1]),background_gradient_refinement_max=float(np.max(abs(bg.field(np.linspace(.01,.99,100),1)-fine.field(np.linspace(.01,.99,100),1)))),holdout=dict(seed=42,hidden=hidden,guesses=guesses,metrics=score(guesses,hidden),neighbor_changes=changes,masked_roots=altered))
        results.append(result);write_json(out/f'{bits}bits.json',result);write_csv(out/f'{bits}bits_neighbor_changes.csv',changes)
        z=np.linspace(0,1,4000);fig,ax=plt.subplots(2,2,figsize=(12,8),layout='constrained');ax[0,0].plot(z,u.field(z),label='L');ax[0,0].plot(z,fine.field(z),label='background');ax[0,0].legend();ax[0,1].plot(z,res.field(z));ax[0,1].set_title('Residual potential');ax[1,0].plot(z,res.field(z,1));ax[1,0].set_title('Residual gradient');x=np.linspace(max(math.sqrt(u.p_omega),u.p_omega-80),u.p_omega,5000);ax[1,1].plot(x,wave.field(x));ax[1,1].set_title('Blind wave: last 80 integer units');fig.suptitle(f'Phase 2 | S={bits}');fig.savefig(out/f'{bits}bits.png',dpi=160);plt.close(fig)
        print(bits,result['blind'],result['detrending_after'],flush=True)
    write_json(out/'results.json',dict(python=platform.python_version(),numpy=np.__version__,source_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in Path(__file__).parent.glob('*.py')},protocol='scaled epsilon; horizon supplied; stationary gradient scan; matched spatial holdout; seed 42 removal',universes=results))
if __name__=='__main__':main()
