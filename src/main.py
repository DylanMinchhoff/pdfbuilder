from parse import parse
from simplify import simplify
from convert_assignments import convert_assignments
from uniqify import uniqify
from opt import opt
from eval import eval
from util import SequentialNameGenerator


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(prog="471c")
    parser.add_argument("input", type=argparse.FileType("r"), help="")
    parser.add_argument("-o", "--output", type=argparse.FileType("w"), default="-")
    parser.add_argument("--run", action="store_true", help="")
    parser.add_argument("--args", default=[], action="extend", nargs="*", type=int, help="")
    options = parser.parse_args()

    with options.input as input:
        fresh = SequentialNameGenerator()

        program = parse(input.read())
        result = simplify(program, fresh)
        result = convert_assignments(result)
        result = uniqify(result, fresh)
        result = opt(result)

        print(result, file=options.output)

        if options.run:
            from eval import Int, eval

            result = eval(result, [Int(a) for a in options.args])
            print(result)
