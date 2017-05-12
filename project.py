from base_class import *
'''' This section imports data from the excel file to create the necessary DS for items '''

product_description = pd.ExcelFile("article_pricing.xlsx")
pdes =product_description.parse("Sheet1",index_col="article")


pipeline_cost = {}
article_details = {}
total_cost = {}

for i, row in pdes.iterrows():
    pipeline_cost[i] = amazon_price_structure(39.99, 0.3, 0.1, 0.25, pdes.volume[i], pdes.no[i], pdes.weight[i])
    article_details[i] = article_properties(pdes.theme[i],i,0.5,0.5,pdes.cp[i],pdes.no[i])

for i, row in pdes.iterrows():
    total_cost [i] = pipeline_cost[i].calculate_shipping() + article_details[i].calculate_selling_price(0.3)
    article_details[i].mrp = total_cost[i]

''' Data import complete - total selling prices are calculated in total_cost dictionary, amazon cost is calculated 
in pipeline_cost dictionary, article details are calculated and setup in article_details dictionary 

For any item, i, the instance can be accessed using key value pair approach '''

active_visitors = 500


customer = {}
for i in range(0,active_visitors,1):
    customer[i] = buyer()

    if article_properties.no_articles == 0:
        break

    for key in article_details.iterkeys():
        if (article_details[key].appeal > customer[i].interest) and (customer[i].buying_power > article_details[key].sp) \
                and (article_details[key].inventory >0):
            article_details[key].if_sold()

            if article_details[key].inventory == 0:
                article_properties.no_articles -= 1

            customer[i].if_bought(article_details[key].sp,article_details[key].name)
            if customer[i].buying_power < 5:
                break

company = operation(1)
print article_properties.total_profit
print article_properties.total_cost_price_to_us
print company.calculate_revenue()
