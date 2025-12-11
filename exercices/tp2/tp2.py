# ## TP 2 - Scraper multi-pages
# **Objectif** : Scraper plusieurs pages avec pagination
# **Site** : http://quotes.toscrape.com
# **Mission**
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
from urllib.parse import urljoin 

url = 'http://quotes.toscrape.com'
headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}
response = requests.get(url , headers=headers)
soup = BeautifulSoup(response.text,'lxml')
quotes_elements = soup.select("div.quote")


# Créer un scraper complet qui :
# 1. Détecte automatiquement le nombre de pages
# 2. Scrape toutes les pages (jusqu'à 10 max)

current_page_url = url
page_count = 0
MAX_PAGES = 10
quotes_data = []

while current_page_url and page_count < MAX_PAGES:
    print(f"Scraping de la page {page_count + 1} : {current_page_url}")
    
    try:
        response = requests.get(current_page_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")
        page_count += 1
        
    except requests.exceptions.RequestException as e:
        print(f"Erreur de requête sur {current_page_url}: {e}")
        break 

    quotes = soup.select(".quote")
    next_button = soup.select_one("li.next a") 
        
    if next_button:
        next_url = next_button['href']
        current_page_url = urljoin(url, next_url)
        
    else:
        print("Fin de la pagination : Lien 'Next' non trouvé.")
        current_page_url = None

    # 3. Pour chaque citation, extrait :
    #    - Texte
    #    - Auteur
    #    - Tags
    #    - URL de l'auteur
    quotes_data = []

    for quote in quotes_elements:
        text = quote.find("span",class_="text").text
        author = quote.find("small",class_="author").text
        tags = [tag.text for tag in quote.find_all("a",class_="tag")]
        author_link = quote.find("a")
        url_author = author_link.get('href') if author_link else None

        quotes_data.append({
            'text' : text,
            'author' : author,
            'tags' : tags,
            "url de l'auteur" : url_author
        })
print(f"Nombre TOTAL de pages parcourues : {page_count}")
print(f"Nombre total de citations collectées : {len(quotes_data)}")


# 4. Crée un fichier Excel avec 3 feuilles :
#    - "Citations" : Toutes les citations
#    - "Auteurs" : Liste unique des auteurs avec nb de citations
#    - "Tags" : Liste des tags avec fréquence
df_citations = pd.DataFrame(quotes_data)

df_auteurs = df_citations['author'].value_counts().reset_index()
df_auteurs.columns = ['Auteur', 'Nombre de citations']
df_auteurs = df_auteurs.sort_values(by='Nombre de citations', ascending=False)

df_exploded_tags = df_citations.explode('tags')

df_tags = df_exploded_tags['tags'].value_counts().reset_index()
df_tags.columns = ['Tag', 'Fréquence']
df_tags = df_tags.sort_values(by='Fréquence', ascending=False)

FILE = 'quotes_analyse.xlsx'

try:
    with pd.ExcelWriter(FILE, engine='xlsxwriter') as writer:
        df_citations.to_excel(writer, sheet_name='Citations', index=False)
        df_auteurs.to_excel(writer, sheet_name='Auteurs', index=False)
        df_tags.to_excel(writer, sheet_name='Tags', index=False)   
    print(f"\n✅ Fichier Excel '{FILE}' créé avec succès (3 feuilles).")
except Exception as e:
    print(f"\n❌ Erreur lors de la sauvegarde Excel : {e}")

# 5. Génère des statistiques :
#    - Top 5 auteurs les plus cités
#    - Top 10 tags les plus utilisés
#    - Longueur moyenne des citations
def autors_top5 ():
    top5 = df_auteurs.head(5)
    print("--- Top 5 des auteurs les plus cités ---")
    print(top5.to_string(index=False)) 
    return top5

def tags_top10 ():
    top10 = df_tags.head(10)
    print("--- Top 10 des tags les plus utilisés ---")
    print(top10.to_string(index=False))
    return top10

def mean_len_citation () :
    df_citations['Longueur'] = df_citations['text'].str.len()
    mean = round(df_citations['Longueur'].mean(),2)
    print("--- Longueur moyenne d'une citation ---")
    print(mean)
    return mean

autors_top5()
tags_top10()
mean_len_citation()

# **Contraintes**
# - Code modulaire (fonctions)
# - Gestion d'erreurs complète
# - Logging
# - Respect du délai entre requêtes