def generate_theory_table():
    models = [
        ("GR", "Fixed G, no scalar field", "✓", "✗", "✗"),
        ("Brans-Dicke", "Scalar-tensor with varying G", "✓", "✓", "✗"),
        ("f(R)", "Higher-order curvature terms", "✓", "✗", "✓"),
        ("Horndeski", "Most general ghost-free scalar-tensor", "✓", "✓", "✓"),
        ("DRIFT", "Recursive entropy-gradient dynamics", "✓", "✓", "✓✓")
    ]
    
    header = "| Model | Description | Vary G | Teff Coupling | Topology Adaptive |\n"
    header += "|-------|-------------|--------|----------------|-------------------|\n"
    rows = [f"| {m[0]} | {m[1]} | {m[2]} | {m[3]} | {m[4]} |" for m in models]
    
    table_md = header + "\n".join(rows)
    with open("output/theory_comparison.md", "w") as f:
        f.write(table_md)

    print("📑 Theory comparison table saved as Markdown.")
