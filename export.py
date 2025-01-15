import cv2
import os
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Export frames from video')
    parser.add_argument('video', type=str, help='video file')
    parser.add_argument('--step', type=int, default=5, help='frame step')
    args = parser.parse_args()

    basename = os.path.splitext(os.path.basename(args.video))[0]
    output = f'{basename}/frames'
    if not os.path.exists(output):
        os.makedirs(output)
    step = args.step

    video = cv2.VideoCapture(args.video)
    count = 0
    while True:
        ret, frame = video.read()
        if not ret:
            break
        if count % step == 0:
            cv2.imwrite(os.path.join(output, f'{count:04d}.png'), frame)
            count += 1
        else:
            count += 1
            continue

    video.release()
    cv2.destroyAllWindows()