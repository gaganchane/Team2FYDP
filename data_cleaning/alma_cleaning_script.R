setwd("/Users/mbr/Desktop/FYDP4B")
getwd()

# read almabase output
alma_data <- read.csv("data-buddy-6.csv", header=T, na.strings=c("", " ", "NA"), stringsAsFactors=FALSE)
View(alma_data)

# create vector of relevant columns
relevant_cols <- c("Name", "Linkedin.URL", "Education..School.1", "Education..Duration.1", "Education..School.2", 
                   "Education..Duration.2", "Employment..Employer.1", "Employment..Title.1", "Employment..Duration.1", 
                   "Employment..Location.1", "Employment..Employer.2", "Employment..Title.2", "Employment..Duration.2", 
                   "Employment..Location.2", "Employment..Employer.3", "Employment..Title.3", "Employment..Duration.3", 
                   "Employment..Location.3", "Employment..Employer.4", "Employment..Title.4", "Employment..Duration.4", 
                   "Employment..Location.4", "Employment..Employer.5", "Employment..Title.5", "Employment..Duration.5", 
                   "Employment..Location.5")

# create a new data frame with only relevant columns
relevant_data <- alma_data[relevant_cols]
relevant_data <- data.frame(lapply(relevant_data, trimws), stringsAsFactors = FALSE)
relevant_data[1,5]
View(relevant_data)

# initialize data frame to which final output will be added
names <- c("ID", "WID", "Name", "URL", "Year", "Employer", "Position", "Duration", "Location")
init_df <- data.frame(matrix(ncol = 9, nrow = 0), stringsAsFactors=FALSE)
colnames(init_df) <- names
count <- 1

# populate init_df with almabase output data
for(i in 1:nrow(relevant_data)){
  
  if(!is.na(relevant_data[i, 8])){
    init_df[count, 1] <- i
    init_df[count, 2] <- paste(c(i, "." , 1), collapse = " ")
    init_df[count, 3] <- relevant_data[i,1]
    init_df[count, 4] <- relevant_data[i,2]
    
    if(relevant_data[i, 5] == "University of Waterloo"){
      duration_split <- strsplit(relevant_data[i, 6], " - ")
      init_df[count, 5] <- duration_split[[1]][2]
    } else {
      duration_split <- strsplit(relevant_data[i, 4], " - ")
      init_df[count, 5] <- duration_split[[1]][2]
    }
    
    init_df[count, 6] <- relevant_data[i,7]
    init_df[count, 7] <- relevant_data[i,8]
    init_df[count, 8] <- relevant_data[i,9]
    init_df[count, 9] <- relevant_data[i,10]
    count = count + 1
    print(count)
  }
  
  if(!is.na(relevant_data[i, 12])){
    init_df[count, 1] <- i
    init_df[count, 2] <- paste(c(i, "." , 2), collapse = " ")
    init_df[count, 3] <- relevant_data[i,1]
    init_df[count, 4] <- relevant_data[i,2]
    
    if(relevant_data[i, 5] == "University of Waterloo"){
      duration_split <- strsplit(relevant_data[i, 6], " - ")
      init_df[count, 5] <- duration_split[[1]][2]
    } else {
      duration_split <- strsplit(relevant_data[i, 4], " - ")
      init_df[count, 5] <- duration_split[[1]][2]
    }
    
    init_df[count, 6] <- relevant_data[i,11]
    init_df[count, 7] <- relevant_data[i,12]
    init_df[count, 8] <- relevant_data[i,13]
    init_df[count, 9] <- relevant_data[i,14]
    count = count + 1
    print(count)
  }
  
  if(!is.na(relevant_data[i, 16])){
    init_df[count, 1] <- i
    init_df[count, 2] <- paste(c(i, "." , 3), collapse = " ")
    init_df[count, 3] <- relevant_data[i,1]
    init_df[count, 4] <- relevant_data[i,2]
    
    if(relevant_data[i, 5] == "University of Waterloo"){
      duration_split <- strsplit(relevant_data[i, 6], " - ")
      init_df[count, 5] <- duration_split[[1]][2]
    } else {
      duration_split <- strsplit(relevant_data[i, 4], " - ")
      init_df[count, 5] <- duration_split[[1]][2]
    }
    
    init_df[count, 6] <- relevant_data[i,15]
    init_df[count, 7] <- relevant_data[i,16]
    init_df[count, 8] <- relevant_data[i,17]
    init_df[count, 9] <- relevant_data[i,18]
    count = count + 1
    print(count)
  }
  
  if(!is.na(relevant_data[i, 20])){
    init_df[count, 1] <- i
    init_df[count, 2] <- paste(c(i, "." , 4), collapse = " ")
    init_df[count, 3] <- relevant_data[i,1]
    init_df[count, 4] <- relevant_data[i,2]
    
    if(relevant_data[i, 5] == "University of Waterloo"){
      duration_split <- strsplit(relevant_data[i, 6], " - ")
      init_df[count, 5] <- duration_split[[1]][2]
    } else {
      duration_split <- strsplit(relevant_data[i, 4], " - ")
      init_df[count, 5] <- duration_split[[1]][2]
    }
    
    init_df[count, 6] <- relevant_data[i,19]
    init_df[count, 7] <- relevant_data[i,20]
    init_df[count, 8] <- relevant_data[i,21]
    init_df[count, 9] <- relevant_data[i,22]
    count = count + 1
    print(count)
  }
  
  if(!is.na(relevant_data[i, 24])){
    init_df[count, 1] <- i
    init_df[count, 2] <- paste(c(i, "." , 5), collapse = " ")
    init_df[count, 3] <- relevant_data[i,1]
    init_df[count, 4] <- relevant_data[i,2]
    
    if(relevant_data[i, 5] == "University of Waterloo"){
      duration_split <- strsplit(relevant_data[i, 6], " - ")
      init_df[count, 5] <- duration_split[[1]][2]
    } else {
      duration_split <- strsplit(relevant_data[i, 4], " - ")
      init_df[count, 5] <- duration_split[[1]][2]
    }
    
    init_df[count, 6] <- relevant_data[i,23]
    init_df[count, 7] <- relevant_data[i,24]
    init_df[count, 8] <- relevant_data[i,25]
    init_df[count, 9] <- relevant_data[i,26]
    count = count + 1
    print(count)
  }
}

# replace "&amp;" with "&"
init_df$Employer <- gsub('&amp;', '&', init_df$Employer)
init_df$Position <- gsub('&amp;', '&', init_df$Position)
View(init_df)

# write init_df to csv
write.csv(init_df, file = "output.csv", row.names = FALSE)

df <- read.csv("mgmt_data_clean.csv")
View(df)
