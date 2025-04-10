import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import subprocess
import threading
from Graphs import *

class FractalUI:
    def __init__(self):    
        # Create the main window
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.root.title("Fractal Generation In Parallel")
        # Create a notebook (tab control) to hold the tabs
        self.tab_control = ttk.Notebook(self.root)

        # Create tabs and add them to the notebook
        tab1 = self.create_tab(self.tab_control, "Generate Fractal")
        tab2 = self.create_tab(self.tab_control, "View Fractals")
        tab3 = self.create_tab(self.tab_control, "View Results")

        # Create widgets for each tab
        self.setupGenFractalTab(tab1)
        self.setupViewFractalTab(tab2)
        self.setupViewResultsTab(tab3)

        # Pack the tab control to make it visible
        self.tab_control.pack(fill="both", expand=True)

        self.root.mainloop()

    def create_tab(self, tab_control, title):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text=title)
        return tab

    def setupGenFractalTab(self, tab):
        # Create and place labels
        lblFractType = ttk.Label(tab, text="Fractal Type:")
        lblFractType.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        lblFractSize = ttk.Label(tab, text="Fractal Size:")
        lblFractSize.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        lblNoProcessors = ttk.Label(tab, text="Number of Processors:")
        lblNoProcessors.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        # Create and place option selection boxes
        fractTypeOptions = ["Mandelbrot", "Julia"]

        self.fractalType = tk.StringVar()
        self.fractalType.set(fractTypeOptions[0])  # Set default option

        option_box1 = ttk.Combobox(tab, textvariable=self.fractalType, values=fractTypeOptions)
        option_box1.grid(row=0, column=1, padx=10, pady=5)

        # Create and place option selection boxes
        fractSizeOptions = ["1000x1000", "2000x2000","5000x5000", "10000x10000"]

        self.fractSize = tk.StringVar()
        self.fractSize.set(fractSizeOptions[0])  # Set default option

        option_box2 = ttk.Combobox(tab, textvariable=self.fractSize, values=fractSizeOptions)
        option_box2.grid(row=1, column=1, padx=10, pady=5)

        # Create and place option selection boxes
        fractNPOptions = ["2", "4", "8", "16", "32"]

        self.noProcessors = tk.StringVar()
        self.noProcessors.set(fractNPOptions[0])  # Set default option

        option_box3 = ttk.Combobox(tab, textvariable=self.noProcessors, values=fractNPOptions)
        option_box3.grid(row=2, column=1, padx=10, pady=5)

        btnGenerateFractalSeries = ttk.Button(tab, text="Generate Fractal in Series",  command=lambda: self.generateFractal(True))
        btnGenerateFractalSeries.grid(row=3, column=0, padx=10, pady=10)
        
        btnGenerateFractal = ttk.Button(tab, text="Generate Fractal in Parallel",  command=lambda: self.generateFractal(False))
        btnGenerateFractal.grid(row=3, column=1, padx=10, pady=10)

    def setupViewFractalTab(self,tab):
        btnSelectImage = tk.Button(tab, text="Select Image", height=5,  command=self.selectImage)
        btnSelectImage.pack(padx=10, pady=10, fill=tk.X)

    def setupViewResultsTab(self, tab):
        # Create and place labels
        lblFractType = ttk.Label(tab, text="Fractal Type:")
        lblFractType.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        lblFractSize = ttk.Label(tab, text="Fractal Size:")
        lblFractSize.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # Create and place option selection boxes
        resultTypeOptions = ["Mandelbrot", "Julia"]

        self.resultType = tk.StringVar()
        self.resultType.set(resultTypeOptions[0])  # Set default option

        option_box1 = ttk.Combobox(tab, textvariable=self.resultType, values=resultTypeOptions)
        option_box1.grid(row=0, column=1, padx=10, pady=5)

        # Create and place option selection boxes
        resultSizeOptions = ["1000x1000", "2000x2000","5000x5000", "10000x10000"]

        self.resultSize = tk.StringVar()
        self.resultSize.set(resultSizeOptions[0])  # Set default option

        option_box2 = ttk.Combobox(tab, textvariable=self.resultSize, values=resultSizeOptions)
        option_box2.grid(row=1, column=1, padx=10, pady=5)

        # Speedup per no processors
        btnViewSpeedupCurve = ttk.Button(tab, text="View Speedup Curve", command=lambda: displaySpeedupGraph(self.resultSize.get(), self.resultType.get()))
        btnViewSpeedupCurve.grid(row=2, column=1, padx=10, pady=10)

        # Efficiency per no processors
        btnViewEfficiencyCurve = ttk.Button(tab, text="View Efficiency Curve", command=lambda: displayEfficiencyGraph(self.resultSize.get(), self.resultType.get()))
        btnViewEfficiencyCurve.grid(row=3, column=1, padx=10, pady=10)

        # Size over time difference for serial and parallel
        btnViewEfficiencyCurve = ttk.Button(tab, text="Serial VS Parallel", command=lambda: displaySerialVSParallel(self.resultType.get()))
        btnViewEfficiencyCurve.grid(row=4, column=1, padx=10, pady=10)


    def generateFractal(self, isSeries):
        # Create the loading screen to let the user know something is happening
        loading_screen = tk.Toplevel(self.root)
        loading_screen.title("Generating")
        loading_screen.geometry("500x200")
        label = ttk.Label(loading_screen, text="Generating {} Fractal of size {} with {} processors, please wait...".format(self.fractalType.get(), self.fractSize.get(), 1 if isSeries else self.noProcessors.get()))
        label.pack(pady=20)

        # Used as parameters for the parallel execution
        noProcessors = self.noProcessors.get()
        scriptName = '{}Parallel.py'.format(self.fractalType.get())
        size = self.fractSize.get().split('x')

        # executes the fractal generation task
        def executeFractaltask():
            command = ['python', '{}.py'.format(self.fractalType.get()), size[0]] if isSeries else ['mpiexec', '-n', noProcessors, 'python', scriptName, size[0]] 
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            stdout, stderr = process.communicate()
            loading_screen.destroy()
            tk.messagebox.showinfo(title='fractal generated Sucessfully', message=stdout)


        # Start the mpi task on a new thread
        genFractThread = threading.Thread(target=executeFractaltask)
        genFractThread.start()


    def selectImage(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")], initialdir='Fractals/')
        if file_path:
            image = Image.open(file_path)
            image.show()


if __name__=="__main__":
    interface = FractalUI()
