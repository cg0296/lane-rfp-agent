from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfgen import canvas

# Colors
DARK_BLUE = HexColor('#1a2744')
MED_BLUE = HexColor('#2c5282')
LIGHT_BLUE = HexColor('#ebf4ff')
ACCENT_GREEN = HexColor('#276749')
LIGHT_GREEN = HexColor('#f0fff4')
ACCENT_ORANGE = HexColor('#c05621')
LIGHT_ORANGE = HexColor('#fffaf0')
GRAY = HexColor('#718096')
LIGHT_GRAY = HexColor('#f7fafc')
BORDER_GRAY = HexColor('#e2e8f0')

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        if self._pageNumber > 1:
            self.setFont("Helvetica", 8)
            self.setFillColor(GRAY)
            self.drawRightString(
                letter[0] - 0.75 * inch,
                0.5 * inch,
                f"Page {self._pageNumber - 1} of {page_count - 1}"
            )
            self.drawString(
                0.75 * inch,
                0.5 * inch,
                "Lane RFP Agent  |  Confidential"
            )


def build_pdf():
    doc = SimpleDocTemplate(
        "C:/Users/Curt/Desktop/FreightAgent/Lane_RFP_Agent_Proposal.pdf",
        pagesize=letter,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=32,
        textColor=DARK_BLUE,
        spaceAfter=6,
        fontName='Helvetica-Bold',
        alignment=TA_CENTER,
    )

    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=14,
        textColor=GRAY,
        spaceAfter=30,
        fontName='Helvetica',
        alignment=TA_CENTER,
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=DARK_BLUE,
        spaceBefore=20,
        spaceAfter=12,
        fontName='Helvetica-Bold',
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=MED_BLUE,
        spaceBefore=16,
        spaceAfter=8,
        fontName='Helvetica-Bold',
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=11,
        textColor=HexColor('#2d3748'),
        spaceAfter=8,
        fontName='Helvetica',
        leading=16,
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=20,
        bulletIndent=8,
        spaceAfter=4,
    )

    checkpoint_style = ParagraphStyle(
        'Checkpoint',
        parent=body_style,
        fontSize=10,
        textColor=ACCENT_ORANGE,
        fontName='Helvetica-BoldOblique',
        leftIndent=20,
    )

    center_style = ParagraphStyle(
        'Center',
        parent=body_style,
        alignment=TA_CENTER,
    )

    story = []

    # ─── TITLE PAGE ───
    story.append(Spacer(1, 2 * inch))
    story.append(Paragraph("Lane RFP Agent", title_style))
    story.append(Spacer(1, 8))

    # Divider line
    divider_data = [['', '', '']]
    divider_table = Table(divider_data, colWidths=[2.5 * inch, 2 * inch, 2.5 * inch])
    divider_table.setStyle(TableStyle([
        ('LINEBELOW', (1, 0), (1, 0), 2, MED_BLUE),
    ]))
    story.append(divider_table)
    story.append(Spacer(1, 12))

    story.append(Paragraph("Automated Carrier Rate Collection & Comparison", subtitle_style))
    story.append(Spacer(1, 1.5 * inch))

    # Info box
    info_data = [
        ['Prepared by', 'Golden Tech Solutions'],
        ['Date', 'March 30, 2026'],
        ['Version', '1.0 - High Level Overview'],
        ['Classification', 'Confidential'],
    ]
    info_table = Table(info_data, colWidths=[1.8 * inch, 3 * inch])
    info_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (0, -1), GRAY),
        ('TEXTCOLOR', (1, 0), (1, -1), DARK_BLUE),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('LINEBELOW', (0, 0), (-1, -2), 0.5, BORDER_GRAY),
    ]))
    story.append(info_table)

    story.append(PageBreak())

    # ─── THE PROBLEM ───
    story.append(Paragraph("The Problem", h1_style))
    story.append(Paragraph(
        "Managing freight lane RFPs is a manual, time-intensive process. When a client sends a "
        "spreadsheet with hundreds of lanes to quote, your team must:",
        body_style
    ))

    problems = [
        "Manually email the spreadsheet to multiple carriers",
        "Wait for each carrier to respond with their rates",
        "Open and compare multiple returned spreadsheets side by side",
        "Identify the lowest rate for each individual lane across all carrier responses",
        "Apply a standard markup to every winning rate",
        "Compile the final spreadsheet with carrier assignments and marked-up rates",
        "Send the completed spreadsheet back to the client",
    ]
    for p in problems:
        story.append(Paragraph(f"<bullet>&bull;</bullet> {p}", bullet_style))

    story.append(Spacer(1, 12))

    # Pain point box
    pain_data = [[Paragraph(
        "<b>The core bottleneck:</b> Consolidating responses from multiple carriers across "
        "100-500 lanes per project, repeated multiple times per week. "
        "This is where the majority of manual hours are spent.",
        ParagraphStyle('PainBody', parent=body_style, textColor=ACCENT_ORANGE, fontSize=11)
    )]]
    pain_table = Table(pain_data, colWidths=[6.5 * inch])
    pain_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), LIGHT_ORANGE),
        ('BOX', (0, 0), (-1, -1), 1, ACCENT_ORANGE),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
    ]))
    story.append(pain_table)

    story.append(PageBreak())

    # ─── THE SOLUTION ───
    story.append(Paragraph("The Solution: Lane RFP Agent", h1_style))
    story.append(Paragraph(
        "An intelligent agent that automates the carrier rate collection and comparison process "
        "while keeping your team in full control at every step.",
        body_style
    ))
    story.append(Spacer(1, 8))

    # Key principles box
    principles_data = [[Paragraph(
        "<b>Key Principles</b><br/><br/>"
        "&#8226; <b>Human-in-the-loop:</b> Your team reviews and approves at every stage<br/>"
        "&#8226; <b>Transparent:</b> Full visibility into what the agent is doing<br/>"
        "&#8226; <b>Flexible:</b> Override any automated decision at any time<br/>"
        "&#8226; <b>Secure:</b> All communication stays within your existing email workflows",
        ParagraphStyle('PrincipleBody', parent=body_style, textColor=ACCENT_GREEN, fontSize=11)
    )]]
    principles_table = Table(principles_data, colWidths=[6.5 * inch])
    principles_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), LIGHT_GREEN),
        ('BOX', (0, 0), (-1, -1), 1, ACCENT_GREEN),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
    ]))
    story.append(principles_table)

    story.append(PageBreak())

    # ─── WORKFLOW OVERVIEW ───
    story.append(Paragraph("Workflow Overview", h1_style))
    story.append(Spacer(1, 8))

    # Flow diagram as styled table
    flow_steps = [
        ("1", "INGEST", "Client spreadsheet arrives via email"),
        ("", "CHECKPOINT", "Review parsed spreadsheet before proceeding"),
        ("2", "DISTRIBUTE", "Agent emails spreadsheet to carrier list"),
        ("", "CHECKPOINT", "Review carrier list and email before sending"),
        ("3", "COLLECT", "Agent monitors inbox for carrier responses"),
        ("", "CHECKPOINT", "View response dashboard, decide when to stop waiting"),
        ("4", "CONSOLIDATE", "Agent compares all rates, picks lowest per lane"),
        ("", "CHECKPOINT", "Review comparison, override any picks"),
        ("5", "DELIVER", "Agent applies markup and generates final spreadsheet"),
        ("", "CHECKPOINT", "Final review before sending to client"),
    ]

    flow_data = []
    for step_num, label, desc in flow_steps:
        if label == "CHECKPOINT":
            flow_data.append([
                '',
                Paragraph(f"<font color='#c05621'><b>CHECKPOINT</b></font>",
                          ParagraphStyle('FlowCP', parent=body_style, fontSize=9, alignment=TA_CENTER)),
                Paragraph(f"<font color='#c05621'>{desc}</font>",
                          ParagraphStyle('FlowCPDesc', parent=body_style, fontSize=9, textColor=ACCENT_ORANGE)),
            ])
        else:
            flow_data.append([
                Paragraph(f"<font color='white'><b>{step_num}</b></font>",
                          ParagraphStyle('StepNum', parent=body_style, fontSize=14, alignment=TA_CENTER, textColor=white)),
                Paragraph(f"<b>{label}</b>",
                          ParagraphStyle('StepLabel', parent=body_style, fontSize=11, alignment=TA_CENTER)),
                Paragraph(desc, body_style),
            ])

    flow_table = Table(flow_data, colWidths=[0.6 * inch, 1.4 * inch, 4.5 * inch])
    flow_style = [
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]

    for i, (step_num, label, _) in enumerate(flow_steps):
        if label == "CHECKPOINT":
            flow_style.append(('BACKGROUND', (0, i), (-1, i), LIGHT_ORANGE))
            flow_style.append(('LINEBELOW', (0, i), (-1, i), 0.5, BORDER_GRAY))
        else:
            flow_style.append(('BACKGROUND', (0, i), (0, i), MED_BLUE))
            flow_style.append(('BACKGROUND', (1, i), (-1, i), LIGHT_BLUE))
            flow_style.append(('LINEBELOW', (0, i), (-1, i), 0.5, BORDER_GRAY))

    flow_table.setStyle(TableStyle(flow_style))
    story.append(flow_table)

    story.append(PageBreak())

    # ─── DETAILED STEPS ───
    steps = [
        {
            "num": "1",
            "title": "Step 1: Ingest",
            "subtitle": "Client Spreadsheet Intake",
            "desc": "When a client sends a spreadsheet with lanes to quote, the agent automatically detects and parses it.",
            "details": [
                "Detects incoming client spreadsheet via email",
                "Parses the Excel file and identifies key columns: pickup location, delivery location, number of skids, and weight",
                "Ignores extraneous columns that aren't relevant to the quoting process",
                "Validates data completeness - flags any lanes with missing information",
                "Presents a clean summary of the parsed data for review",
            ],
            "checkpoint": "Your team reviews the parsed spreadsheet to confirm it was read correctly and all lanes are accounted for before moving forward.",
        },
        {
            "num": "2",
            "title": "Step 2: Distribute",
            "subtitle": "Carrier Outreach",
            "desc": "The agent prepares and sends the spreadsheet to your preferred carrier list.",
            "details": [
                "Pulls from your configured list of preferred carriers",
                "Drafts a professional email to each carrier with the spreadsheet attached",
                "Each carrier receives the same standardized spreadsheet format",
                "Emails are sent from your existing email account - carriers see communication from you, not a bot",
                "Tracks which carriers have been contacted and when",
            ],
            "checkpoint": "Your team reviews the carrier list and previews the email before anything is sent. You can add or remove carriers, or edit the message.",
        },
        {
            "num": "3",
            "title": "Step 3: Collect",
            "subtitle": "Response Monitoring",
            "desc": "The agent monitors your inbox for carrier responses and tracks who has replied.",
            "details": [
                "Monitors incoming email for carrier responses with attached spreadsheets",
                "Parses each returned spreadsheet to extract the carrier's rates per lane",
                "Handles variations in how carriers fill out the spreadsheet",
                "Builds a real-time dashboard showing: who has responded, who hasn't, and when each response came in",
                "Can send follow-up reminders to carriers who haven't responded after a configurable time window",
            ],
            "checkpoint": "Your team can view the response dashboard at any time. You decide when enough carriers have responded and trigger the next step - no arbitrary deadlines.",
        },
        {
            "num": "4",
            "title": "Step 4: Consolidate",
            "subtitle": "Rate Comparison & Carrier Selection",
            "desc": "This is where the heavy lifting happens. The agent builds a complete comparison matrix across all carriers and lanes.",
            "details": [
                "Creates a master comparison: every lane mapped against every carrier's quoted rate",
                "Identifies the lowest rate for each lane automatically",
                "Tags the winning carrier for each lane",
                "Flags any lanes where no carrier provided a rate",
                "Highlights lanes where rates are unusually close or where a secondary carrier might be preferred",
                "Generates a clear, sortable comparison view",
            ],
            "checkpoint": "Your team reviews the full comparison matrix and can override any selection. If you prefer a specific carrier for certain lanes - for any reason - you can make that change before proceeding.",
        },
        {
            "num": "5",
            "title": "Step 5: Deliver",
            "subtitle": "Final Spreadsheet Generation",
            "desc": "The agent applies the standard markup and generates the client-ready spreadsheet.",
            "details": [
                "Applies the 15% markup to each winning carrier's rate",
                "Populates the carrier name and marked-up rate into the original spreadsheet format",
                "Preserves the client's original formatting and any additional columns",
                "Generates the final Excel file ready for delivery",
                "Drafts a response email to the client with the completed spreadsheet attached",
            ],
            "checkpoint": "Your team does a final review of the completed spreadsheet and the draft email before it goes back to the client. Nothing leaves without your approval.",
        },
    ]

    story.append(Paragraph("Detailed Workflow", h1_style))
    story.append(Spacer(1, 8))

    for step in steps:
        step_content = []
        step_content.append(Paragraph(step["title"], h2_style))
        step_content.append(Paragraph(f"<i>{step['subtitle']}</i>",
                                       ParagraphStyle('StepSub', parent=body_style, textColor=GRAY, fontSize=10)))
        step_content.append(Spacer(1, 4))
        step_content.append(Paragraph(step["desc"], body_style))
        step_content.append(Spacer(1, 4))

        for detail in step["details"]:
            step_content.append(Paragraph(f"<bullet>&bull;</bullet> {detail}", bullet_style))

        step_content.append(Spacer(1, 8))

        # Checkpoint box
        cp_data = [[Paragraph(
            f"<b>CHECKPOINT:</b> {step['checkpoint']}",
            ParagraphStyle('CPBody', parent=body_style, textColor=ACCENT_ORANGE, fontSize=10)
        )]]
        cp_table = Table(cp_data, colWidths=[6.5 * inch])
        cp_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), LIGHT_ORANGE),
            ('BOX', (0, 0), (-1, -1), 1, ACCENT_ORANGE),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ]))
        step_content.append(cp_table)
        step_content.append(Spacer(1, 16))

        story.append(KeepTogether(step_content))

    story.append(PageBreak())

    # ─── WHAT CHANGES / WHAT DOESN'T ───
    story.append(Paragraph("What Changes vs. What Stays the Same", h1_style))
    story.append(Spacer(1, 12))

    compare_header = [
        Paragraph("<b>What Changes</b>", ParagraphStyle('CompHead', parent=body_style, textColor=white, fontSize=12, alignment=TA_CENTER)),
        Paragraph("<b>What Stays the Same</b>", ParagraphStyle('CompHead', parent=body_style, textColor=white, fontSize=12, alignment=TA_CENTER)),
    ]

    changes = [
        "Manual emailing to each carrier",
        "Opening and comparing multiple spreadsheets",
        "Searching row by row for the lowest rate",
        "Manually calculating markups",
        "Re-typing rates into the final spreadsheet",
    ]

    stays = [
        "Your carrier relationships",
        "Your team reviews everything before it goes out",
        "Clients see communication from you, not a system",
        "You choose which carriers to use",
        "You control the markup and final pricing",
    ]

    compare_data = [compare_header]
    for i in range(max(len(changes), len(stays))):
        change = changes[i] if i < len(changes) else ""
        stay = stays[i] if i < len(stays) else ""
        compare_data.append([
            Paragraph(f"<bullet>&bull;</bullet> {change}", ParagraphStyle('CompItem', parent=bullet_style, fontSize=10)),
            Paragraph(f"<bullet>&bull;</bullet> {stay}", ParagraphStyle('CompItem', parent=bullet_style, fontSize=10)),
        ])

    compare_table = Table(compare_data, colWidths=[3.25 * inch, 3.25 * inch])
    compare_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), ACCENT_GREEN),
        ('BACKGROUND', (1, 0), (1, 0), MED_BLUE),
        ('BACKGROUND', (0, 1), (0, -1), LIGHT_GREEN),
        ('BACKGROUND', (1, 1), (1, -1), LIGHT_BLUE),
        ('BOX', (0, 0), (-1, -1), 1, BORDER_GRAY),
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, BORDER_GRAY),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_GRAY),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(compare_table)

    story.append(PageBreak())

    # ─── NEXT STEPS ───
    story.append(Paragraph("Next Steps", h1_style))
    story.append(Spacer(1, 12))

    next_steps = [
        ("1", "Align on Workflow", "Review this proposal and confirm the workflow matches your process. Flag any steps that need adjustment."),
        ("2", "Sample Data", "Provide a sample client spreadsheet (can be anonymized) so we can validate the parsing logic against real-world formatting."),
        ("3", "Carrier List", "Share your preferred carrier list and email contacts so we can configure the distribution step."),
        ("4", "Pilot Run", "We'll run the agent against one real project in parallel with your existing process to validate accuracy."),
        ("5", "Go Live", "Once validated, the agent handles the heavy lifting and your team focuses on oversight and client relationships."),
    ]

    for num, title, desc in next_steps:
        ns_data = [[
            Paragraph(f"<font color='white'><b>{num}</b></font>",
                      ParagraphStyle('NSNum', parent=body_style, fontSize=14, alignment=TA_CENTER, textColor=white)),
            Paragraph(f"<b>{title}</b><br/>{desc}", body_style),
        ]]
        ns_table = Table(ns_data, colWidths=[0.6 * inch, 5.9 * inch])
        ns_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), MED_BLUE),
            ('BACKGROUND', (1, 0), (1, 0), LIGHT_BLUE),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('BOX', (0, 0), (-1, -1), 0.5, BORDER_GRAY),
        ]))
        story.append(ns_table)
        story.append(Spacer(1, 8))

    # Build
    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF generated: Lane_RFP_Agent_Proposal.pdf")


if __name__ == "__main__":
    build_pdf()
