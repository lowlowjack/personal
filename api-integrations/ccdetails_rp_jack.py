import scrapy
from bs4 import BeautifulSoup as bs
from getpass import getpass
import re

# See the documentations on scrapy on how to deploy
# Your mileage may on robot.txt protocol. Consider using a proxy or etc.

f=lambda x:re.search('\[\]',x)
def num(i,x):
    if i<10:
        return(x[-1]==str(i) and x[-2]!=str(1))
    else:
        return(x[-2:]==str(i))


class ccdetails_Spider(scrapy.Spider):

    #TO DO: Cut out the BeautifulSoup dependence as it is slow.
    name = "ccdetails"
    http_user='login'
    http_pass=getpass('Password for staging: \n')
    def start_requests(self):
        yield scrapy.Request("https://url.com/admin/product/?q=credit-card",
                                   callback=self.logged_in)

    def logged_in(self, response):
        main=bs(response.body,'lxml')
        ccurilist=main.find_all('a',attrs={"class":"btn btn-warning edit-product"})
        ccurilist=['https://url.com/admin/product/'+k.get('href') for k in ccurilist]
        for i in ccurilist:
            yield scrapy.Request(i)


    def parse(self,response):
        inputs=dict()
        main=bs(response.body,'lxml')

        ##Text inputs
        text=main.find_all('input',attrs={'type':'text'})
        inputs.update({k.get('name'):k.get('value') for k in text})

        ##Number inputs
        num=main.find_all('input',attrs={'type':'number'})
        inputs.update({k.get('name'):k.get('value') for k in num})

        ##Selection inputs
        select=main.find_all('select')
        inputs.update({k.get('name'):k.get('data-value') for k in select})

        ##Checkboxes
        check=main.find_all('input',attrs={'type':'checkbox'})
        inputs.update({k.get('name'):('Y' if k.get('checked')=="" else 'N') for k in check})

        ##Text Areas
        textarea=main.find_all('textarea')
        inputs.update({k.get('name'):k.text for k in textarea})

        ##Handling the table elements
        tabkeys=list(filter(f,list(inputs.keys())))
        for k in tabkeys:
            inputs.pop(k)
            number=0
            d=main.find_all(attrs={'name':k})
            typ=d[0].get('type')
            for i in d:
                if typ=='number' or typ=='text':
                    inputs.update({i.get('name')+str(number):i.get('value')})
                elif typ=='checkbox':
                    inputs.update({i.get('name')+str(number):('Y' if i.get('checked')=="" else 'N')})
                else:
                        inputs.update({i.get('name')+str(number):i.get('data-value')})
                number=number+1
        yield {inputs['name']:inputs}
