import re

CATEGORIES = {
    'FORFAIT': re.compile(r'''(?xi)(forfait|sousc(?:ription|rit)|bonus\s+appel|(?:data|internet)\b|PASS_|\b(?:NET|PASS|Lema|OVO|XTRA|iZiMoon|Wik\s+Appel)\b|(?:NET[\w]*Nuit|NET\s*[-_]?\s*Nuit)|\bF\d+Voix\b|offre\s+(?:promo|spéciale|exceptionnelle)|abonnement|valide\s+jusqu['au\s]|\d+[\.,]?\d*\s*(?:Go|Mo|jrs?|nuit)(?!\s*FCFA))''', re.VERBOSE),
    'FACTURE': re.compile(r'''(?xi)(facture|paiement\s+d[ûu]e?\b|montant\s+(?:du|à\s+payer)|(?:doit|à)\s+payer|référence\s+(?:facture|paiement)|échéance\s*\:|pay[ée](?:\s+le)?|facture.*?(?:LAFIA|CEET|CanalBox)|Cash\s*power|KWh|compteur\s+(?:électrique|d'énergie))''', re.VERBOSE),
    'RETRAIT': re.compile(r'''(?xi)(retrait|retir[ée]|vous\s+avez\s+retir[ée]?|retrait\s+valid[ée]|retrait\s+d'argent|retrait\s+espèces)''', re.VERBOSE),
    'TRANSFERT_ENVOYE': re.compile(r'''(?xi)((?:envoy[ée]|transfert)\b.*?\d+[\s,.]*\d*\s*FCFA.*?(?:au\s+\d+|Beneficiaire\s*:\s*\d+)|transfert\s+(?:effectué|réussi|de)\b.*?\d+[\s,.]*\d*\s*FCFA.*?(?:vers|à|pour)\s+\d+|vous\s+avez\s+envoy[ée])(?!.*re[çc]u)''', re.VERBOSE),
    'CREDIT': re.compile(r'''(?xi)(recharg[ée]?(?!.*(?:forfait|data|internet))|achat\s+de\s+cr[ée]dit|cr[ée]dit\s+(?:valable|de\s+communication|achet[ée])|successfully\s+recharged|\brecharger\b(?!.*(?:forfait|data|internet))|\bcr[ée]dit\b(?!.*(?:data|forfait))|nouveau\s+cr[ée]dit.*?\b(?:FCFA|F\.?)\b|montant\s+du\s+cr[ée]dit)''', re.VERBOSE),
    'TRANSFERT_RECU': re.compile(r'''(?xi)(transfert\s+re[çc]u|transfert\s+en\s+ligne\s+r[ée]ussi.*?de\s+\d+|exp[ée]diteur.*?\d+.*?FCFA|vous\s+avez\s+re[çc]u.*?FCFA|transfert\s+(?:r[ée]ussi|de)\b.*?\d+[\s,.]*\d*\s*FCFA.*?de\s+\d+)''', re.VERBOSE)
}

def categoriser_message(message: str) -> str:
    if not isinstance(message, str) or not message.strip():
        return 'AUTRE'
    message = re.sub(r'\s+', ' ', message.strip(), flags=re.UNICODE)
    message = message.lower()
    category_scores = {category: 0 for category in CATEGORIES}
    for category, pattern in CATEGORIES.items():
        matches = pattern.findall(message)
        if matches:
            category_scores[category] = len(matches)
    best_category = max(category_scores.items(), key=lambda x: x[1])
    return best_category[0] if best_category[1] > 0 else 'AUTRE' 