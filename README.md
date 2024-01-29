# bag_scripts

Efficient rosbag scripts for multi-topics (Camera, IMU, GNSS, UWB and groundtruth) in Python.

And for lidar file, please refer to this [repositorty](https://github.com/zzwu29/livox_repub).

## Getting Started

```bash

git clone https://github.com/zzwu29/bag_scripts.git
```

## Usage

### Extract bag

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

### Create bag
convert IMU from gps timestamp to unix timestamp for [kalibr_bagcreater.py](./kalibr_bagcreater.py) to pack
```bash

python imu_to_unix_csv.py
```

copy and rename images from gps timestamp to unix timestamp for [kalibr_bagcreater.py](./kalibr_bagcreater.py) to pack
```bash

python img_unix_copy.py
```

create rosbag from imu and image topics, refer [here](https://github.com/ethz-asl/kalibr/wiki/Bag-format) for the format requirements(**support rgb images and greyscale images**)
```bash

 python kalibr_bagcreater.py --folder YOUR_FOLDER --output-bag YOUR_BAG.bag [--color]
```

merge multiple rosbags
```bash

python bagmerge.py -o YOUR_OUTPUT_BAG.bag -t TOPIC_BE_MERGED_TO_MAIN_BAG YOUR_MAIN_BAG.bag YOUR_AUXILIARY_BAG.bag
```

### Acknowledgement

 -  [Kalibr](https://github.com/ethz-asl/kalibr)
   
 -  [VIRAL Dataset](https://github.com/ntu-aris/ntu_viral_dataset) and [Dr. Nguyen](https://github.com/brytsknguyen)
   
 -  [uwb_driver](https://github.com/wang-chen/uwb_driver)

 -  [livox_repub](https://github.com/kafeiyin00/livox_repub)

 -  [self-driving-car](https://github.com/udacity/self-driving-car/tree/master/image-localization/community-code/roboauto/scripts)
   
 -  [rosbag_toolkit](https://github.com/neufieldrobotics/rosbag_toolkit)
 
 -  [bagedit](https://github.com/MHarbi/bagedit)
