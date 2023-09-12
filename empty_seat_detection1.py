import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox

#finds every object with label = obj and returns a list of indices
def findEvery(lbl,obj):
    index = 0
    lst = []
    for i in lbl:
        if i==obj:
            lst.append(index)
        index = index+1
    return lst

#returns area of bounding box
def getArea(bb):
    return (bb[2] - bb[0]) * (bb[3] - bb[1])

#returns the iou(percantage of intersection) between two bounding boxes
def intersection_over_union(b1,b2):
    #coordinates of the intersection rectangle
    x1 = max(b1[0],b2[0])
    y1 = max(b1[1],b2[1])
    x2 = min(b1[2],b2[2])
    y2 = min(b1[3],b2[3])
    
    #area of the rectangle
    area_intersection = max(0,x2-x1+1)*max(0,y2-y1+1)
    
    box1_area = (b1[2]-b1[0]+1)*(b1[3]-b1[1]+1)
    box2_area = (b2[2]-b2[0]+1)*(b2[3]-b2[1]+1)
    
    area_union = box1_area+box2_area-area_intersection
    
    #iou calculation
    iou = area_intersection/float(area_union)
    return iou

image = cv2.imread('test33.jpg')
#image = cv2.imread('test4.jpg')
bbox, label, conf = cv.detect_common_objects(image)

#get list of indices of all people in the frame
people = findEvery(label,'person')
#get list of indices of all chairs in the frame
chairs = findEvery(label,'chair')

no_chairs = len(chairs)
no_occupied = 0

#seperate colors for people, chairs and intersecting bounding boxes
person_color = (0,255,0) #green
chair_color = (255, 0, 0)    # Red
intersecting_color = (0, 0, 255)  # Blue
    

# Draw chair bounding boxes with chair_color
for c in chairs:
    occupied = 0
    c_bb = bbox[c]
    cx, cy, cw, ch = c_bb
    image = cv2.rectangle(image, (cx, cy), (cw, ch), chair_color, 2)

    for p in people:
        p_bb = bbox[p]
        
        #draw people bounding boxes
        px, py, pw, ph = p_bb
        image = cv2.rectangle(image, (px,py), (pw,ph), person_color, 2)

        
        #check for intersection
        res = intersection_over_union(c_bb, p_bb)        
        if res:
            # Draw intersecting bounding boxes with intersection_color
            #intersection = (max(cx, px), max(cy, py), min(cw, pw), min(ch, ph))
            
            if(getArea(p_bb)<50000):   #detect_common_objects groups many people into one big bbox
                
                occupied = 1

                #image = cv2.rectangle(image, (intersection[0], intersection[1]), (intersection[2], intersection[3]), intersecting_color, 2)
    if occupied:
        no_occupied = no_occupied+1
                
                

print("Number of occupied chairs: ",no_occupied)
#cv2.putText(image,"Number of occupied chairs: "+str(no_occupied),(50,60),cv2.FONT_HERSHEY_PLAIN,3,(255,255,255),3)  #displays the number of occupied chairs on the frame

print("Number of empty chairs: ",no_chairs-no_occupied)
#cv2.putText(image,"Number of empty chairs: "+str(no_chairs-no_occupied),(50,100),cv2.FONT_HERSHEY_PLAIN,3,(255,255,255),3)  #displays the number of empty chairs on the frame

# Display image
cv2.imshow('Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()  


#issues:
#detection of chairs and people not accurate
#bounding boxes intersecting when person is near a chair
#works only for back view of chair