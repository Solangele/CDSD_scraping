## TP 1 - Scraper basique

# **Objectif** : Créer un scraper simple avec Requests

# **Site** : http://quotes.toscrape.com
import requests
from requests.exceptions import RequestException, Timeout, ConnectionError
import pandas as pd
import time
import os


headers = {
    'User-Agent': 'My Scraper 1.0',
}

# **Mission**
# 1. Créer une fonction `fetch_page(url)` avec gestion d'erreurs
def fetch_page(url, timeout=1):
    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=timeout
        )
        response.raise_for_status()
        return response.text

    except Timeout:
        print(f"Timeout pour {url}")
        return None

    except ConnectionError:
        print(f"Erreur de connexion pour {url}")
        return None

    except requests.exceptions.HTTPError:
        print(f"Erreur HTTP {response.status_code}: {url}")
        return None

    except RequestException as e:
        print(f"Erreur générale: {e}")
        return None
    
(fetch_page)

def save_html_to_file(html_content, filename):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"Sauvegardé dans: {filename}")
        
    except Exception as e:
        print(f"Erreur lors de la sauvegarde du fichier {filename}: {e}")
# 2. Scraper les 3 premières pages du site
# 3. Pour chaque page, extraire le HTML brut
# 4. Compter le nombre de caractères de chaque page
# 5. Sauvegarder chaque page dans un fichier HTML
if __name__ == "__main__":
    OUTPUT_DIR = "html_pages"
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    url1 = "http://quotes.toscrape.com"
    url2 = f"{url1}/page/2/"
    url3 = f"{url1}/page/3/"

    print("=== Affichage page 1 ===")
    html1 = fetch_page(url1)
    if html1:
        print("La première page contient :", len(html1), "caractères.")
        save_html_to_file(html1, os.path.join(OUTPUT_DIR, "page_1.html"))

    print("=== Affichage page 2 ===")
    html2 = fetch_page(url2)
    if html2:
        print("La deuxième page contient :", len(html2), "caractères.")
        save_html_to_file(html2, os.path.join(OUTPUT_DIR, "page_2.html"))

    print("=== Affichage page 3 ===")
    html3 = fetch_page(url3)
    if html3:
        print("La deuxième page contient :", len(html3), "caractères.")
        save_html_to_file(html3, os.path.join(OUTPUT_DIR, "page_3.html"))


# 6. Créer un rapport CSV avec :
#    - URL de la page
#    - Statut HTTP
#    - Taille en octets
#    - Temps de réponse
session = requests.Session()
url = "http://quotes.toscrape.com"
response = session.get(url)
HTTP_code = response.status_code
content = response.content
content_length = len(content)
temps_de_reponse = response.elapsed.total_seconds()

data = {
        'URL': [url],
        'Code_HTTP': [HTTP_code],
        'Taille_Contenu_Octets': [content_length],
        'Temps_Reponse_s': [temps_de_reponse]
    }
df = pd.DataFrame(data)

output = "requests.csv"

if os.path.exists(output):
    df.to_csv(output, mode='w', header=True, index=False)
    print(f"\nDonnées insérées dans {output}")
else:
    df.to_csv(output, mode='w', header=True, index=False)
    print(f"\nFichier {output} créé et rempli.")

# **Contraintes**
# - Utiliser une session
# - Ajouter un délai de 1 seconde entre requêtes
# - Gérer les erreurs proprement

# **Bonus**
# - Logger les étapes