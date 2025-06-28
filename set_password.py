#!/usr/bin/env python
import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projet_categorisation.settings')
django.setup()

from users.models import CustomUser

# Définir le mot de passe pour le superuser
try:
    user = CustomUser.objects.get(phoneNumber='+22890123456')
    user.set_password('admin123')
    user.save()
    print("✅ Mot de passe défini avec succès pour l'utilisateur admin")
    print(f"📱 Numéro: {user.phoneNumber}")
    print(f"🔑 Mot de passe: admin123")
except CustomUser.DoesNotExist:
    print("❌ Utilisateur non trouvé")
except Exception as e:
    print(f"❌ Erreur: {e}") 