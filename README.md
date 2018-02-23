# Harvard Crime Maps

By the Harvard Open Data Project


Based off prior work from https://github.com/Harvard-Open-Data-Project/crimewatchbeta.

## Setup

First, set up a Python3 virtual environment:

```
virtualenv -p python3 venv
```

Switch to that environment:

```
source venv/bin/activate
```

Install required packages:

```
pip install -r requirements.txt
```

Now get a Jupyter kernel for this project:

```
python -m ipykernel install --user --name=crime
```

Finally open up Jupyter:

```
jupyter notebook
```

Be sure to change the Jupyter Kernel to your new `crime` one. Go to Kernel > Change kernel > crime from the notebook page.

To quit the virtual env, use `deactivate`.

Need help? See:

* <https://stackoverflow.com/questions/23842713/using-python-3-in-virtualenv>
* <https://stackoverflow.com/questions/33496350/execute-python-script-within-jupyter-notebook-using-a-specific-virtualenv>
