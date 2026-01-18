import matplotlib
import matplotlib.pyplot as plt
import io
import base64

def generate_pie_chart(incomes, expenses):
    # Если данных нет, график не рисуем
    if incomes == 0 and expenses == 0:
        return None

    labels = ['Доходы', 'Расходы']
    values = [incomes, expenses]
    colors = ['#4ade80', '#f87171']  # Приятный зеленый и красный

    plt.figure(figsize=(5, 5))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
    plt.axis('equal')

    # Сохраняем график в виртуальную память (буфер)
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    # Кодируем картинку в строку, чтобы передать в HTML
    graph = base64.b64encode(image_png)
    return graph.decode('utf-8')