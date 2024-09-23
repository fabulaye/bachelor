estimate_vi=function(data){
  col_names=colnames(data)
  matrix_fill=matrix(0,nrow=ncol(data),ncol=ncol(data))
  df_inc_mse=data.frame(matrix_fill)
  rownames(df_inc_mse)=colnames(data)
  df_purity=data.frame(matrix_fill)
  rownames(df_purity)=colnames(data)
  index=1
  for (col in col_names){
    
    # Subset data: response is the variable with missing values
    # and predictors are the remaining columns
    predictors <- data[ , !colnames(data) %in% col]
    response <- data[ , col]
    
    # Fit a random forest model using complete cases only
    rf_model <- randomForest(x = predictors,
                             y = response, 
                             importance = TRUE)
    
    # Extract and print variable importance for this model
    vi <- importance(rf_model)
    
    inc_mse=vi[,1]
    inc_mse[col]=0
    puritiy=vi[,2]
    #names(inc_mse)=col
    #df_inc_mse=cbind(df_inc_mse,inc_mse)
    df_inc_mse[names(inc_mse),index]=inc_mse
    colnames(df_inc_mse)[index] <- col
    #df_purity=cbind(df_purity,puritiy)
    #browser()
    index=index+1
  }
  return(df_inc_mse)
}

vi_test=estimate_vi(imputed_reduced)
