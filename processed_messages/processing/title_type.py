import re

def extract_credit_type_and_title(message):
    message_lower = message.lower()
    mots_cles_togocom = ['mixx', 'tmoney', 'mixx by yas', 'tu viens de recharger','tu viens','viens' ,'successfully', 'successfully recharged', 'new balence']
    mots_cles_moov = ['credit de communication', 'beneficiaire','communication', 'emoov', 'achat de credit','achat de credit de communication']
    title = "credit"
    if any(mot in message_lower for mot in mots_cles_togocom):
        credit_type = "togocom"
    elif any(mot in message_lower for mot in mots_cles_moov):
        credit_type = "moov"
    else:
        credit_type = "moov"
    return credit_type, title

def extract_facture_type_and_title(message):
    message_lower = message.lower()
    mots_cles_togocom = ['tmoney', 'yas', 'mixx', 'mixx by yas']
    title = "facture"
    if any(mot in message_lower for mot in mots_cles_togocom):
        facture_type = "togocom"
    elif "flooz" in message_lower:
        facture_type = "moov"
    else:
        facture_type = "moov"
    return facture_type, title

def extract_numero(message):
    match = re.search(r'\((\d{8,12})\)', message)
    if match:
        return match.group(1)
    match = re.search(r'au\s+(\d{8,12})', message)
    if match:
        return match.group(1)
    match = re.search(r'(beneficiaire|expediteur)\s*:\s*(\d{8,12})', message, re.IGNORECASE)
    if match:
        return match.group(2)
    return None

def detect_transfer_type(numero, message):
    if not numero:
        return "inconnu"
    message_lower = message.lower()
    numero_str = str(numero)
    prefixes_togocom = {'90', '91', '92', '93', '70', '71', '72'}
    mots_cles_togocom = ['tmoney', 'mixx by yas', 'nouveau solde mixx by yas', 'vous avez envoyé']
    prefixes_moov = {'99', '98', '97', '96', '79', '78', '77', '76'}
    mots_cles_moov = ['transfert reussi', 'transfert recu', 'flooz', 'nouveau solde flooz']
    if (len(numero_str) in [8,9,10,11] and numero_str[:2] in prefixes_togocom) or any(mot in message_lower for mot in mots_cles_togocom):
        return "togocom"
    if numero_str.startswith('228') and len(numero_str) >= 5:
        prefix = numero_str[3:5]
        if prefix in prefixes_moov or any(mot in message_lower for mot in mots_cles_moov):
            return "moov"
    return "inconnu"

def extract_transfert_type_and_title(message):
    numero = extract_numero(message)
    transfert_type = detect_transfer_type(numero, message)
    if transfert_type == "togocom":
        title = "transfert togocom à togocom"
    elif transfert_type == "moov":
        title = "transfert de moov à moov"
    else:
        title = "inconnu"
    return transfert_type, title

def extract_forfait_type_and_title(message):
    titres_togocom = [
        "f150 m", "f150v", "f 250 m", "f250 m", "f450 m", "f450 v", "f600 m", "f600v",
        "f900 m", "f900v", "f1400m", "f1400v", "f2500m", "f2500v", "f5000m", "f5000v",
        "f7000m", "f7000v", "f9500m", "f9500v", "lema", "ovo", "relax", "net","souscrit", 
        "kozoh", "Tmoney","yas","mixx", "mixx by yas","Nouveau Solde","recharge"
    ]
    titres_moov = [
        "izi free", "izi cool", "izikif", "izi relax", "izi wik", "izi moon",
        "izi small1", "izi small2", "izi medium1", "izi medium2", "izi large",
        "izi", "izimoon", "flooz", "vous venez", "vous venez de souscrire", "souscrire"
    ]
    message_lower = message.lower()
    for mot in titres_togocom:
        if mot in message_lower:
            return "togocom", mot
    for mot in titres_moov:
        if mot in message_lower:
            return "moov", mot
    return "inconnu", "forfait"

def extract_retrait_type_and_title(message):
    message_lower = message.lower()
    mots_cles_moov = ['retrait valide', 'flooz', 'frais ht', 'taf']
    mots_cles_togocom = ['vous avez retire', 'tmoney', 'yas', 'mixx', 'mixx by yas', 'tmoney devient mixx']
    title = "retrait"
    
    if any(mot in message_lower for mot in mots_cles_moov):
        retrait_type = "moov"
        if "flooz" in message_lower:
            title = "Retrait Flooz"
    elif any(mot in message_lower for mot in mots_cles_togocom):
        retrait_type = "togocom"
        if "mixx by yas" in message_lower or "tmoney devient mixx" in message_lower:
            title = "Retrait Mixx By Yas"
        elif "tmoney" in message_lower:
            title = "Retrait TMoney"
        else:
            title = "Retrait Togocom"
    else:
        retrait_type = "inconnu"
        title = "Retrait"
    
    return retrait_type, title

def extract_type_and_title(message, category):
    if category == "CREDIT":
        return extract_credit_type_and_title(message)
    elif category == "FACTURE":
        return extract_facture_type_and_title(message)
    elif category in ("TRANSFERT_RECU", "TRANSFERT_ENVOYE"):
        return extract_transfert_type_and_title(message)
    elif category == "FORFAIT":
        return extract_forfait_type_and_title(message)
    elif category == "RETRAIT":
        return extract_retrait_type_and_title(message)
    else:
        return "inconnu", "inconnu" 