import numpy as np


class CUCB:

    def __init__(self, M, K, N, rho, q) -> None:
        self.M = M 
        self.N = N
        self.K = K

        self.rho = rho
        self.q = q

    def set_results_dictionary(self, result_dict):
        self.results = result_dict

    def update_rule(self, t, mu_hat, T_i):
        # Ponderador (página 7)
        sum_part = np.sqrt((3 * np.log(t)) / (2 * T_i + 1e-9))

        # Formula final
        mu_bar = np.min([mu_hat + sum_part, np.ones(self.M)], axis=0)
        # mu_bar = mu_obs + sum_part

        return mu_bar

    def update_mu_hat_t_i(self, S, X_T, t, S_T):
        # x = [
        #     np.random.binomial(N, rho[i]) / N \
        #         if bool(S[i]) else np.random.binomial(N, q[i] * rho[i]) / N 
        #         for i in range(M)
        # ]

        x = np.zeros(self.M)

        for i in range(self.M):
            if bool(S[i]):
                x[i] = np.random.binomial(self.N, self.rho[i]) / self.N
            else:
                x[i] = np.random.binomial(self.N, self.rho[i] * self.q[i]) / self.N

        X_T[t - 1] = x

        mu_hat = np.ma.array(X_T[:t], mask=~S_T[:t].astype(bool)).mean(axis=0).data
        # mu_hat = X_T[:t].mean(axis=0)
        # mu_hat[mu_hat == 0] = 1
        return mu_hat

    def oracle(self, mu_bar):
        idx = np.flip(np.argsort(mu_bar))[:self.K]

        S = np.zeros(self.M)
        S[idx] = 1

        return S


class UCB1:
    def __init__(self, M, K, N, q, rho) -> None:
        self.M = M
        self.K = K
        
        self.rho = rho
        self.N = N
        self.q = q

    def initialization(self, T_i):

        x = [
            (np.random.binomial(self.N, self.rho[i]) / self.N) + 1e-11\
                for i in range(self.M)
        ]

        T_i += 1

        mu_hat = x

        return mu_hat

    def oracle(self, mu_hat, t, T_i):
        
        sum_terms = mu_hat + np.sqrt((2 * np.log(t)) / T_i)

        arg_max = np.argmax(sum_terms)

        a = np.zeros(self.M)
        a[arg_max] = 1

        return a

    def update_mu_hat(self, X_T, a, t, A_T):
                # x = [
        #     np.random.binomial(N, rho[i]) / N \
        #         if bool(S[i]) else np.random.binomial(N, q[i] * rho[i]) / N 
        #         for i in range(M)
        # ]

        x = np.zeros(self.M)

        for i in range(self.M):
            if bool(a[i]):
                x[i] = np.random.binomial(self.N, self.rho[i]) / self.N
            else:
                x[i] = np.random.binomial(self.N, self.rho[i] * self.q[i]) / self.N

        X_T[t - 1] = x

        mu_hat = np.ma.array(X_T[:t], mask=~A_T[:t].astype(bool)).mean(axis=0).data
        # mu_hat = X_T[:t].mean(axis=0)
        # mu_hat[mu_hat == 0] = first_mu_hat[mu_hat == 0]
        
        return mu_hat
        
    


class LLR:
    def __init__(self, M, K, N, q, rho, underreporting=False) -> None:
        self.M = M
        self.K = K
        
        # Si hay subreporte se alcanza cualquiera, si no lo hay solo se llega a 
        # los brazos activados
        self.L = M if underreporting else K

        self.rho = rho
        self.N = N
        self.q = q



    def initialization(self, T_i):

        x = [
            (np.random.binomial(self.N, self.rho[i]) / self.N) + 1e-11\
                for i in range(self.M)
        ]

        T_i += 1

        mu_hat = x

        return mu_hat

    
    def oracle(self, mu_hat, t, T_i):
        
        sum_terms = mu_hat + np.sqrt(((self.L + 1) * np.log(t)) / T_i)

        idx_sorted_terms = np.flip(np.argsort(sum_terms))[:self.K]

        a = np.zeros(self.M)
        a[idx_sorted_terms] = 1

        return a

    def update_mu_hat(self, X_T, a, t, A_T):
                # x = [
        #     np.random.binomial(N, rho[i]) / N \
        #         if bool(S[i]) else np.random.binomial(N, q[i] * rho[i]) / N 
        #         for i in range(M)
        # ]

        x = np.zeros(self.M)

        for i in range(self.M):
            if bool(a[i]):
                x[i] = np.random.binomial(self.N, self.rho[i]) / self.N
            else:
                x[i] = np.random.binomial(self.N, self.rho[i] * self.q[i]) / self.N

        X_T[t - 1] = x

        mu_hat = np.ma.array(X_T[:t], mask=~A_T[:t].astype(bool)).mean(axis=0).data
        # mu_hat = X_T[:t].mean(axis=0)
        # mu_hat[mu_hat == 0] = first_mu_hat[mu_hat == 0]
        
        return mu_hat
        

    