# House Valuation API

## Installation Instructions

To install and run the API server, do the following.  Run `pipenv shell` and then `pipenv install`
from the `finalproject` directory.  Then run `python manage.py makemigrations` and
`python manage.py migrate` from that same root directory.  Finally, run `python manage.py runserver`.
You can then visit `localhost:8000` in your browser
(Chrome preferred) to see the website.  The website usage instructions are baked into the
highly user-centric design (the website is intuitive to use).  Unfortunately,
since it is assumed developers are going to be the ones using this tool, the website is not
styled (this is also because frontend/design was not a focus of this project).


## Project Overview

In this project, I developed a machine learning model for
predicting house prices given various features about the house (check out my Jupyter notebook,
`analysis.ipynb`, for my data cleaning, analysis, and modeling work -- also available in [collab](https://colab.research.google.com/drive/1VkDsuf7LOxqaS4V5Q9NKlbidnJnyvDT2?usp=sharing)).

Then, I developed a DRF API for predicting a house price with various features of the house
(described on the website on the Test API page).  Through the websites,
developers can sign up to register an account and receive and API key.  Also through
the website, you can test the API with a completely unstyled and developer-friendly
data-input and response GUI (see the Test API page).  Developers can
log in, log out, and delete their account.  There is also a route, `/api`, to which
you can post a JSON object with the following integer fields to get a price prediction:

---
| Name                     | Field                 |
|--------------------------|-----------------------|
| Air Conditioning         | airconditioning       |
| Number of Bathrooms      | bathroomcnt           |
| Number of Bedrooms       | bedroomcnt            |
| Square Feet              | squarefeet            |
| County                   | countyfips            |
| Number of Fireplaces     | fireplacecnt          |
| Number of Full Bathrooms | fullbathcnt           |
| Garage Car Capacity      | garagecarcnt          |
| Garage Square Feet       | garagetotalsqft       |
| Heating Type             | heatingorsystemtypeid |
| Number of Pools          | poolcnt               |
| Land Use Type            | propertylandusetypeid |
| City                     | cityproxy             |
| Zip Code                 | zipcodeproxy          |
| Number of 3/4 Bathrooms  | threequarterbathcnt   |
| Year Built               | yearbuilt             |
| Number of Stories        | numberofstories       |
---

Also, for the categorical features see the website (or datadesc.py)
for the possible values.  There are a few features for which the names
in the dropdown on the website is different from the
integer value which should be passed into the API:

Air Conditioning:

---
| Category Name      | Category Value |
|--------------------|----------------|
| None               | 0              |
| Yes                | 13             |
| Central            | 1              |
| Wall Unit          | 11             |
| Refrigeration      | 9              |
| Window Unit        | 12             |
| Evaporative Cooler | 3              |
---

Land Use Type:

---
| Category Name                              | Category Value |
|--------------------------------------------|----------------|
| Single Family Residential                  | 261            |
| Duplex (2 Units, Any Combination)          | 246            |
| Condominium                                | 266            |
| Residential General                        | 260            |
| Cluster Home                               | 265            |
| Mobile Home                                | 263            |
| Planned Unit Development                   | 269            |
| Quadruplex (4 Units, Any Combination)      | 248            |
| Triplex (3 Units, Any Combination)         | 247            |
| Cooperative                                | 267            |
| Townhouse                                  | 264            |
| Manufactured, Modular, Prefabricated Homes | 275            |
| Store/Office (Mixed Use)                   | 47             |
| Commercial/Office/Residential Mixed Used   | 31             |
---

Heating Type:

---
| Category Name   | Category Value |
|-----------------|----------------|
| Central         | 2              |
| None            | 0              |
| Floor/Wall      | 7              |
| Solar           | 20             |
| Forced air      | 6              |
| Radiant         | 18             |
| Yes             | 24             |
| Hot Water       | 12             |
| Gravity         | 10             |
| Baseboard       | 1              |
| Other           | 14             |
| Space/Suspended | 21             |
| Heat Pump       | 11             |
| Steam           | 19             |
---

