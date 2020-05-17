import os
import pandas as pd
from datetime import datetime
from django.db.models import Sum
from fpdf import FPDF
from pylab import title, xlabel, ylabel, xticks, bar, legend, axis, savefig
from apps.accounts.models import Transaction
from django.conf import settings


def generate_report(user_id, start, end):
    df = pd.DataFrame()
    current_year = datetime.now().year
    feb_spend = Transaction.objects.filter(created_timestamp__year=current_year, owner_id=user_id,
                                             created_timestamp__month=2, sender_id=user_id).aggregate(Sum('amount'))
    march_spend = Transaction.objects.filter(created_timestamp__year=current_year, owner_id=user_id,
                                             created_timestamp__month=3, sender_id=user_id).aggregate(Sum('amount'))
    april_spend = Transaction.objects.filter(created_timestamp__year=current_year, owner_id=user_id,
                                             created_timestamp__month=4, sender_id=user_id).aggregate(Sum('amount'))
    may_spend = Transaction.objects.filter(created_timestamp__year=current_year, owner_id=user_id,
                                           created_timestamp__month=5, sender_id=user_id).aggregate(Sum('amount'))

    # earn
    feb_earn = Transaction.objects.filter(created_timestamp__year=current_year, owner_id=user_id,
                                            created_timestamp__month=3, receiver_id=user_id).aggregate(Sum('amount'))
    march_earn = Transaction.objects.filter(created_timestamp__year=current_year, owner_id=user_id,
                                            created_timestamp__month=3, receiver_id=user_id).aggregate(Sum('amount'))
    april_earn = Transaction.objects.filter(created_timestamp__year=current_year, owner_id=user_id,
                                            created_timestamp__month=4, receiver_id=user_id).aggregate(Sum('amount'))
    may_earn = Transaction.objects.filter(created_timestamp__year=current_year, owner_id=user_id,
                                          created_timestamp__month=5, receiver_id=user_id).aggregate(Sum('amount'))

    print(march_spend['amount__sum'])
    df['Month'] = ["Feb", "March", "April", "May"]
    df['Spend'] = [
    	int(feb_spend['amount__sum'])/10000 if march_spend['amount__sum'] else 0,
        int(march_spend['amount__sum'])/10000 if march_spend['amount__sum'] else 0,
        int(april_spend['amount__sum'])/10000 if april_spend['amount__sum'] else 0,
        int(may_spend['amount__sum'])/10000 if may_spend['amount__sum'] else 0,
    ]
    df['Earn'] = [
    	int(feb_earn['amount__sum'])/10000 if feb_earn['amount__sum'] else 0,
        int(march_earn['amount__sum'])/10000 if march_earn['amount__sum'] else 0,
        int(april_earn['amount__sum'])/10000 if april_earn['amount__sum'] else 0,
        int(may_earn['amount__sum'])/10000 if may_earn['amount__sum'] else 0,
    ]

    title("Recent 4 months sped/expanse report")
    xlabel('Month')
    ylabel('Amount/10000SGD')

    c = [2.0, 4.0, 6.0, 8.0]
    m = [x - 0.5 for x in c]

    xticks(c, df['Month'])

    bar(m, df['Spend'], width=0.5, color="#91eb87", label="Spend")
    bar(c, df['Earn'], width=0.5, color="#eb879c", label="Earn")

    legend()
    axis([0, 10, 0, 8])
    savefig('barchart.png')

    pdf = FPDF()
    pdf.add_page()
    pdf.set_xy(0, 0)
    pdf.set_font('arial', 'B', 12)
    pdf.cell(60)
    pdf.cell(75, 10, "Report from {} to {}".format(start, end), 0, 2, 'C')
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
    pdf.image('barchart.png', x=None, y=None, w=0, h=0, type='', link='')
    pdf.output('core/report.pdf', 'F')



