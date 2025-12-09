## Exercice - BeautifulSoup basique

# **Objectif** : Extraire des données avec BeautifulSoup

# **Site** : http://quotes.toscrape.com
import requests
from bs4 import BeautifulSoup
import json

url = "http://quotes.toscrape.com"
headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}


# **Tâches**
# 1. Récupérer la page d'accueil
response = requests.get(url,headers=headers)


# 2. Parser avec BeautifulSoup
soup = BeautifulSoup(response.text, "lxml")

# 3. Trouver toutes les citations (class="quote")
quote_item = soup.select(".quote")


# 4. Pour chaque citation, extraire :
#    - Le texte de la citation
#    - L'auteur
#    - Les tags
# 5. Afficher les 5 premières citations
# 7. Créer une liste de dictionnaires avec les données
quotes = []
for i,quote in enumerate(quote_item[:5]):
    text = quote.select(".text")[0].get_text()      
    author = quote.select(".author")[0].get_text()   
    tags_block = quote.select(".tags")[0]
    tags_list = [tag.get_text() for tag in tags_block.select(".tag")]
    
    
    print(f"--- Citation {i + 1} ---")
    print(f"TEXTE : {text}")
    print(f"AUTEUR: {author}")
    print(f"TAGS  : {', '.join(tags_list)}")

    data = {
        'TEXTE': text,
        'AUTEUR': author,
        'TAGS': tags_list,
    } 
    quotes.append(data)

# 6. Compter le nombre total de citations sur la page
total_text = len(quote_item)
print(f"Nombre de citations sur la page : {total_text}")


# 8. **Bonus** : Sauvegarder dans un fichier JSON
JSON_FILENAME = "quotes_data.json"

try:
    with open(JSON_FILENAME, 'w', encoding='utf-8') as f:
        json.dump(quotes, f, ensure_ascii=False, indent=4) 
    print(f"Données sauvegardées avec succès dans {JSON_FILENAME} (Total: {len(quotes)} enregistrements).")
except Exception as e:
    print(f"\n❌ Erreur lors de la sauvegarde JSON: {e}")
 