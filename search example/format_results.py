
import json
import sys


inp = sys.argv[1]
with open(inp, "r") as f:
    data: dict[str, dict[str, list[list[str|float]]]] = json.loads(f.read())

    schemes = {s:i for (i, s) in enumerate(data.keys())}
    def start_adjust():
        print("\\begin{minipage}{\\textwidth}")   
        print("\\begin{adjustwidth}{-3cm}{-3cm}")
    def start_table():
        print("{{")
        print("\\rowcolors{2}{gray!25}{white}")
        print("\\begin{center}")
        print("\\begin{tabularx}{17cm}{ | X l | X l | X l | }")
        print("\\hline \\")
        print("\\rowcolor{gray!50}& &".join(data.keys())+"&\\\\")
        print("\\hline \\")
    def end_table():
        print("\\hline")
        print("\\end{tabularx}")
        print("\\end{center}")
        print("}}")
        print("\\end{adjustwidth}")
        print("\\end{minipage}")
        print("\\\\")

    per_m: dict[str, dict[str, list[list[str|float]]]] = {}
    for (scheme, d) in data.items():
        for (m, z) in d.items():
            if m not in per_m:
                per_m[m] = {}
            per_m[m][scheme] = z
    
    for (m, d) in per_m.items():
        start_adjust()
        print("\\vspace{\\baselineskip}")
        print(f"\\hspace{{1cm}}\\textbf{{Metric: {m}}} \\\\")
        print("\\vspace{-0.8\\baselineskip}")
        start_table()
        l: list[None | list[list[str|float]]] = [None for _ in range(len(schemes))]
        for (scheme, lst) in d.items():
            l[schemes[scheme]] = lst
        b: list[list[tuple[str, float]]] = [[(x[0], abs(x[1])) for x in y[:10]] for y in l]
        f = True
        for p in zip(*b):
            z = m if f else ""
            f = False
            print("&".join(f"\\raggedleft {x[0]} & ${x[1]:.2f}$" for x in p) + " \\\\")
        end_table()