from random import randint
from copy import deepcopy

# imprimindo geração
def imprime_geracao (populacao, g):
    print("Geração" + str(g) + "(" + str(len(populacao)) + "):" + str([item[0] for item in populacao]))
# fim

# imprimindo geração
def imprime_cruzamento (populacao, g):
    print("Cruzamento" + str(g) + "(" + str(len(populacao)) + "):" + str([item[0] for item in populacao]))
# fim

# imprimindo geração
def imprime_mutacao (populacao, g):
    print("Mutação" + str(g) + "(" + str(len(populacao)) + "):" + str([item[0] for item in populacao]))
# fim

# verificando possiveis candidatos
def verifica_candidatos (populacao, mochila):
    candidatos = []
    for i, ind in enumerate(populacao):
        if ind[0][1] <= mochila:
            candidatos.append(deepcopy(ind[0][0]))
    if len(candidatos) == 0:
        return 0
    return candidatos
# fim

# gerando individuo guloso
def guloso (itens, mochila):
    individuo = [[0, 0, 0]]
    while individuo[0][1] < mochila:
        maior = [0, 1]
        for i, item in enumerate(itens):
            if not (i in individuo):
                if (item[0] / item[1] > maior[0] / maior[1]):
                    maior = item
                    maior_indice = i
        individuo.append(maior_indice)
        individuo[0][0] += maior[0]
        individuo[0][1] += maior[1]
    individuo[0][0] -= itens[individuo[-1]][0]
    individuo[0][1] -= itens[individuo[-1]][1]
    individuo.pop()
    return individuo
# fim

# gerando individuo aleatorio
def populacao_aleatoria (itens, mochila):
    individuo = [[0, 0, 0]]
    item = 0
    while individuo[0][1] < mochila:
        item = randint(0, int(len(itens))-1)
        if not (item in individuo):
            individuo.append(item)
            individuo[0][0] += itens[item][0]
            individuo[0][1] += itens[item][1]
    if individuo[0][1] > mochila:
        individuo.remove(item)
        individuo[0][0] -= itens[item][0]
        individuo[0][1] -= itens[item][1]
    return individuo
# fim

# escolhendo o melhor individuo (elitismo)
def elitismo (populacao, mochila):
    populacao_e = []
    maior = [0, 0]
    maior_indice = 0
    for i, ind in enumerate(populacao):
        if (ind[0][1] <= mochila):
            if (ind[0][0] > maior[0]):
                maior = ind[0]
                maior_indice = i
    populacao_e.append(deepcopy(populacao[maior_indice]))
    return populacao_e
# fim

# fazendo cruzamento
def cruzamento (populacao, itens, tx_cruzamento):
    populacao_c = []
    while len(populacao) > 1:
        rand = randint(0,len(populacao)-1)
        populacao_c.append(populacao[rand])
        populacao_c.append(populacao[(rand+1)%len(populacao)])
        populacao.remove(populacao_c[-1])
        populacao.remove(populacao_c[-2])
        if randint(0, 99) <= tx_cruzamento * 100:
            filhos = []
            filhos.append(populacao_c[-1])
            filhos.append(populacao_c[-2])
            qde_cromossomos = 10
            #print("pai" + str(filhos))
            for i in range(qde_cromossomos):
                for cromossomo in filhos[0][1:]:
                    if not (cromossomo in filhos[1][1:]):
                        filhos[1].append(cromossomo)
                        filhos[1][0][0] += itens[cromossomo][0]
                        filhos[1][0][1] += itens[cromossomo][1]
                        filhos[0].remove(cromossomo)
                        filhos[0][0][0] -= itens[cromossomo][0]
                        filhos[0][0][1] -= itens[cromossomo][1]
                        break
                for cromossomo in filhos[1][1:]:
                    if not (cromossomo in filhos[0][1:]):
                        filhos[0].append(cromossomo)
                        filhos[0][0][0] += itens[cromossomo][0]
                        filhos[0][0][1] += itens[cromossomo][1]
                        filhos[1].remove(cromossomo)
                        filhos[1][0][0] -= itens[cromossomo][0]
                        filhos[1][0][1] -= itens[cromossomo][1]
                        break
            populacao_c.append(deepcopy(filhos[0]))
            populacao_c.append(deepcopy(filhos[1]))
    if len(populacao) > 0:
        populacao_c.append(populacao[0])

    return populacao_c
