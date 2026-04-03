"""
Constraint verification module.
"""


def check_constraint(disparity, epsilon=0.05):
    """
    Verify if disparity satisfies the fairness constraint.

    Args:
        disparity: Computed disparity value
        epsilon: Maximum allowed disparity threshold

    Returns:
        True if constraint is satisfied, False otherwise
    """
    return disparity <= epsilon
