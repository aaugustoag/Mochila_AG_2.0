from random import randint
from copy import deepcopy

# imprimindo geração
def imprime_geracao (populacao, g):
    print("Geração" + str(g) + "(" + str(len(populacao)) + "):" + str([item[0] for item in populacao]))
# fim

# imprimindo cruzamento
def imprime_cruzamento (populacao, g):
    print("Cruzamento" + str(g) + "(" + str(len(populacao)) + "):" + str([item[0] for item in populacao]))
# fim

# imprimindo mutação
def imprime_mutacao (populacao, g):
    print("Mutação" + str(g) + "(" + str(len(populacao)) + "):" + str([item[0] for item in populacao]))
# fim

# gerando individuo aleatorio
def populacao_aleatoria (itens, mochila):
    individuo = [[0, 0, 0, 0, 0]]
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
            qde_cromossomos = int(len(filhos[0])/5)+1
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
            qde_cromossomos = int(len(mutante)/5)+1
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

#################################################################
# beneficio do individuo
def valor (individuo):
  return individuo[0][0]

# peso do individuo
def peso (individuo):
  return individuo[0][1]

# aptidao beneficio do individuo
def apt_valor (individuo):
  return individuo[0][2]

# aptidao peso do individuo
def apt_peso (individuo):
  return individuo[0][3]

# aptidao peso do individuo
def dist (individuo):
  return individuo[0][4]

# funcao aptidao
def aptidao (populacao, mochila):
    maior_v = max(populacao,key=valor)[0][0]
    maior_p = max(populacao,key=peso)[0][1]
    menor_p = min(populacao,key=peso)[0][1]
    for ind in populacao:
        ind[0][2] = int((ind[0][0]*(-1) + maior_v) / maior_v * 1000)
        ind[0][3] = int((ind[0][1] - menor_p) / (menor_p + 1) * 1000)
        if ind[0][1] > mochila:
            ind[0][2] += int((ind[0][1] - mochila) / maior_p * 1000)
            ind[0][3] += int((ind[0][1] - mochila) / maior_p * 1000)
    return populacao

# selecao do pareto
def pareto (populacao,mochila):
    populacao = aptidao(populacao, mochila)
    pareto = []
    i=0
    populacao_p = []
    for ind in populacao:
        ind[1:] = sorted(ind[1:])
        if not(ind in populacao_p):
            populacao_p.append(ind)
    while len(populacao_p) > 0:
        i+=1
        px = []
        for ind in populacao_p:
            px.append(ind)
            for ind0 in px:
                if (ind[0][2] < ind0[0][2]) and (ind[0][3] < ind0[0][3]):
                    px.remove(ind0)
                if (ind[0][2] > ind0[0][2]) and (ind[0][3] > ind0[0][3] and ind in px):
                    px.remove(ind)
        pareto.append(px)
        for ind in px:
            populacao_p.remove(ind)
        #print("\nPareto"+str(i)+":\n"+str(px))
    return pareto

def distancia (front):
    front = sorted(front,key=apt_peso)
    front = sorted(front,key=apt_valor)
    front[0][0][4] = float("inf")
    front[-1][0][4] = float("inf")
    #print(len(front),front[1:-1])
    for i, ind in enumerate(front[1:-1]):
        ind[0][4] = (front[i-1][0][2] - front[i+1][0][2])**2 + (front[i-1][0][3] - front[i+1][0][3])**2
        #if dist == 0:
            #front.remove(ind)
        #print(front[i-1],ind,front[i+1])
    return front

def selecao (pareto, tam_pop):
    populacao = []
    for front in pareto:
        front = distancia(front)
        front = sorted(front,key=dist,reverse=True)
        for ind in front:
            if len(populacao) >= tam_pop:
                break
            populacao.append(ind)
        if len(populacao) >= tam_pop:
            break
    return populacao