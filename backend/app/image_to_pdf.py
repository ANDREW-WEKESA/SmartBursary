"""
Image to PDF converter for National ID documents
Combines front and back images into a single PDF
"""
from io import BytesIO
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


def images_to_pdf(front_image_bytes: bytes, back_image_bytes: bytes) -> BytesIO:
    """
    Convert two images (front and back of ID) into a single PDF
    
    Args:
        front_image_bytes: Image bytes for front of ID
        back_image_bytes: Image bytes for back of ID
        
    Returns:
        BytesIO: PDF file as bytes buffer
    """
    # Create PDF buffer
    pdf_buffer = BytesIO()
    
    # Create canvas with A4 size
    c = canvas.Canvas(pdf_buffer, pagesize=A4)
    width, height = A4
    
    # Process front image
    front_img = Image.open(BytesIO(front_image_bytes))
    
    # Convert to RGB if necessary (handle PNG with transparency)
    if front_img.mode in ('RGBA', 'LA', 'P'):
        background = Image.new('RGB', front_img.size, (255, 255, 255))
        if front_img.mode == 'P':
            front_img = front_img.convert('RGBA')
        background.paste(front_img, mask=front_img.split()[-1] if front_img.mode == 'RGBA' else None)
        front_img = background
    
    # Calculate dimensions to fit on page with margin
    margin = 50
    available_width = width - (2 * margin)
    available_height = height - (2 * margin)
    
    # Scale image to fit
    img_width, img_height = front_img.size
    scale = min(available_width / img_width, available_height / img_height)
    scaled_width = img_width * scale
    scaled_height = img_height * scale
    
    # Center image on page
    x = (width - scaled_width) / 2
    y = (height - scaled_height) / 2
    
    # Add front image to first page
    front_buffer = BytesIO()
    front_img.save(front_buffer, format='JPEG', quality=85)
    front_buffer.seek(0)
    
    c.drawImage(ImageReader(front_buffer), x, y, width=scaled_width, height=scaled_height)
    
    # Add title
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width / 2, height - 30, "National ID - Front")
    
    # Start new page for back image
    c.showPage()
    
    # Process back image
    back_img = Image.open(BytesIO(back_image_bytes))
    
    # Convert to RGB if necessary
    if back_img.mode in ('RGBA', 'LA', 'P'):
        background = Image.new('RGB', back_img.size, (255, 255, 255))
        if back_img.mode == 'P':
            back_img = back_img.convert('RGBA')
        background.paste(back_img, mask=back_img.split()[-1] if back_img.mode == 'RGBA' else None)
        back_img = background
    
    # Scale back image
    img_width, img_height = back_img.size
    scale = min(available_width / img_width, available_height / img_height)
    scaled_width = img_width * scale
    scaled_height = img_height * scale
    
    # Center image on page
    x = (width - scaled_width) / 2
    y = (height - scaled_height) / 2
    
    # Add back image to second page
    back_buffer = BytesIO()
    back_img.save(back_buffer, format='JPEG', quality=85)
    back_buffer.seek(0)
    
    c.drawImage(ImageReader(back_buffer), x, y, width=scaled_width, height=scaled_height)
    
    # Add title
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width / 2, height - 30, "National ID - Back")
    
    # Save PDF
    c.save()
    
    # Return buffer
    pdf_buffer.seek(0)
    return pdf_buffer


def single_image_to_pdf(image_bytes: bytes, title: str = "Document") -> BytesIO:
    """
    Convert a single image into a PDF
    
    Args:
        image_bytes: Image bytes
        title: Document title
        
    Returns:
        BytesIO: PDF file as bytes buffer
    """
    # Create PDF buffer
    pdf_buffer = BytesIO()
    
    # Create canvas with A4 size
    c = canvas.Canvas(pdf_buffer, pagesize=A4)
    width, height = A4
    
    # Process image
    img = Image.open(BytesIO(image_bytes))
    
    # Convert to RGB if necessary
    if img.mode in ('RGBA', 'LA', 'P'):
        background = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'P':
            img = img.convert('RGBA')
        background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
        img = background
    
    # Calculate dimensions
    margin = 50
    available_width = width - (2 * margin)
    available_height = height - (2 * margin)
    
    # Scale image
    img_width, img_height = img.size
    scale = min(available_width / img_width, available_height / img_height)
    scaled_width = img_width * scale
    scaled_height = img_height * scale
    
    # Center image
    x = (width - scaled_width) / 2
    y = (height - scaled_height) / 2
    
    # Add image
    img_buffer = BytesIO()
    img.save(img_buffer, format='JPEG', quality=85)
    img_buffer.seek(0)
    
    c.drawImage(ImageReader(img_buffer), x, y, width=scaled_width, height=scaled_height)
    
    # Add title
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width / 2, height - 30, title)
    
    # Save PDF
    c.save()
    
    # Return buffer
    pdf_buffer.seek(0)
    return pdf_buffer
