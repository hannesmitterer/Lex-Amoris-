"""
Constraint verification module.
"""


def check_constraint(disparity, epsilon=0.05):
    """
    Verify if disparity satisfies the fairness constraint.

    Args:
        disparity: Computed disparity value (must be non-negative)
        epsilon: Maximum allowed disparity threshold

    Returns:
        True if constraint is satisfied, False otherwise

    Note:
        Disparity values are expected to be non-negative (absolute differences).
        The demographic_parity function returns abs(dp0 - dp1).
    """
    if disparity < 0:
        raise ValueError(f"Disparity must be non-negative, got {disparity}")
    return disparity <= epsilon
