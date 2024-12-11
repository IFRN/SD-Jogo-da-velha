import socket ##Os sockets podem ser definidos como um processo de comunicação que permite dois diferentes processos de conversarem e trocarem informação entre si.
import pickle

def print_tabuleiro(board):
    for i in range(3):
        print(f"{board[i][0]} | {board[i][1]} | {board[i][2]}")
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

        board, jogador_atual = data
        print_tabuleiro(board)
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
