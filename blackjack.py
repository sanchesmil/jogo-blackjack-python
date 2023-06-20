import random 

saldo = 0
aposta = 0
jogando = True

# variáveis usadas para criar as cartas
naipes = ('H','D','S','C')
cartas_valor = {'Two':2,'Three':3,'Four':4,'Five':5,'Six':6,'Seven':7,'Eight':8,'Nine':9,'Ten':10,'Jack':10,'Queen':10,'King':10,'Ace':11}
    
    
class Carta:  
    def __init__(self,naipe,nome,valor):
        self.naipe = naipe
        self.nome = nome
        self.valor = valor
        
    def __str__(self):
        return self.naipe + '-' + self.nome + '-' + str(self.valor)
                      
class Baralho:   
    def __init__(self,naipes,cartas_valor):
        
        self.baralho = []  # inicia o baralho 
        
        # cria as cartas e adiciona ao baralho
        for naipe in naipes:
            for nome,valor in cartas_valor.items():
                self.baralho.append(Carta(naipe,nome,valor))
             
    def __str__(self):
        cartas_baralho = ''
        for carta in self.baralho:
            cartas_baralho += "\n" + carta.__str__()
            
        return "O baralho possui: " + cartas_baralho
    
    def fornecer_carta(self):
        return self.baralho.pop()
    
    def embaralhar(self):
        random.shuffle(self.baralho) 
                
class Mao:
    def __init__(self):
        self.cartas = []
        self.valor = 0
        self.hidden = False
    
    def valor_real(self):            
        # ajuste de valor carta 'Ace'
        for carta in self.cartas:
            if carta.nome == 'Ace' and self.valor > 21:
                return self.valor - 10        
            else:
                return self.valor
    
    def add_carta(self,carta,hidden = False):
        self.cartas.append(carta)
        self.valor += carta.valor
        self.hidden = hidden
        
    def __str__(self):
        
        if len(self.cartas) == 2 and self.hidden == True:
            return self.cartas[0].__str__() + ' + carta escondida'
        else:
            mao_com = [] 
            for carta in self.cartas:
                mao_com.append(carta.__str__())
            
            mao_com = ', '.join(mao_com) + ' (Total: ' + str(self.valor_real()) + ')'
            return mao_com


# define o saldo inicial no jogo
def definir_saldo_inicial():
    
    global saldo
    
    while True:
        try:   
            saldo = int(input('Informe o seu saldo inicial no Jogo: ') ) 
            break
        except ValueError:
            print("Atenção: O valor informado deve ser um número inteiro.")
            continue
            
# informa o valor da aposta
def definir_aposta():
    global aposta, saldo
    while True:
        try:
            aposta = int(input("Informe o valor da sua aposta: "))
            print(" ")
            
            if aposta > saldo:
                print("Atenção: Você não possui recursos suficientes. Refaça sua aposta.")
                continue
            else:
                break
                
        except ValueError:
            print("Atenção: Informe um valor válido. ")
            continue

# distribuir cartas 
def distribuir_cartas():
    
    global baralho, cartas_jogador,cartas_dealer
    
    cartas_jogador.add_carta(baralho.fornecer_carta())
    cartas_jogador.add_carta(baralho.fornecer_carta())
    
    cartas_dealer.add_carta(baralho.fornecer_carta())
    cartas_dealer.add_carta(baralho.fornecer_carta(), True) # informa que o atributo 'hidden' = True
    
def mostrar_cartas(msg = ''):
    global cartas_jogador,cartas_dealer
    
    print('-------')
    print('\nCartas Jogador: ',cartas_jogador)
    print('Cartas Dealer: ',cartas_dealer)
  
    print(' ')
    print(msg)


def checa_vencedor():
    global cartas_jogador,cartas_dealer, saldo, aposta
    
    msg = ''
    vencedor = ''
    mostrar_cartas()
    
    if cartas_jogador.valor_real() == 21 and cartas_dealer.valor_real() == 21:
        msg = "Houve empate: Jogador e Dealer fizeram BlackJack!"   
    elif cartas_jogador.valor_real() == 21:
        msg = "Parabéns. Você fez um BlackJack e venceu o jogo." 
        saldo += aposta
    elif cartas_dealer.valor_real() == 21:
        msg = "Você perdeu. O Dealer fez um BlackJack!"
        saldo -= aposta    
    elif cartas_jogador.valor_real() > 21:
        msg = "Você estourou. Dealer venceu o jogo."
        saldo -= aposta
    elif cartas_dealer.valor_real() > 21:
        msg = "Dealer estourou. Parabéns, você venceu o jogo."
        saldo += aposta
    
    if msg:
        vencedor = True
        print(msg)
        print('Saldo final: ', saldo)
        print(' ')
                   
    return vencedor

def jogar_novamente():
    
    continuar = False
    
    while True:
        try: 
            nova_partida = str(input('Deseja jogar novamente? (S/N)')).lower()
        except:
            print('Entrada inválida.')
            continue
        else:
            if nova_partida != 's' and nova_partida != 'n':
                print('Entrada inválida!')
                continue

            if nova_partida == 's':
                print('Jogar novamente')
                continuar = True
                break
            else:
                print('Fim de Jogo')
                break
        
    return continuar

    
## ---- INICIA O JOGO ----- ## 

print("")
print('Bem vindo ao Jogo BlackJack')
print("")

# define saldo inicial e aposta
definir_saldo_inicial()
    
while jogando:
    
    definir_aposta()
    
    # cria e embaralha o baralho
    baralho = Baralho(naipes,cartas_valor)
    baralho.embaralhar()

    # define as maos do jogador e dealer
    cartas_jogador = Mao()
    cartas_dealer = Mao()

    # distribui 2 cartas ao jogador e ao dealer
    distribuir_cartas()

    print('-------')
    print('Distribuição inicial')
    print('Saldo inicial: ', saldo)
        
    while True:

        # checa se alguem já fez um blackjack
        if checa_vencedor():
            if not jogar_novamente():
                jogando = False
            break 
                
        try: 
            continuar = str(input("Digite 'h' para pedir outra carta ou 's' para esperar.")).lower()  
            
            if continuar != 's' and continuar != 'h':
                print('Entrada inválida!')
                #continue
                
            else:
                if continuar == 'h':
                    print(' ')
                    print('Jogador pegou uma carta')
                    cartas_jogador.add_carta(baralho.fornecer_carta()) 
                else: 
                    print(' ')
                    print('Jogador esperou')            
                    print('Dealer pegou uma carta')
                    cartas_dealer.add_carta(baralho.fornecer_carta())
        except:
            print('Entrada inválida.')
            continue
            
