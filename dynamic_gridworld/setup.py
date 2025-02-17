from setuptools import setup, find_packages

setup(
    name="dynamic-gridworld",                
    version="0.1.0",                         
    description="A dynamic grid world environment for reinforcement learning",
    author="Mark",                           
    packages=find_packages(),                
    install_requires=[
        "gym",                               
        "pygame",                            
        "numpy"                              
    ],
    python_requires=">=3.7",                 
)
