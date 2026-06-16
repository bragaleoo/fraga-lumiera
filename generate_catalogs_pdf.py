import json
import os
from PIL import Image, ImageDraw, ImageFont

# 1. Load product data
with open("parsed_products.json", "r", encoding="utf-8") as f:
    products = json.load(f)

# 2. Setup paths and fonts
font_dir = "C:\\Windows\\Fonts"
font_serif_bold = os.path.join(font_dir, "georgiab.ttf")
font_serif_regular = os.path.join(font_dir, "georgia.ttf")
font_sans_bold = os.path.join(font_dir, "arialbd.ttf")
font_sans_regular = os.path.join(font_dir, "arial.ttf")

# Fallback check
if not os.path.exists(font_serif_bold):
    font_serif_bold = "arialbd.ttf"
    font_serif_regular = "arial.ttf"
    font_sans_bold = "arialbd.ttf"
    font_sans_regular = "arial.ttf"

# Colors
GOLD_COLOR = (197, 160, 89)
BG_COLOR = (10, 10, 12)
WHITE_COLOR = (245, 245, 247)
GRAY_COLOR = (158, 158, 159)

# Define fonts with appropriate sizes
f_header_title = ImageFont.truetype(font_serif_regular, 32)
f_header_sub = ImageFont.truetype(font_sans_regular, 14)
f_prod_id = ImageFont.truetype(font_sans_bold, 14)
f_prod_title = ImageFont.truetype(font_serif_bold, 28)
f_prod_desc = ImageFont.truetype(font_sans_regular, 16)
f_price_lbl = ImageFont.truetype(font_sans_bold, 14)
f_price_val = ImageFont.truetype(font_serif_regular, 26)
f_obs_note = ImageFont.truetype(font_sans_regular, 14)
f_footer_logo = ImageFont.truetype(font_serif_regular, 30)
f_footer_page = ImageFont.truetype(font_sans_regular, 14)

def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = " ".join(current_line + [word])
        # Calculate text bounding box
        bbox = font.getbbox(test_line)
        w = bbox[2] - bbox[0]
        if w <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))
    return lines

def fit_image(img, target_w, target_h):
    img_ratio = img.width / img.height
    target_ratio = target_w / target_h
    if img_ratio > target_ratio:
        new_w = int(img.height * target_ratio)
        offset = (img.width - new_w) // 2
        img = img.crop((offset, 0, offset + new_w, img.height))
    else:
        new_h = int(img.width / target_ratio)
        offset = (img.height - new_h) // 2
        img = img.crop((0, offset, img.width, offset + new_h))
    return img.resize((target_w, target_h), Image.Resampling.LANCZOS)

def draw_separator_gradient(draw, x_start, x_end, y):
    # Renders a subtle divider line
    draw.line([x_start, y, x_end, y], fill=(197, 160, 89, 100), width=1)

