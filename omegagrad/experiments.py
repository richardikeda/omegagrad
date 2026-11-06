"""Run: python -m omegagrad.experiments --bits 6 8 10 12 --seeds 0 1 2."""
import argparse
import csv
import hashlib
import json
import math
import platform
from pathlib import Path
from datetime import datetime, timezone
import time

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy.stats import ks_2samp, spearmanr

from .universe import ToyUniverse
from .omegasieve import geometry, OmegaSieve


def clean(value):
    if isinstance(value, dict):
        return {k:clean(v) for k,v in value.items()}
    if isinstance(value, (list,tuple,np.ndarray)):
        return [clean(v) for v in value]
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (float,np.floating)):
        return float(value) if math.isfinite(value) else None
    return value


def write_json(path, data):
    path.write_text(json.dumps(clean(data), indent=2, ensure_ascii=False, allow_nan=False), encoding='utf-8')


def write_csv(path, rows):
    if not rows:
        path.write_text('', encoding='utf-8')
        return
    with path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(clean(rows))


def regression_metrics(y, pred):
    residual = y-pred
    variance = np.sum((y-y.mean())**2)
    return dict(mae=float(np.abs(residual).mean()),
                r2=float(1-np.sum(residual**2)/variance) if variance else None)


def prediction_analysis(gaps, seed=1234):
    """Top 70% training, next one interval embargo, lower held-out region.

    All features remain oracle-informed through L. Held-out refers to fitted
    regression coefficients, NOT independence from the prime targets.
    """
    rows = [r for r in reversed(gaps) if r['next_lower_gap'] is not None
            and r['barrier_count'] == 1 and math.isfinite(r['lambda_asymmetry'])]
    if len(rows) < 12:
        return dict(status='insufficient_barriers', sample_count=len(rows))
    y = np.array([r['next_lower_gap'] for r in rows], float)
    lam = np.log([r['lambda_asymmetry'] for r in rows])
    gap = np.array([r['gap'] for r in rows],float)
    split = int(.7*len(rows))
    test_start = split+1
    if len(rows)-test_start < 3:
        return dict(status='insufficient_test_rows', sample_count=len(rows))
    train, test = slice(0,split), slice(test_start,None)
    def fitted(features, train_y):
        x = np.column_stack(features)
        center, scale = x[train].mean(0), x[train].std(0)
        scale[scale == 0] = 1
        design = np.column_stack([np.ones(len(y)), (x-center)/scale])
        beta = np.linalg.lstsq(design[train],train_y,rcond=None)[0]
        return design[test]@beta
    baseline = np.repeat(y[train].mean(),len(y[test]))
    lambda_pred = fitted([lam], y[train])
    gap_pred = fitted([gap], y[train])
    joint_pred = fitted([gap,lam], y[train])
    rng = np.random.default_rng(seed)
    null_mae = [regression_metrics(y[test], fitted([lam],rng.permutation(y[train])))['mae'] for _ in range(200)]
    actual_mae = regression_metrics(y[test], lambda_pred)['mae']
    return dict(status='retrospective_oracle_features', sample_count=len(rows), train_count=split,
        embargo_count=1, test_count=len(y[test]), split='descending spatial 70/30, one interval embargo',
        spearman_lambda_next_lower_gap=float(spearmanr(lam,y).statistic),
        train_mean=regression_metrics(y[test],baseline), current_gap=regression_metrics(y[test],gap[test]),
        fitted_gap=regression_metrics(y[test],gap_pred), log_lambda=regression_metrics(y[test],lambda_pred),
        gap_plus_log_lambda=regression_metrics(y[test],joint_pred),
        train_label_shuffle_mae_percentiles=np.percentile(null_mae,[5,50,95]).tolist(),
        shuffle_fraction_mae_at_most_observed=(1+sum(m <= actual_mae for m in null_mae))/201,
        predictions=[dict(lower_prime=r['lower_prime'],upper_prime=r['upper_prime'],
            actual=float(actual),train_mean=float(base),log_lambda=float(lp),fitted_gap=float(gp),
            gap_plus_log_lambda=float(jp)) for r,actual,base,lp,gp,jp in
            zip(rows[test_start:], y[test],baseline,lambda_pred,gap_pred,joint_pred)],
        limitation='L and lambda contain the target primes; this is not blind prime prediction. '
                   'Shuffle is a diagnostic, not a valid spatial-independence significance test.')


