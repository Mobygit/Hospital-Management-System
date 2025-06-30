from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Laboratory
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from io import BytesIO
from django.core.files.base import ContentFile
from django.conf import settings
import os

@receiver(post_save, sender=Laboratory)
def generate_pdf_report(sender, instance, created, **kwargs):
    if instance.status == 'Done' and not instance.report_file:
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        # --- Draw top section: Logo + MobyCare + Lab Report Title ---

        # Logo path (adjust if needed)
        logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/logo/logo.png')

        # Logo size
        logo_width = 1.0 * inch
        logo_height = 1.0 * inch

        # Logo position (top-right corner)
        logo_x = width - inch - logo_width
        logo_y = height - inch

        try:
            # Draw the logo
            p.drawImage(logo_path, logo_x, logo_y, width=logo_width, height=logo_height, preserveAspectRatio=True, mask='auto')

            # # Draw "MobyCare" text next to the logo
            # text_x = logo_x + logo_width + 0.1 * inch  # space beside logo
            # text_y = logo_y + (logo_height / 2) - 6    # vertically centered with logo

            # p.setFont("Helvetica-Bold", 14)
            # p.setFillColor(colors.darkblue)
            # p.drawString(text_x, text_y, "MobyCare")
            # p.setFillColor(colors.black)  # Reset for rest of document

        except Exception as e:
            print(f"Error loading/drawing logo: {e}")

        # Title on top-left
        p.setFont("Helvetica-Bold", 18)
        p.drawString(inch, height - inch * 1.5, "Lab Report")

        # --- Patient Details ---
        p.setFont("Helvetica", 12)
        p.drawString(inch, height - inch * 2, f"Patient Name: {instance.patient.First_name} {instance.patient.Last_name}")
        p.drawString(inch, height - inch * 2.25, f"Appointment Date: {instance.appointment_date.strftime('%Y-%m-%d')}")
        p.drawString(inch, height - inch * 2.5, f"Mobile: {instance.mobile}")

        # Divider Line
        p.setStrokeColor(colors.grey)
        p.setLineWidth(0.5)
        p.line(inch, height - inch * 2.75, width - inch, height - inch * 2.75)

        # --- Test Results Table ---
        tests = [test.name for test in instance.tests.all()]
        data = [['Test Name', 'Result']]
        for test_name in tests:
            data.append([test_name, instance.result or "Pending"])

        table = Table(data, colWidths=[3*inch, 3*inch])
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])
        table.setStyle(style)

        # Draw table below patient info
        table.wrapOn(p, width, height)
        table.drawOn(p, inch, height - inch * 5)

        # Footer
        p.setFont("Helvetica-Oblique", 10)
        p.drawString(inch, inch, "This is a computer-generated report. For any inquiries, contact support@example.com")

        # Finalize PDF
        p.showPage()
        p.save()

        pdf = buffer.getvalue()
        buffer.close()

        # Save to model field
        instance.report_file.save(f"lab_report_{instance.id}.pdf", ContentFile(pdf))
        instance.save()




# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Laboratory
# from reportlab.lib.pagesizes import letter
# from reportlab.lib.units import inch
# from reportlab.pdfgen import canvas
# from reportlab.lib import colors
# from reportlab.platypus import Table, TableStyle
# from io import BytesIO
# from django.core.files.base import ContentFile
# from django.conf import settings
# import os

# @receiver(post_save, sender=Laboratory)
# def generate_pdf_report(sender, instance, created, **kwargs):
#     if instance.status == 'Done' and not instance.report_file:
#         buffer = BytesIO()
#         p = canvas.Canvas(buffer, pagesize=letter)
#         width, height = letter

#         # Path to logo image
#         logo_path = os.path.join(settings.BASE_DIR, 'static/images/logo/logo.png')  # Adjust if needed

#         # Draw logo
#         try:
#             p.drawImage(logo_path, inch, height - inch * 1.25, width=2*inch, preserveAspectRatio=True, mask='auto')
#         except Exception as e:
#             print(f"Logo not found or error loading logo: {e}")

#         # Header
#         p.setFont("Helvetica-Bold", 18)
#         p.drawString(inch, height - inch * 1.5, "Lab Report")

#         # Patient info
#         p.setFont("Helvetica", 12)
#         p.drawString(inch, height - inch * 2, f"Patient Name: {instance.patient.First_name} {instance.patient.Last_name}")
#         p.drawString(inch, height - inch * 2.25, f"Appointment Date: {instance.appointment_date.strftime('%Y-%m-%d')}")
#         p.drawString(inch, height - inch * 2.5, f"Mobile: {instance.mobile}")

#         # Draw line
#         p.setStrokeColor(colors.grey)
#         p.setLineWidth(0.5)
#         p.line(inch, height - inch * 2.75, width - inch, height - inch * 2.75)

#         # Prepare tests data table
#         tests = [test.name for test in instance.tests.all()]
#         data = [['Test Name', 'Result']]
#         for test_name in tests:
#             # Assuming a generic result text here; if you want per test result, adapt accordingly
#             data.append([test_name, instance.result or "Pending"])

#         # Create table
#         table = Table(data, colWidths=[3*inch, 3*inch])
#         style = TableStyle([
#             ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
#             ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#             ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#             ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#             ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#             ('GRID', (0, 0), (-1, -1), 1, colors.black),
#         ])
#         table.setStyle(style)

#         # Position table below patient info
#         table.wrapOn(p, width, height)
#         table.drawOn(p, inch, height - inch * 5)

#         # Footer text
#         p.setFont("Helvetica-Oblique", 10)
#         p.drawString(inch, inch, "This is a computer-generated report. For any inquiries, contact support@example.com")

#         # Save and close
#         p.showPage()
#         p.save()

#         pdf = buffer.getvalue()
#         buffer.close()

#         # Save PDF to report_file field
#         instance.report_file.save(f"lab_report_{instance.id}.pdf", ContentFile(pdf))
#         instance.save()





