import numpy as np
np.set_printoptions(suppress=True)
np.set_printoptions(precision=6)

from math import *

# https://docs.ros.org/en/noetic/api/sensor_msgs/html/msg/Imu.html
# https://github.com/ethz-asl/kalibr/wiki/Bag-format

# imu shoule be t(ns) g(rad/s) a(m/s2)
if __name__ == '__main__':
    imu_file = "adis.txt"
    gps_week = 2257   #!!!!!!! change here, check http://www.igs.gnsswhu.cn/index.php/home/data_product/igs.html
    
    start_sec, end_sec = 284450, 284680
    start_sec, end_sec = 284431, 284700

    imu_data = np.loadtxt(imu_file)
    imu_dt = imu_data[1:,0] - imu_data[0:-1,0]
    imu_rate = round(1/np.mean(imu_dt))
    imu_dt = float(imu_rate)
    print("IMU rate was detected as "+str(imu_rate)+" Hz.")


    deg2rad = pi/180.0
    rad2deg = 180.0/pi

    imu_t_idx = [0]
    imu_t_data = imu_data[:,imu_t_idx]
    valid_idx = np.where((imu_t_data[:,0]>=start_sec) & (imu_t_data[:,0]<=end_sec))[0]

    imu_data = imu_data[valid_idx,:]
    imu_t_idx = [0]
    imu_t_data = imu_data[:,imu_t_idx]
    # https://zhuanlan.zhihu.com/p/383645111
    err = 315964800 # start time difference

    # http://www.leapsecond.com/java/gpsclock.htm
    leapsec = 18 #GPS time was zero at 0h 6-Jan-1980 and since it is not perturbed by leap seconds GPS is now ahead of UTC by 18 seconds.

    imu_t_data = imu_t_data + gps_week * 86400 * 7 + err - leapsec
    imu_t_data = np.round(imu_t_data*1e5)
    # imu_t_data = imu_t_data * 1e9

    # 1: deg/s, 2: rad/s 3: deg 4: rad/s
    imu_g_unit = 1
    imu_g_xyz_idx = [1,2,3]
    imu_g_data = imu_data[:,imu_g_xyz_idx]
    if imu_g_unit == 1:
        imu_g_data = imu_g_data*deg2rad
    elif imu_g_unit == 3:
        imu_g_data = imu_g_data*deg2rad/imu_dt
    elif imu_g_unit == 4:
        imu_g_data = imu_g_data/imu_dt

    # 1: m/s2, 2: m/s
    imu_a_unit = 1
    imu_a_xyz_idx = [4,5,6]
    imu_a_data = imu_data[:,imu_a_xyz_idx]
    if imu_a_unit == 2:
        imu_a_data = imu_a_data/imu_dt

    with open("imu0.csv","w") as f:
        idx = 0
        num = np.shape(imu_t_data)[0]
        while 1:
            if idx >= num:
                break
            f.write("%d"%imu_t_data[idx][0] + "0000,"+
                    "%.10f"%imu_g_data[idx,0] + ","+"%.10f"%imu_g_data[idx,1] + ","+"%.10f"%imu_g_data[idx,2] + ","+
                    "%.10f"%imu_a_data[idx,0] + ","+"%.10f"%imu_a_data[idx,1] + ","+"%.10f"%imu_a_data[idx,2] +"\n")
            idx = idx + 1
            print("Process ===== %.2f"%(100*idx/num)+"% =====\r", end='')