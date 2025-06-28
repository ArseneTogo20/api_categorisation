import re

def extract_transfer_amount_fee(message):
    amount_patterns = [
        # Patterns pour gros montants (7+ chiffres)
        r'envoyé\s*(\d{1,3}(?:\s\d{3})*)\s*FCFA',
        r'envoyé\s*(\d{1,3}(?:,\d{3})*)\s*FCFA',
        r'envoyé\s*(\d+)\s*FCFA',
        r'Montant:\s*(\d{1,3}(?:,\d{3})*)\s*FCFA',
        r'Montant:\s*(\d{1,3}(?:\s\d{3})*)\s*FCFA',
        r'Montant:\s*(\d+)\s*FCFA',
        r'envoyé\s*(\d+\.?\d*)\s*FCFA',
        # Pattern générique pour capturer n'importe quel montant
        r'(\d{1,3}(?:\s\d{3})*)\s*FCFA.*?envoyé',
        r'(\d{1,3}(?:,\d{3})*)\s*FCFA.*?envoyé',
        r'(\d+)\s*FCFA.*?envoyé'
    ]
    amount = None
    for pattern in amount_patterns:
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            amount_str = match.group(1).replace(' ', '').replace(',', '')
            try:
                amount = float(amount_str)
                break
            except ValueError:
                continue
    
    fees_match = re.search(r'Frais:\s*(\d+)\s*FCFA', message, re.IGNORECASE)
    fees = float(fees_match.group(1)) if fees_match else 0.0
    return {'amount': amount or 0, 'fee': fees or 0}

def extract_facture_amount_fee(message):
    patterns = [
        # Patterns pour gros montants
        r'payé\s*(\d{1,3}(?:\s\d{3})*)\s*FCFA',
        r'payé\s*(\d{1,3}(?:,\d{3})*)\s*FCFA',
        r'payé\s*(\d+)\s*FCFA',
        r'Montant:\s*(\d{1,3}(?:,\d{3})*)\s*FCFA',
        r'Montant:\s*(\d{1,3}(?:\s\d{3})*)\s*FCFA',
        r'Montant:\s*(\d+)\s*FCFA',
        r'Achat de (\d{1,3}(?:\s\d{3})*)\s*FCFA',
        r'Achat de (\d{1,3}(?:,\d{3})*)\s*FCFA',
        r'Achat de (\d+)\s*FCFA',
        r'paiement de (\d+)\s*FCFA',
        r'payé\s*(\d+)\s*F\s*à',
        # Pattern générique
        r'(\d{1,3}(?:\s\d{3})*)\s*FCFA.*?(?:payé|paiement)',
        r'(\d{1,3}(?:,\d{3})*)\s*FCFA.*?(?:payé|paiement)',
        r'(\d+)\s*FCFA.*?(?:payé|paiement)'
    ]
    amount = None
    for pattern in patterns:
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            amount_str = match.group(1).replace(' ', '').replace(',', '')
            try:
                amount = float(amount_str)
                break
            except ValueError:
                continue
    return {'amount': amount or 0, 'fee': 0}

def extract_credit_amount_fee(message):
    amount_patterns = [
        # Patterns pour gros montants
        r'rechargé\s*(\d{1,3}(?:\s\d{3})*)\s*FCFA',
        r'rechargé\s*(\d{1,3}(?:,\d{3})*)\s*FCFA',
        r'rechargé\s*(\d+)\s*FCFA',
        r'recharger\s*(\d+\.?\d*)\s*FCFA',
        r'Montant:\s*(\d{1,3}(?:,\d{3})*)\s*FCFA',
        r'Montant:\s*(\d{1,3}(?:\s\d{3})*)\s*FCFA',
        r'Montant:\s*(\d+)\s*FCFA',
        r'Credit de (\d+)\s*FCFA',
        r'SOS Crédit de (\d+)F',
        # Pattern générique
        r'(\d{1,3}(?:\s\d{3})*)\s*FCFA.*?rechargé',
        r'(\d{1,3}(?:,\d{3})*)\s*FCFA.*?rechargé',
        r'(\d+)\s*FCFA.*?rechargé'
    ]
    amount = None
    for pattern in amount_patterns:
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            amount_str = match.group(1).replace(' ', '').replace(',', '')
            try:
                amount = float(amount_str)
                break
            except ValueError:
                continue
    return {'amount': amount or 0, 'fee': 0}

