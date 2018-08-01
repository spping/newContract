from flask import Flask, render_template, request
import collections
app = Flask(__name__)

from FutureContract import InFutureContract, OutFutureContract
from db_about import DBSession

@app.route('/', methods = ['GET', 'POST'])
@app.route('/<variety>', methods = ['POST', 'GET'])
def index(variety = None):

    if request.args:
        keys = [ifc.exchange for ifc in DBSession().query(InFutureContract, InFutureContract.exchange).distinct(InFutureContract.exchange)]
        print(keys)
        if request.args['location'] in keys:
            contracts = DBSession().query(InFutureContract).filter(InFutureContract.product == request.args['variety']).first().to_dict()
        else:
            contracts = DBSession().query(OutFutureContract).filter(OutFutureContract.product == request.args['variety']).first().to_dict()
        return render_template('contract.html', contracts = contracts)


    # return render_template('contract.html', contracts = DBSession().query(InFutureContract).first().to_dict())
    context = collections.defaultdict(list)
    fcs = DBSession().query(InFutureContract, InFutureContract.exchange, InFutureContract.product)
    for fc in fcs:
        context[fc.exchange].append(fc.product)
    fcs = DBSession().query(OutFutureContract, OutFutureContract.exchange, OutFutureContract.product)
    for fc in fcs:
        if fc.exchange.startswith('美国洲际交易所'):
            print(fc.exchange)
            context['美国洲际交易所'].append(fc.product)
            continue
        if fc.exchange.startswith('芝加哥商业交易所'):
            print(fc.exchange)
            context['芝加哥商业交易所'].append(fc.product)
            continue
        context[fc.exchange].append(fc.product)
    return render_template('tabbar.html', context = context)

if __name__ == '__main__':
    app.run(host='0.0.0.0')