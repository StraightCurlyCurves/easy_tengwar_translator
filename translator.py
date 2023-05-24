#-*- coding: UTF-8 -*-
import re

german_and = False
consonants = 'bcdfghjklmnpqrstvwxyz&0CH$'

def replace_special_signs(line: str):
    special_signs_mapping = {ord('’'): "'", ord('„'): '@', ord('“'): '"', ord('ß'): '$', ord('–'): '-'}
    return line.translate(special_signs_mapping)

def replace_und_and(line: str, german_and=german_and):
    if german_and:
        return line.replace('und', '&')
    else:
        return line.replace('and', '&')
    
def replace_sch(line: str):
    return line.replace('sch', 'C')

def replace_ch(line: str):
    return line.replace('ch', '0')

def set_umlaut_sign(line: str):
    mapping = {ord('ä'): 'Mä', ord('ö'): 'Mö', ord('ü'): 'Mü'}
    return line.translate(mapping)

def set_double_consonant_sign(line: str):
    for c in consonants:
        line = line.replace(c+c, c+'1')
    return line

def set_repeating_consonant_sign(line: str):
    for c in consonants:
        if c =='$':
            pattern = f"\\{c}(?=[^1 ]\\{c})"
        else:
            pattern = f"{c}(?=[^1 ]{c})"
        # pattern = f"(?=({c}[^1 ]{c}))"
        x = re.finditer(pattern, line) # search for x*x where x is a consonant and * any letter but 1 or space     
        for match in x:
            i = match.start()
            line_list = list(line)
            if len(line_list[i:-1]) >= 3: # ensure index in bounds
                if line_list[i+3] == '1': # if there is a 1 like in 'foff' -- > fof1 don't repeat
                    continue
            line_list[i+2] = line_list[i+1]
            line_list[i+1] = 'Q'
            line = ''.join(line_list)
    return line

def set_vowel_first_letter(line: str):
    pattern = r"\b([aeiou])"
    replacement = r"Y\1"
    line = re.sub(pattern, replacement, line)
    return line

def set_double_vowel_sign(line: str):
    # aeiou --> aBeBiBoBu
    pattern = r"([aeiou])(?=[aeiou])"
    replacement = r"\1B"
    line = re.sub(pattern, replacement, line)
    # fa, &a --> fBa, &Ba
    pattern = r"(?<=[f&])([aeiou])"
    replacement = r"B\1"
    line = re.sub(pattern, replacement, line)
    # f1a, &1a --> f1Ba, &1Ba
    pattern = r"(?<=f1|&1)([aeiou])"
    replacement = r"B\1"
    line = re.sub(pattern, replacement, line)
    # fQa, &Qa --> fQBa, &QBa
    pattern = r"(?<=fQ|&Q)([aeiou])"
    replacement = r"B\1"
    line = re.sub(pattern, replacement, line)
    return line

def design_g_G(line: str):
    pattern = r"g(?=[1Qaeiou])"
    replacement = r"G"
    line = re.sub(pattern, replacement, line)
    return line

def design_sch(line: str):
    pattern = r"C(?=[bhpzr])"
    replacement = r"H"
    line = re.sub(pattern, replacement, line)
    return line

def design_double_consonant_sign(line: str):
    pattern = r"(?<=[f&])1"
    replacement = r"2"
    line = re.sub(pattern, replacement, line)
    pattern = r"(?<=[Gks])1"
    replacement = r"3"
    line = re.sub(pattern, replacement, line)
    pattern = r"(?<=[jnqxyzC])1"
    replacement = r"4"
    line = re.sub(pattern, replacement, line)
    pattern = r"(?<=[lr])1"
    replacement = r"5"
    line = re.sub(pattern, replacement, line)
    pattern = r"(?<=t)1"
    replacement = r"6"
    line = re.sub(pattern, replacement, line)
    return line

def design_repeating_consonant_sign(line: str):
    pattern = r"(?<=t)Q"
    replacement = r"7"
    line = re.sub(pattern, replacement, line)
    pattern = r"(?<=[lr])Q"
    replacement = r"8"
    line = re.sub(pattern, replacement, line)
    pattern = r"(?<=[hfkmnsx0C&])Q"
    replacement = r"9"
    line = re.sub(pattern, replacement, line)
    pattern = r"(?<=[z])Q"
    replacement = r"Z"
    line = re.sub(pattern, replacement, line)
    pattern = r"(?<=M.{1}f)9"
    replacement = r"Z"
    line = re.sub(pattern, replacement, line)
    return line

def design_umlaut(line: str):
    for vu, v in zip('äöü', 'aou'):
        pattern = f"M({vu})(?=s3|z4|GQ|s9)"
        replacement = f"N{v}"
        line = re.sub(pattern, replacement, line)
    return line

def design_vowel_a(line: str):
    # vowel follows directly 
    pattern = r"(?<=[0cdmpH])a"
    replacement = r"A"
    line = re.sub(pattern, replacement, line)
    pattern = r"(?<=[jtvw])a"
    replacement = r"ä"
    line = re.sub(pattern, replacement, line)
    pattern = r"(?<=[nsxyz])a"
    replacement = r"à"
    line = re.sub(pattern, replacement, line)
    # vowel follows after double/repeating consonant sign
    pattern = r"(?<=[0cdmpH][123456789QZ])a"
    replacement = r"A"
    line = re.sub(pattern, replacement, line)
    pattern = r"(?<=[jtvw][123456789QZ])a"
    replacement = r"ä"
    line = re.sub(pattern, replacement, line)
    pattern = r"(?<=[nsxyz][123456789QZ])a"
    replacement = r"à"
    line = re.sub(pattern, replacement, line)
    # special case l
    pattern = r"(?<=[wdgGjkvB&]l)a"
    replacement = r"à"
    line = re.sub(pattern, replacement, line)
    pattern = r"(?<=[wdgGjkvB&]l[123456789QZ])a"
    replacement = r"à"
    line = re.sub(pattern, replacement, line)
    return line

