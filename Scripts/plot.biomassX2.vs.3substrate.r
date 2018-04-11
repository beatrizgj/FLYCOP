#!/usr/bin/env Rscript

# FLYCOP 
# Author: Beatriz García-Jiménez
# April 2018

args = commandArgs(trailingOnly=TRUE)
if (length(args)<10) {
  stop("At least 10 arguments must be supplied: <input_file.txt> <output_file.pdf> <met1_ID> <met2_ID> <met3_ID> <endCycle> <title> <colSubs1> <colSubs2> <colSubs3> [<strain1> <strain2>]", call.=FALSE)
} else {
  inputFile=args[1]
  outFile=args[2]
  met1=args[3]
  met2=args[4]
  met3=args[5]
  endCycle=as.numeric(args[6])
  title=args[7]
  color1=args[8]
  color2=args[9]
  color3=args[10]
  if(length(args)==12){
    strain1=args[11]
    strain2=args[12]
  }else{
    strain1="strain1"
    strain2="strain2"
  }
}

xMax=endCycle

df0=read.csv(inputFile,sep='\t',header=FALSE,col.names=c('hours','biomass1','biomass2','sub1','sub2','sub3'))
df=df0[0:endCycle*10,]

yMax=max(df$biomass1,df$biomass2)
y2Max=max(df$sub1,df$sub2,df$sub3)


pdf(outFile,pointsize=20)
par(lwd=3)
plot(df$hours*0.1,df$biomass1,xlab='time(h)',ylab='biomass (gr/L)',type='l',lwd=4,col="green",xlim=c(0,xMax),ylim=c(0,yMax),main=title)
par(new=TRUE)
plot(df$hours*0.1,df$biomass2,xlab="",ylab="",type='l',lwd=4,col="red",xlim=c(0,xMax),ylim=c(0,yMax))
par(new=TRUE,lwd=2)
plot(df$hours*0.1,df$sub1,type='l',col=color1,axes=FALSE,xlab="",ylab="",lwd=4,xlim=c(0,xMax),ylim=c(0,y2Max))
par(new=TRUE)
plot(df$hours*0.1,df$sub2,type='l',col=color2,axes=FALSE,xlab="",ylab="",lwd=4,xlim=c(0,xMax),ylim=c(0,y2Max))
par(new=TRUE)
plot(df$hours*0.1,df$sub3,type='l',col=color3,axes=FALSE,xlab="",ylab="",lwd=4,xlim=c(0,xMax),ylim=c(0,y2Max))

axis(side=4)
mtext('metabolite Conc. (mM)',side=4,cex=par("cex.lab"))
par(lty=1)
legend("topleft", c(strain1,strain2,met1,met2,met3), lty=c(1,1,1,1,1), lwd=c(3,3,4,4,4), col=c("green","red",color1,color2,color3),cex=0.65)
invisible(dev.off())
