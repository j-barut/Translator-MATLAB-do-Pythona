
MATLAB_BUILTINS = {
    'disp': 'print',
    'zeros': 'np.zeros',
    'ones': 'np.ones',
    'eye': 'np.eye',
    'rand': 'np.random.rand',
    'linspace': 'np.linspace',
    'sin': 'np.sin',
    'cos': 'np.cos',
    'tan': 'np.tan',
    'exp': 'np.exp',
    'log': 'np.log',
    'log10': 'np.log10',
    'sqrt': 'np.sqrt',
    'sum': 'np.sum',
    'mean': 'np.mean',
    'max': 'np.max',
    'min': 'np.min',
    'length': 'len',
    'size': 'np.shape'
}

MATLAB_RESERVED_NAMES = set(MATLAB_BUILTINS.keys())