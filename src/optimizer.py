import scipy.optimize as sco
import numpy as np


def volatility(portifolio_weights,
               _expected_returns,
               returns_Covariance,
               _risk_free_rate):
    return np.sqrt(np.dot(portifolio_weights,
                          np.dot(returns_Covariance, portifolio_weights.T)))


def sharpe_ratio(portifolio_weights,
                 expected_returns,
                 returns_Covariance,
                 risk_free_rate):
    portifolio_returns = portifolio_weights.dot(expected_returns)
    returns_variance =\
        np.sqrt(np.dot(portifolio_weights,
                       np.dot(returns_Covariance, portifolio_weights.T)))
    return (portifolio_returns - risk_free_rate) / returns_variance


def get_weights_minimizing_metric(expected_returns, expected_Covariance_df, risk_free_rate, metric):
    # Equal weigts for each asset
    n_assets = len(expected_returns)
    assets = list(expected_Covariance_df.columns)
    initial_weigts_guess = np.array([1 / n_assets] * n_assets)
    cost_function_args = (
        expected_returns, expected_Covariance_df, risk_free_rate)

    result = sco.minimize(
        metric,
        x0=initial_weigts_guess,
        args=cost_function_args,
        method="SLSQP",
        bounds=tuple((0, 1) for _ in range(n_assets)),
        constraints=[{"type": "eq", "fun": lambda x: np.sum(x) - 1}],
    )

    return dict(zip(assets, result['x']))
