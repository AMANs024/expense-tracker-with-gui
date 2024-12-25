import matplotlib.pyplot as plt

def generate_charts(data, month=None):
    if data.empty:
        return None, None
        
    category_data = data.groupby('Category')['Amount'].sum()
    
    # Generate Bar Chart
    bar_path = "static/bar_chart.png"
    category_data.plot(kind='bar', title='Expense by Category', color='skyblue', figsize=(8, 5))
    plt.ylabel("Amount")
    plt.xlabel("Category")
    plt.tight_layout()
    plt.savefig(bar_path)
    plt.close()

    # Generate Pie Chart
    pie_path = "static/pie_chart.png"
    category_data.plot(kind='pie', title='Expense Distribution', autopct='%1.1f%%', figsize=(6, 6))
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(pie_path)
    plt.close()
    
    return bar_path, pie_path