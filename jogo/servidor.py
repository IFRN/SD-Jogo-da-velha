import socket
import pickle

def print_tabuleiro(board):
    for i in range(3):
        print(f"{board[i][0]} | {board[i][1]} | {board[i][2]}")
        if i < 2:
            print("--+---+--")

def verificar_ganhador(board):
    for linha in board:
        if linha[0] == linha[1] == linha[2] and linha[0] != " ":
            return linha[0]
    for coluna in range(3):
        if board[0][coluna] == board[1][coluna] == board[2][coluna] and board[0][coluna] != " ":
            return board[0][coluna]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != " ":
        return board[0][2]
    if all(cell != " " for linha in board for cell in linha):
        return "Empate"
    return None

def servidor():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 51351))
    server_socket.listen(2)

    print("Aguardando conexões...")
    conn1, addr1 = server_socket.accept()
    print(f"Jogador 1 conectado: {addr1}")
    conn2, addr2 = server_socket.accept()
    print(f"Jogador 2 conectado: {addr2}")

    board = [[" " for _ in range(3)] for _ in range(3)]
    jogador_atual = "X"

    while True:
        # Envia o tabuleiro para o jogador atual
        conn = conn1 if jogador_atual == "X" else conn2
        conn.sendall(pickle.dumps((board, jogador_atual)))

        # Recebe a jogada do jogador
        jogada = pickle.loads(conn.recv(1024))
        linha, coluna = jogada

        # Atualiza o tabuleiro
        if 0 <= linha < 3 and 0 <= coluna < 3 and board[linha][coluna] == " ":
            board[linha][coluna] = jogador_atual
        else:
            conn.sendall(pickle.dumps("Movimento inválido!"))
            continue

        # Verifica o resultado
        resultado = verificar_ganhador(board)
        if resultado:
            conn1.sendall(pickle.dumps(resultado))
            conn2.sendall(pickle.dumps(resultado))
            break

        # Alterna o jogador
        jogador_atual = "O" if jogador_atual == "X" else "X"

    print("Encerrando o jogo...")
    conn1.close()
    conn2.close()
    server_socket.close()

if __name__ == "__main__":
    servidor()
