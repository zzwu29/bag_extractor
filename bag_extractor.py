#!/usr/bin/env python
# -*- coding: utf-8 -*-
# python extract_image.py 
# --bag * 
# --image_topics * 
# --imu_topics * 
# --gnss_topics * 
# --uwb_topics * 
# --gt_topics * 
# --output_folder ?(~/Desktop/)

import os
import argparse
import cv2
import sys
import rosbag

from cv_bridge import CvBridge

def bag2image(bag=str, image_topic=str, output_folder=str):
    # support an image topic

    print("Extract images from %s on topic %s into %s" % (bag, image_topic, output_folder))

    bag_to_read = rosbag.Bag(bag, "r")
    bridge = CvBridge()
    count = 0
    for topic, msg, t in bag_to_read.read_messages(topics=image_topic):
	# for img raw
        cv_img = bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")
	# for img compressed        
	# cv_img = bridge.compressed_imgmsg_to_cv2(msg, desired_encoding="passthrough")

        timestr="%d"%(msg.header.stamp.to_sec()*1e9)
	
	#img filename: frame+num
        # cv2.imwrite(os.path.join(args.output_dir, "frame%06i.png" % count), cv_img)
	#img filename: rostime ns
        cv2.imwrite(os.path.join(output_folder,timestr+".jpg"), cv_img)

        print("Wrote image %i" % count)
        count += 1

    bag_to_read.close()

    return

def bag2imu(bag=str, imu_topic=str, output_folder=str):
    # support an imu topic

    print("Extract imu records from %s on topic %s into %s" % (bag, imu_topic, output_folder))

    bag_to_read = rosbag.Bag(bag, "r")
    imu = open(os.path.join(output_folder,"imu.txt"),"w")
    for topic, msg, t in bag_to_read.read_messages(topics=imu_topic):

        acc_y = "%.10f" % msg.linear_acceleration.y
        acc_x = "%.10f" % msg.linear_acceleration.x
        acc_z = "%.10f" % msg.linear_acceleration.z
        w_y = "%.10f" % msg.angular_velocity.y
        w_x = "%.10f" % msg.angular_velocity.x
        w_z = "%.10f" % msg.angular_velocity.z

        timestr="%.6f"%(msg.header.stamp.to_sec())

        imudata = timestr + " " + w_x + " " + w_y + " " + w_z + " " + acc_x + " " + acc_y + " " + acc_z
        imu.write(imudata)
        imu.write('\n')
    bag_to_read.close()

    return

def bag2gnss(bag=str, gnss_topic=str, output_folder=str):
    # support an gnss topic

    print("Extract gnss records from %s on topic %s into %s" % (bag, gnss_topic, output_folder))

    bag_to_read = rosbag.Bag(bag, "r")
    gnss = open(os.path.join(output_folder,"gnss.txt"),"w")
    for topic, msg, t in bag_to_read.read_messages(topics=gnss_topic):

        pos_x = "%.10f" % msg.latitude
        pos_y = "%.10f" % msg.longitude
        pos_z = "%.10f" % msg.altitude
        v0="%.6f" % msg.position_covariance[0]
        v1="%.6f" % msg.position_covariance[1]
        v2="%.6f" % msg.position_covariance[2]
        v3="%.6f" % msg.position_covariance[3]
        v4="%.6f" % msg.position_covariance[4]
        v5="%.6f" % msg.position_covariance[5]
        v6="%.6f" % msg.position_covariance[6]
        v7="%.6f" % msg.position_covariance[7]
        v8="%.6f" % msg.position_covariance[8]

        timestr="%.6f"%(msg.header.stamp.to_sec())

        gnssdata = timestr + " " + pos_x + " " + pos_y + " " + pos_z + " "+v0+ " "+v1+ " "+v2+ " "+v3+ " "+v4+ " "+v5+ " "+v6+ " "+v7+ " "+v8
        gnss.write(gnssdata)
        gnss.write('\n')
    bag_to_read.close()

