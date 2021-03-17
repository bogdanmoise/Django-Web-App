def scrape():
    from bs4 import BeautifulSoup as soup
    from urllib.request import urlopen as req_u
    import csv

    page_url = 'https://www.emag.ro/laptopuri/filter/tip-laptop-f7882,ultraportabil-v-4670916/c?ref=subcat_1_fashion-grid_2'

    client = req_u(page_url)
    page_html = client.read()
    client.close()

    page_soup = soup(page_html, 'html.parser')
    containers = page_soup.find_all('div', {'class': 'card'})

    with open('home/static/web_scraper_files/laptops.csv', 'w', newline='') as file:
        file_writer = csv.writer(file, delimiter=',')

        file_headers = ['Index', 'Product Name', 'Stock', 'Price', 'Old Price']
        file_writer.writerow(file_headers)

        i = 0
        for container in containers:
            i += 1

            try:
                container_name = container.find_all('a', {'class': 'product-title js-product-url'})
                product_name = container_name[0].text.strip()

                product_name = product_name.replace(',', '')
                product_name = product_name.replace('™', '')
                product_name = product_name.replace('®', '')
                product_name = product_name.replace('ᵉ', '')
                product_name = product_name.replace('î', 'i')
            except:
                continue

            try:
                container_stock = container.find_all('p', {'class': 'product-stock-status'})
                product_stock = container_stock[0].text.strip()
            except:
                continue

            try:
                container_price_now = container.find_all('p', {'class': 'product-new-price'})
                product_price_now = container_price_now[0].text.strip()
                product_price_now = product_price_now[:-6]
                product_price_now += ' lei '
            except:
                continue

            try:
                container_price_old = container.find_all('p', {'class': 'product-old-price'})
                product_price_old = container_price_old[0].text.strip()

                if not product_price_old:
                    product_price_old = 'no sale :('
                else:
                    product_price_old = product_price_old[:5]
                    product_price_old += ' lei '
            except:
                continue

            print(f'Product {i}')
            print(product_name)
            print(f'Stock: {product_stock}')
            print(f'Price: {product_price_now}')
            print(f'Old Price: {product_price_old}')
            print()

            product = [i, product_name, product_stock, product_price_now, product_price_old]
            file_writer.writerow(product)

def read_file():
    import csv

    items = []

    with open('home/static/web_scraper_files/laptops.csv', 'r') as file:
        rows = csv.reader(file, delimiter=',')
        for row in rows:
            if row[0] == 'Index':
                continue
            items.append({
                'index': row[0],
                'name': row[1],
                'stock': row[2],
                'price': row[3],
                'old_price': row[4]
            })

    return items

