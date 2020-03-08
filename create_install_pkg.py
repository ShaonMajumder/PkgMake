import time

import os
import shutil

import subprocess
import platform

pkgname = 'PkgMake'

def execute_shell(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line 
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


def cleaning_before_commit(pkgname):

	files=pkgname+""".egg-info
build
dist
"""+pkgname+"""/__pycache__
"""
	print("Cleaning files -",files)

	files = files.split('\n')

	for file in files:
		if os.path.exists(file):
			try:
				shutil.rmtree(file)
			except:
				os.remove(file)




if __name__ == '__main__':
	mode = 'pypi'
	username = input("Give pypi username : ")
	password = input("Give pypi password : ")
	if platform.system() == 'Linux':
		if mode == 'pypi':
			commands = f"""python3 setup.py sdist
twine upload dist/* -u """+username+""" -p """+password
		elif mode == 'local':
			commands = f"""pip3 uninstall """+pkgname+""" -y
python3 setup.py sdist bdist_wheel
python3 setup.py install
pip3 install --upgrade """+pkgname

	elif platform.system() == 'Windows':
		if mode == 'pypi':
			commands = f"""python setup.py sdist
twine upload dist/* -u """+username+""" -p """+password
		elif mode == 'local':
			commands = f"""pip3 uninstall """+pkgname+""" -y
python setup.py sdist bdist_wheel
python setup.py install
pip3 install --upgrade """+pkgname


	commands = commands.split("\n")

	for command in commands:
		for path in execute_shell(command):
		    print(path, end="")

	cleaning_before_commit(pkgname)

