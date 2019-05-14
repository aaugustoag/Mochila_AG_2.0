import matplotlib.pyplot as plt
from Principal import funcoes
from copy import deepcopy

#        0     1     2     3     4     5     6     7     8     9     10    11
#itens2=[[3,5],[7,2],[4,5],[6,8],[3,6],[6,6],[7,1],[1,7],[1,1],[3,3],[3,2],[4,1]]


#instancia = input('Selecione a instancia:\n1- 40 itens:\n2- 100 itens:\n3- 10.000 itens:\n4- 10.000-2 itens:\n5- 11.000 itens:\n6- 100.000 iten:\n')

#instancia = int(instancia)

for i in range(1):
    itens=[]
    instancia = i+6

    if instancia == 1:
        print("Arquivo KNAPDATA40.TXT selecionado")
        #/home/alexandreaag/PycharmProjects/Mochila_AG/Principal/
        arq = open('KNAPDATA40.TXT', 'r')
    elif instancia == 2:
        print("Arquivo KNAPDATA100.TXT selecionado")
        arq = open('KNAPDATA100.TXT', 'r')
    elif instancia == 3:
        print("Arquivo KNAPDATA10000.TXT selecionado")
        arq = open('KNAPDATA10000.TXT', 'r')
    elif instancia == 4:
        print("Arquivo KNAPDATA10000_2.TXT selecionado")
        arq = open('KNAPDATA10000_2.TXT', 'r')
    elif instancia == 5:
        print("Arquivo KNAPDATA11000.TXT selecionado")
        arq = open('KNAPDATA11000.TXT', 'r')
    elif instancia == 6:
        print("Arquivo KNAPDATA100000.TXT selecionado")
        arq = open('KNAPDATA100000.TXT', 'r')
    else:
        exit()

    texto = arq.readlines()
    mochila = int(texto[0])
    for linha in texto[2:]:
        linha_split=linha.split(",")
        linha_split[2]=linha_split[2][:-1]
        itens.append([int(linha_split[2]),int(linha_split[1])])
    arq.close()

    tam_pop=10
    qde_geracoes=50
    tx_mutacao=0.1
    tx_cruzamento=0.7
    dispersao=[]
    n_aplicacoes = 11

    for t in range(n_aplicacoes):
        populacao=[]
        individuo=[[0,0]]
        convergencia=[]
        valor_minimo=[]

        #gerando melhor individuo com guloso
        #populacao.append(funcoes.guloso(itens,mochila))
        #fim

        #gerando o restante da populacao inicial
        for i in range(tam_pop):
            populacao.append(funcoes.populacao_aleatoria(itens,mochila))
        #fim

        g=0
        #funcoes.imprime_geracao(populacao,g)

        # armazenando possiveis candidatos
        convergencia.append(max(funcoes.verifica_candidatos(populacao, mochila)))
        valor_minimo.append(min(funcoes.verifica_candidatos(populacao, mochila)))
        # fim

        for g in range(qde_geracoes):

            populacao_e=funcoes.elitismo(populacao, mochila)
            populacao_c=funcoes.cruzamento(populacao,itens,tx_cruzamento)
            populacao=deepcopy(populacao_e)+deepcopy(populacao_c)
            #funcoes.imprime_cruzamento(populacao_c, g+1)

            populacao_m=funcoes.mutacao(populacao,itens,tx_mutacao)
            populacao=deepcopy(populacao_e)+deepcopy(populacao_m)+deepcopy(populacao_c)
            #funcoes.imprime_mutacao(populacao_m, g+1)

            populacao_s=funcoes.selecao(populacao,mochila,tam_pop)
            populacao=deepcopy(populacao_e)+deepcopy(populacao_s)
            #funcoes.imprime_geracao(populacao, g+1)
            #print("Melhor individuo" + str(g+1) + ": " + str(funcoes.elitismo(populacao, mochila)[0][0]))

            # armazenando possiveis candidatos
            convergencia.append(max(funcoes.verifica_candidatos(populacao, mochila)))
            valor_minimo.append(min(funcoes.verifica_candidatos(populacao, mochila)))
            # fim

        melhor_solucao = funcoes.elitismo(populacao, mochila)
        melhor_solucao[0][0].pop()
        print("Melhor Solução" + str(t+1) + ": " + str(melhor_solucao)[2:-1])
        dispersao.append(max(convergencia))

        # plota curvas de convergencia
        if t==0:
            plt.figure('Convergencias' + str(instancia), figsize=(12, 10 * n_aplicacoes))
        plt.subplot(n_aplicacoes, 1, t+1)
        plt.plot(convergencia, 'b')
        plt.plot(valor_minimo, 'r')
        plt.xlabel("Geracoes")
        plt.ylabel(str(funcoes.elitismo(populacao, mochila)[0][0][0]))
        # fim

    # plota boxplots das geracoes
    fig = plt.figure('Dispercao' + str(instancia), figsize=(10, 6))
    ax = fig.add_subplot(111)
    plt.xlabel('Dispersao: ' + str(min(dispersao)) + '~' + str(max(dispersao)) + '\n' + str(dispersao))
    plt.ylabel("Melhores Solucoes x 11")
    bp = ax.boxplot(dispersao)
plt.show()
    # fim