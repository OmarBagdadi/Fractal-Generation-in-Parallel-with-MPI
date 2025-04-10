from ColorUtils import hsvToRgb
from PIL import Image
import numpy as np
import colorsys
from mpi4py import MPI
import pickle
import os
import sys

class JuliaParallel:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.Get_rank()
        self.size = self.comm.Get_size()
        self.ca = -0.8
        self.cb = 0.156
        self.colourPixels = None  # Initialize to None
        self.setupJulia()

    def setupJulia(self):
        maxIterations = 100
        self.start = MPI.Wtime()

        # Calculate the range of rows for this process
        rows_per_process = self.height // self.size
        self.start_row = self.rank * rows_per_process

        # Initialize the colourPixels array for this process
        local_colours = [[(0,0,0) for j in range(self.width)] for i in range(rows_per_process)]
        # print("Process {} gets here start".format(self.rank))
        for x in range(self.width):
            for y in range(rows_per_process):
                
                a = self.translate(x, 0, self.width, -1.5, 1.5)
                b = self.translate(y + (self.rank * rows_per_process), 0, self.height, -1.5, 1.5)
                self.start_row += 1
                n = 0

                while n < maxIterations:
                    new_a = a * a - b * b
                    new_b = 2 * a * b

                    if abs(a + b) > 4:
                        break

                    a = new_a + self.ca
                    b = new_b + self.cb

                    n += 1

                hue = n / maxIterations
                hue +=  0.355                                   # shifts the colour to a blue colour in the colour spectrum
                brightness = 1.0 if n < maxIterations else 0.0
                rgb_color = hsvToRgb(hue, 1.0, brightness)

                if n == maxIterations:
                    local_colours[y][x] = (0, 0, 0)
                else:
                    local_colours[y][x] = rgb_color
                
        
        # Gather data from all processes
        # print("Process {} gets here finished".format(self.rank))
        # self.comm.barrier()
        self.colourPixels = self.comm.gather(local_colours, root=0)
        self.end = MPI.Wtime()

        # Process 0 combines data and prints the time
        if self.rank == 0:
            self.colourPixels = np.vstack(self.colourPixels)
            print("Time taken to complete a {}x{} Julia fractal in parallel: {}".format(self.width, self.height ,(self.end - self.start)))

    def translate(self, value, fromMin, fromMax, toMin, toMax):
        return (value - fromMin) * (toMax - toMin) / (fromMax - fromMin) + toMin

    def printJulia(self):
        if self.rank == 0:
            # Save the results of the fractal generated
            filePath = 'data/JuliaResults{}x{}.pkl'.format(self.width,self.height)
            if os.path.exists(filePath):
                try:
                    with open(filePath, 'rb') as file:
                        data = pickle.load(file)
                        if str(self.size) in data:
                            data[str(self.size)].append(self.end - self.start)
                        else:
                            data[str(self.size)] = [(self.end - self.start)]
                        with open(filePath, 'wb') as file:
                            # print(data)
                            pickle.dump(data, file)
                except (EOFError, pickle.UnpicklingError):
                    print("File exists but cannot be loaded with pickle.")
            else:
                data = {str(self.size) : [(self.end - self.start)]}
                with open(filePath, 'wb') as file:
                    pickle.dump(data, file)

            # Convert the color pixel array to a NumPy array
            formattedPixels = np.array(self.colourPixels, dtype=np.uint8)

            # Create an image from the NumPy array using Pillow's Image.fromarray
            juliaImage = Image.fromarray(formattedPixels)

            # Save the resulting image
            juliaImage.save("Fractals/Julia_{}x{}.png".format(self.width,self.height))

if __name__ == "__main__":
    size = int(sys.argv[1])
    julia = JuliaParallel(size, size)
    julia.printJulia()