def validate_engine(universe):
    samples = np.r_[np.linspace(.013,.987,13), universe.normalized_primes[[0,-1]],1.0]
    gradient_errors, loss_errors, fd_errors = [], [], []
    h = math.sqrt(universe.epsilon)*1e-3
    for z in samples:
        loss, g = universe.value_gradient(float(z),'autograd')
        analytic = universe.field(z,1)
        gradient_errors.append(abs(g-analytic))
        loss_errors.append(abs(loss-universe.field(z)))
        fd = (universe.field(z+h)-universe.field(z-h))/(2*h)
        fd_errors.append(abs(fd-analytic)/max(1,abs(analytic)))
    return dict(samples=len(samples), max_autograd_gradient_abs_error=max(gradient_errors),
        max_autograd_loss_abs_error=max(loss_errors),
        max_finite_difference_gradient_scaled_error=max(fd_errors))


def plot_universe(u, geom, run, folder, tag):
    width = math.sqrt(u.epsilon)
    z = np.unique(np.r_[np.linspace(0,1,8000),
        np.clip((u.normalized_primes[:,None]+width*np.linspace(-3,3,17)).ravel(),0,1)])
    fig, axes = plt.subplots(3,1,figsize=(12,10),layout='constrained')
    axes[0].plot(z,u.field(z),color='#155e75',lw=.8)
    roots = geom['roots']
    for kind,color,marker in [('minimum','#059669','o'),('maximum','#e11d48','x')]:
        positions = [r['z'] for r in roots if r['kind']==kind]
        axes[0].scatter(positions,u.field(positions),s=12,c=color,marker=marker,label=kind)
    axes[0].legend(loc='best')
    axes[0].set(ylabel='L(z)',xlabel='z')
    axes[1].plot(z,u.field(z,1),color='#be123c',lw=.7)
    axes[1].axhline(0,color='black',lw=.7)
    axes[1].set(ylabel="dL/dz",xlabel='z')
    trajectory = run['trajectory']
    axes[2].plot([t['step'] for t in trajectory],[t['z'] for t in trajectory],lw=.6,c='#94a3b8')
    for phase,color in [('descent','#2563eb'),('escape','#ea580c')]:
        subset = [t for t in trajectory if t['phase']==phase]
        axes[2].scatter([t['step'] for t in subset],[t['z'] for t in subset],s=1,c=color,label=phase)
    axes[2].set(ylabel='z',xlabel='Iteration (escape is externally controlled)')
    axes[2].legend()
    fig.suptitle(f'OMEGAGRAD | S={u.s_bits} | P_omega={u.p_omega} | {tag} | epsilon={u.epsilon:.3g}')
    for ax in axes:
        ax.grid(alpha=.15)
    fig.savefig(folder/'landscape.png',dpi=180)
    plt.close(fig)


def plot_comparison(results, output):
    fig, axes = plt.subplots(2,2,figsize=(12,9),layout='constrained')
    colors = ['#155e75','#7c3aed','#d97706','#e11d48']
    for tag,style in [('fixed','-'),('scaled','--')]:
        subset = [r for r in results if r['summary']['epsilon_mode']==tag]
        if not subset:
            continue
        bits = [r['summary']['s_bits'] for r in subset]
        axes[0,0].plot(bits,[r['summary']['minimum_count']/r['summary']['prime_count'] for r in subset],style+'o',label=tag)
        axes[0,1].plot(bits,[r['summary']['coverage_mean'] for r in subset],style+'o',label=tag)
    for color,r in zip(colors,[r for r in results if r['summary']['epsilon_mode']=='scaled']):
        widths = np.array([b['width_over_local_spacing'] for b in r['geometry']['basins']])
        widths = np.sort(widths[np.isfinite(widths)])
        axes[1,0].plot(widths,np.arange(1,len(widths)+1)/len(widths),color=color,label=f"S={r['summary']['s_bits']}")
        rows = [g for g in r['geometry']['gaps'] if g['barrier_count']==1 and g['next_lower_gap'] is not None]
        axes[1,1].scatter([np.log(g['lambda_asymmetry']) for g in rows],[g['next_lower_gap'] for g in rows],s=10,alpha=.5,color=color,label=f"S={r['summary']['s_bits']}")
    axes[0,0].set(xlabel='S_bits',ylabel='Local minima / primes',ylim=(0,1.08),title='Smoothing changes the topology')
    axes[0,1].set(xlabel='S_bits',ylabel='Validated prime coverage',ylim=(0,1.08),title='Controlled OmegaSieve (mean over seeds)')
    axes[1,0].set(xlabel='Basin width / mean adjacent prime gap',ylabel='Empirical CDF',title='Scaled epsilon; interior basins')
    axes[1,1].set(xlabel='log(lambda)',ylabel='Next lower gap (integer units)',title='Retrospective association; oracle-informed')
    for ax in axes.flat:
        if ax.get_legend_handles_labels()[0]:
            ax.legend(fontsize=8)
        ax.grid(alpha=.2)
    fig.savefig(output/'comparison.png',dpi=180)
    plt.close(fig)


