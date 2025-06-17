import os
import subprocess
import sys
import venv


def create_venv(venv_dir="venv"):
    print("Creating virtual environment...")
    venv.create(venv_dir, with_pip=True)


def install_requirements(venv_dir="venv"):
    print("Installing packages from requirements.txt...")
    pip_path = os.path.join(venv_dir, "Scripts" if os.name == "nt" else "bin", "pip")
    subprocess.check_call([pip_path, "install", "-r", "requirements.txt"])


def run_main_script(venv_dir="venv", entry="ec2_init.py"):
    print("Running your app...")
    python_path = os.path.join(
        venv_dir, "Scripts" if os.name == "nt" else "bin", "python"
    )
    subprocess.check_call([python_path, entry])


def main():
    create_venv()
    install_requirements()
    run_main_script()
    print("\nAll done!")


if __name__ == "__main__":
    main()
