import os
from PIL import Image, ImageDraw, ImageFont

def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = " ".join(current_line + [word])
        if font.getlength(test_line) <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))
    return lines

def generate_image():
    width, height = 1024, 1024
    img = Image.new("RGB", (width, height), "#FFFFFF")
    draw = ImageDraw.Draw(img)

    font_dir = "/usr/share/fonts/truetype/dejavu/"
    font_bold_path = os.path.join(font_dir, "DejaVuSans-Bold.ttf")
    font_reg_path = os.path.join(font_dir, "DejaVuSans.ttf")

    f_masthead = ImageFont.truetype(font_bold_path, 36)
    f_date = ImageFont.truetype(font_bold_path, 15)
    f_h1 = ImageFont.truetype(font_bold_path, 14)
    f_b1 = ImageFont.truetype(font_reg_path, 11)
    f_h2 = ImageFont.truetype(font_bold_path, 12)
    f_b2 = ImageFont.truetype(font_reg_path, 10)
    f_tag = ImageFont.truetype(font_bold_path, 10)

    color_red = "#8B0000"
    color_navy = "#1C3B5E"
    color_text = "#1A1A1A"
    color_muted = "#555555"
    color_box_bg = "#F9F9F9"
    color_border = "#CCCCCC"

    # --- Masthead ---
    draw.rectangle([0, 0, width, 110], fill="#F4F4F4")
    draw.rectangle([0, 0, width, 6], fill=color_red)
    
    title_text = "THE WORLD IN ONE PAGE"
    title_w = f_masthead.getlength(title_text)
    draw.text(((width - title_w) / 2, 18), title_text, fill=color_red, font=f_masthead)

    draw.line([20, 62, width - 20, 62], fill=color_navy, width=2)
    date_text = "WEDNESDAY, 25 NOVEMBER 2026  |  GLOBAL NEWS BRIEFING & INTELLIGENCE"
    date_w = f_date.getlength(date_text)
    draw.text(((width - date_w) / 2, 72), date_text, fill=color_navy, font=f_date)
    draw.line([20, 96, width - 20, 96], fill=color_navy, width=1)

    col_w = 318
    gap = 15
    left_m = 20

    def get_col_x(c):
        return left_m + c * (col_w + gap)

    def draw_box(x, y, w, h, bg=color_box_bg, border=color_border):
        draw.rectangle([x, y, x + w, y + h], fill=bg, outline=border, width=1)

    def draw_story(x, y, w, h, tag, headline, body, f_h, f_b, has_pic=False, pic_type=None):
        draw_box(x, y, w, h)
        draw.rectangle([x, y, x + w, y + 20], fill=color_navy)
        draw.text((x + 8, y + 4), tag.upper(), fill="#FFFFFF", font=f_tag)

        content_x = x + 10
        content_w = w - 20
        text_y = y + 26

        if has_pic:
            pic_w = 90
            pic_h = 70
            pic_x = x + w - pic_w - 10
            pic_y = text_y + 4
            content_w = w - pic_w - 30
            
            draw.rectangle([pic_x, pic_y, pic_x + pic_w, pic_y + pic_h], fill="#FFFFFF", outline=color_navy, width=1)
            draw_pictogram(draw, pic_type, pic_x, pic_y, pic_w, pic_h)

        h_lines = wrap_text(headline, f_h, content_w)
        for line in h_lines[:2]:
            draw.text((content_x, text_y), line, fill=color_text, font=f_h)
            text_y += f_h.size + 2

        text_y += 3
        b_lines = wrap_text(body, f_b, content_w)
        max_b_y = y + h - 10
        for line in b_lines:
            if text_y + f_b.size > max_b_y:
                break
            draw.text((content_x, text_y), line, fill=color_muted, font=f_b)
            text_y += f_b.size + 2

    def draw_pictogram(draw, ptype, px, py, pw, ph):
        cx = px + pw / 2
        cy = py + ph / 2
        if ptype == "hormuz":
            draw.polygon([(cx - 30, cy + 10), (cx + 30, cy + 10), (cx + 22, cy + 24), (cx - 22, cy + 24)], fill=color_navy)
            draw.rectangle([cx - 10, cy - 2, cx + 10, cy + 10], fill=color_muted)
            draw.ellipse([cx + 15, cy - 15, cx + 35, cy + 5], fill=color_red)
            draw.line([cx - 25, cy - 10, cx - 15, cy - 20], fill=color_red, width=2)
        elif ptype == "houthi":
            draw.line([cx - 25, cy, cx + 25, cy], fill=color_navy, width=2)
            draw.line([cx, cy - 12, cx, cy + 12], fill=color_navy, width=2)
            draw.polygon([(cx - 12, cy - 12), (cx + 12, cy - 12), (cx, cy - 22)], fill=color_navy)
            draw.polygon([(cx - 15, cy + 22), (cx - 5, cy + 8), (cx + 5, cy + 15), (cx + 15, cy + 22)], fill=color_red)
        elif ptype == "russia":
            draw.rectangle([cx - 25, cy + 15, cx + 25, cy + 18], fill=color_navy)
            draw.rectangle([cx - 20, cy - 15, cx - 10, cy + 15], fill=color_red)
            draw.rectangle([cx - 5, cy - 5, cx + 5, cy + 15], fill=color_navy)
            draw.rectangle([cx + 10, cy - 20, cx + 20, cy + 15], fill=color_red)
        elif ptype == "space":
            draw.polygon([(cx, cy - 22), (cx - 8, cy + 12), (cx + 8, cy + 12)], fill=color_navy)
            draw.rectangle([cx - 3, cy + 12, cx + 3, cy + 20], fill=color_red)
            draw.ellipse([cx - 12, cy - 5, cx + 12, cy + 18], outline=color_muted)

    # Row 1
    lead_x = get_col_x(0)
    lead_w = col_w * 2 + gap
    draw_story(
        lead_x, 116, lead_w, 245,
        tag="LEAD · STRAIT OF HORMUZ",
        headline="TWO OIL TANKERS STRUCK BY NAVAL MINES & BURN IN HORMUZ",
        body="Iran's Revolutionary Guard Navy claims two oil tankers struck unauthorised naval mines and caught fire early Wednesday in the Strait of Hormuz. No vessels named and no independent confirmation. On Monday, Guard claimed three US-escorted tankers hit mines—also unverified.",
        f_h=f_h1, f_b=f_b1, has_pic=True, pic_type="hormuz"
    )

    col2_x = get_col_x(2)
    draw_story(
        col2_x, 116, col_w, 245,
        tag="MIDDLE EAST · CONFLICT",
        headline="HOUTHIS TARGET RAS TANURA REFINERY & RIYADH",
        body="Yemen's Houthis say they attacked Saudi Arabia's Ras Tanura oil refinery and Riyadh's financial district. Coalition intercepts 4 drones; 11 wounded Tuesday in Riyadh tower strike. Coalition strikes Hodeidah port.",
        f_h=f_h2, f_b=f_b2, has_pic=True, pic_type="houthi"
    )

    # Row 2
    row2_y = 371
    row2_h = 205
    draw_story(
        get_col_x(0), row2_y, col_w, row2_h,
        tag="RUSSIA · WAR CASUALTIES",
        headline="700,000 RUSSIAN CASUALTIES IN UKRAINE WAR",
        body="Leaked Rosstat data published Wednesday indicates at least 490,334 Russian soldiers dead since Feb 2022 (nearly 500k); counting missing, about 700,000. Putin vowed Tuesday to retaliate for refinery strikes.",
        f_h=f_h2, f_b=f_b2, has_pic=True, pic_type="russia"
    )

    draw_story(
        get_col_x(1), row2_y, col_w, row2_h,
        tag="SPACE · TIANGONG",
        headline="CHINA LAUNCHES SHENZHOU-24; FIRST PAKISTANI IN ORBIT",
        body="Launched Wednesday at 08:18 from Jiuquan and docked at Tiangong at 11:56. Muhammad Zeeshan Ali, 40, becomes first Pakistani in orbit and first foreign astronaut aboard Tiangong, flying with Tang Hongbo and Wu Yi.",
        f_h=f_h2, f_b=f_b2, has_pic=True, pic_type="space"
    )

    draw_story(
        get_col_x(2), row2_y, col_w, row2_h,
        tag="TECH · MARKETS",
        headline="HUAWEI GUILTY OF THEFT; NVIDIA SHARES FALL 7%",
        body="Huawei found guilty of stealing US trade secrets (acquitted of racketeering). Nvidia shares drop 7% as US AG dodges questions on Trump's role in Jensen Huang's return.",
        f_h=f_h2, f_b=f_b2, has_pic=False
    )

    # Row 3
    row3_y = 586
    row3_h = 190
    draw_story(
        get_col_x(0), row3_y, col_w, row3_h,
        tag="SPORT · FOOTBALL",
        headline="CAS REINSTATES SENEGAL AS 2025 AFCON WINNERS",
        body="Court of Arbitration for Sport unanimously reinstates Senegal as 2025 Africa Cup of Nations winners, confirming January's 1-0 extra-time win over Morocco.",
        f_h=f_h2, f_b=f_b2, has_pic=False
    )

    draw_story(
        get_col_x(1), row3_y, col_w, row3_h,
        tag="ECONOMY · MARKETS",
        headline="TARIFFS LOOM AS ASIAN STOCKS TUMBLE",
        body="Trump administration poised to unveil Section 301 tariffs on 16 trading partners. Asian stocks tumble: South Korea down 5.3%, Taiwan 5.1%, Nikkei 2.9%. Brent $90.97, Bitcoin $59,258.",
        f_h=f_h2, f_b=f_b2, has_pic=False
    )

    draw_story(
        get_col_x(2), row3_y, col_w, row3_h,
        tag="CHINA · POLITICS",
        headline="SHANGHAI PARTY CHIEF CHEN JINING PROBED",
        body="Anti-graft probe opens into Shanghai party chief Chen Jining, the fourth Politburo member investigated since 2025.",
        f_h=f_h2, f_b=f_b2, has_pic=False
    )

    # Row 4
    row4_y = 791
    row4_h = 215
    draw_story(
        get_col_x(0), row4_y, 490, row4_h,
        tag="COLOMBIA · SECURITY",
        headline="HOSTAGES FREED IN CARTAGENA SUPERMARKET; CAR BOMB INJURES 23",
        body="Armed men held dozens hostage in a Cartagena supermarket before all hostages were freed safely without casualties. A separate car bomb injures at least 23 people.",
        f_h=f_h2, f_b=f_b2, has_pic=False
    )

    draw_story(
        get_col_x(0) + 504, row4_y, 480, row4_h,
        tag="BANGLADESH · LABOR",
        headline="BANGLADESH TEXTILE MINIMUM WAGE RISES 36%",
        body="Bangladesh textile minimum wage rises 36% following weeks of widespread protests across manufacturing hubs.",
        f_h=f_h2, f_b=f_b2, has_pic=False
    )

    footer_text = "MAKE.FUN NEWS-IMAGE-20261125  •  VERIFIED WORLD NEWS SUMMARY  •  PRODUCED FOR BOUNTY"
    f_footer = ImageFont.truetype(font_reg_path, 9)
    fw = f_footer.getlength(footer_text)
    draw.text(((width - fw) / 2, 1008), footer_text, fill=color_muted, font=f_footer)

    output_path = "entry.png"
    img.save(output_path, "PNG")
    print(f"Generated {output_path} successfully.")

if __name__ == "__main__":
    generate_image()
