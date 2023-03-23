'''
    Example of usage: 
        print('generate figure 8')

        self.indent = gen_header(f, figsize=(-1.0, 5.0, -1.0, 2.0), standalone=False)

        # Add first polygon
        poly_A = np.zeros((3, 2))
        poly_A[0] = [0, 0]
        poly_A[1] = [1, 0]
        poly_A[2] = [0, 1]


        # Add second polygon
        poly_B = np.zeros((4, 2))
        poly_B[0] = [0, 0]
        poly_B[1] = [1, 0]
        poly_B[2] = [1, 1]
        poly_B[3] = [0, 1]

        angle = 45.0
        rot = np.array([
            [ np.cos(2.0*np.pi*angle/360), np.sin(2.0*np.pi*angle/360)],
            [-np.sin(2.0*np.pi*angle/360), np.cos(2.0*np.pi*angle/360)],
            ])
        poly_B = poly_B @ rot
        poly_B += [3, 0]

        # Draw elements
        style_A = {
                #'color': 'red!60!black',
                'fill': 'red!40!white',
                'fill opacity': '0.2'
                }
        style_B = {
        #'color': 'green!60!black',
        'fill': 'green',
        'fill opacity': '0.1'
        }
        add_shape(poly_B, f, style=style_B, self.indent=self.indent)
        add_shape(poly_A, f, style=style_A, self.indent=self.indent)
'''

import numpy as np


