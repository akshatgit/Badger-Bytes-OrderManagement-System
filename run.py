from server import app


if __name__ == '__main__':
    # SIGINT to stop (Ctrl + C)
    app.run(host='127.0.0.1',port=6969, debug=True)

    # pdfkit.from_url('http://127.0.0.1:5000/customer/review','shaurya.pdf')