def extract_forfait_amount_fee(message):
    amount_patterns = [
        r'(?:NET|PASS|Lema|Ovo|F)(\d{2,4})\b',
        r'F\s?(\d{2,4})\s?[MV]',
        r'\((\d{1,3}(?:\s\d{3})*)\s*FCFA\)',
        r'\((\d{1,3}(?:,\d{3})*)\s*FCFA\)',
        r'\((\d+)\s*FCFA\)',
        r'Montant:\s*(\d{1,3}(?:,\d{3})*)\s*FCFA',
        r'Montant:\s*(\d{1,3}(?:\s\d{3})*)\s*FCFA',
        r'Montant:\s*(\d+)\s*FCFA',
        r'forfait de (\d+,\d+)Go'
    ]
    amount = None
    for pattern in amount_patterns:
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            amount = match.group(1).replace(',', '.')
            try:
                amount = int(float(amount)) if float(amount).is_integer() else float(amount)
            except ValueError:
                continue
            break
    fees_match = re.search(r'Frais:\s*(\d+)\s*FCFA', message, re.IGNORECASE)
    fees = float(fees_match.group(1)) if fees_match else 0.0
    return {'amount': amount or 0, 'fee': fees or 0}

def extract_retrait_amount_fee(message):
    amount_patterns = [
        # Patterns pour gros montants
        r'retire\s*(\d{1,3}(?:\s\d{3})*)\s*FCFA',
        r'retire\s*(\d{1,3}(?:,\d{3})*)\s*FCFA',
        r'retire\s*(\d+)\s*FCFA',
        r'vous\s+avez\s+retir[ée]?\s*(\d{1,3}(?:\s\d{3})*)\s*FCFA',
        r'vous\s+avez\s+retir[ée]?\s*(\d{1,3}(?:,\d{3})*)\s*FCFA',
        r'vous\s+avez\s+retir[ée]?\s*(\d+)\s*FCFA',
        r'retir[ée]?\s*(\d{1,3}(?:\s\d{3})*)\s*FCFA',
        r'retir[ée]?\s*(\d{1,3}(?:,\d{3})*)\s*FCFA',
        r'retir[ée]?\s*(\d+)\s*FCFA',
        r'Montant:\s*(\d{1,3}(?:,\d{3})*)\s*FCFA',
        r'Montant:\s*(\d{1,3}(?:\s\d{3})*)\s*FCFA',
        r'Montant:\s*(\d+)\s*FCFA',
        r'Retrait validé.*?(\d{1,3}(?:,\d{3})*)\s*FCFA',
        r'Retrait validé.*?(\d{1,3}(?:\s\d{3})*)\s*FCFA',
        r'Retrait validé.*?(\d+)\s*FCFA',
        r'(\d{1,3}(?:\s\d{3})*)\s*FCFA.*?retir[ée]?',
        r'(\d{1,3}(?:,\d{3})*)\s*FCFA.*?retir[ée]?',
        r'(\d+)\s*FCFA.*?retir[ée]?'
    ]
    amount = None
    for pattern in amount_patterns:
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            amount_str = match.group(1).replace(' ', '').replace(',', '')
            try:
                amount = float(amount_str)
                break
            except ValueError:
                continue
    
    fees_patterns = [
        r'Frais:\s*(\d{1,3}(?:\s\d{3})*)\s*FCFA',
        r'Frais:\s*(\d{1,3}(?:,\d{3})*)\s*FCFA',
        r'Frais:\s*(\d+)\s*FCFA',
        r'Frais HT:\s*(\d{1,3}(?:,\d{3})*)\s*FCFA',
        r'Frais HT:\s*(\d{1,3}(?:\s\d{3})*)\s*FCFA',
        r'Frais HT:\s*(\d+)\s*FCFA',
        r'frais.*?(\d+)\s*FCFA'
    ]
    fees = None
    for pattern in fees_patterns:
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            fees_str = match.group(1).replace(' ', '').replace(',', '')
            try:
                fees = float(fees_str)
                break
            except ValueError:
                continue
    return {'amount': amount or 0, 'fee': fees or 0}

EXTRACTION_FUNCTIONS = {
    'CREDIT': extract_credit_amount_fee,
    'FACTURE': extract_facture_amount_fee,
    'TRANSFERT_RECU': extract_transfer_amount_fee,
    'TRANSFERT_ENVOYE': extract_transfer_amount_fee,
    'FORFAIT': extract_forfait_amount_fee,
    'RETRAIT': extract_retrait_amount_fee,
}

def extract_amount_and_fee(message, category):
    func = EXTRACTION_FUNCTIONS.get(category.upper())
    if func:
        return func(message)
    return {'amount': 0, 'fee': 0} 