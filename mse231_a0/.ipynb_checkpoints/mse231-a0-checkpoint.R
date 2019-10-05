# Name: Michael Spencer

n_sim <- 1e5
norm_dice <- c(1, 2, 3, 4, 5, 6)
total_rolls <- 0

find_sample_space <- function() {
  
  whole_roll = integer()
  trip = FALSE
  
  while (!trip) {
    
    roll <- sample(norm_dice, 1, replace = TRUE)
    
    if (roll %in% c(1, 3, 5)) {
      
      whole_roll = integer()
      
    } else {
      
      whole_roll = c(whole_roll, roll)
      
    }  
    
    if (roll == 6) trip = TRUE
    
  }
  
  length(whole_roll)
  
}

for (i in 1:n_sim) {
  
  total_rolls <- total_rolls + find_sample_space()
  
}

paste0("Expected number of throws: ", total_rolls / n_sim)