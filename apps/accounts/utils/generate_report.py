import os
import pandas as pd
from datetime import datetime
from django.db.models import Sum
from fpdf import FPDF
from matplotlib.pyplot import title, xlabel, ylabel, xticks, bar, legend, axis, savefig
import matplotlib.pyplot as plt
from apps.accounts.models import Transaction
df = pd.DataFrame()


def generate_report(user_id, start, end):
    
    current_year = datetime.now().year
    current_month = datetime.now().month
    feb_spend = Transaction.objects.filter(
        created_timestamp__year=current_year, 
        created_timestamp__month=current_month-3,
        sender_id=user_id
    ).aggregate(Sum('amount'))
    march_spend = Transaction.objects.filter(
        created_timestamp__year=current_year,
        created_timestamp__month=current_month-2,
        sender_id=user_id).aggregate(Sum('amount'))
    april_spend = Transaction.objects.filter(
        created_timestamp__year=current_year,
        created_timestamp__month=current_month-1,
        sender_id=user_id).aggregate(Sum('amount'))
    may_spend = Transaction.objects.filter(
        created_timestamp__year=current_year,
        created_timestamp__month=current_month, sender_id=user_id
        ).aggregate(Sum('amount'))

    # earn
    feb_earn = Transaction.objects.filter(
        created_timestamp__year=current_year, 
        receiver_id=user_id,
        created_timestamp__month=current_month-3
        ).aggregate(Sum('amount')
    )
    march_earn = Transaction.objects.filter(
        created_timestamp__year=current_year, 
        receiver_id=user_id,
        created_timestamp__month=current_month-2
        ).aggregate(Sum('amount')
    )
    april_earn = Transaction.objects.filter(
        created_timestamp__year=current_year,
        created_timestamp__month=current_month-1,
        receiver_id=user_id).aggregate(Sum('amount')
    )
    may_earn = Transaction.objects.filter(
        created_timestamp__year=current_year, 
        receiver_id=user_id,
        created_timestamp__month=current_month).aggregate(Sum('amount')
    )
    
    df = pd.DataFrame()
    df['Month'] = ["Feb", "March", "April", "May"]

    df['Spend'] = [
        int(feb_spend['amount__sum'])/1000 if march_spend['amount__sum'] else 0.00,
        int(march_spend['amount__sum'])/1000 if march_spend['amount__sum'] else 0.00,
        int(april_spend['amount__sum'])/1000 if april_spend['amount__sum'] else 0.00,
        int(may_spend['amount__sum'])/1000 if may_spend['amount__sum'] else 0.00
    ]
    df['Earn'] = [
        int(feb_earn['amount__sum'])/1000 if feb_earn['amount__sum'] else 0.00,
        int(march_earn['amount__sum'])/1000 if march_earn['amount__sum'] else 0.00,
        int(april_earn['amount__sum'])/1000 if april_earn['amount__sum'] else 0.00,
        int(may_earn['amount__sum'])/1000 if may_earn['amount__sum'] else 0.00
    ]
    title("Recent 4 months sped/expanse report")
    xlabel('Month')
    ylabel('Amount/(1000)SGD')

    c = [2.0, 4.0, 6.0, 8.0]
    m = [1.5, 3.5, 5.5, 7.5]

    xticks(c, df['Month'])
    bar([], 0)
    bar(m, df['Earn'], width=0.5, color="#91eb87", label="Earn")
    bar(c, df['Spend'], width=0.5, color="#eb879c", label="Spend")

    legend()
    axis([0, 10, 0, 100])
    savefig('barchart.png')
    # close it to avoid web server crush
    plt.close()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_xy(0, 0)
    pdf.set_font('arial', 'B', 12)
    pdf.cell(60)
    pdf.cell(75, 10, "User expanse report from {} to {}".format(start, end), 0, 2, 'C')
    pdf.cell(90, 10, " ", 0, 2, 'C')
    pdf.cell(-40)
    pdf.cell(50, 10, 'Month', 1, 0, 'C')
    pdf.cell(40, 10, 'Spend', 1, 0, 'C')
    pdf.cell(40, 10, 'Earn', 1, 2, 'C')
    pdf.cell(-90)
    pdf.set_font('arial', '', 12)
    for i in range(0, len(df)):
        pdf.cell(50, 10, '%s' % (df['Month'].iloc[i]), 1, 0, 'C')
        pdf.cell(40, 10, '%s' % (str(df.Earn.iloc[i])), 1, 0, 'C')
        pdf.cell(40, 10, '%s' % (str(df.Spend.iloc[i])), 1, 2, 'C')
        pdf.cell(-90)
    pdf.cell(90, 10, " ", 0, 2, 'C')
    pdf.cell(-30)
    pdf.image('barchart.png', x=1, y=None, w=0, h=0, type='', link='')
    pdf.output('core/report.pdf', 'F')



