# use a different env than the framework, usually you need a clean terminal and use anaconda or miniconda
# if not yet, need to install pyhf

import logging
import json
import numpy as np
import sys

import matplotlib.pyplot as plt

import pyhf

from pyhf.contrib.viz import brazil

logging.basicConfig(level=logging.INFO)
model_file = sys.argv[1]

# open the mode file stored in json
with open(model_file) as serialized:
    spec = json.load(serialized)
workspace = pyhf.Workspace(spec)
model = workspace.model(measurement_name="Measurement")
data = workspace.data(model)
# look at the model spec
# def pretty_json(jsonlike, indent=None):
#   if indent is None: indent = 4
#   print(json.dumps(jsonlike, indent=indent))
# pretty_json(model.spec)
print(f"Channels in model: {model.config.channels}\n")
print(f"Number of bins in channel: {model.config.channel_nbins}\n")

init_pars = model.config.suggested_init()
print(f"expected data: {model.expected_data(init_pars)}")

par_bounds = model.config.suggested_bounds()
print(f"initialization parameters: {model.config.suggested_init()}")
print(f"init values: {init_pars}")
print(f"bounds: {par_bounds}")

# fit
unconpars = pyhf.infer.mle.fit(data, model)
print(f"parameters post unconstrained fit: {unconpars}")

# upper limit
(
    obs_limit,
    exp_limits,
    (poi_tests, tests),
) = pyhf.infer.intervals.upper_limits.upper_limit(
    data, model, np.linspace(0, 0.1, 100), level=0.01, return_results=True
)
# new versions only!

fig, ax = plt.subplots(figsize=(10, 7))
artists = brazil.plot_results(poi_tests, tests, test_size=0.05, ax=ax)
print(tests)
print(f"expected upper limits: {exp_limits}")
print(f"observed upper limit : {obs_limit}")
print(obs_limit)
#fig.show()
fig.savefig('tmp_limit.png')

