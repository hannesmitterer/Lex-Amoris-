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
        group: Group membership array (must contain only 0 or 1)

    Returns:
        Absolute disparity value

    Raises:
        ValueError: If group contains values other than 0 or 1
    """
    unique_groups = np.unique(group)
    if not np.all(np.isin(unique_groups, [0, 1])):
        raise ValueError(f"Group must contain only 0 or 1, found: {unique_groups}")

    g0 = y_pred[group == 0]
    g1 = y_pred[group == 1]

    dp0 = np.mean(g0) if len(g0) > 0 else 0
    dp1 = np.mean(g1) if len(g1) > 0 else 0

    return abs(dp0 - dp1)
