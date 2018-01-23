setwd("/Users/mbr/Desktop/FYDP4B")
getwd()

df <- read.csv("mgmt_clean_data.csv")
View(df)

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
names <- c("ID", "WORK_ID", "COOP_ID", "Name", "URL", "Year", "Company", "Position", "Duration", "Start.Date", 
           "Start.Month", "Start.Year", "End.Date.pres", "End.Year", "End.Month", "Full.Location", "City", "Province", "Country")
init_df <- data.frame(matrix(ncol = 19, nrow = 0), stringsAsFactors=FALSE)
colnames(init_df) <- names
count <- 1

# populate init_df with almabase output data
for(i in 1:nrow(relevant_data)){
  
  if(!is.na(relevant_data[i, 8])){
    init_df[count, 1] <- i
    init_df[count, 2] <- i
    init_df[count, 3] <- i
    init_df[count, 4] <- relevant_data[i,1]
    init_df[count, 5] <- relevant_data[i,2]
    
    if(relevant_data[i, 5] == "University of Waterloo"){
      edu_duration_split <- strsplit(relevant_data[i, 6], " - ")
      init_df[count, 6] <- edu_duration_split[[1]][2]
    } else {
      edu_duration_split <- strsplit(relevant_data[i, 4], " - ")
      init_df[count, 6] <- edu_duration_split[[1]][2]
    }
    
    init_df[count, 7] <- relevant_data[i,7]
    init_df[count, 8] <- relevant_data[i,8]
    
    emp_duration_split <- strsplit(relevant_data[i, 9], " - ")
    start_duration_split <- strsplit(emp_duration_split[[1]][1], " ")
    
    if (!is.na(start_duration_split[[1]][2])){
      start_month <- start_duration_split[[1]][1]
      start_year <- start_duration_split[[1]][2]
      
      if(emp_duration_split[[1]][2] == "Present"){
        
        end_duration_split <- "pres"
        end_month <- "pres"
        end_year <- "pres"
      } else {
        end_duration_split <- strsplit(emp_duration_split[[1]][2], " ")
        end_month <- end_duration_split[[1]][1]
        end_year <- end_duration_split[[1]][2]
      }
      
      if(match(start_month, month.abb) < 10){
        start_month_num <- paste(c("0", match(start_month, month.abb)), collapse="") 
      } else {
        start_month_num <- match(start_month, month.abb)
      }
      
      start_date <- paste(c(start_month_num, start_year), collapse="/") 
      
      if(end_month == "pres"){
        end_month_num <- "pres"
      } else if (match(end_month, month.abb) < 10){
        end_month_num <- paste(c("0", match(end_month, month.abb)), collapse="")
      } else {
        end_month_num <- match(end_month, month.abb)
      }
      
      if(end_month_num == "pres"){
        end_date <- end_month_num
      } else {
        end_date <- paste(c(end_month_num, end_year), collapse="/") 
      }
      
      duration <- paste(c(start_date, end_date), collapse="-")
      
    } else {
      
      start_date <- emp_duration_split[[1]][1]
      start_month_num <- "NA"
      start_year <- emp_duration_split[[1]][1]
      end_date <- emp_duration_split[[1]][2]
      end_month_num <- "NA"
      end_year <- emp_duration_split[[1]][2]
      duration <- paste(c(start_date, end_date), collapse="-")
    }
    
    init_df[count, 9] <- duration
    init_df[count, 10] <- start_date
    init_df[count, 11] <- start_month_num
    init_df[count, 12] <- start_year
    init_df[count, 13] <- end_date
    init_df[count, 14] <- end_month_num
    init_df[count, 15] <- end_year
    init_df[count, 16] <- relevant_data[i,10]
    init_df[count, 17] <- i
    init_df[count, 18] <- i
    init_df[count, 19] <- i
    
    count = count + 1
    print(count)
  }
  
  if(!is.na(relevant_data[i, 12])){
    init_df[count, 1] <- i
    init_df[count, 2] <- i
    init_df[count, 3] <- i
    init_df[count, 4] <- relevant_data[i,1]
    init_df[count, 5] <- relevant_data[i,2]
    
    if(relevant_data[i, 5] == "University of Waterloo"){
      edu_duration_split <- strsplit(relevant_data[i, 6], " - ")
      init_df[count, 6] <- edu_duration_split[[1]][2]
    } else {
      edu_duration_split <- strsplit(relevant_data[i, 4], " - ")
      init_df[count, 6] <- edu_duration_split[[1]][2]
    }
    
    init_df[count, 7] <- relevant_data[i,11]
    init_df[count, 8] <- relevant_data[i,12]
    
    emp_duration_split <- strsplit(relevant_data[i, 13], " - ")
    start_duration_split <- strsplit(emp_duration_split[[1]][1], " ")
    
    if (!is.na(start_duration_split[[1]][2])){
      start_month <- start_duration_split[[1]][1]
      start_year <- start_duration_split[[1]][2]
      
      if(emp_duration_split[[1]][2] == "Present"){
        
        end_duration_split <- "pres"
        end_month <- "pres"
        end_year <- "pres"
      } else {
        end_duration_split <- strsplit(emp_duration_split[[1]][2], " ")
        end_month <- end_duration_split[[1]][1]
        end_year <- end_duration_split[[1]][2]
      }
      
      if(match(start_month, month.abb) < 10){
        start_month_num <- paste(c("0", match(start_month, month.abb)), collapse="") 
      } else {
        start_month_num <- match(start_month, month.abb)
      }
      
      start_date <- paste(c(start_month_num, start_year), collapse="/") 
      
      if(end_month == "pres"){
        end_month_num <- "pres"
      } else if (match(end_month, month.abb) < 10){
        end_month_num <- paste(c("0", match(end_month, month.abb)), collapse="")
      } else {
        end_month_num <- match(end_month, month.abb)
      }
      
      if(end_month_num == "pres"){
        end_date <- end_month_num
      } else {
        end_date <- paste(c(end_month_num, end_year), collapse="/") 
      }
      
      duration <- paste(c(start_date, end_date), collapse="-")
      
    } else {
      
      start_date <- emp_duration_split[[1]][1]
      start_month_num <- "NA"
      start_year <- emp_duration_split[[1]][1]
      end_date <- emp_duration_split[[1]][2]
      end_month_num <- "NA"
      end_year <- emp_duration_split[[1]][2]
      duration <- paste(c(start_date, end_date), collapse="-")
    }
    
    init_df[count, 9] <- duration
    init_df[count, 10] <- start_date
    init_df[count, 11] <- start_month_num
    init_df[count, 12] <- start_year
    init_df[count, 13] <- end_date
    init_df[count, 14] <- end_month_num
    init_df[count, 15] <- end_year
    init_df[count, 16] <- relevant_data[i,14]
    init_df[count, 17] <- i
    init_df[count, 18] <- i
    init_df[count, 19] <- i
    
    count = count + 1
    print(count)
  }
  
  if(!is.na(relevant_data[i, 16])){
    init_df[count, 1] <- i
    init_df[count, 2] <- i
    init_df[count, 3] <- i
    init_df[count, 4] <- relevant_data[i,1]
    init_df[count, 5] <- relevant_data[i,2]
    
    if(relevant_data[i, 5] == "University of Waterloo"){
      edu_duration_split <- strsplit(relevant_data[i, 6], " - ")
      init_df[count, 6] <- edu_duration_split[[1]][2]
    } else {
      edu_duration_split <- strsplit(relevant_data[i, 4], " - ")
      init_df[count, 6] <- edu_duration_split[[1]][2]
    }
    
    init_df[count, 7] <- relevant_data[i,15]
    init_df[count, 8] <- relevant_data[i,16]
    
    emp_duration_split <- strsplit(relevant_data[i, 17], " - ")
    start_duration_split <- strsplit(emp_duration_split[[1]][1], " ")
    
    if (!is.na(start_duration_split[[1]][2])){
      start_month <- start_duration_split[[1]][1]
      start_year <- start_duration_split[[1]][2]
      
      if(emp_duration_split[[1]][2] == "Present"){
        
        end_duration_split <- "pres"
        end_month <- "pres"
        end_year <- "pres"
      } else {
        end_duration_split <- strsplit(emp_duration_split[[1]][2], " ")
        end_month <- end_duration_split[[1]][1]
        end_year <- end_duration_split[[1]][2]
      }
      
      if(match(start_month, month.abb) < 10){
        start_month_num <- paste(c("0", match(start_month, month.abb)), collapse="") 
      } else {
        start_month_num <- match(start_month, month.abb)
      }
      
      start_date <- paste(c(start_month_num, start_year), collapse="/") 
      
      if(end_month == "pres"){
        end_month_num <- "pres"
      } else if (match(end_month, month.abb) < 10){
        end_month_num <- paste(c("0", match(end_month, month.abb)), collapse="")
      } else {
        end_month_num <- match(end_month, month.abb)
      }
      
      if(end_month_num == "pres"){
        end_date <- end_month_num
      } else {
        end_date <- paste(c(end_month_num, end_year), collapse="/") 
      }
      
      duration <- paste(c(start_date, end_date), collapse="-")
      
    } else {
      
      start_date <- emp_duration_split[[1]][1]
      start_month_num <- "NA"
      start_year <- emp_duration_split[[1]][1]
      end_date <- emp_duration_split[[1]][2]
      end_month_num <- "NA"
      end_year <- emp_duration_split[[1]][2]
      duration <- paste(c(start_date, end_date), collapse="-")
    }
    
    init_df[count, 9] <- duration
    init_df[count, 10] <- start_date
    init_df[count, 11] <- start_month_num
    init_df[count, 12] <- start_year
    init_df[count, 13] <- end_date
    init_df[count, 14] <- end_month_num
    init_df[count, 15] <- end_year
    init_df[count, 16] <- relevant_data[i,18]
    init_df[count, 17] <- i
    init_df[count, 18] <- i
    init_df[count, 19] <- i
    
    count = count + 1
    print(count)
  }
  
  if(!is.na(relevant_data[i, 20])){
    init_df[count, 1] <- i
    init_df[count, 2] <- i
    init_df[count, 3] <- i
    init_df[count, 4] <- relevant_data[i,1]
    init_df[count, 5] <- relevant_data[i,2]
    
    if(relevant_data[i, 5] == "University of Waterloo"){
      edu_duration_split <- strsplit(relevant_data[i, 6], " - ")
      init_df[count, 6] <- edu_duration_split[[1]][2]
    } else {
      edu_duration_split <- strsplit(relevant_data[i, 4], " - ")
      init_df[count, 6] <- edu_duration_split[[1]][2]
    }
    
    init_df[count, 7] <- relevant_data[i,19]
    init_df[count, 8] <- relevant_data[i,20]
    
    emp_duration_split <- strsplit(relevant_data[i, 21], " - ")
    start_duration_split <- strsplit(emp_duration_split[[1]][1], " ")
    
    if (!is.na(start_duration_split[[1]][2])){
      start_month <- start_duration_split[[1]][1]
      start_year <- start_duration_split[[1]][2]
      
      if(emp_duration_split[[1]][2] == "Present"){
        
        end_duration_split <- "pres"
        end_month <- "pres"
        end_year <- "pres"
      } else {
        end_duration_split <- strsplit(emp_duration_split[[1]][2], " ")
        end_month <- end_duration_split[[1]][1]
        end_year <- end_duration_split[[1]][2]
      }
      
      if(match(start_month, month.abb) < 10){
        start_month_num <- paste(c("0", match(start_month, month.abb)), collapse="") 
      } else {
        start_month_num <- match(start_month, month.abb)
      }
      
      start_date <- paste(c(start_month_num, start_year), collapse="/") 
      
      if(end_month == "pres"){
        end_month_num <- "pres"
      } else if (match(end_month, month.abb) < 10){
        end_month_num <- paste(c("0", match(end_month, month.abb)), collapse="")
      } else {
        end_month_num <- match(end_month, month.abb)
      }
      
      if(end_month_num == "pres"){
        end_date <- end_month_num
      } else {
        end_date <- paste(c(end_month_num, end_year), collapse="/") 
      }
      
      duration <- paste(c(start_date, end_date), collapse="-")
      
    } else {
      
      start_date <- emp_duration_split[[1]][1]
      start_month_num <- "NA"
      start_year <- emp_duration_split[[1]][1]
      end_date <- emp_duration_split[[1]][2]
      end_month_num <- "NA"
      end_year <- emp_duration_split[[1]][2]
      duration <- paste(c(start_date, end_date), collapse="-")
    }
    
    init_df[count, 9] <- duration
    init_df[count, 10] <- start_date
    init_df[count, 11] <- start_month_num
    init_df[count, 12] <- start_year
    init_df[count, 13] <- end_date
    init_df[count, 14] <- end_month_num
    init_df[count, 15] <- end_year
    init_df[count, 16] <- relevant_data[i,22]
    init_df[count, 17] <- i
    init_df[count, 18] <- i
    init_df[count, 19] <- i
    
    count = count + 1
    print(count)
  }
  
  if(!is.na(relevant_data[i, 24])){
    init_df[count, 1] <- i
    init_df[count, 2] <- i
    init_df[count, 3] <- i
    init_df[count, 4] <- relevant_data[i,1]
    init_df[count, 5] <- relevant_data[i,2]
    
    if(relevant_data[i, 5] == "University of Waterloo"){
      edu_duration_split <- strsplit(relevant_data[i, 6], " - ")
      init_df[count, 6] <- edu_duration_split[[1]][2]
    } else {
      edu_duration_split <- strsplit(relevant_data[i, 4], " - ")
      init_df[count, 6] <- edu_duration_split[[1]][2]
    }
    
    init_df[count, 7] <- relevant_data[i,23]
    init_df[count, 8] <- relevant_data[i,24]
    
    emp_duration_split <- strsplit(relevant_data[i, 25], " - ")
    start_duration_split <- strsplit(emp_duration_split[[1]][1], " ")
    
    if (!is.na(start_duration_split[[1]][2])){
      start_month <- start_duration_split[[1]][1]
      start_year <- start_duration_split[[1]][2]
      
      if(emp_duration_split[[1]][2] == "Present"){
        
        end_duration_split <- "pres"
        end_month <- "pres"
        end_year <- "pres"
      } else {
        end_duration_split <- strsplit(emp_duration_split[[1]][2], " ")
        end_month <- end_duration_split[[1]][1]
        end_year <- end_duration_split[[1]][2]
      }
      
      if(match(start_month, month.abb) < 10){
        start_month_num <- paste(c("0", match(start_month, month.abb)), collapse="") 
      } else {
        start_month_num <- match(start_month, month.abb)
      }
      
      start_date <- paste(c(start_month_num, start_year), collapse="/") 
      
      if(end_month == "pres"){
        end_month_num <- "pres"
      } else if (match(end_month, month.abb) < 10){
        end_month_num <- paste(c("0", match(end_month, month.abb)), collapse="")
      } else {
        end_month_num <- match(end_month, month.abb)
      }
      
      if(end_month_num == "pres"){
        end_date <- end_month_num
      } else {
        end_date <- paste(c(end_month_num, end_year), collapse="/") 
      }
      
      duration <- paste(c(start_date, end_date), collapse="-")
      
    } else {
      
      start_date <- emp_duration_split[[1]][1]
      start_month_num <- "NA"
      start_year <- emp_duration_split[[1]][1]
      end_date <- emp_duration_split[[1]][2]
      end_month_num <- "NA"
      end_year <- emp_duration_split[[1]][2]
      duration <- paste(c(start_date, end_date), collapse="-")
    }
    
    init_df[count, 9] <- duration
    init_df[count, 10] <- start_date
    init_df[count, 11] <- start_month_num
    init_df[count, 12] <- start_year
    init_df[count, 13] <- end_date
    init_df[count, 14] <- end_month_num
    init_df[count, 15] <- end_year
    init_df[count, 16] <- relevant_data[i,26]
    init_df[count, 17] <- i
    init_df[count, 18] <- i
    init_df[count, 19] <- i
    
    count = count + 1
    print(count)
  }
}

# replace "&amp;" with "&"
init_df$Company <- gsub('&amp;', '&', init_df$Company)
init_df$Position <- gsub('&amp;', '&', init_df$Position)
View(init_df)

# write init_df to csv
write.csv(init_df, file = "output.csv", row.names = FALSE)