def bag2uwb(bag=str, uwb_topic=str, output_folder=str):
    # support an uwb topic
    # from uwb_driver.msg import UwbRange # Install from https://github.com/ntu-aris/uwb_driver

    # Header  header                              # ROS header
    # uint16  msgId                               # Message ID handled by p4xx automatically
    # uint8   requester_id                        # Identity number of the requesting P4xx
    # uint8   responder_id                        # Identity number of the responding P4xx
    # int8    requester_idx                       # Index number of the node in the responding array passed by rosparam
    # int8    responder_idx                       # Index number of the node in the responding array passed by rosparam
    # uint8   range_status                        # Status/error codes for the range conversation
    # uint8   antenna                             # Antenna where the measurement was carried out
    # uint16  stopwatch_time                      # How long the range conversation took, in ms
    # float32 distance                            # Distance measurement using ToF
    # float32 coarse_range                        # Distance measurement using signal strength
    # float32 filtered_range                      # Distance measurement using filter
    # float32 distance_err                        # Distance error estimate
    # float32 coarse_range_err                    # Coarse range error
    # float32 filtered_range_err                  # Filter range error
    # float32 distance_dot                        # Range velocity estimated by Pxx
    # float32 distance_dot_err                    # Range velocity error estimated by Pxx
    # uint8   range_meas_type                     # Range measurement type
    # uint16  requester_LED_flag                  # requester's received scan: 16 for NLS
    # uint16  responder_LED_flag                  # responder's received scan: 16 for NLS
    # uint16  noise                               # Noise
    # uint16  vPeak                               # Absolute maximum value in the leading edge window of the received waveform
    # int32   coarse_tof_in_bins                  # Coarse tof in bins
    # uint32  uwb_time                            # ms since radio boot at the time of the range conversation nb
    # geometry_msgs/Point requester_location      # Location of the requester node if known (explicitly declared as anchor by rosparam), otherwise 99999 indicates unknown.
    # geometry_msgs/Point responder_location      # Location of the responder node if known (explicitly declared as anchor by rosparam), otherwise 99999 indicates unknown.
    # geometry_msgs/Point rqst_antenna_offset     # Location of the antenna in the body frame of the requester.
    # geometry_msgs/Point rspd_antenna_offset     # Location of the antenna in the body frame of the responder.

    print("Extract uwb records from %s on topic %s into %s" % (bag, uwb_topic, output_folder))
    bag_to_read = rosbag.Bag(bag,'r')
    uwb = open(os.path.join(output_folder,"uwb.csv"),"w")

    uwb.write("timeUWB"           +","+\
        "msgId"               +","+\
        "requester_id"        +","+\
        "responder_id"        +","+\
        "requester_idx"       +","+\
        "responder_idx"       +","+\
        "range_status"        +","+\
        "antenna"             +","+\
        "stopwatch_time"      +","+\
        "distance"            +","+\
        "coarse_range"        +","+\
        "filtered_range"      +","+\
        "distance_err"        +","+\
        "coarse_range_err"    +","+\
        "filtered_range_err"  +","+\
        "distance_dot"        +","+\
        "distance_dot_err"    +","+\
        "range_meas_type"     +","+\
        "requester_LED_flag"  +","+\
        "responder_LED_flag"  +","+\
        "noise"               +","+\
        "vPeak"               +","+\
        "coarse_tof_in_bins"  +","+\
        "uwb_time"            +","+\
        "requester_locationx" +","+\
        "requester_locationy" +","+\
        "requester_locationz" +","+\
        "responder_locationx" +","+\
        "responder_locationy" +","+\
        "responder_locationz" +","+\
        "rqst_antenna_offsetx"+","+\
        "rqst_antenna_offsety"+","+\
        "rqst_antenna_offsetz"+","+\
        "rspd_antenna_offsetx"+","+\
        "rspd_antenna_offsety"+","+\
        "rspd_antenna_offsetz"
        )
    uwb.write("\n")
    for topic, msg, t in bag_to_read.read_messages(topics=uwb_topic):
        timeUWB             = "%.6f" %  msg.header.stamp.to_sec()
        msgId               = str(msg.msgId         )         
        requester_id        = str(msg.requester_id  )         
        responder_id        = str(msg.responder_id  )         
        requester_idx       = str(msg.requester_idx )         
        responder_idx       = str(msg.responder_idx )         
        range_status        = str(msg.range_status  )         
        antenna             = str(msg.antenna       )         
        stopwatch_time      = str(msg.stopwatch_time)         
        distance            = "%.6f"%msg.distance               
        coarse_range        = "%.6f"%msg.coarse_range           
        filtered_range      = "%.6f"%msg.filtered_range         
        distance_err        = "%.6f"%msg.distance_err           
        coarse_range_err    = "%.6f"%msg.coarse_range_err       
        filtered_range_err  = "%.6f"%msg.filtered_range_err     
        distance_dot        = "%.6f"%msg.distance_dot           
        distance_dot_err    = "%.6f"%msg.distance_dot_err       
        range_meas_type     = str(msg.range_meas_type   )    
        requester_LED_flag  = str(msg.requester_LED_flag)    
        responder_LED_flag  = str(msg.responder_LED_flag)    
        noise               = str(msg.noise             )    
        vPeak               = str(msg.vPeak             )    
        coarse_tof_in_bins  = str(msg.coarse_tof_in_bins)    
        uwb_time            = str(msg.uwb_time          ) 
        requester_locationx ="%.6f" %msg.requester_location.x 
        requester_locationy ="%.6f" %msg.requester_location.y 
        requester_locationz ="%.6f" %msg.requester_location.z 
        responder_locationx ="%.6f" %msg.responder_location.x 
        responder_locationy ="%.6f" %msg.responder_location.y 
        responder_locationz ="%.6f" %msg.responder_location.z 
        rqst_antenna_offsetx="%.6f" %msg.rqst_antenna_offset.x
        rqst_antenna_offsety="%.6f" %msg.rqst_antenna_offset.y
        rqst_antenna_offsetz="%.6f" %msg.rqst_antenna_offset.z
        rspd_antenna_offsetx="%.6f" %msg.rspd_antenna_offset.x   
        rspd_antenna_offsety="%.6f" %msg.rspd_antenna_offset.y   
        rspd_antenna_offsetz="%.6f" %msg.rspd_antenna_offset.z   

        uwbData = \
            timeUWB             +","+\
            msgId               +","+\
            requester_id        +","+\
            responder_id        +","+\
            requester_idx       +","+\
            responder_idx       +","+\
            range_status        +","+\
            antenna             +","+\
            stopwatch_time      +","+\
            distance            +","+\
            coarse_range        +","+\
            filtered_range      +","+\
            distance_err        +","+\
            coarse_range_err    +","+\
            filtered_range_err  +","+\
            distance_dot        +","+\
            distance_dot_err    +","+\
            range_meas_type     +","+\
            requester_LED_flag  +","+\
            responder_LED_flag  +","+\
            noise               +","+\
            vPeak               +","+\
            coarse_tof_in_bins  +","+\
            uwb_time            +","+\
            requester_locationx +","+\
            requester_locationy +","+\
            requester_locationz +","+\
            responder_locationx +","+\
            responder_locationy +","+\
            responder_locationz +","+\
            rqst_antenna_offsetx+","+\
            rqst_antenna_offsety+","+\
            rqst_antenna_offsetz+","+\
            rspd_antenna_offsetx+","+\
            rspd_antenna_offsety+","+\
            rspd_antenna_offsetz
        uwb.write(uwbData)
        uwb.write("\n")
    bag_to_read.close()

    return

