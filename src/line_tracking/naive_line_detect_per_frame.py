import numpy as np
import numpy.typing as npt

import cv2, pyelsed

def detect_lines(img : npt.NDArray) -> npt.NDArray:
    # By default, `cv2.imread` reads images in a BGR (Blue-Green-Red) format.
    # Thus, the same formatting is considered in the call of `cvtColor`.
    # It may be changed in case we explictly change it in our pipeline. 
    img_grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Call the ELSED line detection algorithm.
    segments, scores = pyelsed.detect(img_grayscale)
    # * Despite the fact that the C implementation source code
    # * seems to handle non-grayscale colour mapping internally,
    # * by doing the transformation itself,
    # * the Python API seems to require the input to already
    # * be provided in grayscale colour mapping.
    #
    # * TLDR: Always make the input of `pyelsed.detect` grayscale,
    # * otherwise an error will be raised.

    for s in segments.astype(np.int32):
        cv2.line(img, (s[0], s[1]), (s[2], s[3]), (0, 255, 0), 1, cv2.LINE_AA)
    
    return img