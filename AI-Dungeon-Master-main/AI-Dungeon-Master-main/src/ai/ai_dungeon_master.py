import os
import openai

class AIDungeonMaster:
    def __init__(self):
        self.ready = True
        self.api_key = os.getenv('OPENAI_API_KEY')
        openai.api_key = self.api_key

    def run_campaign(self, prompt, model="gpt-3.5-turbo"):
        if not self.api_key:
            return "API anahtarı bulunamadı. Lütfen .env dosyanıza OPENAI_API_KEY ekleyin."
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "system", "content": "You are a creative and challenging Dungeon Master for a tabletop RPG campaign."},
                          {"role": "user", "content": prompt}],
                max_tokens=512,
                temperature=1.1
            )
            return response.choices[0].message["content"].strip()
        except Exception as e:
            return f"LLM API hatası: {e}" 