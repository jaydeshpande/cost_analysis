# The project creates a basic skeleton for determining cost price and sales volume
# Use the variables listed in the class to change the values and determine the impact

from numpy import random as rd
import pandas as pd
import time as t

class amazon_price_structure: # This class is used to calculate the cost of delivery/fulfilment
    total_no_items = 0
    """
    Default values for price structure:
    per_cu_ft = 0.25 ## Price of storage per cubic ft assumed standard over the year
    amazon_per_mo = 39.99 ## subscription fee - allows us to be prime
    standard_shipping = 0.3 ## standard shipping fee per article
    variable_shipping = 0.1 ## variable shipping fee based on weight per article
    storage_vol = 1 ## cubic ft volume -- vary this to study the effect
    no_items = 50 ## no of articles to be solde -- vary this to study the effect
    weight_items = 0.2 ## weight of the articles -- vary this to study the effect
    """
    def __init__(self,amazon_per_mo, standard_shipping, variable_shipping,
                 per_cu_ft,storage_vol,no_items,weight_items):
        self.per_cu_ft = per_cu_ft
        self.amazon_per_mo = amazon_per_mo
        self.standard_shipping = standard_shipping
        self.variable_shipping = variable_shipping
        self.storage_vol = storage_vol
        self.no_items = no_items
        self.weight_items = weight_items
        amazon_price_structure.total_no_items += no_items

    def calculate_storage(self):
        storage_cost = self.per_cu_ft*self.storage_vol # this calculation assumes monthly cost -- likely to vary
        return storage_cost

    def calculate_shipping(self):
        return self.standard_shipping

    def calculate_variable_shipping(self):
        return self.variable_shipping*self.weight_items

    def calculate_monthly_amazon_per_item(self):
        return self.amazon_per_mo/amazon_price_structure.total_no_items # assumes monthly charges

    def total_amazon_per_item(self):
        return self.calculate_monthly_amazon_per_item() + self.calculate_shipping() + self.calculate_storage() + self.calculate_variable_shipping()

class article_properties:
    no_articles = 0
    fusion_articles = 0
    standard_articles = 0

    def __init__(self,theme,name,weight,volume,cp):
        article_properties.no_articles+=1 # increment counter representing articles
        self.fusion = theme
        self.name = name
        self.weight = weight
        self.volume = volume
        self.cp = cp
        self.sp = 0
        self.probability = rd.random()
        self.appeal = rd.random() # Appeal of a product -- if exceeds buyer interest then buyer buys the product

    def if_fusion_product(self):
        if self.fusion == 'fusion':
            article_properties.fusion_articles += 1
        elif self.fusion == 'standard':
            article_properties.standard_articles += 1
        else:
            print "Invalid Article Theme - correct themes standard, fusion"

    def calculate_selling_price(self,profit_in_percent):
        self.sp = self.cp*(1+profit_in_percent)
        return self.sp

    ''' 
    def cost_of_marketing(self,marketing_budget):
        expenditure = marketing_budget * (1-self.probability)
    '''

    def if_sold(self):
        article_properties.no_articles -= 1


    @classmethod
    def how_many_fusion(cls):
        return cls.fusion_articles
    @classmethod
    def how_many_standard(cls):
        return cls.standard_articles

class buyer:
    no_buyers = 0

    def __init__(self):
        buyer.no_buyers+=1 # increment counter representing articles
        self.interest = rd.random() # buyer interest needs to be topped by product appeal  45/
        self.buying_power = rd.randint(0,45) # this models a random buying power
        self.bought_articles = 0
        self.basket = []

    def if_bought(self,article_price,article):
        self.buying_power -= article_price
        self.bought_articles += 1
        self.interest = rd.random() # after the buyer has bought something, it will recalculate the interest
        # recalculating interest is an interesting idea - sort of tells about mass shopping
        # try making the interest unchanged to see the effect
        self.basket.append(article)
        print "Customer Bought {}".format(article)
''' This section imports data from the excel file to create the necessary DS for items '''

product_description = pd.ExcelFile("article_pricing.xlsx")
pdes =product_description.parse("Sheet1",index_col="article")


pipeline_cost = {}
article_details = {}
total_cost = {}

for i, row in pdes.iterrows():
    pipeline_cost[i] = amazon_price_structure(39.99, 0.3, 0.1, 0.25, pdes.volume[i], pdes.no[i], pdes.weight[i])
    article_details[i] = article_properties(pdes.theme[i],i,0.5,0.5,pdes.cp[i])

for i, row in pdes.iterrows():
    total_cost [i] = pipeline_cost[i].total_amazon_per_item() + article_details[i].calculate_selling_price(0.02)

''' Data import complete - total selling prices are calculated in total_cost dictionary, amazon cost is calculated 
in pipeline_cost dictionary, article details are calculated and setup in article_details dictionary 

For any item, i, the instance can be accessed using key value pair approach '''

active_visitors = 100

customer = {}
for i in range(0,active_visitors,1):
    customer[i] = buyer()

    for key in article_details.iterkeys():
        print article_details[key].appeal, customer[i].interest
        t.sleep(0.2)
        if (article_details[key].appeal > customer[i].interest) and (customer[i].buying_power > article_details[key].sp) \
                and (article_details[key].no_articles >0):
            article_details[key].if_sold()
            print article_details[key].no_articles
            print customer[i].buying_power

            customer[i].if_bought(article_details[key].sp,article_details[key].name)
            if customer[i].buying_power < 5:
                print customer[i].buying_power
                break
    print customer[i].basket


print "\n Everything sold out"
