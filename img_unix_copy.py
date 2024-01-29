import os
import shutil

if __name__ == '__main__':
    # https://github.com/ethz-asl/kalibr/wiki/Bag-format
    img_orig_path = "./data/284000/"
    img_copy_path = "../bag/cam0/"
    gps_week = 2257   #!!!!!!! change here, check http://www.igs.gnsswhu.cn/index.php/home/data_product/igs.html
    start_sec, end_sec = 284450, 284680
    start_sec, end_sec = 284431, 284700

    # https://zhuanlan.zhihu.com/p/383645111
    err = 315964800 # start time difference

    # http://www.leapsecond.com/java/gpsclock.htm
    leapsec = 18 #GPS time was zero at 0h 6-Jan-1980 and since it is not perturbed by leap seconds GPS is now ahead of UTC by 18 seconds.

    list = os.listdir(img_orig_path)
    file_idx = 0
    for file in list:
        filename = file.split('.')[0]  # mind the origin file name here!!!!!!
        file_t = float(filename)/1e9
        if file_t > end_sec:
            break
        if file_t >= start_sec and file_t <= end_sec:
            file_t_unix = file_t + gps_week * 86400 * 7 + err - leapsec
            file_t_unix = str(round(file_t_unix*1e5))+"0000"
            filename_unix = file_t_unix + "."+file.split('.')[1]
            output_file = filename_unix
            shutil.copyfile(os.path.join(img_orig_path,file), os.path.join(img_copy_path,output_file))
            print("img " + str(file_idx)+ " " +file+" was copied as",output_file)
            file_idx = file_idx + 1
