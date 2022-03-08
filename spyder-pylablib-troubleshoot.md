
## `conda`, `spyder`, and `pylablib` installation

The prerequsites for the `spyder` IDE and the `pylablib` library are currently in conflict when installed to their most recent versions. These instructions allow you to have a downgraded version of `spyder` installed with the other equipment control prerequisites. 

### New `conda` virtual environment

To create a new `conda` virtual environment use the following command.

`conda create --name {name} python=3.8 spyder=4.1.5 scipy numpy matplotlib pyserial`

- `conda create --name {name}` creates an environment with the given name in `{name}`. An example would be `conda create --name control` to create an environment named `control`.
- `python=3.8 spyder=4.1.5` installs these packages with these specific versions. Note the version number of `spyder`.
- `scipy numpy matplotlib pyserial` are other prerequisite packages which should be installed at the same time in the `conda` command. You may add more packages here or install them after.

`conda` will then present you with all the prerequisite packages for these packages. Proceed with `y` then `enter`.

### Additional `pip` installs for `spyder`

Next you need:

- `pip install pyqt5==5.12.3 --user` 
- `pip install pyqtwebengine=5.12.3 --user`

Let both install and this will allow you to start `spyder`.

### Control packages

To finish creating the environment for equipment control, you need:  

- `pip install pyvisa --user`
- `pip install pylablib --user`

Again let both install themselves and their dependencies.

## Conclusion

Congrats, this should have installed the prerequisite packages for equipment control to and allow you to use them with `spyder` in their own environment. 

Let us know if these instructions no longer work for you. Remember to **not** update packages these packages (`pyqt5, pyqtwebengine, spyder, pylablib`) as these will most likely break your installation. 









____________________________________________________________________
Section added March 03, 2022 by Daniel Hutama

Alternatively, you can set up your fresh install to work with Spyder. After installing through Anaconda, execute the following pip commands in your Anaconda prompt.

pip install --upgrade spyder=4.1.5 --user
pip uninstall pyqt5
pip install --upgrade pyqt5=5.12.3 --user
pip install pylablib --user
pip install pyvisa
If you still have issues after this, try downgrading to Python 3.6 and use pip to upgrade/downgrade any conflicting dependencies.

If you still have issues, feel free to contact me.

-DH
