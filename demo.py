import pyelsed
import cv2
from matplotlib import pyplot as plt
import numpy as np
from scipy import signal

img1 = cv2.imread('frames/frame_0003.jpg', cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread('frames/frame_0004.jpg', cv2.IMREAD_GRAYSCALE)

segments, scores = pyelsed.detect(img1)

dbg = cv2.cvtColor(img1, cv2.COLOR_GRAY2RGB)

for s in segments.astype(np.int32):
    if ((s[0] - s[2])**2 + (s[3] - s[1])**2)**0.5 > 600:
        cv2.line(dbg, (s[0], s[1]), (s[2], s[3]), (0, 255, 0), 1, cv2.LINE_AA)
        point1 = np.array([s[0], s[1]])
        point2 = np.array([s[2], s[3]])

img1 = img1.astype(float) / 255.0
img2 = img2.astype(float) / 255.0

#Iv = cv2.Sobel(img1, cv2.CV_64F, 1, 0, ksize=3)
#Iu = cv2.Sobel(img1, cv2.CV_64F, 0, 1, ksize=3)

kernel_x = np.array([[-1, 1], [-1, 1]])
kernel_y = np.array([[-1, -1], [1, 1]])
kernel_t = np.array([[1, 1], [1, 1]])

I1_smooth = cv2.GaussianBlur(img1, (3,3), 0)
I2_smooth = cv2.GaussianBlur(img2, (3,3), 0)

Iv = signal.convolve2d(I1_smooth,[[-0.25,0.25],[-0.25,0.25]],'same') + signal.convolve2d(I2_smooth,[[-0.25,0.25],[-0.25,0.25]],'same')
Iu = signal.convolve2d(I1_smooth,[[-0.25,-0.25],[0.25,0.25]],'same') + signal.convolve2d(I2_smooth,[[-0.25,-0.25],[0.25,0.25]],'same')
It = signal.convolve2d(I1_smooth,[[0.25,0.25],[0.25,0.25]],'same') + signal.convolve2d(I2_smooth,[[-0.25,-0.25],[-0.25,-0.25]],'same')

""" Iv = cv2.filter2D(I1_smooth, -1, kernel_x) #Gradient over X
Iu = cv2.filter2D(I1_smooth, -1, kernel_y) #Gradient over Y
It = cv2.filter2D(I2_smooth, -1, kernel_t) - cv2.filter2D(I1_smooth, -1, kernel_t)  #Gradient over Time """

random_values = np.random.rand(100)
sampled_points = point1 + random_values[:, np.newaxis] * (point2 - point1)

# Draw each point on the image
for point in sampled_points:
    cv2.circle(dbg, point.astype(int), 5, (0, 0, 255), thickness=-1)

#It = img1 - img2
v1, u1 = point1

v = sampled_points[:, 0]
u = sampled_points[:, 1]

U, V = u - u1, v1 - v
IU = Iu[sampled_points[:, 1].astype(int), sampled_points[:, 0].astype(int)]
IV = Iv[sampled_points[:, 1].astype(int), sampled_points[:, 0].astype(int)]
IT = It[sampled_points[:, 1].astype(int), sampled_points[:, 0].astype(int)]

M = np.column_stack((IU, IV, IU * V + IV * U))
b = M.T @ IT

print(np.linalg.pinv(M.T @ M) @ b)
plt.imshow(dbg)
plt.show()
