########################################################################
## Mon Jun 20 16:15:00 PDT 2016
##
## reads in ICPSR-LabDataSlavesByAgeSex18{5,6}0.csv  and melts and munges
## it so that it can be read in the long way
########################################################################
library(reshape2)
d50<-read.csv(file="ICPSR-LabDataSlavesByAgeSex1850.csv",header=T)
d50$X<-NULL
d50.long<-melt(d50,id=1:4)
write.csv(x=d50.long,file="ICPSR-LabDataSlavesByAgeSex1850-long.csv",row.names=F)

d60<-read.csv(file="ICPSR-LabDataSlavesByAgeSex1860.csv",header=T)
d60$X<-NULL
d60.long<-melt(d60,id=1:4)
write.csv(x=d60.long,file="ICPSR-LabDataSlavesByAgeSex1860-long.csv",row.names=F)
