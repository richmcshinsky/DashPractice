# Dash Practice
==============================
This takes fake data about payments made over the last ten years and plots it using Dash. The purpose is to practice using a variety of Dash functionality in order to become familier with the software and packages. 
To run the Dash application, just use [python app.py] in the terminal in the src folder of the project. 
The model was quickly made from pycaret and is not meant for realistic predictions. This project is to demonstrate Dash, not predictive quality. 

Project Organization
------------

    ├── README.md                  <- The top-level README for developers using this project.
    │
    ├──  notebooks                 <- Jupyter notebooks. 
    │   └── Data_Exploration.ipynb
    │
    ├── requirements.txt           <- The requirements file for reproducing the analysis environment
    │
    ├──  src                       <- Source code for use in this project.
    │   ├──  app.py                <- The main application file that builds the visuals and interactions
    │   ├── data                   <- Data files
    │   │   └──  benchmarks.csv
    │   │
    │   ├──   functions            <- code pulled out of app.py to reduce complexity and fluff
    │   │   └── data_prep.py
    │   │
    ├── tests                      <- unit tests for the functions, not yet implemented
