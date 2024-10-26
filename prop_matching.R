#install.packages("MatchIt")
library(MatchIt)
library(readxl)
library("writexl")
#install.packages("cobalt")
library(cobalt)

setwd("C:/Users/lukas/Desktop/bachelor/data")
#data=read_excel("matching_input.xlsx") 
data=read_excel("financials_merge_treatment_and_control_categorials_cleaned_imputed_dropped.xlsx")


data$reverse_treatment <- ifelse(data$treatment == 1, 0, 1)
#data_dropped=data[,-c("Rechtsform","bvdid")]

initial_unbalance=function(){
m.out0 <- matchit(treatment ~ ., data = data,
                  method = NULL, distance = "glm")

summary(m.out0)}


set.seed("1871")
m.out1 <- matchit(reverse_treatment ~ toas+closdate_year, data = data,
                  method = "nearest", distance = "glm",caliper=0.4, group = "bvdid",ratio = 3)

summary(m.out1, un = FALSE)
#print(m.out1$discarded)

love_plot=function(){
love.plot(m.out1, 
                       var.order = "alphabetical", 
                       abs = TRUE, 
                       thresholds = c(m = 0.1),
                       colors = c("blue", "red"),
                       title = "Balance Before and After Matching")}


matched_data=match.data(m.out1)
#matched_data_complete=cbind(matched_data,data[,concat_vars])
write_xlsx(matched_data, "matching_output.xlsx")