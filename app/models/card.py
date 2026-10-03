from datetime import datetime, date
from app import db

class Card(db.Model):
    __tablename__ = 'cards'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    english_phrase = db.Column(db.Text, nullable=False)
    phonetic_ipa = db.Column(db.String(255), nullable=False)
    cadence_data = db.Column(db.JSON, nullable=False)           # Estrutura JSON com palavras e ênfase
    portuguese_translation = db.Column(db.Text, nullable=False)
    context_note = db.Column(db.String(255), nullable=True)     # Ex: "Uso formal em reuniões"
    status = db.Column(db.Enum('new', 'learning', 'review'), default='new')
    repetition_interval = db.Column(db.Integer, default=0)      # Intervalo em minutos
    next_review_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_at = db.Column(db.Date, nullable=False, default=date.today)

    def to_dict(self):
        """Converte o objecto para dicionário facilitando o envio para o Frontend."""
        return {
            "id": self.id,
            "english_phrase": self.english_phrase,
            "phonetic_ipa": self.phonetic_ipa,
            "cadence_data": self.cadence_data,
            "portuguese_translation": self.portuguese_translation,
            "context_note": self.context_note,
            "status": self.status,
            "repetition_interval": self.repetition_interval,
            "next_review_at": self.next_review_at.isoformat() if self.next_review_at else None
        }