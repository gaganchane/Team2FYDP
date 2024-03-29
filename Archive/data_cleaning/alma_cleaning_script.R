# install.packages("dplyr")
# install.packages("maps")
# install.packages("tm")
# http://www.geodatasource.com/world-cities-database/free
# http://www.downloadexcelfiles.com/wo_en/download-list-cities-canada#.Wn_HyJM-eYU

library(dplyr)
library(maps)
library(tm)

setwd("C://Users//Joash//Desktop//University Stuff//4B uni stuff//Team2FYDP//data_cleaning")

#clean <- read.csv("chem-2012-1.csv")
#View(clean)

# read almabase output
alma_data <- read.csv("update_mgmt_7.csv", header=T, na.strings=c("", " ", "NA"), stringsAsFactors=FALSE)
#View(alma_data)

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

# initialize data frame to which final output will be added
names <- c("ID", "WORK_ID", "COOP_ID", "Name", "URL", "Year", "Company", "Position", "Duration", "Start.Date", 
           "Start.Month", "Start.Year", "End.Date.pres", "End.Month", "End.Year", "Full.Location", "City", "Country")
init_df <- data.frame(matrix(ncol = 18, nrow = 0), stringsAsFactors=FALSE)
colnames(init_df) <- names
count <- 1

date.format <- function(duration){
  emp_duration_split <- strsplit(duration, " - ")
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
      if(!is.na(end_duration_split[[1]][2])){
        end_month <- end_duration_split[[1]][1]
        end_year <- end_duration_split[[1]][2]
      } else {
        end_month <- NA
        end_year <- end_duration_split[[1]][1]
      }
    }

    if(match(start_month, month.abb) < 10){
      start_month_num <- paste(c("0", match(start_month, month.abb)), collapse="") 
    } else {
      start_month_num <- match(start_month, month.abb)
    }
    
    start_date <- paste(c(start_month_num, start_year), collapse="/") 
    
    if(!is.na(end_month)){
      if(end_month == "pres"){
        end_month_num <- "pres"
      } else if (match(end_month, month.abb) < 10){
        end_month_num <- paste(c("0", match(end_month, month.abb)), collapse="")
      } else {
        end_month_num <- match(end_month, month.abb)
      } 
    } else {
      end_month_num <- "Unavailable"
    }

    if(end_month_num == "pres"){
      end_date <- end_month_num
    } else if (end_month_num != "Unavailable"){
      end_date <- paste(c(end_month_num, end_year), collapse="/") 
    } else {
      end_date <- end_year
    }
    
    final_duration <- paste(c(start_date, end_date), collapse="-")
    
  } else {
    
    start_date <- emp_duration_split[[1]][1]
    start_month_num <- "Unavailable"
    start_year <- emp_duration_split[[1]][1]
    end_date <- emp_duration_split[[1]][2]
    end_month_num <- "Unavailable"
    end_year <- emp_duration_split[[1]][2]
    final_duration <- paste(c(start_date, end_date), collapse="-")
  }
  
  return.vector <- c(start_date, start_month_num, start_year, end_date, end_month_num, end_year, final_duration)
  return(return.vector)
}

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
    
    date.vector <- date.format(relevant_data[i, 9])
    
    init_df[count, 9] <- date.vector[7]
    init_df[count, 10] <- date.vector[1]
    init_df[count, 11] <- date.vector[2]
    init_df[count, 12] <- date.vector[3]
    init_df[count, 13] <- date.vector[4]
    init_df[count, 14] <- date.vector[5]
    init_df[count, 15] <- date.vector[6]
    init_df[count, 16] <- relevant_data[i,10]
    init_df[count, 17] <- NA
    init_df[count, 18] <- NA
    
    count = count + 1
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
    
    date.vector <- date.format(relevant_data[i, 13])
    
    init_df[count, 9] <- date.vector[7]
    init_df[count, 10] <- date.vector[1]
    init_df[count, 11] <- date.vector[2]
    init_df[count, 12] <- date.vector[3]
    init_df[count, 13] <- date.vector[4]
    init_df[count, 14] <- date.vector[5]
    init_df[count, 15] <- date.vector[6]
    init_df[count, 16] <- relevant_data[i,14]
    init_df[count, 17] <- NA
    init_df[count, 18] <- NA
    
    count = count + 1
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
    
    date.vector <- date.format(relevant_data[i, 17])
    
    init_df[count, 9] <- date.vector[7]
    init_df[count, 10] <- date.vector[1]
    init_df[count, 11] <- date.vector[2]
    init_df[count, 12] <- date.vector[3]
    init_df[count, 13] <- date.vector[4]
    init_df[count, 14] <- date.vector[5]
    init_df[count, 15] <- date.vector[6]
    init_df[count, 16] <- relevant_data[i,18]
    init_df[count, 17] <- NA
    init_df[count, 18] <- NA
    
    count = count + 1
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
    
    date.vector <- date.format(relevant_data[i, 21])
    
    init_df[count, 9] <- date.vector[7]
    init_df[count, 10] <- date.vector[1]
    init_df[count, 11] <- date.vector[2]
    init_df[count, 12] <- date.vector[3]
    init_df[count, 13] <- date.vector[4]
    init_df[count, 14] <- date.vector[5]
    init_df[count, 15] <- date.vector[6]
    init_df[count, 16] <- relevant_data[i,22]
    init_df[count, 17] <- NA
    init_df[count, 18] <- NA
    
    count = count + 1
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
    
    date.vector <- date.format(relevant_data[i, 25])
    
    init_df[count, 9] <- date.vector[7]
    init_df[count, 10] <- date.vector[1]
    init_df[count, 11] <- date.vector[2]
    init_df[count, 12] <- date.vector[3]
    init_df[count, 13] <- date.vector[4]
    init_df[count, 14] <- date.vector[5]
    init_df[count, 15] <- date.vector[6]
    init_df[count, 16] <- relevant_data[i,26]
    init_df[count, 17] <- NA
    init_df[count, 18] <- NA
    
    count = count + 1
  }
}

