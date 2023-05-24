import pytest
from translator import *
from translator import consonants

def test_replace_special_signs():
    line = '’’„„““ßß––'
    line_expected = '\'\'@@""$$--'
    line_translated = replace_special_signs(line)
    assert line_expected == line_translated

def test_replace_und_and():
    line = 'undandund andundand'
    line_expected = '&and& and&and'
    line_translated = replace_und_and(line, german_and=True)
    assert line_expected == line_translated
    line = 'undandund andundand'
    line_expected = 'und&und &und&'
    line_translated = replace_und_and(line, german_and=False)
    assert line_expected == line_translated

def test_replace_sch():
    line = 'schsch'
    line_expected = 'CC'
    line_translated = replace_sch(line)
    assert line_expected == line_translated

def test_replace_ch():
    line = 'chch'
    line_expected = '00'
    line_translated = replace_ch(line)
    assert line_expected == line_translated

def test_set_umlaut_sign():
    line = 'ÄÖÜäöü'.lower()
    line_expected = 'MäMöMüMäMöMü'
    line_translated = set_umlaut_sign(line)
    assert line_expected == line_translated

def test_set_double_consonant_sign():
    for c in consonants:
        line = f'{c}{c}{c} a{c} {c} {c}a{c}{c} {c}{c}{c}{c}'
        line_expected = f'{c}1{c} a{c} {c} {c}a{c}1 {c}1{c}1'
        line_translated = set_double_consonant_sign(line)
        assert line_expected == line_translated

def test_set_repeating_consonant_sign():
    for c in consonants:
        line = f'{c}1{c} a{c} {c} {c}a{c}1 {c}1{c}1{c} {c}a{c}'
        line_expected = f'{c}1{c} a{c} {c} {c}a{c}1 {c}1{c}1{c} {c}Qa'
        line_translated = set_repeating_consonant_sign(line)
        assert line_expected == line_translated
        line = f'{c}a'
        line_expected = f'{c}a'
        line_translated = set_repeating_consonant_sign(line)
        assert line_expected == line_translated
        line = f'{c}a{c}a'
        line_expected = f'{c}Qaa'
        line_translated = set_repeating_consonant_sign(line)
        assert line_expected == line_translated
        line = f'{c}a{c}1'
        line_expected = f'{c}a{c}1'
        line_translated = set_repeating_consonant_sign(line)
        assert line_expected == line_translated

def test_set_vowel_first_letter():
    for v in 'aeiou':
        line = f'{v}n {v}{v}n n{v}n {v}'
        line_expected = f'Y{v}n Y{v}{v}n n{v}n Y{v}'
        line_translated = set_vowel_first_letter(line)
        assert line_expected == line_translated

def test_set_double_vowel_sign():
    lines = []
    lines_expected = []
    lines.append('a')
    lines_expected.append('a')
    lines.append('ai')
    lines_expected.append('aBi')
    lines.append('aeiou')
    lines_expected.append('aBeBiBoBu')
    lines.append('fa &a')
    lines_expected.append('fBa &Ba')
    lines.append('f1a &1a')
    lines_expected.append('f1Ba &1Ba')
    lines.append('fQa &Qa')
    lines_expected.append('fQBa &QBa')

    for line, line_expected in zip(lines, lines_expected):
        line_translated = set_double_vowel_sign(line)
        assert line_expected == line_translated

def test_design_g_G():
    line = 'g1gQgagegigogu'
    line_expected = 'G1GQGaGeGiGoGu'
    line_translated = design_g_G(line)
    assert line_expected == line_translated

def test_design_sch():
    line = 'CbChCpCzCr'
    line_expected = 'HbHhHpHzHr'
    line_translated = design_sch(line)
    assert line_expected == line_translated

def test_design_double_consonant_sign():
    line = 'f1&1 G1k1s1 j1n1q1x1y1z1C1 l1r1 t1'
    line_expected = 'f2&2 G3k3s3 j4n4q4x4y4z4C4 l5r5 t6'
    line_translated = design_double_consonant_sign(line)
    assert line_expected == line_translated

def test_design_repeating_consonant_sign():
    line = 'tQ lQrQ hQfQkQmQnQsQxQ0QCQ&Q zQ MöfQ'
    line_expected = 't7 l8r8 h9f9k9m9n9s9x909C9&9 zZ MöfZ'
    line_translated = design_repeating_consonant_sign(line)
    assert line_expected == line_translated

def test_design_umlaut():
    line = 'Mäs3 Möz4 MüGQ Müs9 M s9'
    line_expected = 'Nas3 Noz4 NuGQ Nus9 M s9'
    line_translated = design_umlaut(line)
    assert line_expected == line_translated

def test_design_vowel_a():
    line = 'ca Ham ta na c1a H2a H6a ham7a tQa nZa klang bal5ast l8a glanz kl5a'
    line_expected = 'cA HAm tä nà c1A H2A H6A ham7A tQä nZà klàng bal5ast l8a glànz kl5à'
    line_translated = design_vowel_a(line)
    assert line_expected == line_translated

def test_design_vowel_e():
    line = 'ce Hem te ne c1e H2e H6e hem7e tQe nZe kleng bel5est l8e glenz kl5e'
    line_expected = 'cE HEm tE né c1E H2E H6E hem7E tQE nZé kléng bel5est l8e glénz kl5é'
    line_translated = design_vowel_e(line)
    assert line_expected == line_translated

def test_design_vowel_i():
    line = 'mi ni m1i n1i li l1i'
    line_expected = 'mI n% m1I n1% l% l1%'
    line_translated = design_vowel_i(line)
    assert line_expected == line_translated

def test_design_vowel_o():
    line = 'mo do so m1o d1o s1o'
    line_expected = 'mO dö s+ m1O d1ö s1+'
    line_translated = design_vowel_o(line)
    assert line_expected == line_translated

def test_design_vowel_u():
    line = 'mu du m1u d1u'
    line_expected = 'mU dü m1U d1ü'
    line_translated = design_vowel_u(line)
    assert line_expected == line_translated

def test_design_space():
    line = 're re er'
    line_expected = 're*re er'
    line_translated = design_space(line)
    assert line_expected == line_translated

def test_design_und_and():
    line = 'n&'
    line_expected = 'n&'
    line_translated = design_und_and(line)
    assert line_expected == line_translated
    line = '&N &la &1N &1la'
    line_expected = '#N #la #1N #1la'
    line_translated = design_und_and(line)
    assert line_expected == line_translated