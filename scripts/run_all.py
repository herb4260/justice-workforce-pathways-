from generate_synthetic_data import generate
from validate_data import validate
from analyze_quantitative import run as quantitative
from analyze_qualitative import run as qualitative
from make_figures import run as figures

def main():
    p,s,i=generate(); validate(p,s,i); quantitative(p,s); qualitative(i); figs=figures();
    print(f'Pipeline complete: {p.person_id.nunique()} officers, {len(p)} panel rows, {len(figs)} SVG figures.')
if __name__=='__main__': main()
