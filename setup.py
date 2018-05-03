from distutils.core import setup
import py2exe


Mydata_files = [('.', ['config.json'])]

setup(
    options = {
                "py2exe": {
                    "packages": ["encodings"],
                    "bundle_files": 1
                }
            },
    zipfile = None,
    console = ["pykong.py"],
    data_files = Mydata_files,
)

#python setup.py py2exe