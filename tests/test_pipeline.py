from pathlib import Path
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

from generate_synthetic_data import generate, interviews
from validate_data import validate
from analyze_quantitative import run as quantitative_run
from analyze_qualitative import run as qualitative_run


def test_reproducible():
    assert generate(123).equals(generate(123))


def test_validation():
    summary = validate(generate())
    assert summary['wave4_n'] >= 250


def test_100_seeds():
    for seed in range(1000, 1100):
        validate(generate(seed))


def test_models_are_finite_and_stable():
    estimates = quantitative_run(generate())
    assert np.isfinite(estimates[['estimate', 'se', 'ci_low', 'ci_high', 'p_value']]).all().all()
    assert estimates.se.max() < 10
    turnover = estimates[estimates.model == 'Discrete-time turnover']
    assert len(turnover) >= 5
    assert turnover.se.max() < 5
    interaction = estimates[(estimates.model == 'GEE distress') & estimates.term.str.contains('org_stress:supervisor_support', regex=False)]
    assert len(interaction) == 1


def test_qualitative():
    data = generate()
    interview_data = interviews(data)
    coded, frequencies, joint = qualitative_run(interview_data, data)
    assert len(coded) == 240
    assert joint.mean_distress.between(1, 7).all()


def test_synthetic_ids():
    data = generate()
    assert data.person_id.str.startswith('JWP').all()