def run_suite(bits, modes, seeds, output, backend='analytic', momentum=.5, noise=.02):
    output.mkdir(parents=True,exist_ok=True)
    results = []
    print('mode   bits P_omega primes minima barriers coverage grid_stable',flush=True)
    for s in bits:
        for mode in modes:
            start = time.perf_counter()
            u = ToyUniverse(s)
            if mode == 'scaled':
                u = ToyUniverse(s, 1e-6*(61/u.p_omega)**2)
            folder = output/f'{mode}_{s}bits'
            folder.mkdir(exist_ok=True)
            validation = validate_engine(u)
            geom = geometry(u)
            prediction = prediction_analysis(geom['gaps'])
            runs = []
            for seed in seeds:
                run = OmegaSieve(u,seed=seed,backend=backend,momentum=momentum,noise=noise).run()
                write_csv(folder/f'trajectory_seed{seed}.csv',run['trajectory'])
                runs.append(run)
            plot_universe(u,geom,runs[0],folder,mode)
            widths = [b['width_z'] for b in geom['basins']]
            summary = dict(epsilon_mode=mode,s_bits=s,p_omega=u.p_omega,prime_count=len(u.primes),
                epsilon=u.epsilon,smoothing_width_integer=math.sqrt(u.epsilon)*u.p_omega,
                minimum_count=len(geom['basins']),barrier_count=sum(g['barrier_count'] for g in geom['gaps']),
                gaps_without_barrier=sum(g['barrier_count']==0 for g in geom['gaps']),
                basin_width_mean=float(np.mean(widths)),basin_width_cv=float(np.std(widths)/np.mean(widths)),
                basin_width_sum=float(sum(widths)),grid_stable=geom['grid_stable'],
                max_root_gradient_residual=max(r['gradient_residual'] for r in geom['roots']),
                max_root_newton_error_estimate=max(r['newton_error_estimate'] for r in geom['roots']),
                mean_normalized_prime_gap=float(np.diff(u.normalized_primes).mean()),
                coverage_mean=float(np.mean([r['coverage'] for r in runs])),
                coverage_min=float(min(r['coverage'] for r in runs)),coverage_max=float(max(r['coverage'] for r in runs)),
                run_statuses=';'.join(r['status'] for r in runs),elapsed_seconds=time.perf_counter()-start)
            compact_runs = [{k:v for k,v in r.items() if k!='trajectory'} for r in runs]
            result = dict(summary=summary,validation=validation,geometry=geom,prediction=prediction,runs=compact_runs)
            write_csv(folder/'gaps.csv',geom['gaps'])
            write_csv(folder/'basins.csv',geom['basins'])
            write_csv(folder/'stationary_points.csv',geom['roots'])
            write_csv(folder/'predictions.csv',prediction.get('predictions',[]))
            write_json(folder/'results.json',result)
            results.append(result)
            print(f"{mode:6} {s:4} {u.p_omega:7} {len(u.primes):6} {len(widths):6} {summary['barrier_count']:8} "
                  f"{summary['coverage_mean']:8.1%} {geom['grid_stable']} ({summary['elapsed_seconds']:.1f}s)",flush=True)
    comparisons = []
    for mode in modes:
        group = [r for r in results if r['summary']['epsilon_mode']==mode]
        for first,second in zip(group,group[1:]):
            a = np.array([b['width_over_local_spacing'] for b in first['geometry']['basins']])
            b = np.array([b['width_over_local_spacing'] for b in second['geometry']['basins']])
            a,b = a[np.isfinite(a)],b[np.isfinite(b)]
            if not len(a) or not len(b):
                continue
            # KS distance only. Spatially dependent deterministic data do not
            # justify the usual independent-sample p-value interpretation.
            comparisons.append(dict(mode=mode,bits_a=first['summary']['s_bits'],bits_b=second['summary']['s_bits'],
                interior_basins_a=len(a),interior_basins_b=len(b),ks_distance=float(ks_2samp(a,b).statistic),
                median_a=float(np.median(a)),median_b=float(np.median(b))))
    metadata = dict(created_utc=datetime.now(timezone.utc).isoformat(),python=platform.python_version(),
        numpy=np.__version__,scipy=scipy.__version__,matplotlib=matplotlib.__version__,
        bits=bits,modes=modes,seeds=seeds,backend=backend,momentum=momentum,noise=noise,
        domain=[0,1],fixed_epsilon=1e-6,scaled_epsilon='1e-6*(61/P_omega)**2',
        source_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in Path(__file__).parent.glob('*.py')})
    write_csv(output/'summary.csv',[r['summary'] for r in results])
    write_csv(output/'scale_comparisons.csv',comparisons)
    write_json(output/'results.json',dict(metadata=metadata,scale_comparisons=comparisons,universes=results))
    plot_comparison(results,output)
    write_report(output,results,comparisons,metadata)
    return results


