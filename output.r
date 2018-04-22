library(edgeR)
seqdata <- read.delim('GSE98877_gf_vs_spf_rna_seq.txt',stringAsFactors = False)
countdata <- seqdata[,-(1)]
rownames(countdata) <- seqdata[,1]
colnames(countdata) <- c("SPF01","SPF02","SPF03","SPF04","GF01","GF02","GF03","GF04","GF05","GF06","GF07","GF08","GF09","SPF05","SPF06","SPF07")
dgList <- DGEList(counts = countdata, genes = rownames(countdata))
dgList$samples
plotMDS(dgList)
title'MDS plot'
sampleType <- rep('GF',ncol(dgList))
sampleType[grep('SPF',colnames(dgList))]<-'SPF')
designMat <- model.matrix(~0 + sampleType)
dgList <- estimateGLMCommonDisp(dgList, design= designMat)
dgList <- estimateGLMTrendedDisp(dgList, design = designMat)
dgList <- estimateGLMTagwiseDisp(dgList, design = designMat)
plotBCV(dgList)
title'BCV plot'
fit <- glmQLFit(dgList,designMat)
head(fit$coefficients)
contrast_matrix <- makeContrasts(sampleType(GF) - sampleType(SPF),levels = designMat)
Result <- glmQLFTest(fit,contrast = contrast_matrix)
topTags(Result)
write.csv(topTags(Result),file= 'Top 10 differentially expressed genes using edgeR.csv')
is.de <- decideTestsDGE(Result)
summary(is.de)
plotMD(Result,status = is.de,values = c(1,-1),col=c('red','blue'),legend = 'topright')