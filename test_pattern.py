import re

# Test du pattern RETRAIT
pattern = re.compile(r'(?xi)(retrait|retir[ée]|vous\s+avez\s+retir[ée]?|retrait\s+valid[ée]|retrait\s+d\'argent|retrait\s+espèces)', re.VERBOSE)

message = "TMoney devient Mixx By Yas. Vous avez retire 1 500 FCFA auprès de l'agent NANA 20 (18112), le 03-03-25 08:01. Frais: 100 FCFA. Nouveau solde: 109 FCFA . Ref: 10522621268."

print("Message:", message)
print("Message en minuscules:", message.lower())
print("Pattern:", pattern.pattern)
print("Match trouvé:", bool(pattern.search(message.lower())))
print("Matches:", pattern.findall(message.lower()))

# Test avec d'autres patterns
patterns = {
    'retrait': r'retrait',
    'retire': r'retir[ée]',
    'vous avez retire': r'vous\s+avez\s+retir[ée]?'
}

for name, pat in patterns.items():
    p = re.compile(pat, re.IGNORECASE)
    print(f"{name}: {bool(p.search(message))}")

print("\n" + "="*50)
print("TEST EXTRACTION MONTANTS ET FRAIS")
print("="*50)

# Test extraction montant
amount_patterns = [
    r'retire\s*(\d{1,3}(?:\s\d{3})*)\s*FCFA',
    r'vous\s+avez\s+retir[ée]?\s*(\d{1,3}(?:\s\d{3})*)\s*FCFA',
    r'retir[ée]?\s*(\d{1,3}(?:\s\d{3})*)\s*FCFA',
    r'(\d{1,3}(?:\s\d{3})*)\s*FCFA.*?retir[ée]?'
]

print("Test extraction montant:")
for i, pattern in enumerate(amount_patterns):
    p = re.compile(pattern, re.IGNORECASE)
    match = p.search(message)
    if match:
        amount = float(match.group(1).replace(' ', '').replace(',', ''))
        print(f"  Pattern {i+1}: {amount} FCFA")
    else:
        print(f"  Pattern {i+1}: Aucun match")

# Test extraction frais
fees_patterns = [
    r'Frais:\s*(\d{1,3}(?:\s\d{3})*)\s*FCFA',
    r'Frais HT:\s*(\d{1,3}(?:,\d{3})*)\s*FCFA',
    r'Frais:\s*(\d+)\s*FCFA',
    r'frais.*?(\d+)\s*FCFA'
]

print("\nTest extraction frais:")
for i, pattern in enumerate(fees_patterns):
    p = re.compile(pattern, re.IGNORECASE)
    match = p.search(message)
    if match:
        fees = float(match.group(1).replace(' ', '').replace(',', ''))
        print(f"  Pattern {i+1}: {fees} FCFA")
    else:
        print(f"  Pattern {i+1}: Aucun match") 