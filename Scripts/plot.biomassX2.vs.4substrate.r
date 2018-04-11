#!/usr/bin/env Rscript

# FLYCOP 
# Author: Beatriz García-Jiménez
# April 2018

args = commandArgs(trailingOnly=TRUE)
if (length(args)<10) {
  stop("At least 10 arguments must be supplied: <input_file.txt> <output_file.pdf> <met1_ID> <met2_ID> <met3_ID> <met4_ID> <endCycle> <title> <colSubs1> <colSubs2> <colSubs3> <colSubs4> [<strain1> <strain2>]", call.=FALSE)
} else {
  inputFile=args[1]
  outFile=args[2]
  met1=args[3]
  met2=args[4]
  met3=args[5]
  met4=args[6]
  endCycle=as.numeric(args[7])
  title=args[8]
  color1=args[9]
  color2=args[10]
  color3=args[11]
  color4=args[12]
  if(length(args)==14){
    strain1=args[13]
    strain2=args[14]
  }else{
    strain1="strain1"
    strain2="strain2"
  }
}


xMax=endCycle

df=read.csv(inputFile,sep='\t',header=FALSE,col.names=c('hours','biomass1','biomass2','sub1','sub2','sub3','sub4'))
yMax=max(df$biomass1,df$biomass2)
y2Max=max(df$sub1,df$sub2,df$sub3,df$sub4)

pdf(outFile,pointsize=20)
par(lwd=3)
plot(df$hours*0.1,df$biomass1,xlab='time(h)',ylab='biomass (gr/L)',type='l',lwd=4,col="green",ylim=c(0,yMax),main=title)
par(new=TRUE)
plot(df$hours*0.1,df$biomass2,xlab="",ylab="",type='l',lwd=4,col="red",ylim=c(0,yMax))
par(new=TRUE,lwd=2)
plot(df$hours*0.1,df$sub1,type='l',col=color1,axes=FALSE,xlab="",ylab="",lwd=4,ylim=c(0,y2Max))
par(new=TRUE)
plot(df$hours*0.1,df$sub2,type='l',col=color2,axes=FALSE,xlab="",ylab="",lwd=4,ylim=c(0,y2Max))
par(new=TRUE)
plot(df$hours*0.1,df$sub3,type='l',col=color3,axes=FALSE,xlab="",ylab="",lwd=4,ylim=c(0,y2Max))
par(new=TRUE)
plot(df$hours*0.1,df$sub4,type='l',col=color4,axes=FALSE,xlab="",ylab="",lwd=4,ylim=c(0,y2Max))

axis(side=4)
mtext('metabolite Conc. (mM)',side=4,cex=par("cex.lab"))
par(lty=1)
legend("left", c(strain1,strain2,met1,met2,met3,met4), lty=c(1,1,1,1,1,1), lwd=c(3,3,4,4,4,4), col=c("green","red",color1,color2,color3,color4),cex=0.65)
invisible(dev.off())
