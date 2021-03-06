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


    def calculate_shipping(self):
         total_shipping =  self.standard_shipping + \
         self.variable_shipping*self.weight_items + \
         self.amazon_per_mo / amazon_price_structure.total_no_items + \
         self.per_cu_ft * self.storage_vol
         return total_shipping

class article_properties:
    no_articles = 0
    fusion_articles = 0
    standard_articles = 0
    total_cost_price_to_us = 0
    total_profit = 0

    def __init__(self,theme,name,weight,volume,cp,inv):
        article_properties.no_articles+=1 # increment counter representing articles
        self.fusion = theme
        self.name = name
        self.weight = weight
        self.volume = volume
        self.cp = cp
        article_properties.total_cost_price_to_us += cp*inv
        self.sp = 0
        self.profit = 0
        self.inventory = inv
        self.appeal = rd.random() # Appeal of a product -- if exceeds buyer interest then buyer buys the product
        self.mrp = 0

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

    def if_sold(self):
        if self.inventory >= 1:
            self.inventory -= 1
            article_properties.total_profit += self.sp - self.cp

        elif self.inventory == 0:
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
        self.basket = []

    def if_bought(self,article_price,article):
        self.buying_power -= article_price
        self.interest = rd.random() # after the buyer has bought something, it will recalculate the interest
        # recalculating interest is an interesting idea - sort of tells about mass shopping
        # try making the interest unchanged to see the effect
        self.basket.append(article)

class operation:

    def __init__(self,employees):
        self.employees = employees
        self.month = 1
        self.fixed_costs = 200 # comprises of registration costs


    def calculate_revenue(self):
        min_salary = self.employees*130
        self.revenue = article_properties.total_profit - (min_salary + self.fixed_costs)
        return self.revenue