from datetime import date, datetime
from app import db
from app.models.card import Card
from app.services.phrase_service import PhraseService

# Lista de frases essenciais e práticas do dia a dia para estudo
DAILY_PHRASES_POOL = [
    ("I am looking forward to hearing from you.", "Encerramento comum e cortês para mensagens formais ou de trabalho."),
    ("Could you please repeat that more slowly?", "Pedido educado para repetição de fala em conversa."),
    ("I have never thought about it that way before.", "Expressão de reflexão ao ouvir uma perspetiva diferente."),
    ("Let me know if you need any further assistance.", "Oferta de apoio adicional em ambiente profissional."),
    ("I will get back to you as soon as possible.", "Compromisso de retorno rápido para contactos."),
    ("What do you usually do on the weekend?", "Pergunta comum para iniciar diálogo social descontraído."),
    ("It makes no sense to worry about that now.", "Expressão para relativizar preocupações imediatas."),
    ("I am running a little bit late today.", "Aviso informal de atraso em compromissos."),
    ("Could you give me a hand with this task?", "Pedido informal de ajuda ou colaboração."),
    ("How long does it take to get there by car?", "Dúvida comum sobre tempo de deslocação e percurso."),
    ("I completely agree with what you just said.", "Concordância direta e clara durante uma reunião."),
    ("Take your time, there is no rush at all.", "Expressão cordial para tranquilizar alguém apressado."),
    ("Can I have the check, please?", "Pedido educado da conta em restaurantes e cafés."),
    ("That sounds like a great idea to me.", "Demonstração de aprovação em relação a uma sugestão."),
    ("I am trying to improve my English skills every day.", "Frase motivacional de progresso e consistência nos estudos."),
    ("Could you recommend a good place to have lunch?", "Pedido de recomendação gastronómica local."),
    ("I appreciate your time and consideration.", "Agradecimento polido em comunicações profissionais."),
    ("I am not quite sure if I understand your point.", "Maneira educada de pedir clarificação num debate."),
    ("Everything is going according to plan so far.", "Atualização positiva sobre o progresso de um projeto."),
    ("Nice to finally meet you in person.", "Cumprimento comum no primeiro encontro presencial com alguém.")
]

class DailyFetcherService:
    @staticmethod
    def ensure_daily_cards():
        """
        Garante que existem pelo menos 20 frases disponíveis para estudo hoje.
        Se ainda não foram geradas, insere as 20 frases enriquecidas na base de dados.
        """
        hoje = date.today()
        total_hoje = Card.query.filter_by(created_at=hoje).count()

        if total_hoje >= 20:
            return total_hoje

        cards_criados = 0
        for phrase, context in DAILY_PHRASES_POOL:
            # Evita duplicar a mesma frase na base de dados
            existe = Card.query.filter_by(english_phrase=phrase).first()
            if existe:
                continue

            ipa_text = PhraseService.get_phonetic_ipa(phrase)
            cadence = PhraseService.calculate_cadence(phrase)
            translation = PhraseService.translate_to_portuguese(phrase)

            novo_card = Card(
                english_phrase=phrase,
                phonetic_ipa=ipa_text,
                cadence_data=cadence,
                portuguese_translation=translation,
                context_note=context,
                status='new',
                repetition_interval=0,
                next_review_at=datetime.utcnow(),
                created_at=hoje
            )
            db.session.add(novo_card)
            cards_criados += 1

        db.session.commit()
        return cards_criados