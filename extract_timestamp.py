import os
from math import *

def extract_timestamp(dir = "", prefix = "", time_scale = 1e9, syn_eps = 1e-3):
    list = os.listdir(dir)

    with open(prefix + "timestamp.txt", "w") as f:
        for file in list:
            base=os.path.splitext(file)[0]
            ext=os.path.splitext(file)[1]

            t_unix_sec = float(int(base))/time_scale
            
            # https://zhuanlan.zhihu.com/p/383645111
            err = 315964800 # start time difference
            
            # http://www.leapsecond.com/java/gpsclock.htm
            leapsec = 18 #GPS time was zero at 0h 6-Jan-1980 and since it is not perturbed by leap seconds GPS is now ahead of UTC by 18 seconds.

            t_gps_sec = t_unix_sec - err + 18
            gps_week = floor(t_gps_sec/(86400 * 7)) # gps week
            gps_sow = t_gps_sec - gps_week*(86400 * 7) # sec of week
            dow =  floor(gps_sow/(86400)) # day of week
            gps_sod =  gps_sow - dow*(86400) # sec of day
            hour =  floor(gps_sod/(3600)) # hour
            soh =  gps_sod - hour*(3600)
            min =  floor(soh/(60)) # hour
            sec =  soh - min*(60)
            # print(gps_week,gps_sow,hour,min,sec)
            if file == list[0]:
                print("start === " + "t_unix(s) [" + str(t_unix_sec) + "],"
                      + "t_gps [week "+ str(gps_week) +" sec "+str(gps_sow)+ " hms " +str(hour) + " "+str(min) + " "+str(sec) + " " +"]")
            if file == list[-1]:
                print("end === " + "t_unix(s) [" + str(t_unix_sec) + "],"
                      + "t_gps [week "+ str(gps_week) +" sec "+str(gps_sow)+ " hms " +str(hour) + " "+str(min) + " "+str(sec) + " " +"]")
            
            if fabs(gps_sow - round(gps_sow*1000)/1000)<=syn_eps:
                output_time = round(gps_sow*1000)/1000 #modify timestamp to a accurate value
            else:
                output_time = int(gps_sow*1000)/1000
            
            f.write(str(output_time) + ","+file+"\n")


if __name__ == '__main__':
    img_path = "../img0/data/"
    lidar_path = "../pcd/"
    
    extract_timestamp(img_path,time_scale = 1e9,prefix="cam_")
    extract_timestamp(lidar_path,time_scale = 1e6,prefix="lidar_")


