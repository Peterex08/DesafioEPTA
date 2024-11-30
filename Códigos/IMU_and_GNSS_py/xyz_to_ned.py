import numpy as np
from scipy.spatial.transform import Rotation
from ahrs.filters import SAAM, Madgwick, Mahony
from ahrs import DCM
from quat2rotmatrix import quaternion_rotation_matrix
from rpy import quat2eulers

quat = np.array([0.7071, 0.0, 0.7071, 0.0])

def xyztoned(accel, gyro, magneto, time):
    AcX, AcY, AcZ = accel
    GyX, GyY, GyZ = gyro
    MgX, MgY, MgZ = magneto

    npaccel = np.array(accel)
    npgyro = np.array(gyro)
    npmagneto = np.array(magneto)

    roll = np.arctan2(AcY, AcZ)
    pitch = np.arctan2(-AcX, np.sqrt(AcY**2 + AcZ**2))
    yaw = -np.arctan2(MgY*np.cos(roll) - MgZ*np.sin(roll), MgX*np.cos(pitch) + MgY*np.sin(pitch)*np.sin(roll) + MgZ*np.sin(pitch)*np.cos(roll))

    #quat = Rotation.from_euler('xyz', [roll, pitch, yaw], degrees = False).as_quat()

    global quat

    #quat = Madgwick().updateMARG(quat, gyr = npgyro, acc = npaccel, mag = npmagneto)

    quat = SAAM().estimate(accel, magneto)

    rotmatrix = quaternion_rotation_matrix(quat)

    #rotmatrix = DCM(q = quat)

    #v = np.array([[0],[0],[1]])
    
    invrotmatrix = rotmatrix.T

    accshape = npaccel.reshape(3,1)

    test = (invrotmatrix @ accshape)
    #eulers = quat2eulers(quat)

    print(np.round(test, 2))



    