# Add in column with select topic
# > 'selection' command
#

args <- commandArgs()
#print(args)
csv.tmp <- args[6]
df.tmp <- read.csv(csv.tmp, header=F)

sink(csv.tmp)

#colnames(df.tmp) <- c("member")

#today <- Sys.Date()
#today <- format(today, format="%m%d")

choice <- 

df.tmp$topic <- choice
print(df.tmp)

sink()