# replace "&amp;" with "&"
init_df$Company <- gsub('&amp;', '&', init_df$Company)
init_df$Position <- gsub('&amp;', '&', init_df$Position)

# Sort dataframe by ID, Start.Year, Start.Month
#init_df$Start.Month <- as.numeric(as.character(init_df$Start.Month))
#init_df$Start.Year <- as.numeric(as.character(init_df$Start.Year))
init_df <- arrange(init_df, ID, Start.Year, Start.Month)

# Add COOP.ID and WORK.ID
# Alumni that have ongoing "second job" from prior to graduation will count as WORD_ID/full time job
coopcount = 1
workcount = 1

if(!is.na(init_df[i, 'Year'])){
  if(init_df[1, 'Start.Year'] < init_df[1, 'Year'] & (init_df[1, 'End.Date.pres'] != "pres")){
    init_df[1, 'COOP_ID'] <- coopcount
    init_df[1, 'WORK_ID'] <- NA
    coopcount = coopcount + 1
  } else {
    init_df[1, 'WORK_ID'] <- workcount
    init_df[1, 'COOP_ID'] <- NA
    workcount = workcount + 1
  }
} else {
  init_df[1, 'WORK_ID'] <- workcount
  init_df[1, 'COOP_ID'] <- NA
  workcount = workcount + 1
}

for (i in 2:nrow(init_df)){
  
  if(init_df[i, 'ID'] != init_df[i-1, 'ID']){
    coopcount = 1
    workcount = 1
  }
  
  if(!is.na(init_df[i, 'Year'])){
    if((init_df[i, 'Start.Year'] < init_df[i, 'Year']) & (init_df[i, 'End.Date.pres'] != "pres")){
      init_df[i, 'COOP_ID'] <- coopcount
      init_df[i, 'WORK_ID'] <- NA
      coopcount = coopcount + 1
    } else {
      init_df[i, 'WORK_ID'] <- workcount
      init_df[i, 'COOP_ID'] <- NA
      workcount = workcount + 1
    }
  } else {
    init_df[i, 'WORK_ID'] <- workcount
    init_df[i, 'COOP_ID'] <- NA
    workcount = workcount + 1
  }
}

