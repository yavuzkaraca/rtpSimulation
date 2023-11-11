CONTINUOUS_GRADIENTS = "continuous_gradients"
WEDGES = "wedges"

SUBSTRATE_TYPE = "substrate_type"
MIN_VALUE = "min_value"
MAX_VALUE = "max_value"
ROWS = "rows"
COLS = "cols"
OFFSET = "offset"
ADAPTATION = "adaptation_enabled"
GC_COUNT = "gc_count"
GC_SIZE = "gc_size"
STEP_SIZE = "step_size"
STEP_AMOUNT = "step_amount"
X_STEP_POSSIBILITY = "x_step_possibility"
Y_STEP_POSSIBILITY = "y_step_possibility"
SIGMA = "sigma"

# Default configuration values
DEFAULT_CONFIG = {
    SUBSTRATE_TYPE: CONTINUOUS_GRADIENTS,
    MIN_VALUE: 2,
    MAX_VALUE: 40,
    ROWS: 50,  # number of rows = max value along y-axis
    COLS: 100,  # number of cols = max value along x-axis
    OFFSET: 20,  # should equal gc_size * 2
    ADAPTATION: False,
    GC_COUNT: 50,
    GC_SIZE: 10,
    STEP_SIZE: 1,
    STEP_AMOUNT: 40000,
    X_STEP_POSSIBILITY: 0.50,
    Y_STEP_POSSIBILITY: 0.50,
    SIGMA: 0.18
}

# Current configuration settings
config = DEFAULT_CONFIG
