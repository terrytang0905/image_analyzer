#coding=utf-8
import cv2
import scipy as sp
import os

MIN_MATCH_COUNT=10

def classfiy_sift(image1,image2,size = (132,132)):
    img1 = cv2.resize(image1, size, interpolation=cv2.INTER_CUBIC)
    img2 = cv2.resize(image2, size, interpolation=cv2.INTER_CUBIC)
    #img1 = image1
    #img2 = image2

    #Initiate SIFT detector
    sift1 = cv2.xfeatures2d.SIFT_create()
    sift1.detect(img1)
    sift2 = cv2.xfeatures2d.SIFT_create()
    sift2.detect(img2)

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift1.detectAndCompute(img1,None)
    kp2, des2 = sift2.detectAndCompute(img2,None)

    # FLANN parameters
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks=50)   # or pass empty dictionary
    flann = cv2.FlannBasedMatcher(index_params,search_params)
    matches = flann.knnMatch(des1,des2,k=2)

    # Apply ratio test
    good = []
    for m,n in matches:
        if m.distance < 0.72 * n.distance:
            good.append(m)
    goodcnt=len(good)
    matchcnt=len(matches)
    print('good=%s,match=%s' % (goodcnt,matchcnt))
    ratio_base = goodcnt / matchcnt
    if matchcnt < MIN_MATCH_COUNT:
        return 0

    if int(matchcnt) <= 10:
        ratio = ratio_base / 0.68
    elif int(matchcnt) <= 20:
        ratio = ratio_base / 0.58
    elif int(matchcnt) <= 50:
        ratio = ratio_base / 0.52
    elif int(matchcnt) <= 100:
        ratio = ratio_base / 0.5
    else:
        ratio = ratio_base / 0.48
    return ratio


# #####################################
# visualization
def image_visualize(image1,image2,size = (132,132)):
    img1 = cv2.resize(image1, size, interpolation=cv2.INTER_CUBIC)
    img2 = cv2.resize(image2, size, interpolation=cv2.INTER_CUBIC)
    # img1 = image1
    # img2 = image2

    # Initiate SIFT detector
    sift1 = cv2.xfeatures2d.SIFT_create()
    sift1.detect(img1)
    sift2 = cv2.xfeatures2d.SIFT_create()
    sift2.detect(img2)

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift1.detectAndCompute(img1, None)
    kp2, des2 = sift2.detectAndCompute(img2, None)

    # FLANN parameters
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)  # or pass empty dictionary
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    # Apply ratio test
    good = []
    for m, n in matches:
        if m.distance < 0.72 * n.distance:
            good.append(m)
    print('good=%s,match=%s' % (len(good), len(matches)))

    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]
    view = sp.zeros((max(h1, h2), w1 + w2, 3), sp.uint8)
    view[:h1, :w1, 0] = img1
    view[:h2, w1:, 0] = img2
    view[:, :, 1] = view[:, :, 0]
    view[:, :, 2] = view[:, :, 0]

    for m in good:
        # draw the keypoints
        # print m.queryIdx, m.trainIdx, m.distance
        color = tuple([sp.random.randint(0, 255) for _ in range(3)])
        #print 'kp1,kp2',kp1,kp2
        cv2.line(view, (int(kp1[m.queryIdx].pt[0]), int(kp1[m.queryIdx].pt[1])) , (int(kp2[m.trainIdx].pt[0] + w1), int(kp2[m.trainIdx].pt[1])), color)

    cv2.imshow("view", view)
    cv2.waitKey()


def cmpSiftImage(img1,img2):
    try:
        #print("file1 path %s are exist:" % img1)
        #print("file2 path %s are exist:" % img2)
        if os.access(img1, os.F_OK) and os.access(img2, os.F_OK):
            img1 = cv2.imread(img1, 0)
            img2 = cv2.imread(img2, 0)
            res = classfiy_sift(img1, img2)
            print("compare_ratio:%.3f" % res)
        else:
            print("file path %s or %s are not exist:" % (img1, img2))
        return res
    except:
        return 0


def visualizeSiftImage(img1,img2):
    try:
        if os.access(img1, os.F_OK) and os.access(img2, os.F_OK):
            img1 = cv2.imread(img1,0)
            img2 = cv2.imread(img2, 0)
            res = image_visualize(img1, img2)
        else:
            print("file path %s or %s are not exist:"%(img1,img2))
        return res
    except:
        return 0

if __name__ == '__main__':
    #res=cmpSiftImage('/Users/zhenjietang/Downloads/validate2false/103062_compare.jpeg','/Users/zhenjietang/Downloads/validate2false/103062.jpeg')
    res = visualizeSiftImage('/Users/zhenjietang/Documents/BigDataResearch/Image_compare/validate2false/100004_compare.png',
                       '/Users/zhenjietang/Documents/BigDataResearch/Image_compare/validate2false/100004.jpeg')
    #print('ratio=' % res)
    #image_visualize(img1, img2)