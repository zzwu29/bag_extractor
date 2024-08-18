import os
import string

def rename(path, suffix):
    i = 1
    file_list = os.listdir(path)
    file_list.sort(key=lambda x: int(float(x[:-4])*1e9))
    for file in file_list:
        if file.endswith(suffix):
            # print(file)
            if os.path.isfile(os.path.join(path, file)):
                new_name = file.replace(file, "%03d" % i + suffix)  # 根据需要设置基本文件名
                # print(new_name)
                os.rename(os.path.join(path, file), os.path.join(path, new_name))
                i += 1
    print("End")

if __name__ == "__main__":
    # rename("/home/zzwu/Desktop/lidar_cam_calib/img/",".jpg")
    rename("/home/zzwu/Desktop/lidar_cam_calib/pcd/",".pcd")