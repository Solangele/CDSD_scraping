# Exercice : Récupérer et analyser une page web

# **Site** : http://quotes.toscrape.com (site d'entraînement)

# **Tâches**
# 1. Récupérer la page d'accueil avec Requests
import requests
from urllib.robotparser import RobotFileParser

url = "http://quotes.toscrape.com"

response = requests.get(url)


# 2. Afficher le code de statut
print("Code HTTP :", response.status_code)

# 3. Afficher les 500 premiers caractères du HTML
html = response.text
print("\n=== Aperçu du HTML (500 premiers caractères) ===")
print(html[:500])

# 4. Vérifier l'encodage de la page
print("\nEncodage détecté :", response.encoding)

# 5. Afficher les headers de la réponse
print("\n=== Headers de la réponse ===")
for key, value in response.headers.items():
    print(f"{key}: {value}")

# 6. Récupérer le robots.txt du site
robots_url = f"{url}/robots.txt"
response = requests.get(robots_url)

# 7. **Bonus** : Utiliser une session pour faire 3 requêtes successives
session = requests.Session()
session.headers.update({'User-Agent': 'My Scraper 1.0'})
response1 = session.post(
    'http://quotes.toscrape.com',
    data={'username': 'user', 'password': 'pass'}
)
session.close()