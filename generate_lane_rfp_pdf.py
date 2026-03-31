from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_LEFT, TA_CENTER

# ── Color palette ──────────────────────────────────────────────────────────────
NAVY       = colors.HexColor('#0D1F3C')
NAVY_MID   = colors.HexColor('#1A3560')
ACCENT     = colors.HexColor('#2196F3')   # bright blue accent
ACCENT_LT  = colors.HexColor('#E3F2FD')   # very light blue tint for cards
GREEN      = colors.HexColor('#27AE60')
RED_MUTED  = colors.HexColor('#C0392B')
WHITE      = colors.white
LIGHT_GRAY = colors.HexColor('#F4F6F8')
MID_GRAY   = colors.HexColor('#BDC3C7')
TEXT_DARK  = colors.HexColor('#1A1A2E')
TEXT_MED   = colors.HexColor('#4A5568')

OUTPUT = r'C:\Users\Curt\Desktop\FreightAgent\Lane_RFP_Solutions.pdf'
W, H = letter   # 612 x 792


def draw_rounded_rect(c, x, y, w, h, r, fill_color, stroke_color=None, stroke_width=0.5):
    c.saveState()
    c.setFillColor(fill_color)
    if stroke_color:
        c.setStrokeColor(stroke_color)
        c.setLineWidth(stroke_width)
    else:
        c.setStrokeColor(fill_color)
        c.setLineWidth(0)
    p = c.beginPath()
    p.roundRect(x, y, w, h, r)
    c.drawPath(p, fill=1, stroke=1 if stroke_color else 0)
    c.restoreState()


def draw_text(c, text, x, y, font, size, color, align='left', max_width=None):
    c.saveState()
    c.setFont(font, size)
    c.setFillColor(color)
    if align == 'center':
        c.drawCentredString(x, y, text)
    elif align == 'right':
        c.drawRightString(x, y, text)
    else:
        if max_width:
            # simple word wrap — one paragraph object via canvas
            c.drawString(x, y, text)
        else:
            c.drawString(x, y, text)
    c.restoreState()


def wrapped_lines(c, text, font, size, max_w):
    """Return list of lines wrapping text within max_w."""
    words = text.split()
    lines = []
    current = ''
    c.setFont(font, size)
    for w in words:
        test = (current + ' ' + w).strip()
        if c.stringWidth(test, font, size) <= max_w:
            current = test
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines


def draw_wrapped(c, text, x, y, font, size, color, max_w, line_height=None):
    if line_height is None:
        line_height = size * 1.4
    lines = wrapped_lines(c, text, font, size, max_w)
    c.saveState()
    c.setFillColor(color)
    for i, line in enumerate(lines):
        c.setFont(font, size)
        c.drawString(x, y - i * line_height, line)
    c.restoreState()
    return y - (len(lines) - 1) * line_height   # returns bottom y


def bullet_item(c, text, x, y, font, size, color, max_w, bullet_color=None, lh=None):
    """Draw a bullet point with wrapped text; returns new y below last line."""
    if lh is None:
        lh = size * 1.45
    bx = x
    tx = x + 10
    c.saveState()
    c.setFillColor(bullet_color or color)
    c.setFont(font, size)
    c.drawString(bx, y, '\u2022')
    c.restoreState()
    bottom = draw_wrapped(c, text, tx, y, font, size, color, max_w - 10, lh)
    lines = wrapped_lines(c, text, font, size, max_w - 10)
    return y - len(lines) * lh


