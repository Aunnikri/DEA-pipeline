import sys


class edge_r:
    def __init__(self, filename):
        self.filename = filename
        self.outfile = self.filename + ".txt"
        self.sample_number = input("Enter the number of samples: ")
        self.names = input("Enter the sample names: ")
        self.colnames = ','.join('"{}"'.format(word) for word in self.names.split())
        self.exp_group_count = input("Enter number of experimental groups: ")
        while True:
            self.exp_group_name = input("Enter experimental group name: ")
            self.exp_group = self.exp_group_name.split()
            if len(self.exp_group) == 1:
                break
            else:
                continue

        self.control_group = input("Enter control group name: ")
        self.MDS_title = input("Enter desired title for data exploration plot: ")
        self.BCV_title = input("Enter desired title for BCV plot: ")

    def edge_r_data(self):
        self.stringAsFactors = input(
            "Require string as factor in data frame? Enter True or False:  ")
        if self.stringAsFactors == "True":
            return True
        elif self.stringAsFactors == "False":
            return False

    def edge_r_script(self):
        with open(self.outfile, 'r') as inf, open('output.r', 'w') as outf:
            outf.write("library(edgeR)\n")
            outf.write("seqdata <- read.delim('%s',stringAsFactors = %s)\n" %
                       (self.outfile, self.stringAsFactors))
            outf.write("countdata <- seqdata[,-(1)]\n")
            outf.write("rownames(countdata) <- seqdata[,1]\n")
            outf.write("colnames(countdata) <- c(%s)\n" % self.colnames)
            outf.write("dgList <- DGEList(counts = countdata, genes = rownames(countdata))\n")
            outf.write("dgList$samples\n")
            outf.write("plotMDS(dgList)\n")
            outf.write("title'%s'\n" % self.MDS_title)
            outf.write("sampleType <- rep('%s',ncol(dgList))\n" % self.control_group)
            outf.write("sampleType[grep('%s',colnames(dgList))]<-'%s')\n" %
                       (self.exp_group_name, self.exp_group_name))
            outf.write("designMat <- model.matrix(~0 + sampleType)\n")
            outf.write("dgList <- estimateGLMCommonDisp(dgList, design= designMat)\n")
            outf.write("dgList <- estimateGLMTrendedDisp(dgList, design = designMat)\n")
            outf.write("dgList <- estimateGLMTagwiseDisp(dgList, design = designMat)\n")
            outf.write("plotBCV(dgList)\n")
            outf.write("title'%s'\n" % self.BCV_title)
            outf.write("fit <- glmQLFit(dgList,designMat)\n")
            outf.write("head(fit$coefficients)\n")
            outf.write("contrast_matrix <- makeContrasts(sampleType(%s) - sampleType(%s),levels = designMat)\n" %
                       (self.control_group, self.exp_group_name))
            outf.write("Result <- glmQLFTest(fit,contrast = contrast_matrix)\n")
            outf.write("topTags(Result)\n")
            outf.write(
                "write.csv(topTags(Result),file= 'Top 10 differentially expressed genes using edgeR.csv')\n")
            outf.write("is.de <- decideTestsDGE(Result)\n")
            outf.write("summary(is.de)\n")
            outf.write(
                "plotMD(Result,status = is.de,values = c(1,-1),col=c('red','blue'),legend = 'topright')")


filename = input("Enter the filename: ")
e = edge_r(filename)

e.edge_r_data()
e.edge_r_script()
