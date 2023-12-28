bag_scripts
=============

Efficient rosbag scripts for multi-topics (Camera, IMU, GNSS, UWB and groundtruth) in Python.

And for lidar file, please refer to this [repositorty](https://github.com/zzwu29/livox_repub).

Getting Started
---------------

```bash

git clone https://github.com/zzwu29/bag_scripts.git
```

Usage
--------------

extract raw data
```bash

python bag_extractor.py --bag * --image_topics * --imu_topics * --gnss_topics * --uwb_topics * --gt_topics * --output_folder ?(default: ~/Desktop/)
```


extract timestamp from raw data file name
```bash

python extract_timestamp.py
```

convert IMU unix timestamp to gps time, interpolate IMU raw data, and convert IMU measurement units
```bash

python conv_imu_timestamp.py
```

Acknowledgement
---------------
 -  [Kalibr](https://github.com/ethz-asl/kalibr) kalibr_bagextractor.py
   
 -  [VIRAL Dataset](https://github.com/ntu-aris/ntu_viral_dataset) and [Dr. Nguyen](https://github.com/brytsknguyen)
   
 -  [uwb_driver](https://github.com/wang-chen/uwb_driver)

 -  [livox_repub](https://github.com/kafeiyin00/livox_repub)
