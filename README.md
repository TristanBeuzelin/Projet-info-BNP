# __Nowcast of IPC project__

## __Strucuration of the project__
* __\raw_data_price__ : this folder contains all the price obtained by webscrapping over the webstite of Rungis
* __\price_computed__ : this folder contains all the files made after tha data contained in `\raw_data_price` and transformed by the programs contained in `programms\data_computing` 
* __\programms__ : this folder contains all the programms used in the project : 
  * `\webscrapping` : all the programms used to scrap data
  * `\data_computing` : all the programms used to merge and transform raw data
  * `\simulations` : all the programms used to run various simulations over our data to model the evolution of the IPC
  