def design_vowel_e(line: str):
    # vowel follows directly 
    pattern = r"(?<=[0cdjmptvwH])e"
    replacement = r"E"
    line = re.sub(pattern, replacement, line)
    pattern = r"(?<=[nsxyz])e"
    replacement = r"é"
    line = re.sub(pattern, replacement, line)
    # vowel follows after double/repeating consonant sign
    pattern = r"(?<=[0cdjmptvwH][123456789QZ])e"
    replacement = r"E"
    line = re.sub(pattern, replacement, line)
    pattern = r"(?<=[nsxyz][123456789QZ])e"
    replacement = r"é"
    line = re.sub(pattern, replacement, line)
    # special case l
    pattern = r"(?<=[wdgGjkvB&]l)e"
    replacement = r"é"
    line = re.sub(pattern, replacement, line)
    pattern = r"(?<=[wdgGjkvB&]l[123456789QZ])e"
    replacement = r"é"
    line = re.sub(pattern, replacement, line)
    return line

def design_vowel_i(line: str):
    # vowel follows directly 
    pattern = r"(?<=[0Hdmptvw])i"
    replacement = r"I"
    line = re.sub(pattern, replacement, line)
    pattern = r"(?<=[nsxyz])i"
    replacement = r"%"
    line = re.sub(pattern, replacement, line)
    # vowel follows after double/repeating consonant sign
    pattern = r"(?<=[0Hdmptvw][123456789QZ])i"
    replacement = r"I"
    line = re.sub(pattern, replacement, line)
    pattern = r"(?<=[nsxyz][123456789QZ])i"
    replacement = r"%"
    line = re.sub(pattern, replacement, line)
    # special case l
    pattern = r"(?<=l)i"
    replacement = r"%"
    line = re.sub(pattern, replacement, line)
    pattern = r"(?<=l[123456789QZ])i"
    replacement = r"%"
    line = re.sub(pattern, replacement, line)
    return line

def design_vowel_o(line: str):
    # vowel follows directly 
    pattern = r"(?<=[bcGhmH])o"
    replacement = r"O"
    line = re.sub(pattern, replacement, line)
    pattern = r"(?<=[0djptvw])o"
    replacement = r"ö"
    line = re.sub(pattern, replacement, line)
    pattern = r"(?<=[sn])o"
    replacement = r"+"
    line = re.sub(pattern, replacement, line)
    # vowel follows after double/repeating consonant sign
    pattern = r"(?<=[bcGhmH][123456789QZ])o"
    replacement = r"O"
    line = re.sub(pattern, replacement, line)
    pattern = r"(?<=[0djptvw][123456789QZ])o"
    replacement = r"ö"
    line = re.sub(pattern, replacement, line)
    pattern = r"(?<=[sn][123456789QZ])o"
    replacement = r"+"
    line = re.sub(pattern, replacement, line)
    return line

def design_vowel_u(line: str):
    # vowel follows directly 
    pattern = r"(?<=[bcGhkmH])u"
    replacement = r"U"
    line = re.sub(pattern, replacement, line)
    pattern = r"(?<=[0djptvw])u"
    replacement = r"ü"
    line = re.sub(pattern, replacement, line)
    # vowel follows after double/repeating consonant sign
    pattern = r"(?<=[bcGhkmH][123456789QZ])u"
    replacement = r"U"
    line = re.sub(pattern, replacement, line)
    pattern = r"(?<=[0djptvw][123456789QZ])u"
    replacement = r"ü"
    line = re.sub(pattern, replacement, line)
    return line

def design_space(line: str):
    pattern = r" (?=r)"
    replacement = r"*"
    line = re.sub(pattern, replacement, line)
    return line

def design_und_and(line: str):
    pattern = r"&(?=[NBg])"
    replacement = r"#"
    line = re.sub(pattern, replacement, line)
    pattern = r"&(?=[lr][aeiou])"
    replacement = r"#"
    line = re.sub(pattern, replacement, line)
    pattern = r"&(?=[123456789QZ][NBg])"
    replacement = r"#"
    line = re.sub(pattern, replacement, line)
    pattern = r"&(?=[123456789QZ][lr][aeiou])"
    replacement = r"#"
    line = re.sub(pattern, replacement, line)
    return line

def translate(line: str, german_and=False):
    line = line.lower()
    line = replace_special_signs(line)
    line = replace_und_and(line, german_and)
    line = replace_sch(line)
    line = replace_ch(line)
    line = set_umlaut_sign(line)
    line = set_double_consonant_sign(line)
    line = set_repeating_consonant_sign(line)
    line = set_double_consonant_sign(line) # set_repeating_consonant_sign might make ltlt to lQtt, so tt becomes double consonant
    line = set_vowel_first_letter(line)
    line = set_double_vowel_sign(line)
    line = design_g_G(line)
    line = design_sch(line)
    line = design_double_consonant_sign(line)
    line = design_repeating_consonant_sign(line)
    line = design_umlaut(line)
    line = design_vowel_a(line)
    line = design_vowel_e(line)
    line = design_vowel_i(line)
    line = design_vowel_o(line)
    line = design_vowel_u(line)
    line = design_space(line)
    line = design_und_and(line)
    return line