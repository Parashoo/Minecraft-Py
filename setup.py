import subprocess
import importlib
import sys

module_dict = {"OpenGL": "PyOpenGL", "glfw": "glfw", "PIL": "Pillow", "numpy": "numpy", "glm": "PyGLM"}

def install_packages():
    with open("setup.log", "w") as setup:
        for i in module_dict:
            try:
                importlib.import_module(i)
                setup.write("existing: " + module_dict[i] + "\n")
            except ImportError:
                if sys.platform == "linux":
                    subprocess.check_call([sys.executable, "-m", "pip", "install", module_dict[i]])
                    setup.write("installed: " + module_dict[i] + "\n")
                elif sys.platform == "win32":
                    subprocess.check_call(["python", "-m", "pip", "install", module_dict[i]])
                    setup.write("installed: " + module_dict[i] + "\n")
