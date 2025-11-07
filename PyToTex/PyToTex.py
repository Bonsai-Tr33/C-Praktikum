class SendToTex:
    def __init__(self, filePath):
        self.filePath = filePath

    def __str__(self):
        pass

    def SendValue(self, value, name='value.Tex'):
        '''
            value (int, float, str): value being transformed into Tex
            name (str): name of .Tex file
        '''
        with open(f'{self.filePath}/{name}.Tex', 'w') as f:
            f.write(str(value))

    def SendTable(self, colnum, head, colZip, name='table.Tex'):
        '''
            colnum (int): Number of columns
            head (list[str]): Column headers
            colZip (list[list]): Data in the format [[col1_vals], [col2_vals], ...]
            name (str): name of .Tex file
        '''
        if len(head) != colnum or len(colZip) != colnum:
            raise ValueError('Number of headers and columns must match colnum')

        rows = list(zip(*colZip))

        table_content = []
        table_content.append(r"\begin{tabular}{" + " | ".join(['c'] * colnum) + "}")
        table_content.append(r"\hline")

        table_content.append(" & ".join(head) + r" \\")
        table_content.append(r"\hline")

        for row in rows:
            table_content.append(" & ".join(map(str, row)) + r" \\")
        table_content.append(r"\hline")

        table_content.append(r"\end{tabular}")

        with open(f'{self.filePath}/{name}.Tex', 'w') as f:
            f.write("\n".join(table_content))