import os
import shutil
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='clean up')
    parser.add_argument('video', type=str, help='video file')
    args = parser.parse_args()

    basename = os.path.splitext(os.path.basename(args.video))[0]
    frames = f"{basename}/frames"

    if os.path.exists(args.video):
        shutil.move(args.video, basename)
    if os.path.exists(frames):
        shutil.rmtree(frames)