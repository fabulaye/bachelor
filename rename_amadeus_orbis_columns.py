amadeus_string="""accpra	Char	10	Accounting practice
ace	Float	53	Aver. cost of empl./year
av	Float	53	Added value
capi	Float	53	Shareholder funds: capital
cash	Float	53	Cash & cash equivalent
cf	Float	53	Cash flow
cfop	Float	53	Cash flow/Turnover (%)
closdate	Date		Account date
closdate_year	Float	53	Year part of CLOSDATE
coll	Float	53	Collection period (days)
compcat	Char	12	Company category
cost	Float	53	Costs of goods sold
country	Char	22	Country
cred	Float	53	Current Liabilities: creditors
crpe	Float	53	Credit period (days)
cuas	Float	53	Current assets
culi	Float	53	Current liabilities
curr	Float	53	Current ratio (x)
currency	Char	3	Account currency
debt	Float	53	Current assets: debtors
depr	Float	53	Depreciation
ebit	Float	53	EBIT
ebma	Float	53	EBIT Margin (%)
ebta	Float	53	EBITDA
empl	Float	53	Number of employees
enva	Float	53	Enterprise value
etma	Float	53	EBITDA Margin (%)
exchrate	Float	53	Exchange rate from local currency to USD
exchrate2	Float	53	Exchange rate from local currency to EUR
exex	Float	53	Extr. and other expenses
exop	Float	53	Export turnover/Total turnover (%)
expt	Float	53	Export turnover
exre	Float	53	Extr. and other revenue
extr	Float	53	Extr. and other P/L
fias	Float	53	Fixed assets
fiex	Float	53	Financial expenses
fipl	Float	53	Financial P/L
fire	Float	53	Financial revenue
gear	Float	53	Gearing (%)
grma	Float	53	Gross Margin (%)
gros	Float	53	Gross profit
ic	Float	53	Interest cover (x)
idnr	Char	15	BvDEP ID number
ifas	Float	53	Intangible fixed assets
inte	Float	53	Interest paid
liqr	Float	53	Liquidity ratio (x)
loan	Float	53	Current Liabilities: loans
ltdb	Float	53	Non current liabilities: long term debt
mate	Float	53	Material costs
months	Float	53	Number of months
nat	Float	53	Net assets turnover (x)
ncas	Float	53	Net current assets
ncli	Float	53	Non current liabilities
ocas	Float	53	Other current assets
ocli	Float	53	Other current liabilities
ofas	Float	53	Other fixed assets
oncl	Float	53	Other non-current liabilities
oope	Float	53	Other operating expenses
oppl	Float	53	Operating P/L [=EBIT]
opre	Float	53	Operating revenue (Turnover)
osfd	Float	53	Other shareholders funds
pl	Float	53	P/L for period [=Net income]
plat	Float	53	P/L after tax
plbt	Float	53	P/L before tax
ppe	Float	53	Profit per employee
prma	Float	53	Profit margin (%)
prov	Float	53	Provisions
rcem	Float	53	Return on capital employed (%)
rd	Float	53	Research & Development Expenses
repbas	Char	24	Reporting basis
rshf	Float	53	Return on shareholders funds (%)
rtas	Float	53	Return on total assets (%)
sct	Float	53	Costs of employees/oper. rev.(%)
sfpe	Float	53	Share funds per employee
shfd	Float	53	Shareholders funds
shlq	Float	53	Shareholders liquidity ratio (x)
solr	Float	53	Solvency ratio (%)
staf	Float	53	Costs of employees
stok	Float	53	Current assets: stocks
stot	Float	53	Stock turnover (x)
tape	Float	53	Total assets per employee
taxa	Float	53	Taxation
tfas	Float	53	Tangible fixed assets
toas	Float	53	Total assets
tpe	Float	53	Operat. rev. per employee
tshf	Float	53	Total shareh. funds & liab.
turn	Float	53	Sales
unit	Float	53	Account unit
wcpe	Float	53	Work. capital per employee
wkca	Float	53	Working capital"""

amadeus_split=amadeus_string.split("\n")
def get_variables(split):
    dict={}
    for row in split:
        items=row.split("\t")
        dict[items[0]]=items[3]
    return dict

import pandas as pd
from exploration.desciptive_statistics import data
ama_map=get_variables(amadeus_split)

imputed_csv=pd.read_csv("C:/Users/lukas/Desktop/bachelor/data/imputed_test.csv")


imputed_csv.rename(columns=ama_map,inplace=True)

imputed_data=data(imputed_csv)
imputed_data.statistics.corr_heatmap()