from django.shortcuts import render, redirect
from .models import Holding
from .positions import *
from .helper_functions import get_price, get_fg, txtToArray, cum_up_or_down
from .forms import HoldingForm
from datetime import date
import os

# Create your views here.

def index(request):
    return render(request, 'portfolio/index.html')

def holdings(request):
    if request.user.id:
        module_dir = os.path.dirname(__file__) 
        file_path = os.path.join(module_dir, './static/portfolio/text/coin_list.txt')   #full path to text.
        coin_list = txtToArray(file_path)

        holdings_db = Holding.objects.filter(trader=request.user.id).filter(sold=False) # Holdings from database
        portfolio = Positions() # Holdings as objects - used to print to the front end
        for holding in holdings_db:
            portfolio.add(holding.coin_id, holding.symbol, float(holding.entry_price), float(holding.entry_amount), date=holding.entry_date, dbID=holding.id)
        
        btc = f'{get_price("bitcoin"):,}'
        eth = f'{get_price("ethereum"):,}'
        fg = get_fg()
        fg_class = get_fg(classification=True)


        if request.method == "POST":
            form = HoldingForm(request.POST)
            print("validating")
            print(form.errors)
            print(form.fields["use_mv_entry"])
            if form.is_valid():
                
                print("Holdings")
                obj = form.save(commit=False)
                obj.trader = request.user
                if request.POST.get("use_mv_entry"):
                    obj.entry_price = get_price(obj.coin_id.lower())
                obj.save()
                return redirect('holdings')
        else:
            form = HoldingForm()

        cum_pl = portfolio.get_cumulative_pl()
        stance = cum_up_or_down(cum_pl)

        portfolio.display()
        return render(request, 'portfolio/holdings.html', {
            'coin_list': coin_list,
            'BTC': btc,
            'ETH': eth,
            'FG': fg,
            'FG_class': fg_class,
            'portfolio': portfolio,
            'stance': stance,
            'cum_val': f'{portfolio.get_cumulative_value():,}',
            'cum_pl': f'{cum_pl:,}',
            'cum_pl_perc': f'{portfolio.get_cumulative_pl_percent():,}',
            'form': form,
            'current': True
        })
    else:
        return redirect('user-portfolio')

def delete_holding(request):
    pk = request.POST['pk']
    holding = Holding.objects.get(pk=pk)
    print(f'Holding to be sold: {holding}')
    if request.POST.get('use_mv'):
        holding.exit_price = get_price(holding.coin_id.lower())
    else:
        holding.exit_price = request.POST.get('exit-price')
    holding.sold = True
    holding.save()
    return redirect('holdings')

def previous_holdings(request):
    btc = f'{get_price("bitcoin"):,}'
    eth = f'{get_price("ethereum"):,}'
    fg = get_fg()
    fg_class = get_fg(classification=True)

    prev_holdings_db = Holding.objects.filter(trader=request.user.id).filter(sold=True) # Holdings from database
    previous_portfolio = PreviousPositions()

    for holding in prev_holdings_db:
        previous_portfolio.add(holding.coin_id, holding.symbol, float(holding.entry_price), float(holding.entry_amount), float(holding.exit_price), date=holding.entry_date, inExitDate=holding.exit_date, dbID=holding.id)

    cum_pl = previous_portfolio.get_cumulative_pl()
    stance = cum_up_or_down(cum_pl)
    return render(request, 'portfolio/previous_holdings.html', {
        'BTC': btc,
        'ETH': eth,
        'FG': fg,
        'FG_class': fg_class,
        'previous_portfolio': previous_portfolio,
        'stance': stance,
        'cum_val': f'{previous_portfolio.get_cumulative_value():,}',
        'cum_pl': f'{cum_pl:,}',
        'cum_pl_perc': f'{previous_portfolio.get_cumulative_pl_percent():,}',
        'current': False,
    })

def delete_previous_holding(request, holding_id):
    holding = Holding.objects.get(pk=holding_id)
    current = True if not holding.sold else False
    print(holding)
    holding.delete()


    if current:
        return redirect('holdings')
    else:
        return redirect('previous-holdings')