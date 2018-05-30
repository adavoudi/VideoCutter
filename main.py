import imageio
import argparse
import cv2
import os
import pathlib

parser = argparse.ArgumentParser(description='Trim a video to several parts')
parser.add_argument('video', help='path to the video')
parser.add_argument('--dst', default='.',
                    help='where the video parts will be stored')

args = parser.parse_args()
print(args)

def putText(text, img, lineNum, fontColor='black'):
    colors = {
        'red': (0,0,255),
        'green': (0,255,0),
        'black': (0,0,0),
        'white': (255,255,255)
    }
    font                   = cv2.FONT_HERSHEY_SIMPLEX
    fontScale              = 0.5
    lineType               = 1
    bottomLeftCornerOfText = (10, 20*lineNum)

    cv2.putText(img,text, 
        bottomLeftCornerOfText, 
        font, 
        fontScale,
        colors[fontColor],
        lineType)
    
    return img

def show_info(img):
    putText('<number keys>: fast-forwarding', img, 1, 'white')
    putText('<s>: start a sequence', img, 2, 'white')
    putText('<e>: end a sequence', img, 3, 'white')
    putText('<q>: exit', img, 4, 'white')

    putText('frame: %d' % frameNum, img, 6, 'red')

    if save_frames:
        putText('Saving frames: ', img, 7, 'green')
        putText('  sequence: %d' % sequence_number, img, 8, 'green')

    return img

vid = imageio.get_reader(args.video, 'ffmpeg')

save_frames = False
sequence_number = 0
skipFrameNum = -1

for frameNum, frame in enumerate(vid):
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    if save_frames:
        dirpath = os.path.join(args.dst, str(sequence_number))
        if not os.path.exists(dirpath):
            pathlib.Path(dirpath).mkdir(parents=True, exist_ok=True)
        cv2.imwrite(os.path.join(dirpath, '%d.jpg' % frameNum), frame) 

    if frameNum <= skipFrameNum:
        continue

    frame = show_info(frame)
    cv2.imshow('preview', frame)
    c = cv2.waitKey(10)
    if c == ord('q'):
        break
    elif c == ord('s'):
        if save_frames:
            sequence_number += 1
        save_frames = True
    elif c == ord('e'):
        if save_frames:
            save_frames = False
            sequence_number += 1
    elif c >= ord('1') and c <= ord('9'):
        skipFrameNum = frameNum + 100 * (c - ord('0'))
