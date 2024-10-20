#("missForest")
library("readxl")
#install.packages("readxl")
#remove.packages("missForest")
library("writexl")
#install.packages("writexl")
library("missForestPredict")
install.packages("missForestPredict")
#library("randomForest")
#library("corrplot")
#install.packages("randomForest")

directory <- commandArgs(trailingOnly = TRUE)
directory="C:/Users/Lukas/Desktop/bachelor/data"
#print(directory)
setwd(directory)
df_input=read.csv("miss_forest_input.csv")

#df_input=as.numeric(df_input)
#df_input=df_input %>% select(-"X")
df_input["closdate_year"]=factor(df_input[,"closdate_year"])
df_input["treatment"]=factor(df_input[,"treatment"])
df_input["compcat"]=factor(df_input[,"compcat"])
df_input["bvdid"]=factor(df_input[,"bvdid"])
df_input["integrated_dummy"]=factor(df_input[,"integrated_dummy"])
df_input["startup"]=factor(df_input[,"startup"])
df_input["rechtsform"]=factor(df_input[,"rechtsform"])
df_input["STATUS"]=factor(df_input[,"STATUS"])


col_na_percent=colSums(is.na.data.frame(df_input))/nrow(df_input)
df_input=df_input[col_na_percent<1]
col_na_percent=colSums(is.na.data.frame(df_input))/nrow(df_input)

dont_impute=names(col_na_percent[col_na_percent>=0.5])

pred_matrix=create_predictor_matrix(df_input)
pred_matrix[dont_impute,]=0

set.seed("1871")
mf_model_reduced=missForest(df_input,predictor_matrix=pred_matrix)

errors_reduced=mf_model_reduced$OOB_err
#n_iterations=length(mf_model_reduced$models)
#to_be_dropped=errors_reduced["variable"][errors_reduced["iteration"]==n_iterations & errors_reduced["NMSE"]>=0.6]

errors_reduced=errors_reduced[order(errors_reduced[,"NMSE"],decreasing=TRUE),]

imputed_reduced=mf_model_reduced$ximp
imputed_reduced=imputed_reduced[!colnames(imputed_reduced) %in% dont_impute]

dont_impute_df=data.frame(dont_impute)

write_xlsx(dont_impute_df, "not_imputed_columns.xlsx")
write_xlsx(imputed_reduced, "miss_forest_output.xlsx")
write_xlsx(errors_reduced, "miss_forest_errors.xlsx")
