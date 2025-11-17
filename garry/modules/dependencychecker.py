import sys
import subprocess
import importlib
import traceback

DEPENDENCIES = [
    ("pypdf", "pypdf"),
    ("langchain==0.0.350", "langchain"),
    ("langchain-community==0.0.1", "langchain_community"),
    ("langchain-openai", "langchain_openai"),
    ("langchain-core", "langchain_core"),
    ("langchain-text-splitters", "langchain_text_splitters"),
    ("openai", "openai"),
    ("geopy", "geopy"),
    ("timezonefinder==6.2.0", "timezonefinder"), 
    ("tzdata", "tzdata"),
    ("python-dotenv", "dotenv"),
    ("requests", "requests"),
    ("chromadb", "chromadb"),
]

def dep_install(requirement, import_name):
    print(f"\nChecking: {requirement}")
    try:
        importlib.import_module(import_name)
        print(f"✔ Already installed: {import_name}")
        return True

    except ImportError:
        print(f"⚠ Missing: {import_name} → installing '{requirement}'...")

        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", requirement])
            print(f"✔ Installed: {requirement}")
            importlib.import_module(import_name)
            return True

        except Exception as e:
            print(f"\n❌ FAILED TO INSTALL: {requirement}")
            traceback.print_exception(type(e), e, e.__traceback__)
            return False

def missing_dependencies_exist():
    for requirement, import_name in DEPENDENCIES:
        try:
            importlib.import_module(import_name)
        except ImportError:
            return True  # At least one is missing
    return False         # All installed

def start_depinstal():
    mislib = missing_dependencies_exist()
    if mislib is True:
        check = input("WARNING - This prototype requires download of some dependencies. Write YES to continue instalation or close the program.").strip().lower()
        if check != "yes":
            raise SystemExit("Installation cancelled by user.")
        print("==============================================")
        print("   INSTALLING GARRY REQUIRED DEPENDENCIES")
        print("==============================================")
            
        failed = []
            
        for req, mod in DEPENDENCIES:
            success = dep_install(req, mod)
            if not success:
                failed.append(req)
            
        print("\n==============================================")
        if failed:
            print("⚠ SOME DEPENDENCIES FAILED TO INSTALL:")
            for f in failed:
                print("   - " + f)
        else:
            print("✔ ALL DEPENDENCIES SUCCESSFULLY INSTALLED!")
        print("==============================================\n")
        return None
    else:
        return None