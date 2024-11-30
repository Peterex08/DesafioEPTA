import numpy as np
 
def quaternion_rotation_matrix(Q):

    norm = Q/np.linalg.norm(Q)

    q0 = norm[0]
    q1 = norm[1]
    q2 = norm[2]
    q3 = norm[3]
     
    rot_matrix = np.array([[1 - 2 * (q2**2 + q3**2), 2 * (q1 * q2 - q0 * q3), 2 * (q1 * q3 + q0 * q2)],
        [2 * (q1 * q2 + q0 * q3), 1 - 2 * (q1**2 + q3**2), 2 * (q2 * q3 - q0 * q1)],
        [2 * (q1 * q3 - q0 * q2), 2 * (q2 * q3 + q0 * q1), 1 - 2 * (q1**2 + q2**2)]])
                            
    return rot_matrix