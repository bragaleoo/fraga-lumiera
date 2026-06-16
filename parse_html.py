import json
from html.parser import HTMLParser

class ProductParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.products = []
        self.current_product = None
        self.in_id = False
        self.in_title = False
        self.in_desc = False
        self.in_cash = False
        self.in_install = False
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        cls = attrs_dict.get('class', '')
        
        if tag == 'article' and 'product-card' in cls:
            self.current_product = {
                'line': 'professional' if 'professional-product' in cls else 'home-care',
                'image': '',
                'id': '',
                'title': '',
                'description': '',
                'cash_price': '',
                'installment_price': ''
            }
        elif self.current_product:
            if tag == 'img':
                self.current_product['image'] = attrs_dict.get('src', '')
            elif tag == 'span' and 'product-id' in cls:
                self.in_id = True
            elif tag == 'h3' and 'product-title' in cls:
                self.in_title = True
            elif tag == 'p' and 'product-desc' in cls:
                self.in_desc = True
            elif tag == 'span' and 'price-value-cash' in cls:
                self.in_cash = True
            elif tag == 'span' and 'price-value-install' in cls:
                self.in_install = True
                
    def handle_data(self, data):
        if self.current_product:
            if self.in_id:
                self.current_product['id'] += data
            elif self.in_title:
                self.current_product['title'] += data
            elif self.in_desc:
                self.current_product['description'] += data
            elif self.in_cash:
                self.current_product['cash_price'] += data
            elif self.in_install:
                self.current_product['installment_price'] += data
                
    def handle_endtag(self, tag):
        if self.current_product:
            if tag == 'article':
                # Clean up whitespace
                for key in ['id', 'title', 'description', 'cash_price', 'installment_price']:
                    self.current_product[key] = self.current_product[key].strip()
                self.products.append(self.current_product)
                self.current_product = None
            elif tag == 'span' and self.in_id:
                self.in_id = False
            elif tag == 'h3' and self.in_title:
                self.in_title = False
            elif tag == 'p' and self.in_desc:
                self.in_desc = False
            elif tag == 'span' and self.in_cash:
                self.in_cash = False
            elif tag == 'span' and self.in_install:
                self.in_install = False

def main():
    with open("index.html", "r", encoding="utf-8") as f:
        html_content = f.read()

    parser = ProductParser()
    parser.feed(html_content)

    with open("parsed_products.json", "w", encoding="utf-8") as f:
        json.dump(parser.products, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully parsed {len(parser.products)} products into parsed_products.json.")

if __name__ == "__main__":
    main()
