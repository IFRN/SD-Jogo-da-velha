import socket ##Processo de comunicação
import pickle ##converter tanto em bytes quanto para objetos python

def print_tabuleiro(tabuleiro): ##imprimir tabuleiro 3x3
    for i in range(3):
        print(f"{tabuleiro[i][0]} | {tabuleiro[i][1]} | {tabuleiro[i][2]}")
        if i < 2:
            print("--+---+--")

def cliente():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 51351)) 

    while True:
        # Recebe o estado do jogo
        data = pickle.loads(client_socket.recv(1024))

        if isinstance(data, str):  # Mensagem de resultado
            print(data)
            break

        tabuleiro, jogador_atual = data
        print_tabuleiro(tabuleiro)
        print(f"Você é o jogador '{jogador_atual}'")

        # Envia a jogada
        try:
            linha = int(input("Escolha a linha (0, 1, 2): "))
            coluna = int(input("Escolha a coluna (0, 1, 2): "))
            client_socket.sendall(pickle.dumps((linha, coluna)))
        except ValueError:
            print("Entrada inválida! Tente novamente.")

if __name__ == "__main__":
    cliente()