def write_report(output, results, comparisons, metadata):
    lines = ['# OMEGAGRAD: primeiro laboratorio reproduzivel', '',
        'Configuracao e resultados numericos, sem afirmacao de descoberta de primos desconhecidos.', '',
        f"Execucao UTC: {metadata['created_utc']}. Seeds: {metadata['seeds']}. Backend: {metadata['backend']}.", '',
        '## Protocolo', '',
        '- Corte operacional: maior primo <= 2**S_bits. Nao calcula K(p)+T(p) nem valida um limite fisico cosmologico.',
        '- L(z) = soma log((z-p/P_omega)^2+epsilon); W(x) = soma sin^2(pi*x/p).',
        '- Derivada segunda: soma 2*(epsilon-d^2)/(d^2+epsilon)^2, com d=z-p/P_omega.',
        '- Epsilon fixo = 1e-6. Controle escalado = 1e-6*(61/P_omega)^2; largura de suavizacao em inteiros = 0.061.',
        '- Raizes por brackets + Brent + polimento Newton; malhas iniciam com 8 e 16 amostras por sqrt(epsilon), duplicando ate estabilizar (maximo 128). Estabilidade de malha nao e certificacao de todas as raizes, sobretudo degeneradas.',
        '- Bacias do fluxo deterministico dz/dt=-L\'(z), no dominio [0,1], delimitadas por maximos locais. Nao sao bacias da dinamica com momento/ruido.',
        '- OmegaSieve parte de z=1, usa gradiente, momento e ruido relativo ao passo, com backtracking. Apos convergir, um transporte externo para a esquerda cruza a barreira; cada fase aparece no CSV.',
        '- Rotulagem posterior: arredonda a coordenada inteira, exige erro <=0.25 e primalidade pela lista de referencia. Proximidade a um primo nunca basta para declarar convergencia.',
        '- A funcao potencial ja recebe todos os primos do crivo. Cobertura e recuperacao de uma base conhecida, nao desempenho de um novo crivo de primalidade.', '',
        '## Resultados', '',
        '|epsilon|bits|P_omega|primos|minimos|barreiras|cobertura media|',
        '|---|---:|---:|---:|---:|---:|---:|']
    for r in results:
        s=r['summary']
        lines.append(f"|{s['epsilon_mode']}|{s['s_bits']}|{s['p_omega']}|{s['prime_count']}|{s['minimum_count']}|{s['barrier_count']}|{s['coverage_mean']:.2%}|")
    lines += ['', '## Validacao numerica', '']
    for r in results:
        s,v=r['summary'],r['validation']
        lines.append(f"- {s['epsilon_mode']} S={s['s_bits']}: erro maximo AD vs analitico={v['max_autograd_gradient_abs_error']:.3g}; "
            f"residuo maximo nas raizes={s['max_root_gradient_residual']:.3g}; estimativa |L\'/L\'\'|={s['max_root_newton_error_estimate']:.3g}; "
            f"malha estavel={s['grid_stable']}; estados={s['run_statuses']}.")
    lines += ['', '## Assimetria e proximo gap inferior', '',
        'Para p[k]<p[k+1], lambda=(z*-p[k]/P)/(p[k+1]/P-z*). Alvo: p[k]-p[k-1]. Usa-se log(lambda) para a regressao.',
        'Treino nos 70% superiores, um intervalo de embargo e teste na regiao inferior. Apenas gaps com exatamente uma barreira entram; a selecao pode introduzir vies.',
        'A separacao protege o ajuste da regressao, mas o potencial global continua contendo os primos-alvo. Os resultados sao retrospectivos, sem evidencia de previsao cega.', '',
        '|epsilon|bits|n treino/teste|rho Spearman|MAE media treino|MAE gap ajustado|MAE log(lambda)|R2 log(lambda)|',
        '|---|---:|---:|---:|---:|---:|---:|---:|']
    for r in results:
        p,s=r['prediction'],r['summary']
        if 'log_lambda' in p:
            lines.append(f"|{s['epsilon_mode']}|{s['s_bits']}|{p['train_count']}/{p['test_count']}|{p['spearman_lambda_next_lower_gap']:.3f}|"
                f"{p['train_mean']['mae']:.3f}|{p['fitted_gap']['mae']:.3f}|{p['log_lambda']['mae']:.3f}|{p['log_lambda']['r2']:.3f}|")
        else:
            lines.append(f"|{s['epsilon_mode']}|{s['s_bits']}|amostra insuficiente||||||")
    lines += ['', '## Comparacao de escala', '',
        'Larguras brutas encolhem por normalizacao e pela quantidade de atratores: media=1/numero_de_bacias quando particionam [0,1]. Isso sozinho nao prova invariancia.',
        'Comparacao descritiva das larguras divididas pela media dos gaps adjacentes; exclui primos nas duas bordas. KS e distancia entre CDFs, sem p-valor inferencial.', '',
        '|epsilon|bits A/B|mediana A|mediana B|distancia KS|', '|---|---:|---:|---:|---:|']
    for c in comparisons:
        lines.append(f"|{c['mode']}|{c['bits_a']}/{c['bits_b']}|{c['median_a']:.3f}|{c['median_b']:.3f}|{c['ks_distance']:.3f}|")
    lines += ['', '## Interpretacao e limites', '',
        '- Primos normalizados nao sao necessariamente pontos estacionarios: no primo, os demais termos contribuem um gradiente nao nulo. Medimos o deslocamento real em basins.csv.',
        '- Com epsilon fixo, a largura sqrt(epsilon)*P cresce em unidades inteiras. A fusao/perda de pocos e um efeito da regularizacao que precisa ser separado da aritmetica.',
        '- Mesmo com epsilon escalado, os primos adicionais mudam o campo global. Sem estabilidade quantitativa entre escalas e controles adicionais, nao se conclui invariancia.',
        '- Maximos em uma dimensao sao barreiras, nao selas no sentido multivariado. Nao ha garantia de uma barreira por gap para epsilon positivo arbitrario.',
        '- W(x)=0 codifica multiplos comuns da base, incluindo zero, e nao identifica automaticamente primos. Seu valor/gradiente foi validado nos testes.',
        '- Nao sao demonstrados novos teoremas, estruturas fractais ou ganhos de complexidade. O custo de cada avaliacao do campo e linear no numero de primos previamente conhecidos.',
        '- Proximo teste para previsao: construir observaveis que nao usem os primos ocultados; repetir em regioes/escala independentes e contra controles nao primos.', '',
        '## Artefatos', '',
        '- summary.csv: comparativo; results.json: configuracao, hashes, geometrias, diagnosticos e capturas.',
        '- scale_comparisons.csv e comparison.png: comparacoes de escala.',
        '- Por universo: gaps.csv, basins.csv, stationary_points.csv, predictions.csv, trajectory_seed*.csv, results.json e landscape.png.', '']
    (output/'REPORT.md').write_text('\n'.join(lines),encoding='utf-8')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bits',nargs='+',type=int,default=[6,8,10,12])
    parser.add_argument('--modes',nargs='+',choices=['fixed','scaled'],default=['fixed','scaled'])
    parser.add_argument('--seeds',nargs='+',type=int,default=[0,1,2])
    parser.add_argument('--backend',choices=['analytic','autograd'],default='analytic')
    parser.add_argument('--momentum',type=float,default=.5)
    parser.add_argument('--noise',type=float,default=.02)
    parser.add_argument('--output',type=Path,default=Path('outputs/first_run'))
    args=parser.parse_args()
    run_suite(args.bits,args.modes,args.seeds,args.output,args.backend,args.momentum,args.noise)


if __name__=='__main__':
    main()
