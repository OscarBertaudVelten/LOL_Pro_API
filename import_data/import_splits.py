import requests
import json
import re
import time  # To introduce delay between retries

def fetch_html(url):
    """Récupère le contenu HTML d'une URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Erreur lors de la récupération de {url}: {e}")
        return None

def clean_json(response_text):
    """Supprime les éventuels backticks et le mot 'json' au début."""
    cleaned_text = re.sub(r"^```json\s*", "", response_text, flags=re.MULTILINE)  # Supprime ```json au début
    cleaned_text = re.sub(r"```$", "", cleaned_text, flags=re.MULTILINE)  # Supprime ``` à la fin
    return cleaned_text.strip()

def send_to_openrouter(api_key, model, prompt, html_content):
    """Envoie le contenu HTML à OpenRouter pour analyse."""
    api_url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant. Respond ONLY with valid JSON, without markdown formatting or ```."},
            {"role": "user", "content": f"{prompt}\n\n{html_content}"}
        ]
    }
    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Erreur de communication avec l'API OpenRouter: {e}")
        return None

def process_league(league, url, api_key, model, prompt):
    """Traitement d'une ligue avec tentative de retries."""
    retry_count = 0
    max_retries = 3  # Nombre maximum de tentatives
    delay_between_retries = 1  # Délai entre chaque tentative en secondes
    
    while retry_count < max_retries:
        print(f"Tentative {retry_count + 1} pour {league}...")
        html_content = fetch_html(url)
        if html_content:
            response = send_to_openrouter(api_key, model, prompt, html_content)
            if response and 'choices' in response:
                assistant_reply = response["choices"][0].get("message", {}).get("content", "")
                cleaned_json = clean_json(assistant_reply)  # Nettoyer le JSON avant de le parser
                try:
                    return json.loads(cleaned_json)  # Convertir en vrai JSON
                except json.JSONDecodeError:
                    print(f"Erreur de parsing JSON pour {league}")
                    return {"error": "Invalid JSON response"}
            else:
                print(f"Erreur ou réponse vide pour {league}")
        else:
            print(f"Échec de la récupération du contenu HTML pour {league}")

        # Attendre avant de réessayer
        retry_count += 1
        if retry_count < max_retries:
            print(f"Réessayer dans {delay_between_retries} secondes...")
            time.sleep(delay_between_retries)

    # Retourner un message d'erreur après le nombre de tentatives maximum
    return {"error": "Max retries reached"}

if __name__ == "__main__":
    # Clé API et modèle OpenRouter
    api_key = "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"  # Remplace avec ta clé API
    model = "google/gemini-2.0-flash-lite-preview-02-05:free"
    prompt = "Give me the split names, start and end dates (splitName, startDate, endDate) (date format: YYYY-MM-DD). Return only valid JSON with no extra text, explanations, or formatting, remove the year and league name from the splitName."

    # Dictionnaire des ligues avec leurs URLs
    leagues = {
        'first_stand': 'https://lol.fandom.com/wiki/First_Stand',
        'lck_challengers_league': 'https://lol.fandom.com/wiki/LCK_Challengers_League#Main_Events',
        'lck': 'https://lol.fandom.com/wiki/League_of_Legends_Champions_Korea#Main_Events',
        'lcs': 'https://lol.fandom.com/wiki/League_Championship_Series#Main_Events',
        'lec': 'https://lol.fandom.com/wiki/LoL_EMEA_Championship#Main_Events',
        'lfl': 'https://lol.fandom.com/wiki/Ligue_Française_de_League_of_Legends#Main_Events',
        'ljl-japan': 'https://lol.fandom.com/wiki/League_of_Legends_Japan_League#Main_Events',
        'lla': 'https://lol.fandom.com/wiki/Liga_Latinoamérica#Main_Events',
        'lpl': 'https://lol.fandom.com/wiki/LoL_Pro_League#Main_Events',
        'lta_cross': 'https://lol.fandom.com/wiki/League_of_Legends_Championship_of_The_Americas#Main_Events',
        'lta_n': 'https://lol.fandom.com/wiki/LTA_North#Main_Events',
        'lta_s': 'https://lol.fandom.com/wiki/LTA_South#Main_Events',
        'msi': 'https://lol.fandom.com/wiki/Mid-Season_Invitational',
        'pcs': 'https://lol.fandom.com/wiki/Pacific_Championship_Series#Main_Events',
        'vcs': 'https://lol.fandom.com/wiki/Vietnam_Championship_Series#Main_Events',
        'worlds': 'https://lol.fandom.com/wiki/World_Championship'
    }

    results = {}

    for league, url in leagues.items():
        print(f"Traitement de {league}...")
        result = process_league(league, url, api_key, model, prompt)
        results[league] = result

    # Stocker les résultats dans un fichier JSON propre
    with open("import_data/openrouter_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print("Les résultats ont été enregistrés dans openrouter_results.json")
