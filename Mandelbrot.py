from ColorUtils import hsvToRgb
from PIL import Image
import numpy as np
import colorsys
from mpi4py import MPI
import pickle
import os
import sys

class Mandelbrot:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.colourPixels =[[(0,0,0) for j in range(self.width)] for i in range(self.height)]
        self.setupMandelbrot()

    def setupMandelbrot(self):
        maxIterations = 100

        self.start = MPI.Wtime()
        
        for x in range(self.width):
            for y in range(self.height):

                a = self.translate(y, 0, self.height, -1.5, 1.5)
                b = self.translate(x, 0, self.width, -1.5, 1.5)

                currentA = a
                currentB = b
                n = 0

                while n < maxIterations:
                    new_a = a * a - b * b
                    new_b = 2 * a * b

                    if abs(a + b) > 4:
                        break

                    a = new_a + currentA
                    b = new_b + currentB

                    n += 1

                hue = n / maxIterations
                brightness = 1.0 if n < maxIterations else 0.0
                rgbColor = hsvToRgb(hue, 1.0, brightness)

                if n == maxIterations:
                    self.colourPixels[x][y] = (0, 0, 0)
                else:
                    self.colourPixels[x][y] = rgbColor
        
        self.end = MPI.Wtime()
        print("Time taken to complete a {}x{} Mandelbrot fractal in serial: {}".format(self.width,self.height,self.end - self.start))

    def translate(self, value, fromMin, fromMax, toMin, toMax):
        return (value - fromMin) * (toMax - toMin) / (fromMax - fromMin) + toMin

    def printMandelbrot(self):
        filePath = 'data/MandelbrotSerialResults.pkl'
        if os.path.exists(filePath):
            try:
                with open(filePath, 'rb') as file:
                    # Loads the results file
                    data = pickle.load(file)
                    # Adds the time to the data
                    if '{}x{}'.format(self.width,self.height) in data:
                        data['{}x{}'.format(self.width,self.height)].append(self.end - self.start)
                    else:
                        data['{}x{}'.format(self.width,self.height)] = [(self.end - self.start)]
                    # Saves the data back to the file
                    with open(filePath, 'wb') as file:
                        # print(data)
                        pickle.dump(data, file)
            except (EOFError, pickle.UnpicklingError):
                print("File exists but cannot be loaded with pickle.")
        else:
            # Creates the file and adds the time data to the file
            data = {'{}x{}'.format(self.width,self.height) : [(self.end - self.start)]}
            with open(filePath, 'wb') as file:
                pickle.dump(data, file)

        # Convert the color pixel array to a NumPy array
        formattedPixels = np.array(self.colourPixels, dtype=np.uint8)

        # Create an image from the NumPy array using Pillow's Image.fromarray
        mandelbrotImage = Image.fromarray(formattedPixels)

        # Save the resulting image
        mandelbrotImage.save("Fractals/Mandelbrot_{}x{}.png".format(self.width,self.height))

if __name__ == "__main__":
    size = int(sys.argv[1])
    mandelbrot = Mandelbrot(size, size)
    mandelbrot.printMandelbrot()