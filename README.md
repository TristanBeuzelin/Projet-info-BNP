# __Nowcast of CPI project__

## __Introduction to the project__

The __CPI__ (Consumer Price Index) is a tool used to measure the __inflation__ of products. It is used to predict the variations of prices of product consummed by households between two given periods. It is based on a fixed basket of goods an services. Each product counts in proportion to its weight in household expenditure. 

Furthermore, __Nowcasting__ in economics is the prediction of the present, the very near future, and the very recent past state of an economic indicator. Indeed, some indicators are not always available at every moment so economists have to forecast the present and sometimes the near past to ajdust their decisions. 

In our case, the CPI is released by INSEE around the thirteenth of each month so as things tend to move really fast in economics, it is very hard for economist to work with one month old figures. Predicting the CPI one or two weeks before it is released could help our client (__BNP__) adjusting its strategy and save a lot of money.

## __Description of the project__

The objective of our project does not really lie in the creation of the best predictor of the CPI using Nowcasting method but __it is to demonstrate whether it is possible to do it or not__ in order for the BNP to know whether it should invest into that field or not.

## __Strucuration of the project__
* __`\raw_data_price`__ : this folder contains all the price obtained by webscrapping over the webstite of Rungis
* __`\price_computed`__ : this folder contains all the files made after tha data contained in `\raw_data_price` and transformed by the programs contained in `programms\data_computing` 
* __`\programms`__ : this folder contains all the programms used in the project : 
  * `\webscrapping` : all the programms used to scrap data
  * `\data_computing` : all the programms used to merge and transform raw data
  * `\simulations` : all the programms used to run various simulations over our data to model the evolution of the CPI
  