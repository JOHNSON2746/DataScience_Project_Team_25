df <- read.csv('/Users/zigeliang/Desktop/All/Data Science 2025S1/DS Project 1/datasets & Rmodel/testing_syn_salary(age x industry).csv')
summary(df)

# find the categorical vars 
# we also need to treat YEAR as the categorical var \
# becasue we want to compare the income between different time period
df$Sex <- as.factor(df$Sex)
df$Industry <- as.factor(df$Industry)
df$Year<- as.factor(df$Year)

# treat INCOME as a numerical value 
df$Median.Income.per.year <- as.numeric(gsub(",", "", df$Median.Income.per.year))
 
#1: run simple linear reg
basic.reg <- lm(Median.Income.per.year ~ Industry + Sex + Year, data = df)
summary(basic.reg)

#2: run linear reg sex * industry
reg.sex.x.industry <- lm(Median.Income.per.year ~ Industry * Sex + Year, data = df)
summary(reg.sex.x.industry)

#3 run two-way avowa (Sex * industry + Year)
two.anova.model.1 <- aov(Median.Income.per.year ~ Sex * Industry + Year, data = df)
summary(two.anova.model.1)

#4 run two-way avowa (Sex * industry)
two.anova.model.2<- aov(Median.Income.per.year ~ Sex * Industry + Year, data = df)
summary(two.anova.model.2)





