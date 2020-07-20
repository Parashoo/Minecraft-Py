import subprocess
import importlib
import sys

module_dict = {"OpenGL": "PyOpenGL", "glfw": "glfw", "numpy": "numpy", "glm": "PyGLM", "PIL": "Pillow"}

def install_packages():
    with open("setup.log", "w") as setup:
        for i in module_dict:
            try:
                importlib.import_module(i)
            except ImportError:
                subprocess.check_call([sys.executable, "-m", "pip", "install", module_dict[i]])
            setup.write(module_dict[i] + "\n")
