class edge_R:
    def __init__(self, filename):
        self.filename = filename
        self.exp_group_name = input("Enter experimental group name: ")
        self.exp_sample_number = int(input("Enter the number of experimental samples: "))
        self.control_group = input("Enter control group name: ")
        self.con_sample_number = int(input("Enter the number of control samples: "))

    def edge_R_script(self):
        with open(self.filename, 'r') as inf, open('edge_r_out.r', 'w') as outf:
            outf.write("library(edgeR)\n")
            outf.write("x <- read.csv('%s', row.names = 1)\n" % self.filename)
            outf.write("group <- factor(c(rep('%s',%d), rep('%s',%d)))\n" %
                       (self.exp_group_name, self.exp_sample_number, self.control_group, self.con_sample_number))
            outf.write("y <- DGEList(counts = x,group=group)\n")
            outf.write("y <- calcNormFactors(y)\n")
            outf.write("design <- model.matrix(~group)\n")
            outf.write("y<-estimateDisp(y,design)\n")
            outf.write("fit <-glmFit(y,design)\n")
            outf.write("lrt <-glmLRT(fit,coef=2)\n")
            outf.write("topTags(lrt)\n")
            outf.write("write.csv(topTags(lrt),file= 'top_edgeR_lrt.csv')\n")
            outf.write("is.de <- decideTestsDGE(lrt)\n")
            outf.write("summary(is.de)\n")
            outf.write(
                "plotMD(lrt,status = is.de,values = c(1,-1),col=c('red','blue'),legend = 'topright')\n")


filename = input("Enter the filename: ")
e = edge_R(filename)
e.edge_R_script()
