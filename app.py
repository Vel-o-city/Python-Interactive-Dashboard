import pandas as pd
import numpy as np 

#required for building the interactive dashboard
import panel as pn
pn.extension('tabulator')
import hvplot.pandas
import holoviews as hv
hv.extension('bokeh')

#Reading The CSV file
df=pd.read_csv("/Users/vel/Desktop/projects/random_banking_transactions_with_categories.csv")

#Converting Date  into date data type to do further discrimination
df['Date'] = pd.to_datetime(df['Date'])

# Extract the month and year information
df['Month'] = df['Date'].dt.month
df['Year'] = df['Date'].dt.year

# Get the latest month and year
latest_year = df[df.Year == df['Year'].max()]
latest_month = latest_year['Month'].max()

# Filter the dataframe to include only transactions from the latest month
last_month_expenses = df[(df['Month'] == latest_month)]

last_month_expenses = last_month_expenses.groupby('Category')['Amount'].sum().reset_index()

last_month_expenses['Amount']=last_month_expenses['Amount'].astype('str')
last_month_expenses['Amount']=last_month_expenses['Amount'].str.replace('-','')
last_month_expenses['Amount']=last_month_expenses['Amount'].astype('float')        #get absolute figures

last_month_expenses = last_month_expenses[last_month_expenses["Category"].str.contains("Excluded|unassigned|Other") == False]    #exclude "excluded" category
last_month_expenses = last_month_expenses.sort_values(by='Amount', ascending=False)    #sort values
last_month_expenses['Amount'] = last_month_expenses['Amount'].round().astype(int)      #round values
last_month_expenses_tot = last_month_expenses['Amount'].sum()


def calculate_difference(event):
    income = float(income_widget.value)
    recurring_expenses = float(recurring_expenses_widget.value)
    monthly_expenses = float(monthly_expenses_widget.value)
    difference = income - recurring_expenses - monthly_expenses
    difference_widget.value = str(difference)

income_widget = pn.widgets.TextInput(name="Income", value="0")
recurring_expenses_widget = pn.widgets.TextInput(name="Recurring Expenses", value="0")
monthly_expenses_widget = pn.widgets.TextInput(name="Non-Recurring Expenses", value=str(last_month_expenses_tot))
difference_widget = pn.widgets.TextInput(name="Last Month's Savings", value="0")

income_widget.param.watch(calculate_difference, "value")
recurring_expenses_widget.param.watch(calculate_difference, "value")
monthly_expenses_widget.param.watch(calculate_difference, "value")

damn=pn.Column(income_widget, recurring_expenses_widget, monthly_expenses_widget, difference_widget)
last_month_expenses_chart = last_month_expenses.hvplot.bar(
    x='Category', 
    y='Amount', 
    height=250, 
    width=650, 
    title="Last Month Expenses",
    ylim=(0, 1000))


df['Date'] = pd.to_datetime(df['Date'])            # convert the 'Date' column to a datetime object
df['Month-Year'] = df['Date'].dt.to_period('M')    # extract the month and year from the 'Date' column and create a new column 'Month-Year'
monthly_expenses_trend_by_cat = df.groupby(['Month-Year', 'Category'])['Amount'].sum().reset_index()

monthly_expenses_trend_by_cat['Amount']=monthly_expenses_trend_by_cat['Amount'].astype('str')
monthly_expenses_trend_by_cat['Amount']=monthly_expenses_trend_by_cat['Amount'].str.replace('-','')
monthly_expenses_trend_by_cat['Amount']=monthly_expenses_trend_by_cat['Amount'].astype('float')
monthly_expenses_trend_by_cat = monthly_expenses_trend_by_cat[monthly_expenses_trend_by_cat["Category"].str.contains("Other") == False]

monthly_expenses_trend_by_cat = monthly_expenses_trend_by_cat.sort_values(by='Amount', ascending=False)
monthly_expenses_trend_by_cat['Amount'] = monthly_expenses_trend_by_cat['Amount'].round().astype(int)
monthly_expenses_trend_by_cat['Month-Year'] = monthly_expenses_trend_by_cat['Month-Year'].astype(str)
monthly_expenses_trend_by_cat = monthly_expenses_trend_by_cat.rename(columns={'Amount': 'Amount '})


#Define Panel widget

select_category1 = pn.widgets.Select(name='Select Category', options=[
    'All','Appliances', 'Groceries', 'Credit Cards', 'Loans', 'Entertainment', 'Utilities', 'Travel','Restaurant',
])
select_category1
# define plot function
def plot_expenses(category):
    if category == 'All':
        plot_df = monthly_expenses_trend_by_cat.groupby('Month-Year').sum()
    else:
        plot_df = monthly_expenses_trend_by_cat[monthly_expenses_trend_by_cat['Category'] == category].groupby('Month-Year').sum()
    plot = plot_df.hvplot.bar(x='Month-Year', y='Amount ')
    return plot
    
# define callback function
@pn.depends(select_category1.param.value)
def update_plot(category):
    plot = plot_expenses(category)
    return plot

# create layout
monthly_expenses_trend_by_cat_chart = pn.Column(select_category1, update_plot)
monthly_expenses_trend_by_cat_chart[1].width = 600


df = df[['Date', 'Category','Amount']]
df['Amount']=df['Amount'].astype('str')
df['Amount']=df['Amount'].str.replace('-','')
df['Amount']=df['Amount'].astype('float')        #get absolute figures

df = df[df["Category"].str.contains("Other") == False]    #exclude "excluded" category
df['Amount'] = df['Amount'].round().astype(int)      #round values
df['Date']=df['Date'].dt.date


# Define a function to filter the dataframe based on the selected category
def filter_df(category):
    if category == 'All':
        return df
    return df[df['Category'] == category]

# Create a DataFrame widget that updates based on the category filter
summary_table = pn.widgets.DataFrame(filter_df('All'), height = 300,width=400)

# Define a callback that updates the dataframe widget when the category filter is changed
def update_summary_table(event):
    summary_table.value = filter_df(event.new)

# Add the callback function to the category widget
select_category1.param.watch(update_summary_table, 'value')


# Create Final Dashboard

template = pn.template.FastListTemplate(
    title="Finance Summary Dashboard",
    theme='dark',
    sidebar_width=300,
    sidebar=[
        pn.pane.Markdown("## *Too many people spend money they earned..to buy things they don't want..to impress people that they don't like. --Will Rogers*"),
        pn.pane.Markdown(""),
        pn.pane.Markdown(""),
        damn
    ],
    main=[
        pn.Row(last_month_expenses_chart, sizingmode="stretch_both"),
        select_category1,
        pn.GridBox(
            monthly_expenses_trend_by_cat_chart[1],
            summary_table,
            ncols=2,
            width=500,  
            align='start',
            sizing_mode='stretch_width'
        )
    ]
)


template.show()

