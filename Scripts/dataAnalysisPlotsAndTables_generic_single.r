#!/usr/bin/env Rscript

# FLYCOP 
# Author: Beatriz García-Jiménez
# April 2018

suppressMessages(library(car))
suppressMessages(library(ellipse))
suppressMessages(library(RColorBrewer))

args = commandArgs(trailingOnly=TRUE)
if (length(args)<3) {
  stop("At least 3 arguments must be supplied: <domainName (string)> <experimentID (number)> <fitnessID (string)>", call.=FALSE)
} else {
  domainName=args[1]
  id=args[2]
  fitnessID=args[3]
}


# cleaning
suffix=paste("Scenario",id,sep="")
setwd(paste(domainName,'_scenario',id,'_FLYCOPdataAnalysis',sep=""))


my_colors <- brewer.pal(11, "RdYlBu")
my_colors=colorRampPalette(my_colors)(25)
data=read.csv('tableParamWithFitness.csv',sep='\t',header=TRUE) 
formula=formula(paste("~",paste(colnames(data),collapse="+"),sep=""))

header=paste(suffix,", Fitness=",fitnessID,sep="")
# correlation ellipse plot
corrMatrix<-cor(data)
pdf(paste('correlationEllipsePlot_',suffix,".pdf",sep=""),title=header)
plotcorr(corrMatrix, col=my_colors[corrMatrix*15+15], type="lower", mar=c(1,1,1,1), main=paste("Correlation plot.",suffix))
invisible(dev.off())
write.table(corrMatrix,paste('corrMatrix_',suffix,".txt",sep=""),quote=FALSE,sep="\t")

# Scatterplot, with lower diagonal with correlations:
panel.cor <- function(x, y, digits = 3, prefix = "", cex.cor=1, ...) # from help(pairs) # Only correlation, with modifications from below code
{
  usr <- par("usr"); on.exit(par(usr))
  par(usr = c(0, 1, 0, 1))
  # correlation coefficient
  r <- cor(x,y)
  txt <- format(c(r, 0.123456789), digits = digits)[1]
  txt <- paste("r= ", txt, sep = "")
  text(0.5, 0.6, txt, cex=1)
}
pdf(paste('scatterplotMatrix_',suffix,"_withCorr.pdf",sep=""),title=header)
scatterplotMatrix(formula, data=data, smooth=list(smoother=""),lower.panel=panel.cor,main=header)
invisible(dev.off())

# Removing not stable configurations
# To retrieve standard deviation values:
tableSd=read.table('avgfitnessAndStdev.txt',sep=",",header=FALSE,row.names=NULL)
colnames(tableSd)=c('mean','sd')
pdf(paste('fitnessVsSd_',suffix,'.pdf',sep=""))
plot(tableSd,main=paste("Correlation plot.",suffix))
invisible(dev.off())
pdf(paste('fitnessVsSd_',suffix,'sdLt0.1.pdf',sep=""))
plot(tableSd[tableSd$sd<0.1,],main=paste("Correlation plot",suffix,'sd<0.1',sep=", "))
invisible(dev.off())
data$sd=tableSd$sd
data <- subset(data,select=c(1:(length(data)-2),sd,fitness))
dataSorted <- data [with(data, order(-fitness)), ]
write.table(dataSorted,paste('dataTable_',suffix,".txt",sep=""),quote=FALSE,sep="\t",row.names=TRUE, col.names=TRUE)
data_sdLt0.1=data[data$sd<0.1,]
pdf(paste('scatterplotMatrix_',suffix,'sdLt0.1.pdf',sep=""),title=paste(header,'sd<0.1',sep=', '))
scatterplotMatrix(formula,data=data_sdLt0.1, smooth=list(smoother=""),main=paste(header,'sd<0.1',sep=', '))
invisible(dev.off())

corrMatrix<-cor(data_sdLt0.1)
pdf(paste('correlationEllipsePlot_',suffix,'sdLt0.1.pdf',sep=""),title=paste(header,'sd<0.1',sep=', '))
plotcorr(corrMatrix, col=my_colors[corrMatrix*15+15], type="lower", mar=c(1,1,1,1), main=paste(header,'sd<0.1',sep=', '))
invisible(dev.off())

sink(paste('corrMatrices_',suffix,'.txt',sep=''))
print('All configurations:')
print(dim(data)[1])
cor(data)
print('Sd<0.1:')
print(dim(data_sdLt0.1)[1])
cor(data_sdLt0.1)
sink()
