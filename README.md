bag_scripts
=============

Efficient rosbag scripts for multi-topics (Camera, IMU, GNSS, UWB and groundtruth) in Python

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

Acknowledgement
---------------
   [Kalibr](https://github.com/ethz-asl/kalibr) kalibr_bagextractor.py
   
   [VIRAL Dataset](https://github.com/ntu-aris/ntu_viral_dataset) and [Dr. Nguyen](https://github.com/brytsknguyen)
   
   [wang-chen](https://github.com/wang-chen/uwb_driver)
