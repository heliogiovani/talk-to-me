from app import create_app

app = create_app()

if __name__ == '__main__':
    print("-------------------------------------------------------")
    print(" A iniciar o servidor da Aplicação de Flashcards...")
    print(" Aceda no seu navegador através de: http://127.0.0.1:5000")
    print(" Para parar o servidor, pressione Ctrl + C no terminal.")
    print("-------------------------------------------------------")
    app.run(debug=True, host='127.0.0.1', port=5000)