# Installing
1. Clone this repo using `git clone git@github.com:jaynavar/Copysets.git`.
1. `cd` into the Copysets repo.
1. Install the dependencies using `sudo pip install -r requirements.txt`.

# Running Figure 6 reproduction

`$ python2 Main_Figure6.py [options]`

Use `-h` to list all options available. Some important parameters are `-r` which allows you to render the graph locally without saving to a file, and `-s` which saves all data and figures to a timestamped directory under `data_Figure6`. You can use the `--simulation` flag to generate the data using simulations rather than the equations.

# Running Repeated Failures experiment

`$ python2 Main_RepeatedFailures.py [options]`

Use `-h` to list all options available. Some important parameters are `-r` which allows you to render the graph locally without saving to a file, and `-s` which saves all data and figures to a timestamped directory under `data_RepeatedFailures`.

# Viewing Experiment Data

All data from the experiments used in the report are stored under `data_Figure6` and `data_RepeatedFailures`. Each experiment includes a `TRIAL_INFO.txt` file which lists the parameters used for the given experiment. You can reproduce the figures from any given experiment by running the appropriate tool (i.e. `Main_Figure6.py` or `Main_RepeatedFailures.py`) with the `--load <experiment_dir>/DATA.json` option. Note that for `Main_Figure6.py` you must ensure the parameters passed into the tool are the same as those specified in the `TRIAL_INFO.txt` file for the given experiment. The data files are stored in the experiment directories in a file labelled `DATA.json`.
