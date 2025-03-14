import requests
import json
import re
import os

# Load existing results
def load_results(filename="import_data/openrouter_results.json"):
    """Charge les résultats existants depuis un fichier JSON."""
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# Save updated results
def save_results(results, filename="import_data/openrouter_results.json"):
    """Enregistre les résultats mis à jour dans un fichier JSON."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

# Clean JSON response from OpenRouter
def clean_json(response_text):
    """Supprime les backticks ```json et ``` de la réponse."""
    cleaned_text = re.sub(r"^```json\s*", "", response_text, flags=re.MULTILINE)  # Supprime ```json au début
    cleaned_text = re.sub(r"```$", "", cleaned_text, flags=re.MULTILINE)  # Supprime ``` à la fin
    return cleaned_text.strip()

# Fetch HTML content from a URL
def fetch_html(url):
    """Récupère le contenu HTML d'une URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Erreur lors de la récupération de {url}: {e}")
        return None

# Send HTML to OpenRouter API
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

if __name__ == "__main__":
    # API Key and OpenRouter model
    api_key = "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"  # Replace with your API key
    model = "google/gemini-2.0-flash-lite-preview-02-05:free"
    prompt = "Give me the split names, start and end dates (splitName, startDate, endDate) (date format: YYYY-MM-DD). Return only valid JSON with no extra text, explanations, or formatting, remove the year and league name from the splitName."

    # League URLs
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

    # Load existing results and find errors
    results = load_results()
    leagues_to_retry = {league: url for league, url in leagues.items() if league not in results or "error" in results[league]}

    if not leagues_to_retry:
        print("✅ Aucune ligue en erreur, tout est déjà bon !")
    else:
        print(f"🔄 Retrying {len(leagues_to_retry)} leagues with errors...")

        for league, url in leagues_to_retry.items():
            print(f"🔄 Retrying {league}...")
            html_content = fetch_html(url)
            if html_content:
                response = send_to_openrouter(api_key, model, prompt, html_content)
                if response and 'choices' in response:
                    assistant_reply = response["choices"][0].get("message", {}).get("content", "")
                    cleaned_json = clean_json(assistant_reply)  # Remove backticks before parsing
                    try:
                        results[league] = json.loads(cleaned_json)  # Convert to valid JSON
                        print(f"✅ {league} fixed successfully!")
                    except json.JSONDecodeError:
                        print(f"❌ JSON parsing error for {league}")
                        results[league] = {"error": "Invalid JSON response"}
                else:
                    print(f"❌ API returned an empty or invalid response for {league}")
                    results[league] = {"error": "Empty or invalid API response"}

        # Save updated results
        save_results(results)
        print("✅ Results updated in openrouter_results.json")
