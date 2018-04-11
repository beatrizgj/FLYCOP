#!/usr/bin/env Rscript

# FLYCOP 
# Author: Beatriz García-Jiménez
# April 2018

args = commandArgs(trailingOnly=TRUE)
if (length(args)<4) {
   stop("At least 4 arguments must be supplied: <input_file.txt> <output_file.pdf> <met1_ID> <met2_ID> <strain1> <strain2>.", call.=FALSE)
} else {
  inputFile=args[1]
  outFile=args[2]
  met1=args[3]
  met2=args[4]
  if(length(args)==6){
    strain1=args[5]
    strain2=args[6]
  }else{
    strain1="strain1"
    strain2="strain2"
  }
}

df=read.csv(inputFile,sep='\t',header=FALSE,col.names=c('hours','biomass1','biomass2','sub1','sub2'))

yMax=max(df$biomass1,df$biomass2)
yMax=1.5

pdf(outFile,pointsize=20)
par(lwd=3)
plot(df$hours*0.1,df$biomass1,xlab='time(h)',ylab='biomass (gr/L)',type='l',lwd=4,col="black",ylim=c(0,yMax))
par(new=TRUE)
plot(df$hours*0.1,df$biomass2,xlab="",ylab="",type='l',lwd=4,col="black",lty=2,ylim=c(0,yMax))
par(new=TRUE,lwd=2)
plot(df$hours*0.1,df$sub1,type='l',lwd=4,col="blue",axes=FALSE,xlab="",ylab="",ylim=c(0, max(df$sub1,df$sub2)))
par(new=TRUE)
plot(df$hours*0.1,df$sub2,type='l',lwd=4,col="red",axes=FALSE,xlab="",ylab="",ylim=c(0, max(df$sub1,df$sub2)))
axis(side=4)
mtext('metabolite Conc. (mM)',side=4,cex=par("cex.lab"))
par(lty=1)
legend("topright", c(strain1,strain2,met1,met2), lty=c(1,2,1,1), lwd=c(4,4,4,4), col=c("black","black","blue","red"))
invisible(dev.off())
