Title: Hint: Excel Might be all You Need for Your Next Linear Regression Model!
Date: 2022-03-22
Modified: 2022-03-22
Status: draft
Tags: datascience, machine learning
Slug: regression
Authors: Brian Roepke
Summary: Simple Linear Regression Three Ways: R, Python, and Excel
Header_Cover: images/covers/divide.jpg
Og_Image: images/covers/divide.jpg
Twitter_Image: images/covers/divide.jpg

## Introduction

Linear regression is the most common type of regression analysis and is an incredibly powerful tool when two or more variables are involved.  While there are many different regression algorithms out there, in your day-to-day life, on smaller projects, or in business oriented use cases, you might just find that you can apply this model to data to help you bring predictions to life.  

While you can use all of the fancy ways you've learned recently with R and Python to perform a linear regression, I wanted to bring Excel back to your attention and show just how powerful it can be to build a prediction model in a matter of minutes! 

## Regression in R

Let's start off with **R**.  R is a statistical compution platform that extremely popular in the Data Science and Analytics communities.  R is open source and the ecosystem of libraries is extensive! 

We'll quicly build a model by passing our `X` and `y` data into the `lm` function. One of the things that I personally love about the **R** implementaion is the `summary` function.  It outputs a table that contains most of what you need to interpret the results.

```r
library(ggplot2)

X <- c(182301, 232824, 265517, 307827, 450753, 484245,
535776, 594604, 629684, 659109, 694050, 874305)
y <- c(4761393, 5104714, 5023121, 5834911, 5599829,
6712668, 7083847, 7296756, 7602863, 7643765, 7739618, 9147263)

data <- data.frame(X, y)

# Output a text based summary of the regression model
model <- lm(y ~ X, data = data)
summary(model)

# Plot the results
ylab <- c(2.5, 5.0, 7.5, 10)
ggplot(data = data, mapping = aes(x = X, y = y)) +
    geom_point() +
    geom_smooth(method = "lm", se = TRUE, formula = y~x) +
    theme_minimal() +
    expand_limits(x = c(0,NA), y = c(0,NA)) +
    scale_y_continuous(labels = paste0(ylab, "M"), 
        breaks = 10^6 * ylab) +
    scale_x_continuous(labels = scales::comma)
```

```text
Call:
lm(formula = y ~ X, data = data)

Residuals:
    Min      1Q  Median      3Q     Max 
-767781  -57647   86443  131854  361211 

Coefficients:
             Estimate Std. Error t value Pr(>|t|)    
(Intercept) 3.548e+06  2.240e+05   15.84 2.07e-08 ***
X           6.254e+00  4.203e-01   14.88 3.77e-08 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 296100 on 10 degrees of freedom
Multiple R-squared:  0.9568,	Adjusted R-squared:  0.9525 
F-statistic: 221.4 on 1 and 10 DF,  p-value: 3.775e-08
```

In the summary output is a way to quickly identify the coeeficients that are statistically significant with the notation: 

`Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1`

Additionally, `ggplot2` is a powerful visualization library that allows us to easily render the scatterplot along with the regression line for quick inspection.

![GG Plot Output]({static}../../images/posts/regression_04.png)

## Regression in Python

If you're interested in producing similar results in Python, the best way is to use the `OLS` (*Ordinary Least Squares*) model from `statsmodels`.  It has the closest output to the base R `lm` package producing a similar summary table.  We'll start by importing the packages we need to run the model.

```python
import matplotlib.pyplot as plt
import statsmodels.api as sm
```

Next, let's prepare our data.  We'll start with two Python lists for our `X` and `y` data.  Additionally we need to add additional constant data to the `X` data to account for the intercept.

```python
X = [182301, 232824, 265517, 307827, 450753, 484245, 
     535776, 594604, 629684, 659109, 694050, 874305]
y = [4761393, 5104714, 5023121, 5834911, 5599829, 6712668, 
     7083847, 7296756, 7602863, 7643765, 7739618, 9147263]

# Add an intercept
X_i = sm.add_constant(X)
X_i
```
```text
array([[1.00000e+00, 1.82301e+05],
       [1.00000e+00, 2.32824e+05],
       [1.00000e+00, 2.65517e+05],
       [1.00000e+00, 3.07827e+05],
       [1.00000e+00, 4.50753e+05],
       [1.00000e+00, 4.84245e+05],
       [1.00000e+00, 5.35776e+05],
       [1.00000e+00, 5.94604e+05],
       [1.00000e+00, 6.29684e+05],
       [1.00000e+00, 6.59109e+05],
       [1.00000e+00, 6.94050e+05],
       [1.00000e+00, 8.74305e+05]])
```

And next, we can **fit** the model to our data, and print a **summary** similar to **R**

```python
mod = sm.OLS(y, X_i)
results = mod.fit()
print(results.summary())
```

![Python Regression]({static}../../images/posts/regression_05.png)



## Regression in Excel!

Finally! Let's use the **Excel** application to perform the same regression analysis.  One of the things about Excel is that it has AMAZING depth when it comes to numarical analysis that many users have never discovered.  Let's take a look at how we can perform the exact same analysis using Excel, but accomplish it in just a few minutes! 

Start by navigating to the **Data Analysis** pack which is located in the **Data** tab. 

![Data Analysis Tools]({static}../../images/posts/regression_01.png)

From here we can select the **Regression** tool.

![Regression]({static}../../images/posts/regression_02.png)

And as with most things in Excel, we simply populat the dialog with the right rows and columns and set a few additional otptions.  Shown here are some of the most common settings that you should choose to give you a robust output.

![Regression Settings]({static}../../images/posts/regression_03.png)

And finally, we can see the output from our analysis.  Excel creates a new sheet with the results. It contains evaluation statistics such as the R-Squared and Adjusted R-Squared.  It also produces and [ANOVA](https://en.wikipedia.org/wiki/Analysis_of_variance) table producing values such as the **Sum of Squares** (SS), **Mean Square** (MS), and **F-Statistic**.  The **F-Statistic** can tell us if the model is statistically significant typically when the value is less than `0.05`. 

![Excel Regression]({static}../../images/posts/regression_06.png)

Next we might want to **predict new values**.  There are a couple of ways to do this. The first is you can directly reference the cell that was outputted from the regression analysis tool in Excel.  The second is computing the **slope** and **intercept** yourself and using this in our regression formula.  I tend to do it this way and wanted to show how you accomplish it.  There are two formulas that you will use, appropriatly named `=SLOPE` and `=INTERCEPT`.  Simply select the approprate `X` and `y` cells in the formual as shown below.

![Slope and Intercept]({static}../../images/posts/regression_07.png)

One you have your slop and intercept, you can plug them into the linear regression equasion.

$$Y_{i}=\beta_{0}+\beta_{1} X_{i}$$

Because this is a simple linear regregression we can think of this as the equasion of a line or `Y = MX + B` where `M` is the **Slope** and `B` is the **Y-Intercept**.  Something we learned back in high school math, now paying dividends in data science! 

![Predicting New Values]({static}../../images/posts/regression_08.png)

## Conclusion


*If you liked what you read, [subscribe to my newsletter](https://campaign.dataknowsall.com/subscribe) and you will get my cheat sheet on Python, Machine Learning (ML), Natural Language Processing (NLP), SQL, and more. You will receive an email each time a new article is posted.*

## References

Photo by <a href="https://unsplash.com/@willfrancis?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Will Francis</a> on <a href="https://unsplash.com/s/photos/divide?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>
  

