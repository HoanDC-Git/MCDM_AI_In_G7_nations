import numpy as np

def calculate_critic_weights(matrix, types):
    """
    Computes CRITIC weights and returns all intermediate steps.
    
    Parameters:
        matrix (np.ndarray): Decision matrix (m alternatives x n criteria).
        types (np.ndarray): Criterion types (1 for benefit, -1 for cost).
        
    Returns:
        weights (np.ndarray): Normalized weights for each criterion.
        norm_matrix (np.ndarray): Normalized decision matrix.
        std_devs (np.ndarray): Standard deviations of each criterion.
        corr_matrix (np.ndarray): Correlation matrix between criteria.
        conflict (np.ndarray): Conflict measure (sum of 1 - correlation).
        info_c (np.ndarray): Quantity of information (C = std * conflict).
    """
    m, n = matrix.shape
    norm_matrix = np.empty_like(matrix, dtype=float)
    
    # 1. Normalize the decision matrix
    for j in range(n):
        col = matrix[:, j]
        col_min = np.min(col)
        col_max = np.max(col)
        if col_max == col_min:
            norm_matrix[:, j] = 1.0 # Avoid division by zero
        else:
            if types[j] == -1: # Cost / Non-benefit criterion
                norm_matrix[:, j] = (col_max - col) / (col_max - col_min)
            else: # Benefit criterion
                norm_matrix[:, j] = (col - col_min) / (col_max - col_min)
                
    # 2. Standard deviation of criteria
    std_devs = np.std(norm_matrix, axis=0)
    
    # 3. Correlation matrix
    corr_matrix = np.corrcoef(norm_matrix, rowvar=False)
    # Handle single criterion edge case (returns scalar instead of matrix)
    if n == 1:
        corr_matrix = np.array([[1.0]])
        
    # 4. Conflict measure
    conflict = np.sum(1.0 - corr_matrix, axis=1)
    
    # 5. Quantity of information (C)
    info_c = std_devs * conflict
    
    # 6. Normalize to get weights
    sum_info = np.sum(info_c)
    if sum_info == 0:
        weights = np.ones(n) / n
    else:
        weights = info_c / sum_info
        
    return weights, norm_matrix, std_devs, corr_matrix, conflict, info_c


def calculate_topsis(matrix, weights, types):
    """
    Computes TOPSIS scores and returns all intermediate steps.
    
    Parameters:
        matrix (np.ndarray): Decision matrix (m alternatives x n criteria).
        weights (np.ndarray): Normalized weights for each criterion.
        types (np.ndarray): Criterion types (1 for benefit, -1 for cost).
        
    Returns:
        scores (np.ndarray): Closeness coefficient (TOPSIS scores) for each alternative.
        norm_matrix (np.ndarray): Vector normalized matrix.
        weighted_matrix (np.ndarray): Weighted normalized matrix.
        pis (np.ndarray): Positive Ideal Solution (PIS).
        nis (np.ndarray): Negative Ideal Solution (NIS).
        dist_pis (np.ndarray): Separation distance to PIS (S+).
        dist_nis (np.ndarray): Separation distance to NIS (S-).
    """
    m, n = matrix.shape
    
    # 1. Vector normalization
    col_norms = np.sqrt(np.sum(matrix**2, axis=0))
    # Avoid division by zero
    col_norms[col_norms == 0] = 1.0
    norm_matrix = matrix / col_norms
    
    # 2. Weighted normalized decision matrix
    weighted_matrix = norm_matrix * weights
    
    # 3. Positive and Negative Ideal Solutions (PIS & NIS)
    pis = np.zeros(n)
    nis = np.zeros(n)
    for j in range(n):
        col = weighted_matrix[:, j]
        if types[j] == 1: # Benefit
            pis[j] = np.max(col)
            nis[j] = np.min(col)
        else: # Cost / Non-benefit
            pis[j] = np.min(col)
            nis[j] = np.max(col)
            
    # 4. Separation measures
    dist_pis = np.sqrt(np.sum((weighted_matrix - pis)**2, axis=1))
    dist_nis = np.sqrt(np.sum((weighted_matrix - nis)**2, axis=1))
    
    # 5. Closeness coefficient (TOPSIS score)
    sum_dist = dist_pis + dist_nis
    # Avoid division by zero if an alternative is exactly on both PIS and NIS
    scores = np.zeros(m)
    non_zero = sum_dist > 0
    scores[non_zero] = dist_nis[non_zero] / sum_dist[non_zero]
    
    return scores, norm_matrix, weighted_matrix, pis, nis, dist_pis, dist_nis
