# DolWebscraper
@author: William David
@author email: WilliamDavid825@gmail.com

The author created this web crawler with the intended purpose to be used to grab minimum wages from from the department of labor website and put it in a csv file

Their are 2 files needed:
	special_cases.csv
	zip_code_data.csv
{
	Special_cases.csv should be in the order for the colums City, State, Minimum Wage, and where the Minimum wage came from for the special cases by city. 
	The County, State, Minimum Wage, and where the Minimum wage came from, for the special cases by county. this should be kept under the city section
	there should be an empty row between the county and city sections

	Zip_code_data.csv should be in the order of zipcode, primary_city of the zip code, State(the postal code), and then the county of the zipcode

	Both of these files are already in this folder and should be used as an example of what they should look like if these files need to be updated in the future
}

The output file is the zip_code_wages.csv
The output will come in the form zipcode, city of the zipcode, state of the zipcode, county of the zipcode, jurisdiction of the zipcode(wether the minimum wage was grabed from the city level, county level or state level), and finally the minimum wage of the zipcode

This promgram was created with python 3 using the imports: requests and BeautifulSoup

This is a warning do not change the formating of the 2 files needed, the output file will not be as expected if you do. 
As well, this program will only grap the minimum wages from the dol web site if the formating of the website does not have any dramatic changes - https://www.dol.gov/agencies/whd/minimum-wage/stat

the needed files are only read and the output file is the only one thats writen into

to start click dolfinder.exe file which will ether create the output file or overwrite it if it already exists in the same folder
