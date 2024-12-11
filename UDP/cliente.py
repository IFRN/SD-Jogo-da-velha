import socket ##Processo de comunicação
import pickle ##converter tanto em bytes quanto para objetos python

def print_tabuleiro(tabuleiro): ##imprimir tabuleiro 3x3
    for i in range(3):
        print(f"{tabuleiro[i][0]} | {tabuleiro[i][1]} | {tabuleiro[i][2]}")
        if i < 2:
            print("--+---+--")

def cliente():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Usando UDP (SOCK_DGRAM)
    servidor_addr = ("localhost", 51351)  # Endereço do servidor (localhost e a porta 51351)

    while True:

        udp_socket.sendto(b"Solicitando o estado do jogo", servidor_addr)

        # Estado do jogo
        data, _ = udp_socket.recvfrom(1024)  # Recebe a resposta do servidor
        data = pickle.loads(data)  # Recebe objetos python

        if isinstance(data, str):  # Se a resposta for uma mensagem de resultado (fim de jogo)
            print(data)
            break

        tabuleiro, jogador_atual = data  # O estado do tabuleiro e o jogador atual
        print_tabuleiro(tabuleiro)
        print(f"Você é o jogador '{jogador_atual}'")

        try:
            linha = int(input("Escolha a linha (0, 1, 2): "))
            coluna = int(input("Escolha a coluna (0, 1, 2): "))
            jogada = (linha, coluna)
            udp_socket.sendto(pickle.dumps(jogada), servidor_addr)  # Envia a jogada para o servidor
        except ValueError:
            print("Entrada inválida! Tente novamente.")

    udp_socket.close()  # Fecha o socket UDP

if __name__ == "__main__":
    cliente()
