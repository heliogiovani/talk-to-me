from app.services.phrase_service import PhraseService

test_phrase = "I am looking forward to hearing from you."

print("--- Teste do Serviço de Enriquecimento de Frases ---")
print(f"Frase original: {test_phrase}")

# 1. Transcrição Fonética
ipa_result = PhraseService.get_phonetic_ipa(test_phrase)
print(f"Fonética (IPA): {ipa_result}")

# 2. Tradução
pt_result = PhraseService.translate_to_portuguese(test_phrase)
print(f"Tradução (Google): {pt_result}")

# 3. Análise de Cadência
cadence = PhraseService.calculate_cadence(test_phrase)
print("Cadência calculada:")
for item in cadence:
    print(f"  - Palavra: {item['word']:<10} | Ênfase: {item['emphasis']}")
print("--------------------------------------------------")