import matplotlib
import matplotlib.pyplot as plt
import io
import base64

def generate_pie_chart(incomes, expenses):
    if incomes == 0 and expenses == 0:
        return None

    labels = ['Доходы', 'Расходы']
    values = [incomes, expenses]
    colors = ['#4ade80', '#f87171']

    plt.figure(figsize=(5, 5))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
    plt.axis('equal')

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    graph = base64.b64encode(image_png)
    return graph.decode('utf-8')