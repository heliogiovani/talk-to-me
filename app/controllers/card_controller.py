from datetime import datetime, timedelta
import difflib
import re
from flask import Blueprint, jsonify, request
from sqlalchemy.sql.expression import func
from app import db
from app.models.card import Card
from app.services.daily_fetcher import DailyFetcherService

card_bp = Blueprint('card_bp', __name__, url_prefix='/api/cards')

@card_bp.route('/next', methods=['GET'])
def get_next_card():
    """
    Retorna cards aleatoriamente entre os disponíveis para estudo.
    """
    DailyFetcherService.ensure_daily_cards()
    
    agora = datetime.utcnow()
    # Prioriza cards pendentes de revisão de forma aleatória
    card = Card.query.filter(Card.next_review_at <= agora).order_by(func.rand()).first()
    
    # Se todos estiverem com revisão futura, sorteia qualquer um da base
    if not card:
        card = Card.query.order_by(func.rand()).first()

    if not card:
        return jsonify({"message": "Nenhum cartão encontrado."}), 404

    return jsonify(card.to_dict())

@card_bp.route('/<int:card_id>/review', methods=['POST'])
def review_card(card_id):
    card = Card.query.get_or_404(card_id)
    data = request.get_json() or {}
    difficulty = data.get('difficulty', 'dificil')
    agora = datetime.utcnow()

    if difficulty == 'muito_dificil':
        card.repetition_interval = 15
        card.next_review_at = agora + timedelta(minutes=15)
        card.status = 'learning'
    elif difficulty == 'facil':
        card.repetition_interval = 5760
        card.next_review_at = agora + timedelta(days=4)
        card.status = 'review'
    else:
        card.repetition_interval = 1440
        card.next_review_at = agora + timedelta(days=1)
        card.status = 'review'

    db.session.commit()
    return jsonify({"success": True, "next_review_at": card.next_review_at.isoformat()})

@card_bp.route('/<int:card_id>/check-pronunciation', methods=['POST'])
def check_pronunciation(card_id):
    """
    Validação implacável:
    - Exige conferência estrita palavra a palavra.
    - Se faltar uma palavra ou for falada uma palavra errada, penaliza fortemente.
    """
    card = Card.query.get_or_404(card_id)
    data = request.get_json() or {}
    spoken_text = data.get('spoken_text', '').strip()

    if not spoken_text:
        return jsonify({
            "approved": False,
            "score": 0,
            "message": "Nenhum áudio inteligível detectado."
        })

    def get_tokens(text):
        return re.findall(r"\b[a-zA-Z0-9']+\b", text.lower())

    expected_tokens = get_tokens(card.english_phrase)
    actual_tokens = get_tokens(spoken_text)

    if not actual_tokens:
        return jsonify({"approved": False, "score": 0, "message": "Nenhuma palavra identificada."})

    # Conta correspondência de cada palavra individualmente
    total_expected = len(expected_tokens)
    matched_words = 0
    
    # Compara palavra por palavra na sequência
    matcher = difflib.SequenceMatcher(None, expected_tokens, actual_tokens)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            matched_words += (i2 - i1)

    # Similaridade geral de caracteres
    char_ratio = difflib.SequenceMatcher(None, " ".join(expected_tokens), " ".join(actual_tokens)).ratio()
    word_ratio = matched_words / max(total_expected, len(actual_tokens))

    # Score final exigente (mínimo de 90% para aprovação real)
    final_score = int(round(((word_ratio * 0.7) + (char_ratio * 0.3)) * 100))
    approved = (final_score >= 90) and (matched_words == total_expected)

    return jsonify({
        "approved": approved,
        "score": final_score,
        "expected_phrase": card.english_phrase,
        "recognized_text": spoken_text
    })