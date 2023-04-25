import socket

# Define o conteúdo do pacote
destino = 'B'
dados = 'dados do pacote'
custo = 1

# Cria o socket para enviar o pacote
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Conecta ao roteador simulado
    s.connect(('127.0.0.1', 65432))

    # Codifica os dados do pacote como uma string
    mensagem = f"{destino},{dados},{custo}".encode()

    # Envia a mensagem para o roteador simulado
    s.sendall(mensagem)

    # Aguarda a resposta do roteador simulado
    resposta = s.recv(1024)

    # Exibe a resposta na tela
    print(resposta.decode())
