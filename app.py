import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import skimage as ski
import numpy as np
from scipy.ndimage import convolve
import scipy.ndimage as ndimage

def square_matrix(square): 
    """ This function will calculate the value x  
       (i.e. blurred pixel value) for each 250 * 250 blur image. 
    """
    tot_sum = 0
      
    # Calculate sum of all the pixels in 3 *3  matrix 
    for i in range(10): 
        for j in range(10): 
            tot_sum += square[i][j] 
              
    return tot_sum    # return the average of the sum of pixels 

def boxBlur(image): 
    """ 
    This function will calculate the blurred  
    image for given n * n image.  
    """
    square = []     # This will store the 250 * 250 matrix  
                 # which will be used to find its blurred pixel 
                   
    square_row = [] # This will store one row of a 250 * 250 matrix and  
                    # will be appended in square 
                      
    blur_row = []   # Here we will store the resulting blurred 
                    # pixels possible in one row  
                    # and will append this in the blur_img 
      
    blur_img = [] # This is the resulting blurred image 
      
    # number of rows in the given image 
    n_rows = len(image)  
      
    # number of columns in the given image 
    n_col = len(image[0])  
      
    # rp is row pointer and cp is column pointer 
    rp, cp = 0, 0 
      
    # This while loop will be used to  
    # calculate all the blurred pixel in the first row  
    while rp <= n_rows - 10:  
        while cp <= n_col-10: 
              
            for i in range(rp, rp + 10): 
                  
                for j in range(cp, cp + 10): 
                      
                    # append all the pixels in a row of 250 * 250 matrix 
                    square_row.append(image[i][j]) 
                      
                # append the row in the square i.e. 250 * 250 matrix  
                square.append(square_row) 
                square_row = [] 
              
            # calculate the blurred pixel for given 3 * 3 matrix  
            # i.e. square and append it in blur_row 
            blur_row.append(square_matrix(square)) 
            square = [] 
              
            # increase the column pointer 
            cp = cp + 1
          
        # append the blur_row in blur_image 
        blur_img.append(blur_row) 
        blur_row = [] 
        rp = rp + 1 # increase row pointer 
        cp = 0 # start column pointer from 0 again 
      
    # Return the resulting pixel matrix 
    return blur_img 

def gaussianBlur(image, sigma):
    # Create a 2D Gaussian kernel with a given sigma and size 10x10
    kernel_size = 10
    # kernel = np.fromfunction(lambda x, y: (1/(2*np.pi*sigma**2)) * np.exp(-((x-4.5)**2 + (y-4.5)**2)/(2*sigma**2)), (kernel_size, kernel_size))
    kernel = np.fromfunction(lambda x, y: (1/(2*np.pi*sigma**2)) * np.e ** ((-1*((x-(kernel_size-1)/2)**2+(y-(kernel_size-1)/2)**2))/(2*sigma**2)), (kernel_size, kernel_size))

    # Normalize the kernel
    kernel /= np.sum(kernel)

    # Apply 2D convolution with the Gaussian kernel to the image
    blur_img = ndimage.convolve(image, kernel, mode='constant')

    return blur_img

def median_filter(data, filter_size):
    temp = []
    indexer = filter_size // 2
    data_final = []
    data_final = np.zeros((len(data),len(data[0])))
    for i in range(len(data)):

        for j in range(len(data[0])):

            for z in range(filter_size):
                if i + z - indexer < 0 or i + z - indexer > len(data) - 1:
                    for c in range(filter_size):
                        temp.append(0)
                else:
                    if j + z - indexer < 0 or j + indexer > len(data[0]) - 1:
                        temp.append(0)
                    else:
                        for k in range(filter_size):
                            temp.append(data[i + z - indexer][j + k - indexer])

            temp.sort()
            data_final[i][j] = temp[len(temp) // 2]
            temp = []
    return data_final

# Create a grid of 250x250 pixels filled with ones (white)
grid = [[0 for _ in range(250)] for _ in range(250)]
for x in range(46, 226):
    for y in range(75, 126):
        grid[y][x] = 1
        
for x in range(150, 201):
    for y in range(50, 201):
        grid[y][x] = 1       
        
x1, y1 = 0, 0  
x2, y2 = 249, 249  

# Draw the diagonal line with increased thickness
line_thickness = 5  # Increase thickness to 5 pixels
for i in range(-line_thickness // 2, line_thickness // 2 + 1): #kaza line gamb ba3d
    for j in range(250):
        x = x1 + j
        y = y1 + j + i
        if 0 <= x < 250 and 0 <= y < 250:
            grid[y][x] = 1


x12, y12 = 0, 125  

for i in range(250):
    x = x12 + i
    y = y12 + i
    if x < 250 and y < 250:
        grid[y][x] = 1

# Convert grid list to a NumPy array
grid_array = np.array(grid)
# Call the boxBlur function with the grid image
blurred_image = boxBlur(grid)
blurred_image1 = gaussianBlur(grid_array, 1) 
blurred_image2 = median_filter(grid_array, 3) 


# Plot both images in one window
fig, axes = plt.subplots(1, 4, figsize=(15, 5))

axes[0].imshow(grid, cmap='gray')
axes[0].set_title('Original Image')
axes[0].axis('off')

axes[1].imshow(blurred_image, cmap='gray')
axes[1].set_title('Box Blur Filter')
axes[1].axis('off')

axes[2].imshow(blurred_image1, cmap='gray')
axes[2].set_title('Gaussian Filter')
axes[2].axis('off')

axes[3].imshow(blurred_image2, cmap='gray')
axes[3].set_title('Median Filter')
axes[3].axis('off')

plt.show()
