setwd('/Users/2kisa/programming II/')
library(limma)
library(affy)
mydata<-read.table('GSE23006_series_matrix.txt_out.txt',header = T, row.names = 1, fill = T)
mymatrix <- as.matrix(mydata)
design <- model.matrix(~ 0+factor(c(rep(1,6),rep(2,3),rep(3,3),rep(2,3),rep(3,3),rep(2,3),rep(3,3),rep(2,3),rep(3,3),rep(2,3),rep(3,3),rep(2,3),rep(3,3),rep(2,3),rep(3,3))))
colnames(design) <- c("group1", "group2", "group3")
fit <- lmFit(mymatrix, design)
contrast.matrix <- makeContrasts(group1-group2, group1-group3, levels=design)
fit2 <- contrasts.fit(fit, contrast.matrix)
fit2 <- eBayes(fit2)
results <- decideTests(fit2)
write.fit(fit2, results, "myoutputdata.txt", adjust="BH")


mouth<-as.matrix(topTable(fit2, coef=1, number=30, adjust="BH"))
skin<-as.matrix(topTable(fit2, coef=2, number=30, adjust="BH"))


tops<-cbind(row.names(mouth),row.names(skin))
col_names<-c('mouth','skin')
colnames(tops)<-col_names
tops<-as.matrix(tops)

library(gplots)
mouthc<-c()
skinc<-c()
for (j in 1:30){
  for (i in 1:45101){
    if (row.names(mymatrix)[i]==tops[j,1]){
      mouthc<-cbind(mouthc,mymatrix[i,1:48])
    }
    if (row.names(mymatrix)[i]==tops[j,2]){
      skinc<-cbind(skinc,mymatrix[i,1:48])
    }
  }
}
colnames(mouthc)<-tops[,1]
colnames(skinc)<-tops[,2]
heatmap.2(mouthc,margins = c(8, 10))
heatmap.2(skinc,margins = c(8, 10))