class tikz:
    def __init__(self, out, standalone=False):
        self.indent = ''
        self.out = out
        self.standalone = standalone

    def gen_style(self, style={}):
        txt = ""
        if type(style) == dict:
            for key in style:
                if style[key] == '' or style[key] == None:
                    txt += key + ','
                else:
                    txt += "{}={},".format(key, style[key])
        return txt
    
    def gen_header(self, figsize=(), tikzStyle={}):
        if self.standalone:
            self.out.writelines([
                "\\documentclass[crop, tikz]{standalone}\n",
                "\n",
                "\\usepackage{pgfplots}\n",
                "\\pgfplotsset{compat=1.16}\n",
                "\n",
                "\\usepackage{libertine}\n",
                "\\usepackage{libertinust1math}\n",
                "\\usepackage[T1]{fontenc}\n",
                "\n",
                "\\begin{document}\n",
                "\n",
            ])
            self.indent += '\t'
        self.out.writelines([
            self.indent+"\\setlength{\\fboxsep}{0pt}%\n",
            self.indent+"\\begin{{tikzpicture}}[{}]()\n".format(self.gen_style(tikzStyle)),
            self.indent+"\t\\begin{scope}\n",
        ])
        self.indent += '\t'
        if len(figsize) == 4:
            self.out.writelines([
                self.indent+"\\clip ({}, {}) rectangle ({}, {});\n".format(figsize[0], figsize[2], figsize[1], figsize[3]),
                self.indent+"\\draw[help lines] ({}, {}) grid ({}, {});\n".format(figsize[0], figsize[2], figsize[1], figsize[3]),
            ])
        return '\t\t'
    
    def gen_footer(self):
        self.indent = self.indent[0:-1]
        self.out.writelines([
            self.indent + "\\end{scope}\n",
            self.indent + "\\end{tikzpicture}%\n",
        ])
        if self.standalone:
            self.out.writelines([
                "\\end{document}\n"
            ])
    
    
    '''
        poly: polygon representation (list of points)
        self.out: stream to self.output code to
    '''
    def add_shape(self, poly, style={'color': 'red'}):
        txt = self.indent + "\\draw["
        txt += self.gen_style(style)
        txt += "] "
    
        nb_pts = poly.shape[0]
        for k in range(-1, nb_pts):
            x = poly[k]
            
            txt += "({:.2f}, {:.2f})".format(x[0], x[1])
            txt += " -- " if k < nb_pts-1 else ";\n"
        self.out.write(txt)
    
    def add_fill(self, poly, style={'color': 'red'}):
        txt = self.indent + "\\fill["
        txt += self.gen_style(style)
        txt += "] "
    
        nb_pts = poly.shape[0]
        for k in range(-1, nb_pts):
            x = poly[k]
            
            txt += "({:.2f}, {:.2f})".format(x[0], x[1])
            txt += " -- " if k < nb_pts-1 else ";\n"
        self.out.write(txt)
    
    def set_clip(self, poly):
        txt = self.indent + "\\clip "
        nb_pts = poly.shape[0]
        for k in range(-1, nb_pts):
            x = poly[k]
            
            txt += "({:.2f}, {:.2f})".format(x[0], x[1])
            txt += " -- " if k < nb_pts-1 else ";\n"
        self.out.write(txt)
    
    '''
        Add a line from point A to point B
            A: a 2D point
            B: a 2D point
    '''
    def add_lines(self, A, B, style={}):
        assert(A.shape[0] == B.shape[0])
        txt = ''
        for k in range(A.shape[0]):
            txt += self.indent + "\\draw["
            txt += self.gen_style(style)
            txt += "] "
            txt += "({:.2f}, {:.2f})".format(A[k,0], A[k,1])
            txt += " -- "
            txt += "({:.2f}, {:.2f})".format(B[k,0], B[k,1])
            txt += ";\n"
        self.out.write(txt)
    
    def add_paths(self, paths, style={}):
        assert(len(paths.shape) == 3)
        txt = ''
        for i in range(paths.shape[0]):
            txt += self.indent + "\\draw["
            txt += self.gen_style(style)
            txt += "] "
            for k in range(paths.shape[1]):
                txt += "({:.2f}, {:.2f})".format(paths[i,k,0], paths[i,k,1])
                txt += " -- " if k < paths.shape[1]-1 else ''
            txt += ";\n"
        self.out.write(txt)
    
    def add_path(self, pts, style={}):
        txt = ''
        txt += self.indent + "\\draw["
        txt += self.gen_style(style)
        txt += "] "
        for k in range(pts.shape[0]):
            txt += "({:.2f}, {:.2f})".format(pts[k,0], pts[k,1])
            txt += " -- " if k < pts.shape[0]-1 else ''
        txt += ";\n"
        self.out.write(txt)
    
    def add_points(self, pts, radius=2, style={}):
        lines = []
        #lines.append('\\draw plot[{}] coordinates {{\n'.format(self.gen_style(style)))
        for k in range(pts.shape[0]):
            lines.append("{}\\fill[{}] ({}, {}) circle ({}pt);\n".format(self.indent, self.gen_style(style), pts[k,0], pts[k,1], radius))
            #lines.append('({:.2f}, {:.2f})\n'.format(pts[k,0], pts[k,1]))
        #lines.append('};\n')
        self.out.writelines(lines)
    
    def add_arrow(self, A, B, style={}):
        assert(A.shape[0] == B.shape[0])
        txt = ''
        for k in range(A.shape[0]):
            txt += self.indent + "\\draw[arrows = {-Stealth[reversed, reversed]},"
            txt += self.gen_style(style)
            txt += "] "
            txt += "({:.2f}, {:.2f})".format(A[k,0], A[k,1])
            txt += " to [bend left=45] "
            txt += "({:.2f}, {:.2f})".format(B[k,0], B[k,1])
            txt += ";\n"
        self.out.write(txt)
    
    def add_text(self, P, text, style={}):
        txt = self.indent
        txt += '\\node[{}] at ({:.2f}, {:.2f}) {{ {} }};\n'.format(self.gen_style(style), P[0], P[1], text)
        self.out.write(txt)
    
    def begin_scope(self, style={}):
        self.out.write(self.indent + '\n')
        self.out.write(self.indent + '\\begin{{scope}}[{}]\n'.format(self.gen_style(style)))
        self.indent += '\t'
        
    def end_scope(self):
        self.indent = self.indent[0:-1]
        self.out.write(self.indent + '\\end{scope}\n')
    
    
    def begin_plot(self, style={}):
        self.out.write(self.indent + '\\begin{axis}[' + self.gen_style(style) + ']\n')
        self.indent += '\t'
    
    def end_plot(self):
        self.indent = self.indent[0:-1]
        self.out.write(self.indent + '\\end{axis}\n')
    
    def plot(self, X, Y, style={}, legend=None):
        assert(len(X.shape) == 1)
        assert(len(Y.shape) == 1)
        assert(X.shape[0] == Y.shape[0])
        if not legend:
            style['forget plot'] = None
        self.out.write(self.indent + '\\addplot[' + self.gen_style(style) +'] coordinates {\n')
        for k in range(X.shape[0]):
            self.out.write(self.indent+ '\t({:.5f}, {:.5f})\n'.format(X[k], Y[k]))
        self.out.write(self.indent + '};\n')
        if legend:
            self.out.write(self.indent + '\\addlegendentry{' + legend + '}\n')
        self.out.write('\n')

    def add_rgb_color(self, name, r, g, b):
        self.out.write(self.indent + '\\definecolor{' + name + '}{rgb}{' + str(r) + ',' + str(g) + ',' + str(b) + '}\n')

    def add_cmd(self, cmd):
        self.out.write(self.indent + cmd)
