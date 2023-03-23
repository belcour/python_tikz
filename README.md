# python_tikz
Interface to create tikz figures from python scripts


## Example of usage:

Here is a simple snippets to create a figure and output it to a file.
    with open('figure.tex') as out:
        fig = tikz(out, standalone=True)
        fig.gen_header(figsize=(-1.0, 5.0, -1.0, 2.0))

        [.. print commands ..]

        fig.gen_footer()