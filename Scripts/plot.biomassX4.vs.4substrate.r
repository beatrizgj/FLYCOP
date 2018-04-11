#!/usr/bin/env Rscript

# FLYCOP 
# Author: Beatriz García-Jiménez
# April 2018

args = commandArgs(trailingOnly=TRUE)
if (length(args)<6) {
  stop("At least 10 arguments must be supplied: <input_file.txt> <output_file.pdf> <met1_ID> <met2_ID> <met3_ID> <met4_ID> [<strain1> <strain2> <strain3> <strain4>]", call.=FALSE)
} else {
  inputFile=args[1]
  outFile=args[2]
  met1=args[3]
  met2=args[4]
  met3=args[5]
  met4=args[6]
  if(length(args)==10){
    strain1=args[7]
    strain2=args[8]
    strain3=args[9]
    strain4=args[10]
  }else{
    strain1="strain1"
    strain2="strain2"
    strain3="strain3"
    strain4="strain4"
  }
}

color1='deepskyblue'
color2='coral'
color3='darkolivegreen1'
color4='violet'

df=read.csv(inputFile,sep='\t',header=FALSE,col.names=c('hours','biomass1','biomass2','biomass3','biomass4','sub1','sub2','sub3','sub4'))

yMax=max(df$biomass1,df$biomass2,df$biomass3,df$biomass4)
y2Max=max(df$sub1,df$sub2,df$sub3,df$sub4)

pdf(outFile,pointsize=20)
par(lwd=3)
plot(df$hours*0.1,df$biomass1,xlab='time(h)',ylab='biomass (gr/L)',type='l',lwd=4,col="blue",lty=1,ylim=c(0,yMax))
par(new=TRUE)
plot(df$hours*0.1,df$biomass2,xlab="",ylab="",type='l',lwd=4,col="red",lty=1,ylim=c(0,yMax))
par(new=TRUE)
plot(df$hours*0.1,df$biomass3,xlab="",ylab="",type='l',lwd=4,col="green",lty=1,ylim=c(0,yMax))
par(new=TRUE)
plot(df$hours*0.1,df$biomass4,xlab="",ylab="",type='l',lwd=4,col="purple",lty=1,ylim=c(0,yMax))
par(new=TRUE,lwd=2)
plot(df$hours*0.1,df$sub1,type='l',col=color1,axes=FALSE,xlab="",ylab="",lty=6,lwd=4,ylim=c(0,y2Max))
par(new=TRUE)
plot(df$hours*0.1,df$sub2,type='l',col=color2,axes=FALSE,xlab="",ylab="",lty=6,lwd=4,ylim=c(0,y2Max))
par(new=TRUE)
plot(df$hours*0.1,df$sub3,type='l',col=color3,axes=FALSE,xlab="",ylab="",lty=6,lwd=4,ylim=c(0,y2Max))
par(new=TRUE)
plot(df$hours*0.1,df$sub4,type='l',col=color4,axes=FALSE,xlab="",ylab="",lty=6,lwd=4,ylim=c(0,y2Max))

axis(side=4)
mtext('metabolite Conc. (mM)',side=4,cex=par("cex.lab"))
par(lty=1)
legend("topleft", c(strain1,strain2,strain3,strain4,met1,met2,met3,met4), lty=c(1,1,1,1,6,6,6,6), lwd=c(4,4,4,4,4,4,4,4), col=c("blue","red","green","purple",color1,color2,color3,color4),cex=0.65)
invisible(dev.off())
