from flask import Flask, render_template_string, Response
import pandas as pd
import matplotlib.pyplot as plt
import io

app = Flask(__name__)

def load_and_filter_data(start_date, end_date):
    file_path = r"C:\Users\avram\OneDrive\Desktop\TRG Week 31\mcd.us.txt"
    df = pd.read_csv(file_path, sep=",", engine="python", parse_dates=['Date'], infer_datetime_format=True)

    # Drop 'OpenInt' if it exists
    if 'OpenInt' in df.columns:
        df = df.drop(columns=['OpenInt'])

    # Filter by date
    df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

    return df

def render_html(title, df):
    html_table = df.to_html(classes='table table-striped', index=False)
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title}</title>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    </head>
    <body>
        <div class="container mt-5">
            <h1 class="mb-4">{title}</h1>
            {html_table}
        </div>
    </body>
    </html>
    """
    return render_template_string(html_template)

# Route 1: 1970–1979
@app.route('/mcd_1970s')
def mcd_1970s():
    df = load_and_filter_data("1970-01-01", "1979-12-31")
    return render_html("McDonald's Data (1970–1979)", df)

# Route 2: 2000–2009
@app.route('/mcd_2000s')
def mcd_2000s():
    df = load_and_filter_data("2000-01-01", "2009-12-31")
    return render_html("McDonald's Data (2000–2009)", df)

# Route 3: 2010–2017
@app.route('/mcd_2010s')
def mcd_2010s():
    df = load_and_filter_data("2010-01-01", "2017-12-31")
    return render_html("McDonald's Data (2010–2017)", df)

@app.route('/mcd_1970s_high_low')
def mcd_1970s_high_low():
    try:
        df = load_and_filter_data("1970-01-01", "1979-12-31")

        plt.figure(figsize=(12, 6))
        plt.plot(df['Date'], df['High'], label='High', color='red', linewidth=1.5)
        plt.plot(df['Date'], df['Low'], label='Low', color='blue', linewidth=1.5)
        plt.title("McDonald's High and Low Prices (1970–1979)", fontsize=16)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Price', fontsize=12)
        plt.legend()
        plt.grid(True)

        # Output to PNG
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        return Response(buf, mimetype='image/png')

    except Exception as e:
        return f"An error occurred while generating the plot: {e}"
    
@app.route('/mcd_2000s_high_low')
def mcd_2000s_high_low():
    try:
        df = load_and_filter_data("2000-01-01", "2009-12-31")

        plt.figure(figsize=(12, 6))
        plt.plot(df['Date'], df['High'], label='High', color='red', linewidth=1.5)
        plt.plot(df['Date'], df['Low'], label='Low', color='blue', linewidth=1.5)
        plt.title("McDonald's High and Low Prices (2000–2010)", fontsize=16)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Price', fontsize=12)
        plt.legend()
        plt.grid(True)

        # Output to PNG
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        return Response(buf, mimetype='image/png')

    except Exception as e:
        return f"An error occurred while generating the plot: {e}"

if __name__ == '__main__':
    app.run(debug=True)
