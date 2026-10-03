import re
import urllib.parse
import requests
import eng_to_ipa as ipa

# Palavras gramaticais/funcionais com ênfase fraca no ritmo da fala em inglês
GRAMMAR_WORDS = {
    'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them',
    'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
    'do', 'does', 'did', 'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from',
    'a', 'an', 'the', 'and', 'but', 'or', 'so', 'that', 'as', 'if', 'this', 'that'
}

class PhraseService:
    @staticmethod
    def get_phonetic_ipa(phrase: str) -> str:
        """Gera a transcrição fonética IPA para a frase."""
        raw_ipa = ipa.convert(phrase)
        return f"/{raw_ipa}/"

    @staticmethod
    def calculate_cadence(phrase: str) -> list:
        """
        Classifica as palavras entre ênfase forte ('strong') e fraca ('weak')
        para criar os blocos visuais de ritmo.
        """
        tokens = re.findall(r"\w+|[^\w\s]", phrase, re.UNICODE)
        cadence_list = []

        for token in tokens:
            clean_word = token.lower().strip()
            
            if not clean_word.isalnum():
                continue

            emphasis = "weak" if clean_word in GRAMMAR_WORDS else "strong"

            cadence_list.append({
                "word": token,
                "emphasis": emphasis
            })

        return cadence_list

    @staticmethod
    def translate_to_portuguese(phrase: str) -> str:
        """
        Realiza a tradução direta via endpoint do Google Tradutor enviando cabeçalho de navegador.
        """
        try:
            url = "https://translate.googleapis.com/translate_a/single"
            params = {
                "client": "gtx",
                "sl": "en",
                "tl": "pt",
                "dt": "t",
                "q": phrase
            }
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            response = requests.get(url, params=params, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                translated_segments = [seg[0] for seg in data[0] if seg and seg[0]]
                return "".join(translated_segments).strip()
            return "Tradução indisponível."
        except Exception:
            return "Erro na tradução."