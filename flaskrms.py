from flask import *
import pandas as pd
# import psycopg2
from sqlalchemy import create_engine
from datetime import datetime
app=Flask(__name__)
engine = create_engine("postgresql+psycopg2://postgres:admin@localhost:5432/newdb1")


app.config['SECRET_KEY']='SECRETS'

@app.route('/', methods=['GET','POST'])
@app.route('/home', methods=['GET','POST'])
@app.route('/home.html', methods=['GET','POST'])
def home():
    return render_template('home.html')

@app.route('/Store-wise.html', methods=['GET','POST'])
@app.route('/Store-wise', methods=['GET','POST'])
def Storewise():
    if request.method=='POST':
        # print("Post")
        StoreCat=request.form.get("StoreCategory")
        # print(StoreCat)
        Date55=request.form.get("Date5")
        Month55=request.form.get("Month5")
        Year55=request.form.get("Year5")
        Date66=request.form.get("Date6")
        Month66=request.form.get("Month6")
        Year66=request.form.get("Year6")
        fromdate55=Date55+"/"+Month55+"/"+Year55
        datetime55=datetime.strptime(fromdate55, '%d/%m/%Y')
        fromdate66=Date66+"/"+Month66+"/"+Year66
        datetime66=datetime.strptime(fromdate66, '%d/%m/%Y')
        # print(datetime55)
        # print(type(datetime55))
        StoreRevenue=pd.read_sql("SELECT sum(RevenueSGD) FROM facts INNER JOIN Store ON Store.Store_Key = facts.Store_Key WHERE Store.Store_Name = '"+StoreCat+"' AND (facts.Date_Key between ' {} ' AND ' {} ');".format(datetime55.date(),datetime66.date()), engine)
        # print(StoreRevenue)
        return_obj = StoreRevenue.loc[0,'sum']
        if datetime66<datetime55:
            return render_template('Store-wise.html', StoreCat="TO Date cannot be earlier than FROM Date")
        else:    
            return render_template('Store-wise.html', revenue=return_obj, StoreCat=StoreCat, datetime55=datetime55.strftime('%Y-%m-%d'), datetime66=datetime66.strftime('%Y-%m-%d'))
    else:
        print("Get")
        return render_template('Store-wise.html',StoreCat="Pls. choose category above")

@app.route('/Product-wise.html', methods=['GET','POST'])
@app.route('/Product-wise', methods=['GET','POST'])
def Productwise():
    if request.method=='POST':
        # print("Post")
        ProdCat=request.form.get("ProductCategory")
        # print(ProdCat)
        Date11=request.form.get("Date1")
        Month11=request.form.get("Month1")
        Year11=request.form.get("Year1")
        Date22=request.form.get("Date2")
        Month22=request.form.get("Month2")
        Year22=request.form.get("Year2")
        fromdate11=Date11+"/"+Month11+"/"+Year11
        datetime11=datetime.strptime(fromdate11, '%d/%m/%Y')
        fromdate22=Date22+"/"+Month22+"/"+Year22
        datetime22=datetime.strptime(fromdate22, '%d/%m/%Y')
        ProdRevenue=pd.read_sql("SELECT sum(RevenueSGD) FROM facts INNER JOIN product ON product.product_key = facts.product_key WHERE product.product_category = '"+ProdCat+"' AND (facts.Date_Key between ' {} ' AND ' {} ');".format(datetime11.date(),datetime22.date()), engine)
        # print(ProdRevenue)
        return_obj = ProdRevenue.loc[0,'sum']
        if datetime22<datetime11:
            return render_template('Product-wise.html', ProdCat="TO Date cannot be earlier than FROM Date")
        else:
            return render_template('Product-wise.html', revenue=return_obj, ProdCat=ProdCat, datetime11=datetime11.strftime('%Y-%m-%d'), datetime22=datetime22.strftime('%Y-%m-%d'))
    else:
        print("Get")
        return render_template("Product-wise.html",ProdCat="Pls. choose category above") 
    
@app.route('/Payment-wise.html', methods=['GET','POST'])
@app.route('/Payment-wise', methods=['GET','POST'])
def Paymentwise():
    if request.method=='POST':
        # print("Post")
        PmtCat=request.form.get("PaymentCategory")
        # print(PmtCat)
        Date33=request.form.get("Date3")
        Month33=request.form.get("Month3")
        Year33=request.form.get("Year3")
        Date44=request.form.get("Date4")
        Month44=request.form.get("Month4")
        Year44=request.form.get("Year4")
        fromdate33=Date33+"/"+Month33+"/"+Year33
        datetime33=datetime.strptime(fromdate33, '%d/%m/%Y')
        fromdate44=Date44+"/"+Month44+"/"+Year44
        datetime44=datetime.strptime(fromdate44, '%d/%m/%Y')
        PmtRevenue=pd.read_sql("SELECT sum(RevenueSGD) FROM facts INNER JOIN Payment_Method ON Payment_Method.Payment_Method_Key = facts.Payment_Method_Key WHERE Payment_Method.Payment_Method = '"+PmtCat+"' AND (facts.Date_Key between ' {} ' AND ' {} ');".format(datetime33.date(),datetime44.date()), engine)
        CommRevenue=pd.read_sql("SELECT trunc(sum(facts.RevenueSGD*Payment_Method.Payment_Commission),2) as commission_paid FROM Payment_Method INNER JOIN facts ON Payment_Method.Payment_Method_Key = facts.Payment_Method_Key WHERE Payment_Method.Payment_Method = '"+PmtCat+"' AND (facts.Date_Key between ' {} ' AND ' {} ');".format(datetime33.date(),datetime44.date()), engine)
        # print(PmtRevenue)
        return_obj = PmtRevenue.loc[0,'sum']
        return_obj1 = CommRevenue.loc[0,'commission_paid']
        if datetime44<datetime33:
            return render_template('Payment-wise.html', PmtCat="TO Date cannot be earlier than FROM Date")
        else:
            return render_template('Payment-wise.html', revenue=return_obj, commission=return_obj1, PmtCat=PmtCat, datetime33=datetime33.strftime('%Y-%m-%d'), datetime44=datetime44.strftime('%Y-%m-%d'))
    else:
        print("Get")
        return render_template("Payment-wise.html",PmtCat="Pls. choose category above")

if __name__=='__main__':
    app.run(debug=True)

