# Fractal-Generation-in-Parallel-with-MPI

## About
This project explores generating fractals, specifically the Mandelbrot and Julia sets, by using the parallel programming practices. Using the Message Passing Interface (MPI), the aim is to efficiently generate complex fractals through distributed computing.

Fractals are intricate mathematical patterns that exhibit self-similarity and infinite detail and as you can imagine as the pixel size increases the slower and more computationally intensive it becomes to generate these fractals. The implementation of MPI enables the decomposition of computational tasks across multiple processes, significantly enhancing performance and scalability. By distributing the workload, this project demonstrates the potential of parallel programming in handling computationally intensive tasks.

## Requirements
### Software Dependencies
- Python
- MPI Library (e.g., Open MPI or MS-MPI)
- Required Python Packages:
    - matplotlib
    - numpy
    - mpi4py
    - Pillow
    - Tkinter
    - Pickle

### Installation Instructions
- Install Python and required dependencies
    - with pip you will have to ```pip install``` all the packages stated above
    - with conda you can create your environment via the following command
    ```bash
    conda env create -f environment.yml
    ```
- Install Open MPI or MS-MPI on your system and confirm that the path to ```mpiexec.exe``` is properly configured in your system environment variables, ensuring the ```mpiexec``` command functions correctly in your shell.

## Outputs