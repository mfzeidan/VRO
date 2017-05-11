


library(lpSolveAPI)
library(lpSolve)


#### 0 is number that fills matrix, 2 is number of rows, 3 is number of columns


rotation <- data.frame(players=c('Player1','Player2','Player3','Player4','Player5','Player6'),
                       p1=0,p2=0,p3=0,p4=0,p5=0,p6=0)
                        

skill_level <- data.frame(players=c('Player1','Player2','Player3','Player4','Player5','Player6'),
                          FrontRow = 0,
                          BackRow = 0)

#player 1 front row
skill_level[1,2] <- 2
skill_level[1,3] <- 3
#skill_level

#player 2 front row
skill_level[2,2] <- 4
skill_level[2,3] <- 5
#skill_level

#player 3 front row
skill_level[3,2] <- 1
skill_level[3,3] <- 5
#skill_level

#player 4 front row
skill_level[4,2] <- 2
skill_level[4,3] <- 3
#skill_level

#player 5 front row
skill_level[5,2] <- 4
skill_level[5,3] <- 2


#player 6 front row
skill_level[6,2] <- 3
skill_level[6,3] <- 3

skill_level


