import numpy as np
from PIL import Image


def gradientArr(arr, outArr):
    outArr = np.zeros([np.size(arr, 0), np.size(arr, 1)]).reshape(np.size(arr, 0), np.size(arr, 1))
    for i in range(np.size(arr, 0)):
        for j in range(np.size(arr, 1)):
            if( j> 0 and j < 255) :
                outArr[i,j] = arr[i, j-1] + arr [i, j+1] - 2*arr[i,j]
                if(outArr[i,j] < 0) :
                    outArr[i,j] =0
                elif(outArr[i,j] > 255) :
                    outArr[i,j] = 255
            elif (j == 0): 
                outArr[i,] = arr [i, 1] - 2*arr[i,0]
                if(outArr[i,j] < 0) :
                    outArr[i,j] =0
                elif(outArr[i,j] > 255) :
                    outArr[i,j] = 255
            elif (j==255): 
                outArr[i,j] = arr [i, 254] - 2*arr[i,255]
                if(outArr[i,j] < 0) :
                    outArr[i,j] =0
                elif(outArr[i,j] > 255) :
                    outArr[i,j] = 255
    return outArr
   
def main():
    
    img = Image.open('sample_test_image.png')
    inImgArray = np.asarray(img)
    print(inImgArray)
    print(np.size(inImgArray, 0))
    print(np.size(inImgArray, 1))
    outImgArray = np.zeros([256,256])
    print(outImgArray)   
    outImgArray = gradientArr(inImgArray, outImgArray)
    print(outImgArray) 
    outImg = Image.fromarray(outImgArray)
    if outImg.mode != 'RGB' :
        outImg = outImg.convert('RGB')
    outImg.save('output.png')

if __name__ == "__main__" :
    main()