# determine location (city and country) and add to init_df

# obtain database for all cities and countries
cities <- data.frame(world.cities, stringsAsFactors = FALSE)
setwd("C://Users//Joash//Desktop//University Stuff//4B uni stuff//Team2FYDP//data_cleaning")
canada.cities.data <- read.csv("canadacities.csv", header = TRUE, stringsAsFactors = FALSE)
usa.cities <- subset(cities[,1:2], country.etc == "USA")
canada.cities <- canada.cities.data
#canada.cities$Name <- gsub("[^A-Za-z0-9 ]", "", canada.cities$Name)
other.cities <- subset(cities[,1:2], country.etc != "USA" & country.etc != "Canada")

# remove words like "Area", "Greater" from cities and countries 
stopwords <- c("Area", "Greater")
init_df$Full.Location <- removeWords(init_df$Full.Location, stopwords)
init_df$City <- as.numeric(init_df$City)
init_df$Country <- as.numeric(init_df$Country)

for (i in 1:nrow(init_df)){
  if(is.na(init_df[i, "Full.Location"])){
    init_df[i, "City"] <- NA
    init_df[i, "Country"] <- NA
    next
  }
  
  location.split <- unlist(strsplit(init_df[i, "Full.Location"], split=" "))

  if(tail(location.split, n=1) == "Canada"){
    init_df[i,"Country"] <- "Canada"
    
    if(length(location.split) == 1){
      next
    }
    
    location.split <- head(location.split, -1)
    location.split.concat <- do.call(c, lapply(seq_along(location.split), function(i) combn(location.split, i, FUN = list)))
    
    for(j in 1:length(location.split.concat)){
      location.split.concat[[j]] <- paste(location.split.concat[[j]], collapse = ' ')
    }
    unlist(location.split.concat)
    
    for(k in 1:length(location.split.concat)){
      for(l in 1:nrow(canada.cities)){
        if(tolower(location.split.concat[k]) == tolower(canada.cities[l,1])){
          init_df[i, "City"] <- location.split.concat[k]
        }
      }
    }
    next
  }

  location.split.concat <- do.call(c, lapply(seq_along(location.split), function(i) combn(location.split, i, FUN = list)))
  
  for(j in 1:length(location.split.concat)){
    location.split.concat[[j]] <- paste(location.split.concat[[j]], collapse = ' ')
  }
  
  for(m in 1:length(location.split.concat)){
    for(l in 1:nrow(canada.cities)){
      if(tolower(location.split.concat[m]) == tolower(canada.cities[l,1])){
        init_df[i, "City"] <- location.split.concat[m]
        init_df[i, "Country"] <- "Canada"
        break
      } 
    }
  }
  if((!(is.na(init_df[i, "City"]))) | (!(is.na(init_df[i, "Country"])))){
    next
  }
  
  for(m in 1:length(location.split.concat)){
    for(l in 1:nrow(usa.cities)){
      if(tolower(location.split.concat[m]) == tolower(usa.cities[l,1])){
        init_df[i, "City"] <- location.split.concat[m]
        init_df[i, "Country"] <- "United States"
        break
      }
    }
  }
  if((!(is.na(init_df[i, "City"]))) | (!(is.na(init_df[i, "Country"])))){
    next
  }
  
  if(length(location.split) > 5){
    location.split <- location.split[1:5]
    location.split.concat <- do.call(c, lapply(seq_along(location.split), function(i) combn(location.split, i, FUN = list)))
  }
    
  for(m in 1:length(location.split.concat)){
    for(l in 1:nrow(other.cities)){
      if(tolower(location.split.concat[m]) == tolower(other.cities[l,1])){
        init_df[i, "City"] <- location.split.concat[m]
        init_df[i, "Country"] <- other.cities[l,2]
        break
      }
    }
  }
}
View(init_df)

# write init_df to csv
setwd("C://Users//Joash//Desktop//University Stuff//4B uni stuff//Team2FYDP//data_Cleaning//outputs")
write.csv(init_df, file = "update_mgmt_7_output.csv", row.names = FALSE)