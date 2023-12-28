import numpy as np
from math import *
import matplotlib.pyplot as plt

def read_imu_data(file = "", time_scale = 1e9):
    print("process "+file)
    
    # https://zhuanlan.zhihu.com/p/383645111
    err = 315964800 # start time difference
    
    # http://www.leapsecond.com/java/gpsclock.htm
    leapsec = 18 #GPS time was zero at 0h 6-Jan-1980 and since it is not perturbed by leap seconds GPS is now ahead of UTC by 18 seconds.
    
    imu_data = np.loadtxt(file)
    
    t_unix_sec = imu_data[:,0]
    t_gps_sec = t_unix_sec - err + leapsec
    gps_week = np.floor(t_gps_sec/(86400 * 7)) # gps week
    gps_sow = t_gps_sec - gps_week*(86400 * 7) # sec of week
    
    imu_data[:,0] = gps_sow
    
    return imu_data

def intp_imu_data(data = [], dt = 0.005, rot_offset = np.eye(3,3), g_scale =1.0, a_scale =1.0):
    print("imu start: "+ str(data[0,0]))
    print("imu end: "+ str(data[-1,0]))
    
    process_start = ceil(data[0,0]/dt)*dt
    process_end = floor(data[-1,0]/dt)*dt
    
    print("imu interpolation from "+str(process_start)+" to "+str(process_end))

    t = process_start
    idx = 0
    
    time, gx, gy, gz, ax, ay, az = [], [], [], [], [], [], []
    
    while 1:
        if t > process_end:
            break
        
        while 1:
            if idx + 1 >= len(data[:,0]):
                break
            if data[idx,0] <=t and data[idx+1,0] > t:
                break
            idx = idx + 1

        # idx is found
        time.append(t)
        # do not intp
        if data[idx,0] == t:
            imu_ga_itp = data[idx,1:7]
        else:
            dist_low = t - data[idx,0]
            dist_high = -t + data[idx+1,0]
            imu_ga_itp = (dist_high)/(dist_low+dist_high)*data[idx,1:7] + (dist_low)/(dist_low+dist_high)*data[idx+1,1:7]
        
        g_xyz = np.matmul(rot_offset, np.array(imu_ga_itp[0:3]))*g_scale
        a_xyz = np.matmul(rot_offset, np.array(imu_ga_itp[3:6]))*a_scale
        
        gx.append(g_xyz[0])
        gy.append(g_xyz[1])
        gz.append(g_xyz[2])
        ax.append(a_xyz[0])
        ay.append(a_xyz[1])
        az.append(a_xyz[2])

        t = t + dt

    # finish
    imu_data = np.array([time, gx, gy, gz, ax, ay, az]).T
    return imu_data

def imu_compare(imu_data = [], imu_data_itp = []):
    fig, ax = plt.subplots(3,2)
    ax[0,0].plot(imu_data[:,0],imu_data[:,1],label = "raw")
    ax[0,0].plot(imu_data_itp[:,0],imu_data_itp[:,1],label = "itp")
    ax[1,0].plot(imu_data[:,0],imu_data[:,2])
    ax[1,0].plot(imu_data_itp[:,0],imu_data_itp[:,2])
    ax[2,0].plot(imu_data[:,0],imu_data[:,3])
    ax[2,0].plot(imu_data_itp[:,0],imu_data_itp[:,3])
    ax[0,1].plot(imu_data[:,0],imu_data[:,4])
    ax[0,1].plot(imu_data_itp[:,0],imu_data_itp[:,4])
    ax[1,1].plot(imu_data[:,0],imu_data[:,5])
    ax[1,1].plot(imu_data_itp[:,0],imu_data_itp[:,5])
    ax[2,1].plot(imu_data[:,0],imu_data[:,6])
    ax[2,1].plot(imu_data_itp[:,0],imu_data_itp[:,6])
    fig.legend()
    fig.tight_layout()
    plt.show()

if __name__ == '__main__':
    imu_file_list = [
        "../imu0/imu.txt"
        , "../imu1/imu.txt"
        ]
    
    plot = False # whether to plot
    itp = []
    
    idx = 0
    
    # up IMU1 down IMU0, the axis of IMU1 maybe error
    rot_offset = np.array([
        [0, 1 ,0],
        [0 ,0, -1],
        [-1, 0 ,0]
    ])
    
    for imu_file in imu_file_list:
        imu_data = read_imu_data(file = imu_file)
        if idx == 0:
            # https://docs.ros.org/en/noetic/api/sensor_msgs/html/msg/Imu.html
            imu_data_itp = intp_imu_data(data = imu_data, a_scale=9.81) # the Accelerations should be in m/s^2 (not in g's)
        if idx == 1:
            imu_data_itp = intp_imu_data(data = imu_data, rot_offset = rot_offset.T)
        if plot:
            imu_compare(imu_data=imu_data, imu_data_itp=imu_data_itp)
        itp.append(imu_data_itp)
        np.savetxt("itp_imu_"+str(idx)+".txt", imu_data_itp,fmt='%.3f    %15.10f    %15.10f    %15.10f    %15.10f    %15.10f    %15.10f')
        idx = idx+1

    if plot:
        imu_compare(imu_data=itp[0], imu_data_itp=itp[1])
    


