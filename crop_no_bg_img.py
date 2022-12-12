#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def crop_save(_img):
    # load the image, copy image to origin
    img = cv2.imread(_img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    origin = img.copy()
    
    # morphology
    kernel = np.ones((10,10),np.uint8)
    mor_img = cv2.morphologyEx (img, cv2.MORPH_OPEN, kernel)
    
    # edge detecting
    edged = cv2.Canny(mor_img, 50, 100)
    edged = cv2.dilate(edged, None, iterations=1)
    edged = cv2.erode(edged, None, iterations=1)

    cnts = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    (cnts, _) = contours.sort_contours(cnts)
    
    # max area
    area = list()
    for c in cnts:
        area.append(cv2.contourArea(c))
    idex = (area.index(max(area)))

    # making box
    box = cv2.minAreaRect(cnts[idex])
    box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
    box = np.array(box, dtype="int")
    box = perspective.order_points(box)

    for i in range(4):
        for j in range(2):
            if box[i,j] < 0:
                box[i,j] = 0

    a = int(min(box[:,1]))
    b = int(max(box[:,1]))
    c = int(min(box[:,0]))
    d = int(max(box[:,0]))

    crop_img = origin[a:b, c:d]
    crop_img = Image.fromarray(crop_img)
    
    # img size
    img_size = crop_img.size 
    x = img_size[0]
    y = img_size[1] 
    size = max(x, y) +20
    
    resized_img = Image.new(mode = 'RGB', size = (size, size), color = (0,0,0))
    offset = (round((abs(x - size)) / 2), round((abs(y - size)) / 2))
    resized_img.paste(crop_img, offset)

