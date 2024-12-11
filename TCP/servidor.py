import socket ##Processo de comunicação
import pickle ##converter tanto em bytes quanto para objetos python

def print_tabuleiro(tabuleiro): ##imprimir tabuleiro 3x3
    for i in range(3):
        print(f"{tabuleiro[i][0]} | {tabuleiro[i][1]} | {tabuleiro[i][2]}")
        if i < 2:
            print("--+---+--")

def verificar_ganhador(tabuleiro): ##em que casos ele ganha ou dá empate?
    for linha in tabuleiro:
        if linha[0] == linha[1] == linha[2] and linha[0] != " ":
            return linha[0]
    for coluna in range(3):
        if tabuleiro[0][coluna] == tabuleiro[1][coluna] == tabuleiro[2][coluna] and tabuleiro[0][coluna] != " ":
            return tabuleiro[0][coluna]
    if tabuleiro[0][0] == tabuleiro[1][1] == tabuleiro[2][2] and tabuleiro[0][0] != " ":
        return tabuleiro[0][0]
    if tabuleiro[0][2] == tabuleiro[1][1] == tabuleiro[2][0] and tabuleiro[0][2] != " ":
        return tabuleiro[0][2]
    if all(cell != " " for linha in tabuleiro for cell in linha):
        return "Empate"
    return None

def servidor():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) ##TCP -> orientado à conexão
    server_socket.bind(("localhost", 51351))
    server_socket.listen(2)

    print("Aguardando conexões...")
    conn1, addr1 = server_socket.accept()
    print(f"Jogador 1 conectado: {addr1}")
    conn2, addr2 = server_socket.accept()
    print(f"Jogador 2 conectado: {addr2}")

    tabuleiro = [[" " for _ in range(3)] for _ in range(3)]
    jogador_atual = "X"

    while True:
        # Envia o tabuleiro para o jogador atual
        conn = conn1 if jogador_atual == "X" else conn2
        conn.sendall(pickle.dumps((tabuleiro, jogador_atual)))

        # Recebe a jogada do jogador
        jogada = pickle.loads(conn.recv(1024))
        linha, coluna = jogada

        # Atualiza o tabuleiro
        if 0 <= linha < 3 and 0 <= coluna < 3 and tabuleiro[linha][coluna] == " ":
            tabuleiro[linha][coluna] = jogador_atual
        else:
            conn.sendall(pickle.dumps("Movimento inválido!"))
            continue

        
        resultado = verificar_ganhador(tabuleiro)
        if resultado: # Os dois jogadores recebem o resultado
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
