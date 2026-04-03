"""
Fairness checking module for demographic parity.
"""
import numpy as np


def demographic_parity(y_pred, group):
    """
    Calculate demographic parity disparity between two groups.

    Measures the absolute difference in positive prediction rates
    between group 0 and group 1.

    Args:
        y_pred: Binary predictions array
        group: Group membership array (0 or 1)

    Returns:
        Absolute disparity value
    """
    g0 = y_pred[group == 0]
    g1 = y_pred[group == 1]

    dp0 = np.mean(g0) if len(g0) > 0 else 0
    dp1 = np.mean(g1) if len(g1) > 0 else 0

    return abs(dp0 - dp1)
