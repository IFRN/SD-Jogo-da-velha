import socket ##Processo de comunicação
import pickle ##converter tanto em bytes quanto para objetos python

def print_tabuleiro(tabuleiro): ##imprimir tabuleiro 3x3
    for i in range(3):
        print(f"{tabuleiro[i][0]} | {tabuleiro[i][1]} | {tabuleiro[i][2]}")
        if i < 2:
            print("--+---+--")

def verificar_ganhador(tabuleiro): ##em que casos ele ganha ou dá empate
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
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Usando UDP (SOCK_DGRAM) -> não precisa de conexão continua
    udp_socket.bind(("localhost", 51351))  # Bind na porta 51351

    print("Aguardando conexões...")

    # Espera pela conexão de dois jogadores
    data, addr1 = udp_socket.recvfrom(1024)  # Espera Jogador 1 enviar pacote
    print(f"Jogador 1 conectado: {addr1}")

    data, addr2 = udp_socket.recvfrom(1024)  # Espera Jogador 2 enviar pacote
    print(f"Jogador 2 conectado: {addr2}")

    tabuleiro = [[" " for _ in range(3)] for _ in range(3)]  # Tabuleiro inicial
    jogador_atual = "X"

    while True:
        jogador_atual_info = pickle.dumps((tabuleiro, jogador_atual))  # Serializa o estado do jogo
        # Envia o estado do tabuleiro e o jogador atual para o jogador correto
        udp_socket.sendto(jogador_atual_info, addr1 if jogador_atual == "X" else addr2)

        # Recebe a jogada do jogador
        data, addr = udp_socket.recvfrom(1024)  # Recebe a jogada de um jogador
        jogada = pickle.loads(data)  # Desserializa os dados da jogada
        linha, coluna = jogada  # A jogada do jogador

        # Atualiza o tabuleiro
        if 0 <= linha < 3 and 0 <= coluna < 3 and tabuleiro[linha][coluna] == " ":
            tabuleiro[linha][coluna] = jogador_atual
        else:
            invalid_move_msg = pickle.dumps("Movimento inválido!") 
            udp_socket.sendto(invalid_move_msg, addr)  # Envia a mensagem de erro ao jogador
            continue

        resultado = verificar_ganhador(tabuleiro)
        if resultado:
            # Os dois jogadores recebem o resultado
            resultado_msg = pickle.dumps(f"Jogador {resultado} venceu!" if resultado != "Empate" else "Empate!")
            udp_socket.sendto(resultado_msg, addr1)
            udp_socket.sendto(resultado_msg, addr2)
            break

        # Alterna o jogador
        jogador_atual = "O" if jogador_atual == "X" else "X"

    print("Encerrando o jogo...")
    udp_socket.close()  # Fecha o socket UDP

if __name__ == "__main__":
    servidor()


##BOM DIA!