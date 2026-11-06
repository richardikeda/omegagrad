import json,time,warnings,hashlib,platform
from pathlib import Path
import numpy as np
from scipy.integrate import IntegrationWarning
from scipy.stats import ks_2samp
from omegagrad.phase3 import extended
from omegagrad.experiments import write_json
from omegagrad.tensor_engine import batch_potential
from omegagrad.universe import ToyUniverse
p=Path('outputs/phase3/results.json');d=json.loads(p.read_text());d['initial_geometry']=d['geometry'];d['geometry']=[]
warnings.simplefilter('error',IntegrationWarning)
for bits in [12,14,16]:
 r=extended(bits);d['geometry'].append(r);print('refined',bits,r['model'],flush=True)
d['ks']=[dict(a=a['bits'],b=b['bits'],ks=float(ks_2samp(a['widths'],b['widths']).statistic)) for a,b in zip(d['geometry'],d['geometry'][1:])]
u=ToyUniverse(12);z=np.linspace(.01,.99,2048);start=time.perf_counter();v,g,h=batch_potential(z,u.normalized_primes,u.epsilon);d['tensor_validation']=dict(batch=2048,seconds=time.perf_counter()-start,gradient_max_error=float(np.max(abs(g-u.field(z,1)))),hessian_max_error=float(np.max(abs(h-u.field(z,2)))))
d['metadata']=dict(python=platform.python_version(),numpy=np.__version__,source_sha256={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in Path('omegagrad').glob('*.py')},quadrature='4097 global knots plus local edge refinement; split integration; IntegrationWarning treated as error')
write_json(p,d)
for r in d['geometry']:write_json(Path('outputs/phase3')/f"{r['bits']}bits_geometry.json",r)
