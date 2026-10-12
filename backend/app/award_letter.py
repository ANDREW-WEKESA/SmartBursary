"""
Generate bursary award letter/voucher PDF
Students can download and print to take to their school
"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from io import BytesIO
from datetime import datetime


def generate_award_letter(
    application_number: str,
    applicant_name: str,
    national_id: str,
    institution: str,
    course: str,
    year_of_study: int,
    bursary_name: str,
    amount: float,
    constituency: str = None,
    approved_date: str = None
) -> BytesIO:
    """
    Generate a professional bursary award letter PDF
    
    Returns:
        BytesIO: PDF file buffer
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, 
                           rightMargin=0.75*inch, leftMargin=0.75*inch,
                           topMargin=0.75*inch, bottomMargin=0.75*inch)
    
    # Container for content
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1a472a'),
        alignment=TA_CENTER,
        spaceAfter=12
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1a472a'),
        spaceAfter=10
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        leading=16
    )
    
    # Header - Government Logo placeholder and title
    header_data = [[
        Paragraph('<b>REPUBLIC OF KENYA</b><br/><font size=10>NATIONAL GOVERNMENT CONSTITUENCY DEVELOPMENT FUND</font>', 
                 ParagraphStyle('header', parent=styles['Normal'], alignment=TA_CENTER, fontSize=12))
    ]]
    
    header_table = Table(header_data, colWidths=[6.5*inch])
    header_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#1a472a')),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Title
    if constituency:
        elements.append(Paragraph(f'<b>{constituency.upper()} CONSTITUENCY</b>', title_style))
    elements.append(Paragraph('<b>BURSARY AWARD LETTER</b>', title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Reference number and date
    ref_date = approved_date or datetime.now().strftime('%d %B %Y')
    elements.append(Paragraph(f'<b>Ref No:</b> {application_number}', normal_style))
    elements.append(Paragraph(f'<b>Date:</b> {ref_date}', normal_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Recipient details
    elements.append(Paragraph('<b>TO WHOM IT MAY CONCERN</b>', heading_style))
    elements.append(Spacer(1, 0.15*inch))
    
    # Award details table
    details_data = [
        ['Student Name:', applicant_name.upper()],
        ['National ID/Birth Certificate:', national_id],
        ['Institution:', institution],
        ['Course of Study:', course],
        ['Year of Study:', f'Year {year_of_study}'],
        ['Bursary Program:', bursary_name],
        ['Award Amount:', f'<b>KES {amount:,.2f}</b>']
    ]
    
    details_table = Table(details_data, colWidths=[2.2*inch, 4.3*inch])
    details_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#1a472a')),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#1a472a')),
    ]))
    elements.append(details_table)
    elements.append(Spacer(1, 0.25*inch))
    
    # Award statement
    award_text = f"""
    This is to certify that the above-named student has been awarded a bursary of 
    <b>KES {amount:,.2f}</b> from the {bursary_name} for the academic year {datetime.now().year}/{datetime.now().year + 1}.
    """
    elements.append(Paragraph(award_text, normal_style))
    elements.append(Spacer(1, 0.15*inch))
    
    # Instructions
    instructions_text = """
    <b>INSTRUCTIONS TO THE INSTITUTION:</b><br/>
    Please acknowledge receipt of this award letter and confirm the student's enrollment. 
    The bursary amount should be credited directly to the student's fee account. 
    Kindly provide a fee balance statement for our records.
    """
    elements.append(Paragraph(instructions_text, normal_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Signature section
    signature_data = [
        ['', ''],
        ['_' * 40, '_' * 40],
        ['<b>Authorized by:</b><br/>CDF Committee Chairperson', '<b>Approved by:</b><br/>Constituency Development Fund Officer']
    ]
    
    signature_table = Table(signature_data, colWidths=[3.25*inch, 3.25*inch])
    signature_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTSIZE', (0, 2), (-1, 2), 9),
    ]))
    elements.append(signature_table)
    elements.append(Spacer(1, 0.2*inch))
    
    # Footer
    footer_text = """
    <font size=8>
    <b>IMPORTANT NOTICE:</b> This is an official bursary award letter from the National Government 
    Constituency Development Fund. It should be presented to the institution along with other enrollment documents. 
    For verification, contact the CDF office or check application status at smart-bursary.vercel.app
    </font>
    """
    elements.append(Paragraph(footer_text, 
                             ParagraphStyle('footer', parent=styles['Normal'], 
                                          fontSize=8, textColor=colors.grey, 
                                          alignment=TA_CENTER)))
    
    # Watermark
    elements.append(Spacer(1, 0.1*inch))
    watermark_text = f'<font size=8 color="grey">Generated on {datetime.now().strftime("%Y-%m-%d %H:%M")} | Application: {application_number}</font>'
    elements.append(Paragraph(watermark_text, 
                             ParagraphStyle('watermark', parent=styles['Normal'], 
                                          fontSize=8, textColor=colors.lightgrey, 
                                          alignment=TA_CENTER)))
    
    # Build PDF
    doc.build(elements)
    
    buffer.seek(0)
    return buffer
