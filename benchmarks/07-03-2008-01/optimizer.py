import astoptimizer
config = astoptimizer.Config('builtin_funcs', 'pythonbin')
astoptimizer.patch_compile(config)

import benchmark1

benchmark1.__main__()