def render_product_card(draw, page_img, prod, x, y, width, is_professional):
    # 1. Product Image Box (502x603)
    img_h = int(width * 1.2)  # 5:6 aspect ratio
    img_path = prod["image"]
    
    if os.path.exists(img_path):
        p_img = Image.open(img_path)
        p_img_fitted = fit_image(p_img, width, img_h)
        # Paste with alpha channel check
        if p_img_fitted.mode in ('RGBA', 'LA') or (p_img_fitted.mode == 'P' and 'transparency' in p_img_fitted.info):
            p_img_fitted_rgba = p_img_fitted.convert('RGBA')
            page_img.paste(p_img_fitted_rgba, (x, y), mask=p_img_fitted_rgba)
        else:
            page_img.paste(p_img_fitted, (x, y))
    else:
        # Fallback placeholder rectangle if image not found
        draw.rectangle([x, y, x + width, y + img_h], outline=GOLD_COLOR, width=1)
        draw.text((x + 20, y + img_h // 2), "Image Not Found", fill=GRAY_COLOR, font=f_prod_desc)
    
    # Draw outline around photo
    draw.rectangle([x - 1, y - 1, x + width, y + img_h], outline=GOLD_COLOR, width=1)
    
    # 2. Product ID (gold uppercase)
    id_y = y + img_h + 37
    draw.text((x, id_y), prod["id"].upper(), fill=GOLD_COLOR, font=f_prod_id)
    
    # 3. Product Title
    title_y = id_y + 30
    draw.text((x, title_y), prod["title"], fill=WHITE_COLOR, font=f_prod_title)
    
    # 4. Product Description (wrapped)
    desc_y = title_y + 50
    desc_lines = wrap_text(prod["description"], f_prod_desc, width)
    curr_y = desc_y
    for line in desc_lines:
        draw.text((x, curr_y), line, fill=GRAY_COLOR, font=f_prod_desc)
        curr_y += 26
        
    # 5. Price Separator Line
    sep_y = y + img_h + 327
    draw.line([x, sep_y, x + width, sep_y], fill=(60, 60, 64), width=1)
    
    # 6. Pricing Layout
    price_y = sep_y + 30
    # Left price (À VISTA)
    draw.text((x, price_y), "À VISTA", fill=GOLD_COLOR, font=f_price_lbl)
    draw.text((x, price_y + 50), prod["cash_price"], fill=WHITE_COLOR, font=f_price_val)
    
    # Determine the installment count
    inst_count = 10 if (is_professional and ("Botox" in prod["title"] or "Progressiva" in prod["title"])) else 5
    inst_label = f"{inst_count:02d}X"
    
    # Right price (05x or 10x installment)
    # Check if we have an installment price
    inst_price = prod["installment_price"]
    if not inst_price or "de R$" not in inst_price:
        # Generate installment dynamically if empty or not formatted correctly
        try:
            val = float(prod["cash_price"].replace("R$", "").replace(".", "").replace(",", ".").strip())
            # Select proper markup
            if is_professional:
                inst_val = val * 1.48 if inst_count == 5 else val * 1.14
            else:
                inst_val = val * 1.18
            
            installment_val = inst_val / inst_count
            inst_price = f"{inst_count}x de R$ {installment_val:.2f}".replace(".", ",")
        except Exception:
            inst_price = f"{inst_count}x de R$ --"
            
    # Right-align the installment label and value to prevent overflow
    label_bbox = f_price_lbl.getbbox(inst_label)
    label_w = label_bbox[2] - label_bbox[0]
    label_x = x + width - label_w
    
    price_bbox = f_price_val.getbbox(inst_price)
    price_w = price_bbox[2] - price_bbox[0]
    price_x = x + width - price_w
    
    draw.text((label_x, price_y), inst_label, fill=GOLD_COLOR, font=f_price_lbl)
    draw.text((price_x, price_y + 50), inst_price, fill=WHITE_COLOR, font=f_price_val)

def generate_pdf(line_type, output_pdf_name):
    print(f"\nGenerating catalog for {line_type}...")
    is_prof = line_type == "professional"
    
    # Filter products for this line
    line_products = [p for p in products if p["line"] == line_type]
    print(f"Found {len(line_products)} products.")
    
    pages = []
    
    # Page 1: Load original cover
    line_type_und = line_type.replace("-", "_")
    cover_path = f"assets/pages/{line_type_und}_page_1.jpg"
    if os.path.exists(cover_path):
        pages.append(Image.open(cover_path).convert("RGB"))
        print("Loaded Cover Page.")
    else:
        print(f"Warning: Cover page {cover_path} not found.")
        
    # Page 2: Load original history
    history_path = f"assets/pages/{line_type_und}_page_2.jpg"
    if os.path.exists(history_path):
        pages.append(Image.open(history_path).convert("RGB"))
        print("Loaded History Page.")
    else:
        print(f"Warning: History page {history_path} not found.")
        
    # Product pages (2 products per page)
    prod_idx = 0
    page_num = 2  # History is page 1 (label 01), so product pages start at index 2 (label 02)
    
    while prod_idx < len(line_products):
        page_num += 1
        canvas_w = 1241
        canvas_h = 1755
        
        # Create blank canvas
        page_img = Image.new("RGB", (canvas_w, canvas_h), BG_COLOR)
        draw = ImageDraw.Draw(page_img)
        
        # 1. Gold border
        draw.rectangle([35, 35, canvas_w - 35, canvas_h - 35], outline=GOLD_COLOR, width=2)
        
        # 2. Header
        header_y = 160
        # Draw header text centered
        hdr_text = "CATÁLOGO DE PRODUTOS"
        hdr_bbox = f_header_title.getbbox(hdr_text)
        hdr_w = hdr_bbox[2] - hdr_bbox[0]
        draw.text(((canvas_w - hdr_w) // 2, header_y), hdr_text, fill=WHITE_COLOR, font=f_header_title)
        
        # Draw gold separator
        draw.line([340, header_y + 60, canvas_w - 340, header_y + 60], fill=GOLD_COLOR, width=1)
        
        # Draw subtitle
        sub_text = "FRAGA LUMIÉRA • PROFISSIONAL" if is_prof else "FRAGA LUMIÉRA • HOME CARE"
        sub_bbox = f_header_sub.getbbox(sub_text)
        sub_w = sub_bbox[2] - sub_bbox[0]
        draw.text(((canvas_w - sub_w) // 2, header_y + 90), sub_text, fill=GOLD_COLOR, font=f_header_sub)
        
        # 3. Determine products for this page (up to 2)
        page_prods = line_products[prod_idx:prod_idx + 2]
        prod_idx += 2
        
        if len(page_prods) == 2:
            # Render Left Product
            render_product_card(draw, page_img, page_prods[0], 78, 420, 502, is_prof)
            # Render Right Product
            render_product_card(draw, page_img, page_prods[1], 661, 420, 502, is_prof)
        else:
            # Centered Product (single product on page)
            render_product_card(draw, page_img, page_prods[0], 369, 420, 502, is_prof)
            
        # 4. Professional OBS note
        if is_prof:
            obs_text = "* O valor apresentado na Linha Profissional é válido para compras a partir de 2 unidades."
            obs_bbox = f_obs_note.getbbox(obs_text)
            obs_w = obs_bbox[2] - obs_bbox[0]
            draw.text(((canvas_w - obs_w) // 2, 1560), obs_text, fill=GOLD_COLOR, font=f_obs_note)
            
        # 5. Footer Logo
        logo_text = "FL"
        logo_bbox = f_footer_logo.getbbox(logo_text)
        logo_w = logo_bbox[2] - logo_bbox[0]
        draw.text(((canvas_w - logo_w) // 2, 1630), logo_text, fill=GOLD_COLOR, font=f_footer_logo)
        
        # 6. Page Number
        page_num_str = f"{page_num - 1:02d}"  # Sequential catalog numbers: 02, 03, 04...
        draw.text((1120, 1630), page_num_str, fill=GOLD_COLOR, font=f_footer_page)
        
        # Save page image for debugging/lookbook
        page_jpg_path = f"assets/pages/{line_type_und}_page_{page_num}.jpg"
        page_img.save(page_jpg_path, "JPEG")
        
        pages.append(page_img)
        print(f"Generated Page {page_num} (shows page {page_num_str}). Saved JPG page to {page_jpg_path}")
        
    # Compile PDF
    if pages:
        pages[0].save(output_pdf_name, save_all=True, append_images=pages[1:])
        print(f"Successfully compiled {len(pages)} pages into PDF: {output_pdf_name}")
    else:
        print("Error: No pages to compile.")

# Compile both catalogs
generate_pdf("home-care", "catalogo-home-care.pdf")
generate_pdf("professional", "catalogo-profissional.pdf")
print("\nAll PDF catalogs compiled successfully!")
