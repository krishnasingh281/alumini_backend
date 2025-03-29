from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from io import BytesIO
from .models import AlumniProfile  # Import your Alumni model

def generate_alumni_pdf():
    """Creates a PDF with alumni details in a tabular format."""
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter)

    alumni = AlumniProfile.objects.all()

    data = [["Name", "Batch", "Job Title", "Company"]]

    for alum in alumni:
        alum_name = alum.user.get_full_name() if alum.user.get_full_name() else alum.user.username  # ✅ FIXED!
        data.append([
            alum_name,
            str(alum.graduation_year),
            alum.job_title if alum.job_title else "N/A",
            alum.current_company if alum.current_company else "N/A"
        ])

    table = Table(data, colWidths=[150, 80, 120, 120])

    style = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 12),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ])

    table.setStyle(style)

    pdf.build([table])

    buffer.seek(0)
    return buffer
