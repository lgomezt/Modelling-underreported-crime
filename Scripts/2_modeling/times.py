import numpy as np
import pandas as pd

from tqdm import tqdm
from discovery import Chen, LLR, UCB1


def run_ucb1(distances, T_max, M, K, N, q, rho):
    
    ucb1 =  UCB1(M, K, N, q, rho)
    # Total number of times arm i is played so far
    T_i = np.zeros(M)

    # Mean outcomes

    X_T = np.zeros((T_max, M))

    S_T = np.zeros((T_max, M))

    historical_mu_hat = np.zeros((T_max, M))

    mu_hat = ucb1.initialization(T_i)

    historical_q_hat =  np.zeros((T_max, M))
    for t in tqdm(range(T_max)):
        t += 1

        # save historical mu_hat's
        historical_mu_hat[t - 1] = mu_hat
        q_temp = np.ma.array(X_T[:t], mask=S_T[:t].astype(bool)).mean(axis=0).data
        
        cond_temp = mu_hat == 0
        historical_q_hat[t - 1][cond_temp] = 0
        historical_q_hat[t - 1][~cond_temp] = q_temp[~cond_temp] / mu_hat[~cond_temp]
        #oracle
        a = ucb1.oracle(mu_hat, t, T_i)

        # 0-index
        S_T[t - 1] = a
        T_i[a.astype(bool)] += 1
        
        # update m_hat, t_i
        mu_hat = ucb1.update_mu_hat(X_T, a, t, S_T)

    distances['UCB1'] = np.linalg.norm(historical_mu_hat - np.tile(rho, (T_max, 1)), axis=1)


def run_llr(distances, T_max, M, K, N, q, rho):
    llr = LLR(M, K, N, q, rho, underreporting=False)
    # Total number of times arm i is played so far
    T_i = np.zeros(M)

    # Mean outcomes

    X_T = np.zeros((T_max, M))

    S_T = np.zeros((T_max, M))

    historical_mu_hat = np.zeros((T_max, M))

    mu_hat = llr.initialization(T_i)

    historical_q_hat =  np.zeros((T_max, M))

    for t in tqdm(range(T_max)):
        t += 1

        # save historical mu_hat's
        historical_mu_hat[t - 1] = mu_hat
        q_temp = np.ma.array(X_T[:t], mask=S_T[:t].astype(bool)).mean(axis=0).data
        
        cond_temp = mu_hat == 0
        historical_q_hat[t - 1][cond_temp] = 0
        historical_q_hat[t - 1][~cond_temp] = q_temp[~cond_temp] / mu_hat[~cond_temp]
        #oracle
        a = llr.oracle(mu_hat, t, T_i)

        # 0-index
        S_T[t - 1] = a
        T_i[a.astype(bool)] += 1
        
        # update m_hat, t_i
        mu_hat = llr.update_mu_hat(X_T, a, t, S_T)
        if np.linalg.norm(mu_hat - rho) <= .05:
            break


    distances['LLR'] = np.linalg.norm(historical_mu_hat - np.tile(rho, (T_max, 1)), axis=1)


def run_chen(distances, T_max, M, K, N, rho, q):

    chen = Chen(M, K, N, rho, q)
    # Total number of times arm i is played so far
    T_i = np.zeros(M)

    # Mean outcomes
    mu_hat = np.ones(M)

    X_T = np.zeros((T_max, M))

    S_T = np.zeros((T_max, M))

    historical_mu_hat = np.zeros((T_max, M))

    historical_mu_bar = np.zeros((T_max, M))
    historical_q_hat =  np.zeros((T_max, M))
    for t in tqdm(range(T_max)):
        t += 1

        # save historical mu_hat's
        historical_mu_hat[t - 1] = mu_hat
        q_temp = np.ma.array(X_T[:t], mask=S_T[:t].astype(bool)).mean(axis=0).data

        cond_temp = mu_hat == 0
        historical_q_hat[t - 1][cond_temp] = 0
        historical_q_hat[t - 1][~cond_temp] = q_temp[~cond_temp] / mu_hat[~cond_temp]

        # update rule
        mu_bar = chen.update_rule(t, mu_hat, T_i)
        historical_mu_bar[t - 1] = mu_bar
        
        #oracle
        S = chen.oracle(mu_bar)

        # 0-index
        S_T[t - 1] = S
        T_i[S.astype(bool)] += 1
        
        # update m_hat, t_i
        mu_hat = chen.update_mu_hat_t_i(S, X_T, t, S_T)

        if np.linalg.norm(mu_hat - rho) <= .05:
            break

    distances['Chen'] = np.linalg.norm(historical_mu_hat - np.tile(rho, (T_max, 1)), axis=1)

# Ms = [1000, 10000, 50000]
Ms = [10000, 50000]



for M in Ms:
    # Definimos la semilla para la replicabilidad del código
    np.random.seed(123)

    # Cantidad de brazos (o policías)
    K = int(M * 0.1)
    # Períodos de tiempo
    T_max = 5000
    # Probabilidad de observar el crimen perfectamente en los cuadrantes no visitados
    p = 0
    # Media del crimen por cudrante
    mu_reales = np.random.randint(low = 4, high = 100, size = M)
    # Ahora vamos a encontrar rho que es la probabilidad de éxito de nuestra binomial
    # N puede ser cualquier cosa pero dejamos un número interpretable
    N = 1000
    rho = mu_reales / N

    q = np.random.uniform(size=M)
    # q = .5 * np.ones(M)

    chen = Chen(M, K, N, rho, q)

    distances = pd.DataFrame(index=np.arange(T_max))
    # if M == 1000:
    run_ucb1(distances, T_max, M, K, N, q, rho)

    run_llr(distances, T_max, M, K, N, q, rho)

    run_chen(distances, T_max, M, K, N, rho, q)


    # distances.to_csv(f'distance_{M}.csv', index=False)
    distances.to_csv(f'distance_{M}_con_UCB1.csv', index=False)

