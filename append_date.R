# Add in column with current date
# > 'selection' command
#

args <- commandArgs()
#print(args)
csv.tmp <- args[6]
df.tmp <- read.csv(csv.tmp, header=F)

sink(csv.tmp)

colnames(df.tmp) <- c("member")

today <- Sys.Date()
today <- format(today, format="%m%d")

df.tmp$date <- today
print(df.tmp)

sink()
