class Pars:
    def __init__(self,filename):
        # Taking in filename when creating instance and creating outfile name.
        self.filename = filename
        self.outname = self.filename+"_out.txt"

    def parser(self):
        with open(self.filename, 'r') as infile, open(self.outname,'w') as outfile:
            for line in infile.readlines():
                if line.startswith("!"):
                    continue

                else:
                    outfile.write(line)

# Testing.
project= Pars("GSE23006_series_matrix.txt")
project.parser()