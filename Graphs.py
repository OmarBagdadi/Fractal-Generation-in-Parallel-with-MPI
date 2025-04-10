import matplotlib.pyplot as plt
import pickle
import os

def displaySpeedupGraph(size,type):
    parallelData = None
    serialData = None
    parallelResultsPath = 'data/{}Results{}.pkl'.format(type,size)
    if os.path.exists(parallelResultsPath):
        try:
            with open(parallelResultsPath, 'rb') as file:
                parallelData = pickle.load(file)
                parallelData = dict(sorted(parallelData.items(), key=lambda item: int(item[0])))
        except (EOFError, pickle.UnpicklingError):
            print("File exists but cannot be loaded with pickle.")

    serialResultsPath = 'data/{}SerialResults.pkl'.format(type)
    if os.path.exists(serialResultsPath):
        try:
            with open(serialResultsPath, 'rb') as file:
                serialData = pickle.load(file)
        except (EOFError, pickle.UnpicklingError):
                print("File exists but cannot be loaded with pickle.")
    
    fastestSerialTime = min(serialData[size])
    fastestParallelTimes = [min(times) for times in parallelData.values()]

    speedup = [fastestSerialTime / t for t in fastestParallelTimes]

    processors = [int(num_processors) for num_processors in parallelData.keys()]

    # Create the speedup vs. the number of processors plot
    plt.plot(processors, speedup, marker='o', linestyle='-', color='b')
    plt.xlabel("Number of Processors")
    plt.ylabel("Speedup")
    plt.title("Speedup vs. Number of Processors for the {} {} fractal".format(size,type))
    plt.grid(True)

    # Display the plot
    plt.show()

def displayEfficiencyGraph(size,type):
    parallelData = None
    serialData = None
    parallelResultsPath = 'data/{}Results{}.pkl'.format(type,size)
    if os.path.exists(parallelResultsPath):
        try:
            with open(parallelResultsPath, 'rb') as file:
                parallelData = pickle.load(file)
                parallelData = dict(sorted(parallelData.items(), key=lambda item: int(item[0])))
        except (EOFError, pickle.UnpicklingError):
            print("File exists but cannot be loaded with pickle.")

    serialResultsPath = 'data/{}SerialResults.pkl'.format(type)
    if os.path.exists(serialResultsPath):
        try:
            with open(serialResultsPath, 'rb') as file:
                serialData = pickle.load(file)
        except (EOFError, pickle.UnpicklingError):
                print("File exists but cannot be loaded with pickle.")
    
    fastestSerialTime = min(serialData[size])
    fastestParallelTimes = [min(times) for times in parallelData.values()]

    speedup = [fastestSerialTime / t for t in fastestParallelTimes]

    # Calculate efficiency as speedup divided by the number of processors
    efficiency = [s / int(num_processors) for num_processors, s in zip(parallelData.keys(), speedup)]

    processors = [int(num_processors) for num_processors in parallelData.keys()]

    # Create the speedup vs. the number of processors plot
    plt.plot(processors, efficiency, marker='o', linestyle='-', color='b')
    plt.xlabel("Number of Processors")
    plt.ylabel("Efficiency")
    plt.title("Efficiency vs. Number of Processors for the {} {} fractal".format(size,type))
    plt.grid(True)

    # Display the plot
    plt.show()

def getSmallestTimeFromFile(path):
    with open(path, 'rb') as file:
        parallelData = pickle.load(file)
        parallelData = dict(sorted(parallelData.items(), key=lambda item: int(item[0])))
        
        # Find the item with the shortest time
        smallestEntry = min(parallelData.items(), key=lambda item: min(item[1]))
        processor, times = smallestEntry
        return min(times)

def displaySerialVSParallel(type):
    parallelTimes = []
    serialData = None

    serialResultsPath = 'data/{}SerialResults.pkl'.format(type)
    with open(serialResultsPath, 'rb') as file:
        serialData = pickle.load(file)

    parallelTimes.append(getSmallestTimeFromFile('data/{}Results1000x1000.pkl'.format(type)))
    parallelTimes.append(getSmallestTimeFromFile('data/{}Results2000x2000.pkl'.format(type)))
    parallelTimes.append(getSmallestTimeFromFile('data/{}Results5000x5000.pkl'.format(type)))
    parallelTimes.append(getSmallestTimeFromFile('data/{}Results10000x10000.pkl'.format(type)))

    # Extract image sizes and serial times
    image_sizes = list(serialData.keys())
    serial_times = [min(times) for times in serialData.values()]

    # Create the graph with two lines
    plt.plot(image_sizes, serial_times, label="Serial Times", marker='o', linestyle='-', color='b')
    plt.plot(image_sizes, parallelTimes, label="Parallel Times", marker='o', linestyle='-', color='g')

    plt.xlabel("Image Sizes")
    plt.ylabel("Time (seconds)")
    plt.title("Serial vs Parallel Times for Different Image Sizes")
    plt.legend()
    plt.grid(True)

    # Display the plot
    plt.show()
    


