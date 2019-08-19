# Utilities for calculating DSR in Malaysia

def incometax(x):
    income=x
    rates=[0,0.01,0.03,0.08,0.14,0.21,0.24,0.245,0.25,0.26,0.28]
    bracket=[5000, 15000, 15000, 15000, 20000, 30000, 150000, 150000, 200000, 400000, 1000000]
    tax=0
    for i in range(0,len(bracket)):
        tax+= min(income,bracket[i])*rates[i]
        income-= bracket[i]
        if income<=0:
            return tax
    return tax+(income*rates[i])

def netincome(x):
    personal_relief=9000
    epf_relief=6000

    income=x*12
    chargeable=max(0, income-personal_relief-max(epf_relief-(0.11*income), 6000))
    # Netincome = income - tax - EPF - SOCSO - EIS
    netincome = income - incometax(chargeable) - (income * 0.11) - min(income*0.005, 240) - min(income*0.002, 96)
    return netincome/12


def installmentcal(x,name):
    # x is the total loan amount
    # name is the type of loan which determines the assumed interest rate and payment period.
    # Formula is based on mortgage amount calculator which applies compound interest to principal and then
    # removes the installment amount iteratively.
    
    rates={'HSLNFNCE':[0.046/12,240],'LN':[0.0875/12,48]}
    rates=rates.get(name)
    installment=(rates[0]*x*((1+rates[0])**rates[1]))/(((1+rates[0])**rates[1])-1)
    return installment
