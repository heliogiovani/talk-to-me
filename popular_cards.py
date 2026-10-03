from app import create_app, db
from app.models.card import Card

NATURAL_TRANSLATIONS = {
    "I am looking forward to hearing from you.": "Fico no aguardo de notícias suas. / Aguardo seu retorno.",
    "Could you please repeat that more slowly?": "Poderia repetir mais devagar, por favor?",
    "I have never thought about it that way before.": "Nunca tinha pensado por esse lado antes.",
    "Let me know if you need any further assistance.": "Conte comigo se precisar de mais alguma ajuda.",
    "I will get back to you as soon as possible.": "Te dou um retorno assim que possível.",
    "What do you usually do on the weekend?": "O que você costuma fazer aos fins de semana?",
    "It makes no sense to worry about that now.": "Não adianta esquentar a cabeça com isso agora.",
    "I am running a little bit late today.": "Estou um pouco atrasado hoje.",
    "Could you give me a hand with this task?": "Pode me dar uma mãozinha com esta tarefa?",
    "How long does it take to get there by car?": "Quanto tempo leva para chegar lá de carro?",
    "I completely agree with what you just said.": "Concordo em gênero, número e grau com o que disse.",
    "Take your time, there is no rush at all.": "Sem pressa, faça no seu tempo.",
    "Can I have the check, please?": "Pode me trazer a conta, por favor?",
    "That sounds like a great idea to me.": "Acho uma ótima ideia!",
    "I am trying to improve my English skills every day.": "Estou me dedicando para destravar meu inglês todos os dias.",
    "Could you recommend a good place to have lunch?": "Sabe me indicar um bom lugar para almoçar?",
    "I appreciate your time and consideration.": "Muito obrigado pela sua atenção e consideração.",
    "I am not quite sure if I understand your point.": "Não sei se peguei bem o que você quis dizer.",
    "Everything is going according to plan so far.": "Por enquanto, está tudo correndo conforme o combinado.",
    "Nice to finally meet you in person.": "Que bom finalmente te conhecer pessoalmente!"
}

app = create_app()

with app.app_context():
    print("Atualizando traduções idiomáticas no MySQL...")
    cards = Card.query.all()
    for card in cards:
        if card.english_phrase in NATURAL_TRANSLATIONS:
            card.portuguese_translation = NATURAL_TRANSLATIONS[card.english_phrase]
            print(f"Atualizado: {card.english_phrase} -> {card.portuguese_translation}")

    db.session.commit()
    print("--------------------------------------------------")
    print("Pronto! Todas as traduções estão naturais e idiomáticas.")