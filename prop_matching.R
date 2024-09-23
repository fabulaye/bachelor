#install.packages("MatchIt")
library(MatchIt)
library(readxl)

#args <- commandArgs(trailingOnly = TRUE)

#if(args)==""
setwd("C:/Users/lukas/Desktop/bachelor/data")
data=read_excel("treatment_and_control_merged_imputed.xlsx") 



vars_ignored=c("X","closdate_year","bvdid","summed_annual_subsidy","annual_subsidy","treatment_weight","country","consolidation code","country iso code","accounting practice","source (for publicly quoted companies)","estimated operating revenue","estimated employees","employees original range value","closdate")
#should I include compcat? What are the criteria for including vars in matching--> lit wieder checken 
matchit_data=data[,!colnames(data) %in% vars_ignored]

m.out0 <- matchit(treatment ~ ., data = matchit_data,
                  method = NULL, distance = "glm")

summary(m.out0)
#stratified
m.out1 <- matchit(treatment ~ .-bvdid, data = matchit_data,
                  method = "nearest", distance = "glm",caliper=0.4,exact = ~ bvdid)

summary(m.out1, un = FALSE)

plot(m.out1, type = "jitter", interactive = FALSE)

matched_data=match.data(m.out1)
