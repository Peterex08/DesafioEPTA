import numpy as np
import math

def quat2eulers(q: np.ndarray) -> tuple:
    q0, q1, q2, q3 = q  # Desempacotando o array para os quatérnions

    roll = math.atan2(
        2 * ((q2 * q3) + (q0 * q1)),
        q0**2 - q1**2 - q2**2 + q3**2
    )  # radians

    pitch = math.asin(2 * ((q1 * q3) - (q0 * q2)))

    yaw = math.atan2(
        2 * ((q1 * q2) + (q0 * q3)),
        q0**2 + q1**2 - q2**2 - q3**2
    )

    return (np.degrees([roll, pitch, yaw]))
