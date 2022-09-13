"""
    Generates Snapshots from an RTSP Stream and save them to disk
    Modify SECONDS_TO_SLEEP to modifiy the Snapshots interval.
    If you want to have a Snapshot every Minute set it to 60.
    Currently it creates a Snapshot every 5 Minutes.
    Frames are saved with a datetime file name like frame-20220913-125640.jpg
"""

import av
import time
import logging

logging.basicConfig(level=logging.INFO)

RTSP_URL = "<your rtsp url>"
SECONDS_TO_SLEEP = 60 * 5

def decode_on_frame_and_save_to_disk(url):
    logging.info(f' Try to connect to {url}')
    # Connect to RTSP URL
    video = av.open(url, 'r')
    # Iter over Package to get an frame
    for packet in video.demux():
        # When frame is decoded
        for frame in packet.decode():
            # Current datetime
            ts = time.strftime("%Y%m%d-%H%M%S")
            # Log file loctaion of file
            logging.info(f' Save Frame frame-{ts}.jpg')
            # Save Frame into JPEG
            frame.to_image().save(f'frame-{ts}.jpg')
            # Close Connection to RTSP Source
            video.close()
            logging.info(f' Closing Connection')
            # Return because we just need one frame
            return

if __name__ == "__main__":
    try:
        logging.info(' Start Snapshot Generator')
        while True:
            decode_on_frame_and_save_to_disk(RTSP_URL)
            logging.info(f' Awaiting next iteration, sleep for {SECONDS_TO_SLEEP}sec')
            time.sleep(SECONDS_TO_SLEEP)
    except Exception as error:
        logging.error(error)
