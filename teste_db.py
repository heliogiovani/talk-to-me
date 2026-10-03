from app import create_app, db
from app.models.card import Card

app = create_app()

with app.app_context():
    try:
        # Testa a ligação consultando a tabela de cards
        count = Card.query.count()
        print("----------------------------------------")
        print(" SUCESSO: Ligação ao MySQL efectuada com êxito!")
        print(f" Total de cards registados na base de dados: {count}")
        print("----------------------------------------")
    except Exception as e:
        print("----------------------------------------")
        print(" ERRO ao ligar à base de dados:")
        print(e)
        print("----------------------------------------")