# fim

# fazendo mutacao
def mutacao (populacao, itens, tx_mutacao):
    populacao_m = []
    for ind in populacao:
        if randint(0, 99) <= tx_mutacao * 100:
            mutante = deepcopy(ind)
            qde_cromossomos = 10
            cromossomo = randint(0, len(itens)-1)
            for i in range(qde_cromossomos):
                if int((cromossomo + i * qde_cromossomos) % len(itens)) in mutante:
                    mutante.remove(int((cromossomo + i * qde_cromossomos) % len(itens)))
                    mutante[0][0] -= itens[int((cromossomo + i * qde_cromossomos) % len(itens))][0]
                    mutante[0][1] -= itens[int((cromossomo + i * qde_cromossomos) % len(itens))][1]
                else:
                    mutante.append(int((cromossomo + i * qde_cromossomos) % len(itens)))
                    mutante[0][0] += itens[int((cromossomo + i * qde_cromossomos) % len(itens))][0]
                    mutante[0][1] += itens[int((cromossomo + i * qde_cromossomos) % len(itens))][1]
            populacao_m.append(deepcopy(mutante))
        else:
            populacao_m.append(deepcopy(ind))

    return populacao_m
# fim

# fazendo competicao roleta x1
def selecao (populacao, mochila, tam_pop):
    populacao_s = []
    populacao_aux = []
    valor_acumulado = 0
    maior_v = 0
    maior_p = 0

    for ind in populacao:
        ind[0][2] = 0
        if ind[0][0] > maior_v:
            maior_v = ind[0][0]
        menor_v = maior_v
        if ind[0][0] < menor_v:
            menor_v = ind[0][0]
        if ind[0][1] > maior_p:
            maior_p = ind[0][1]

    populacao = (sorted(populacao, reverse=True))

    #funcao aptidao
    for i,ind in enumerate(populacao):
        if i > 0:
            if sorted(populacao[i][1:]) != sorted(populacao[i-1][1:]):
                if ind[0][1] > mochila:
                    ind[0][2] = int(menor_v * ind[0][0] / maior_v / (ind[0][1] - mochila +1) + menor_v/10)
                    #print(ind, menor_v, int(menor_v * ind[0][0] / maior_v / (ind[0][1] - mochila) + menor_v/10), valor_acumulado)
                else:
                    ind[0][2] = int(ind[0][0] + menor_v/10)
                    #print(ind, menor_v, int(ind[0][0] + menor_v/10), valor_acumulado)
                valor_acumulado += ind[0][2]
                ind[0][2] = valor_acumulado
                populacao_aux.append(deepcopy(ind))
        else:
            if ind[0][1] > mochila:
                ind[0][2] = int(menor_v * ind[0][0] / maior_v / (ind[0][1] - mochila +1) + menor_v/10)
                #print(ind, menor_v, int(menor_v * ind[0][0] / maior_v / (ind[0][1] - mochila) + menor_v/10), valor_acumulado)
            else:
                ind[0][2] = int(ind[0][0] + menor_v/10)
                #print(ind, menor_v, int(ind[0][0] + menor_v/10), valor_acumulado)
            valor_acumulado += ind[0][2]
            ind[0][2] = valor_acumulado
            populacao_aux.append(deepcopy(ind))

    #print("aux" + str(populacao_aux))

    #selecao por roleta de 1
    vitorioso = 0
    while len(populacao_s) < tam_pop-1:
        vitorioso = (vitorioso + randint(0, int(valor_acumulado / 2))) % valor_acumulado
        for ind in populacao:
            if ind[0][2] >= vitorioso:
                populacao_s.append(ind)
                break

    while len(populacao_s) > tam_pop-1:
        populacao_s.pop()

    return populacao_s
# fim