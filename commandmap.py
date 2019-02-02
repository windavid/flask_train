import argparse
import inspect


class CommandMap(dict):
    """
    register functions for command line interface
    use as decorator
    define typing if you want to pass not string arguments to functions
    args will be passed as keyword arguments
    se bellow for an usage example
    ref: Light version of fire.Fire() from fire pip package
    """
    def __init__(self, description="write description here"):
        super().__init__()
        self.p = argparse.ArgumentParser(description=description)
        self.subp = self.p.add_subparsers(dest="fm_command")
        self.subp.required = True

    def register(self, name=None, _help=None):
        name2 = name
        _help2 = _help

        def decorator(call):
            fa = inspect.getfullargspec(call)
            name = name2 or call.__name__
            self[name] = call

            _help = _help2 or inspect.getdoc(call)
            call_parser = self.subp.add_parser(name, description=_help)
            for arg in fa.args:
                _type, _def = None, None
                if fa.annotations:
                    _type = fa.annotations.get(arg, None)
                if fa.defaults:
                    _def = fa.defaults.get(arg, None)
                call_parser.add_argument(arg, type=_type, default=_def, help=f"({_type!s})")
            return call

        return decorator

    def parse_args(self, args=None, namespace=None):
        self.args = self.p.parse_args(args=args, namespace=namespace)
        return self.args

    def launch(self):
        dargs = vars(self.args)  # make dict copy of namespace
        name = dargs.pop('fm_command')
        return self[name](**dargs)