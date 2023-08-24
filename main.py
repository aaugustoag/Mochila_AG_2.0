import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
import funcoes
from copy import deepcopy

#        0     1     2     3     4     5     6     7     8     9     10    11
#itens2=[[3,5],[7,2],[4,5],[6,8],[3,6],[6,6],[7,1],[1,7],[1,1],[3,3],[3,2],[4,1]]


#instancia = input('Selecione a instancia:\n1- 40 itens:\n2- 100 itens:\n3- 10.000 itens:\n4- 10.000-2 itens:\n5- 11.000 itens:\n6- 100.000 iten:\n')

#instancia = int(instancia)

for i in range(1):

    instancia = 3

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

    mochila, itens = funcoes.importa_txt(arq)
    arq.close()

    tam_pop=10
    qde_geracoes=50
    tx_mutacao=0.1
    tx_cruzamento=0.7
    n_aplicacoes = 4

    lista_convergencias = []
    lista_valor_minimo = []
    dispersao = []
    df_populacao = pd.DataFrame(columns = ["Aplicação", "Geração","Aptidão", "Indivíduo"])

    for t in range(n_aplicacoes):
        populacao_final = {}
        populacao=[]
        individuo=[[0,0]]
        convergencia=[]
        valor_minimo=[]
        populacao_valida=[]

        #gerando melhor individuo com guloso
        populacao.append(funcoes.guloso(itens,mochila))
        #fim

        #gerando a populacao inicial
        while len(populacao) < tam_pop:
            populacao.append(funcoes.populacao_aleatoria(itens,mochila))
        #fim

        print("\nAplicação ", (t+1) )
        #funcoes.imprime_geracao(populacao, 0)

        melhor_ind = (max(funcoes.verifica_candidatos(populacao, mochila)))
        df_populacao = df_populacao._append({"Aplicação": t + 1,
                                             "Geração": 0,
                                             "Aptidão": melhor_ind,
                                             "indivíduo": "População"},
                                            ignore_index=True)

        pior_ind = (min(funcoes.verifica_candidatos(populacao, mochila)))
        df_populacao = df_populacao._append({"Aplicação": t + 1,
                                             "Geração": 0,
                                             "Aptidão": pior_ind,
                                             "indivíduo": "População"},
                                            ignore_index=True)

        populacao_valida = (funcoes.verifica_candidatos(populacao, mochila))
        for ind in populacao_valida:
            df_populacao = df_populacao._append({"Aplicação":t+1,
                                                 "Geração":0,
                                                 "Aptidão":ind,
                                                 "Indivíduo":"População"},
                                                ignore_index=True)

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
            melhor_ind = (max(funcoes.verifica_candidatos(populacao, mochila)))
            df_populacao = df_populacao._append({"Aplicação": t + 1,
                                                 "Geração": g + 1,
                                                 "Aptidão": melhor_ind,
                                                 "indivíduo": "População"},
                                                ignore_index=True)

            pior_ind = (min(funcoes.verifica_candidatos(populacao, mochila)))
            df_populacao = df_populacao._append({"Aplicação": t + 1,
                                                 "Geração": g + 1,
                                                 "Aptidão": pior_ind,
                                                 "indivíduo": "População"},
                                                ignore_index=True)

            populacao_valida = (funcoes.verifica_candidatos(populacao, mochila))
            for ind in populacao_valida:
                df_populacao = df_populacao._append({"Aplicação": t + 1,
                                                     "Geração": g+1,
                                                     "Aptidão": ind,
                                                     "indivíduo": "População"},
                                                    ignore_index=True)

            #funcoes.imprime_geracao(populacao, g+1)
            # fim

        # imprime resultado
        melhor_solucao = funcoes.elitismo(populacao, mochila)
        melhor_solucao[0][0].pop()
        print("Melhor Solução " + str(t+1) + ":", melhor_solucao[0][0][1], "\nItens:", melhor_solucao[0][1:])
        # fim

# imprime gráficos
sns.relplot(df_populacao, x="Geração", y="Aptidão",
            col="Aplicação", col_wrap=math.ceil(n_aplicacoes/3),
            hue="Indivíduo", kind="line")
plt.show()
# fim