def generate():
    c = canvas.Canvas(OUTPUT, pagesize=letter)
    c.setTitle('Lane RFP Solutions')

    # ── Full-page navy background ──────────────────────────────────────────────
    c.setFillColor(NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # ── Top header band ────────────────────────────────────────────────────────
    header_h = 82
    header_y = H - header_h
    c.setFillColor(NAVY_MID)
    c.rect(0, header_y, W, header_h, fill=1, stroke=0)

    # Accent bar at very top
    c.setFillColor(ACCENT)
    c.rect(0, H - 5, W, 5, fill=1, stroke=0)

    # Header text
    draw_text(c, 'Lane RFP Solutions', W / 2, H - 38, 'Helvetica-Bold', 26, WHITE, 'center')
    draw_text(c, 'Streamline Your Freight Bid Process', W / 2, H - 58, 'Helvetica', 12, MID_GRAY, 'center')

    # Thin accent underline beneath subtitle
    ul_w = 160
    c.setFillColor(ACCENT)
    c.rect((W - ul_w) / 2, H - 64, ul_w, 2, fill=1, stroke=0)

    # ── Section label: Solution Tiers ──────────────────────────────────────────
    draw_text(c, 'CHOOSE YOUR SOLUTION TIER', W / 2, header_y - 18, 'Helvetica-Bold', 8, ACCENT, 'center')

    # ── Three tier cards ───────────────────────────────────────────────────────
    margin = 22
    gap = 10
    card_w = (W - 2 * margin - 2 * gap) / 3
    card_top = header_y - 28
    card_bottom = 198      # leave room for before/after + footer
    card_h = card_top - card_bottom

    tiers = [
        {
            'label': 'OPTION 1',
            'title': 'Bid Consolidator Tool',
            'price': '',
            'tag': 'STARTER',
            'tag_color': colors.HexColor('#27AE60'),
            'features': [
                'Upload all carrier response spreadsheets',
                'Auto-harmonizes & compares rates across all carriers for every lane',
                'Picks lowest rate per lane, tags the winning carrier',
                'Applies custom markup percentage',
                'Outputs final client-ready spreadsheet',
            ],
            'benefit': 'Saves 4-6 hours per project on manual comparison',
        },
        {
            'label': 'OPTION 2',
            'title': 'Bid Automation Suite',
            'price': '',
            'tag': 'POPULAR',
            'tag_color': ACCENT,
            'features': [
                'Everything in Option 1, PLUS:',
                'Automated carrier outreach \u2014 one click sends RFP via email/text',
                'Monitors inbox & auto-collects returned spreadsheets',
                'Dashboard: who responded, who hasn\'t, response deadlines',
            ],
            'benefit': 'End-to-end automation from client request to final deliverable',
        },
        {
            'label': 'OPTION 3',
            'title': 'Full Lane RFP Agent',
            'price': '',
            'tag': 'ENTERPRISE',
            'tag_color': colors.HexColor('#8E44AD'),
            'features': [
                'Everything in Option 2, PLUS:',
                'AI rate analysis \u2014 flags outliers, suggests negotiation opportunities',
                'Historical rate tracking vs. past projects',
                'Client portal \u2014 branded submission & results interface',
                'Carrier performance scoring: pricing, reliability, on-time trends',
            ],
            'benefit': 'Turns your bid desk into a competitive advantage',
        },
    ]

    for i, tier in enumerate(tiers):
        cx = margin + i * (card_w + gap)
        cy = card_bottom

        # Card shadow (offset rect)
        draw_rounded_rect(c, cx + 3, cy - 3, card_w, card_h, 6,
                          colors.HexColor('#060F1E'))

        # Card body
        draw_rounded_rect(c, cx, cy, card_w, card_h, 6, WHITE)

        # Colored top stripe on card
        stripe_h = 5
        c.saveState()
        c.setFillColor(tier['tag_color'])
        # clip to top of rounded rect
        p = c.beginPath()
        p.roundRect(cx, cy + card_h - stripe_h, card_w, stripe_h + 6, 3)
        c.clipPath(p, stroke=0)
        c.rect(cx, cy + card_h - stripe_h, card_w, stripe_h, fill=1, stroke=0)
        c.restoreState()

        inner_x = cx + 10
        inner_w = card_w - 20
        y_cursor = cy + card_h - 14

        # Tag pill
        tag_text = tier['tag']
        tag_tw = c.stringWidth(tag_text, 'Helvetica-Bold', 6.5) + 10
        draw_rounded_rect(c, inner_x, y_cursor - 8, tag_tw, 12, 3, tier['tag_color'])
        draw_text(c, tag_text, inner_x + tag_tw / 2, y_cursor - 3, 'Helvetica-Bold', 6.5, WHITE, 'center')
        y_cursor -= 18

        # Option label
        draw_text(c, tier['label'], inner_x, y_cursor, 'Helvetica-Bold', 7, TEXT_MED)
        y_cursor -= 13

        # Title
        title_lines = wrapped_lines(c, tier['title'], 'Helvetica-Bold', 11, inner_w)
        c.saveState()
        c.setFillColor(TEXT_DARK)
        for tl in title_lines:
            c.setFont('Helvetica-Bold', 11)
            c.drawString(inner_x, y_cursor, tl)
            y_cursor -= 14
        c.restoreState()

        # Price (skip if empty)
        if tier['price']:
            draw_text(c, tier['price'], inner_x, y_cursor, 'Helvetica-Bold', 15, tier['tag_color'])
            y_cursor -= 7

        # Divider
        c.setStrokeColor(MID_GRAY)
        c.setLineWidth(0.5)
        c.line(inner_x, y_cursor, inner_x + inner_w, y_cursor)
        y_cursor -= 10

        # Features
        for feat in tier['features']:
            y_cursor = bullet_item(c, feat, inner_x, y_cursor, 'Helvetica', 7.2,
                                   TEXT_DARK, inner_w, bullet_color=tier['tag_color'], lh=10.5)
            y_cursor -= 2

        # Benefit box at bottom of card
        benefit_pad = 6
        benefit_lines = wrapped_lines(c, tier['benefit'], 'Helvetica-Oblique', 7, inner_w - benefit_pad * 2)
        benefit_h = len(benefit_lines) * 10 + benefit_pad * 2
        benefit_y = cy + 8
        draw_rounded_rect(c, inner_x, benefit_y, inner_w, benefit_h, 4, ACCENT_LT,
                          stroke_color=ACCENT, stroke_width=0.6)
        draw_text(c, 'BENEFIT', inner_x + benefit_pad, benefit_y + benefit_h - benefit_pad - 1,
                  'Helvetica-Bold', 6, ACCENT)
        by = benefit_y + benefit_h - benefit_pad - 10
        c.saveState()
        c.setFillColor(TEXT_DARK)
        for bl in benefit_lines:
            c.setFont('Helvetica-Oblique', 7)
            c.drawString(inner_x + benefit_pad, by, bl)
            by -= 10
        c.restoreState()

    # ── Before / After section ─────────────────────────────────────────────────
    ba_top = 190
    ba_h = 118
    ba_y = ba_top - ba_h
    label_y = ba_top - 12

    draw_text(c, 'SEE THE DIFFERENCE', W / 2, ba_top + 5, 'Helvetica-Bold', 8, ACCENT, 'center')

    half_w = (W - 2 * margin - gap) / 2
    before_x = margin
    after_x = margin + half_w + gap

    # Before card
    draw_rounded_rect(c, before_x, ba_y, half_w, ba_h, 5,
                      colors.HexColor('#1C0A0A'), stroke_color=RED_MUTED, stroke_width=0.7)
    draw_text(c, 'BEFORE', before_x + half_w / 2, label_y, 'Helvetica-Bold', 9, RED_MUTED, 'center')

    before_items = [
        '4-6 hours manually comparing spreadsheets per project',
        'Copy-paste errors across 100-500 lanes',
        'No visibility into carrier response status',
        'No historical rate data',
    ]
    by2 = label_y - 14
    for item in before_items:
        by2 = bullet_item(c, item, before_x + 12, by2, 'Helvetica', 7.8,
                          colors.HexColor('#E8A8A8'), half_w - 22,
                          bullet_color=RED_MUTED, lh=11)
        by2 -= 3

    # After card
    draw_rounded_rect(c, after_x, ba_y, half_w, ba_h, 5,
                      colors.HexColor('#071C10'), stroke_color=GREEN, stroke_width=0.7)
    draw_text(c, 'AFTER', after_x + half_w / 2, label_y, 'Helvetica-Bold', 9, GREEN, 'center')

    after_items = [
        'Consolidation done in seconds',
        'Zero manual errors',
        'Real-time carrier response tracking',
        'Data-driven carrier selection',
    ]
    ay2 = label_y - 14
    for item in after_items:
        ay2 = bullet_item(c, item, after_x + 12, ay2, 'Helvetica', 7.8,
                          colors.HexColor('#A8E8BC'), half_w - 22,
                          bullet_color=GREEN, lh=11)
        ay2 -= 3

    # ── Footer ─────────────────────────────────────────────────────────────────
    footer_y = ba_y - 2
    c.setFillColor(NAVY_MID)
    c.rect(0, 0, W, footer_y, fill=1, stroke=0)

    c.setStrokeColor(ACCENT)
    c.setLineWidth(0.8)
    c.line(0, footer_y, W, footer_y)

    draw_text(c, 'Ready to automate your bid desk? Let\'s talk.',
              W / 2, footer_y - 14, 'Helvetica-Oblique', 8.5, MID_GRAY, 'center')

    # Bottom accent bar
    c.setFillColor(ACCENT)
    c.rect(0, 0, W, 4, fill=1, stroke=0)

    c.save()
    print(f'PDF written to: {OUTPUT}')


if __name__ == '__main__':
    generate()