def bag2gt(bag=str, gt_topic=str, output_folder=str):
    # support an gt topic

    print("Extract gt records from %s on topic %s into %s" % (bag, gt_topic, output_folder))

    bag_to_read = rosbag.Bag(bag, "r")
    gt = open(os.path.join(output_folder,"PoseStamped.txt"),"w")
    for topic, msg, t in bag_to_read.read_messages(topics=gt_topic):

        pos_y = "%.6f" % msg.pose.position.y
        pos_x = "%.6f" % msg.pose.position.x
        pos_z = "%.6f" % msg.pose.position.z
        q_y = "%.10f" % msg.pose.orientation.y
        q_x = "%.10f" % msg.pose.orientation.x
        q_z = "%.10f" % msg.pose.orientation.z
        q_w = "%.10f" % msg.pose.orientation.w

        timestr="%.6f"%(msg.header.stamp.to_sec())

        gtdata = timestr + " " + pos_x + " " + pos_y + " " + pos_z + " " + q_x + " " + q_y + " " + q_z + " " + q_w
        gt.write(gtdata)
        gt.write('\n')
    bag_to_read.close()

    return

def main():
    parser = argparse.ArgumentParser(description='Extract a ROS bag containing multiple image and imu topics.')
    parser.add_argument('--bag', metavar='bag', help='ROS bag file')
    parser.add_argument('--image_topics',  metavar='image_topics', nargs='*', help='Image topics %(default)s')
    parser.add_argument('--imu_topics',  metavar='imu_topics', nargs='*', help='Imu topics %(default)s')
    parser.add_argument('--gnss_topics',  metavar='gnss_topics', nargs='*', help='Gnss topics %(default)s')
    parser.add_argument('--uwb_topics',  metavar='uwb_topics', nargs='*', help='Uwb topics %(default)s')
    parser.add_argument('--gt_topics',  metavar='gt_topics', nargs='*', help='Gt topics %(default)s')
    parser.add_argument('--output_folder',  metavar='output_folder', nargs='?', default="~/Desktop/", help='Output folder %(default)s')

    args = parser.parse_args()
    print("Extract images from %s on topic %s into %s" % (args.bag, args.image_topics, args.output_folder))
    #print help if no argument is specified
    if len(sys.argv)<2:
        parser.print_help()
        sys.exit(0)

    image_id=0
    if not args.image_topics is None:
        print("cam number: "+str(len(args.image_topics)))
        for image_topic in args.image_topics:
            #create output folder
            try:
                output_folder=os.path.join(args.output_folder,"img"+str(image_id),"data")
                os.makedirs(output_folder)
            except:
                print("-----WARNING: "+output_folder+" cannot be made ! -----")
                pass
            print("start process cam "+str(image_id)+" (topic: "+image_topic+", path: "+output_folder+")")
            bag2image(args.bag, image_topic, output_folder)
            image_id=image_id+1
            print("finish process cam "+str(image_id)+" (topic: "+image_topic+")")
    else:
        print("-----WARNING: no cam topic given ! -----")

    imu_id=0
    if not args.imu_topics is None:
        print("imu number: "+str(len(args.imu_topics)))
        for imu_topic in args.imu_topics:
            output_folder=os.path.join(args.output_folder,"imu"+str(imu_id))
            #create output folder
            try:
                os.makedirs(output_folder)
            except:
                print("-----WARNING: "+output_folder+" cannot be made ! -----")
                pass
            print("start process imu "+str(imu_id)+" (topic: "+imu_topic+", path: "+output_folder+")")
            bag2imu(args.bag, imu_topic, output_folder)
            imu_id=imu_id+1
            print("finish process imu "+str(imu_id)+" (topic: "+imu_topic+")")
    else:
        print("-----WARNING: no imu topic given ! -----")
    
    gnss_id=0
    if not args.gnss_topics is None:
        print("gnss number: "+str(len(args.gnss_topics)))
        for gnss_topic in args.gnss_topics:
            output_folder=os.path.join(args.output_folder,"gnss"+str(gnss_id))
            #create output folder
            try:
                os.makedirs(output_folder)
            except:
                print("-----WARNING: "+output_folder+" cannot be made ! -----")
                pass
            print("start process gnss "+str(gnss_id)+" (topic: "+gnss_topic+", path: "+output_folder+")")
            bag2gnss(args.bag, gnss_topic, output_folder)
            gnss_id=gnss_id+1
            print("finish process gnss "+str(gnss_id)+" (topic: "+gnss_topic+")")
    else:
        print("-----WARNING: no gnss topic given ! -----")

    uwb_id=0
    if not args.uwb_topics is None:
        print("uwb number: "+str(len(args.uwb_topics)))
        for uwb_topic in args.uwb_topics:
            output_folder=os.path.join(args.output_folder,"uwb"+str(uwb_id))
            #create output folder
            try:
                os.makedirs(output_folder)
            except:
                print("-----WARNING: "+output_folder+" cannot be made ! -----")
                pass
            print("start process uwb "+str(uwb_id)+" (topic: "+uwb_topic+", path: "+output_folder+")")
            bag2uwb(args.bag, uwb_topic, output_folder)
            uwb_id=uwb_id+1
            print("finish process uwb "+str(uwb_id)+" (topic: "+uwb_topic+")")
    else:
        print("-----WARNING: no uwb topic given ! -----")

    gt_id=0
    if not args.gt_topics is None:
        print("gt number: "+str(len(args.gt_topics)))
        for gt_topic in args.gt_topics:
            output_folder=os.path.join(args.output_folder,"gt"+str(gt_id))
            #create output folder
            try:
                os.makedirs(output_folder)
            except:
                print("-----WARNING: "+output_folder+" cannot be made ! -----")
                pass
            print("start process gt "+str(gt_id)+" (topic: "+gt_topic+", path: "+output_folder+")")
            bag2gt(args.bag, gt_topic, output_folder)
            gt_id=gt_id+1
            print("finish process gt "+str(gt_id)+" (topic: "+gt_topic+")")
    else:
        print("-----WARNING: no gt topic given ! -----")

    return

if __name__ == '__main__':
    main()
