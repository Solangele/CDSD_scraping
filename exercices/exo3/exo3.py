# ## Exercice - Scraping de livres
# **Objectif** : Scraper un catalogue de livres
# **Site** : http://books.toscrape.com
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd


url = 'http://books.toscrape.com'
headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}


# **Tâches**
# 1. Récupérer la page d'accueil
response = requests.get(url,headers=headers)
soup = BeautifulSoup(response.text, "lxml")

# 2. Pour chaque livre sur la page, extraire :
#    - Titre
#    - Prix (convertir en float)
#    - Note (étoiles → nombre)
#    - Disponibilité (In stock / Out of stock)
#    - URL de l'image
RATING_MAP = {
    'One': 1,
    'Two': 2,
    'Three': 3,
    'Four': 4,
    'Five': 5
}
books_items = soup.select("li.col-xs-6 article.product_pod") 

all_books_data = []

print(f"Trouvé {len(books_items)} livres sur la page.")

for i, book in enumerate(books_items):
    book_data = {}
    try:
        title_element = book.select_one("h3 a")
        book_data['Titre'] = title_element['title'] if title_element else "N/A"   
    except Exception as e:
        book_data['Titre'] = "Erreur Titre"

    try:
        price_text = book.select_one("p.price_color").get_text()
        price = re.search(r"[\d\.]+", price_text)
        if price:
            book_data['Prix'] = float(price.group(0))
        else:
            book_data['Prix'] = None
    except Exception as e:
        book_data['Prix'] = None

    try:
        rating_element = book.select_one("p.star-rating")
        rating_value = 0
        if rating_element:
            rating_classes = rating_element.attrs.get('class', [])
            rating_word_list = [c for c in rating_classes if c in RATING_MAP]
            
            if rating_word_list:
                rating_word = rating_word_list[0]
                rating_value = RATING_MAP[rating_word]
        
        book_data['Note'] = rating_value
        
    except Exception as e:
        book_data['Note'] = None

    try:
        availability_text = book.select_one("p.instock.availability").get_text(strip=True)
        book_data['Disponibilité'] = availability_text.replace('In stock', 'In stock').replace('Out of stock', 'Out of stock').strip()
    except Exception as e:
        book_data['Disponibilité'] = "Erreur Disponibilité"

    try:
        img_element = book.select_one("img.thumbnail")
        book_data['Image_URL_Relative'] = img_element['src'] if img_element else None
        
    except Exception as e:
        book_data['Image_URL_Relative'] = "Erreur URL"

    all_books_data.append(book_data)
    if i < 5:
        print(f"\n--- Livre {i+1} ---")
        print(book_data)

print("\nExtraction terminée.")



# 3. Créer un DataFrame Pandas
df = pd.DataFrame(all_books_data)

# 4. Calculer :
#    - Prix moyen
mean_price = round(df["Prix"].mean(),2)
print(f"La moyenne des prix des livres est de : {mean_price}")

#    - Livre le plus cher
max_price = df["Prix"].max()
print(f"Le livre le plus cher coûte : {max_price}")

#    - Livre le moins cher
min_price = df["Prix"].min()
print(f"Le livre le moins cher coûte : {min_price}")

#    - Répartition par note
df_rating = df.sort_values(["Prix"], ascending=False)
print(df_rating)


# 5. Sauvegarder dans `books.csv`
df.to_csv("output.csv", mode='w', header=True, index=False)

# 6. **Bonus** : Télécharger l'image du livre le plus cher
img_max_price = df_rating.iloc[0]["Image_URL_Relative"] 
print(f"URL de l'image du livre le plus cher : {img_max_price}")