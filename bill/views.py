
import os

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm

from num2words import num2words


def bill_form(request):
    return render(request, "bill/form.html")


def generate_bill(request):

    if request.method != "POST":
        return HttpResponse("Invalid request")

    # ==============================
    # GET FORM DATA
    # ==============================

    name = request.POST.get("name", "")
    address = request.POST.get("address", "")
    description = request.POST.get("description", "")
    fees = request.POST.get("fees", "")
    date = request.POST.get("date", "")
    place_type = request.POST.get("place_type", "")

    if place_type == "indore":
        place = "Indore"
    else:
        place = request.POST.get("manual_place", "")

    # ==============================
    # AMOUNT IN WORDS
    # ==============================

    try:
        fees_number = int(float(fees))

        fees_words = num2words(
            fees_number,
            lang="en",
            to="cardinal"
        )

        # Remove "and" to get:
        # Five Hundred Fifty Five
        fees_words = fees_words.replace(" and ", " ")

        fees_words = fees_words.title()

    except:
        fees_words = ""

    # ==============================
    # CREATE A4 PDF
    # ==============================

    response = HttpResponse(content_type="application/pdf")

    # PDF filename according to user's name
    safe_name = name.strip().replace(" ", "_")

    if not safe_name:
        safe_name = "User"

    response["Content-Disposition"] = (
        f'attachment; filename="{safe_name}.pdf"'
    )

    pdf = canvas.Canvas(response, pagesize=A4)

    page_width, page_height = A4

    # ==============================
    # FONTS
    # ==============================

    normal_font = "Times-Roman"
    bold_font = "Times-Bold"
    bold_italic_font = "Times-BoldItalic"

    # ==============================
    # OPTIONAL ARIAL FONT
    # ==============================

    arial_path = os.path.join(
        settings.BASE_DIR,
        "static",
        "fonts",
        "arial.ttf"
    )

    arial_bold_path = os.path.join(
        settings.BASE_DIR,
        "static",
        "fonts",
        "arialbd.ttf"
    )

    # Arial Normal
    if os.path.isfile(arial_path):

        try:
            pdfmetrics.registerFont(
                TTFont("ArialCustom", arial_path)
            )

            arial_font = "ArialCustom"

        except Exception:
            arial_font = "Helvetica"

    else:
        arial_font = "Helvetica"

    # Arial Bold
    if os.path.isfile(arial_bold_path):

        try:
            pdfmetrics.registerFont(
                TTFont("ArialBoldCustom", arial_bold_path)
            )

            arial_bold_font = "ArialBoldCustom"

        except Exception:
            arial_bold_font = "Helvetica-Bold"

    else:
        arial_bold_font = "Helvetica-Bold"

    # ==============================
    # POSITION HELPER
    # ==============================

    def y_from_top(mm_value):
        return page_height - (mm_value * mm)

    # ==========================================================
    # HEADER
    # ==========================================================

    pdf.setStrokeColorRGB(
        0.67,
        0.13,
        0.13
    )

    pdf.setLineWidth(0.7)

    pdf.line(
        0,
        y_from_top(50.5),
        page_width,
        y_from_top(50.5)
    )

    # ==========================================================
    # SHREE
    # ==========================================================

    pdf.setFillColorRGB(
        0,
        0,
        0
    )

    pdf.setFont(
        bold_font,
        10.5
    )

    shree = "|| Shri Ji ||"

    text_width = pdf.stringWidth(
        shree,
        bold_font,
        10.5
    )

    pdf.drawString(
        (page_width - text_width) / 2,
        y_from_top(11.5) - 10.5,
        shree
    )

    # ==========================================================
    # COMPANY
    # ==========================================================

    pdf.setFont(
        bold_italic_font,
        18.75
    )

    company = "Er. Shreyansh Joshi Consultants"

    text_width = pdf.stringWidth(
        company,
        bold_italic_font,
        18.75
    )

    pdf.setFillColorRGB(
        0.67,
        0.20,
        0.20
    )

    pdf.drawString(
        (page_width - text_width) / 2,
        y_from_top(17.5) - 18.75,
        company
    )

    pdf.setFillColorRGB(
        0,
        0,
        0
    )

    # ==========================================================
    # QUALIFICATION
    # ==========================================================

    pdf.setFont(
        arial_bold_font,
        9
    )

    qual = "B.E. (Civil), AIE, AIV"

    text_width = pdf.stringWidth(
        qual,
        arial_bold_font,
        9
    )

    pdf.drawString(
        (page_width - text_width) / 2,
        y_from_top(27.5) - 9,
        qual
    )

    # ==========================================================
    # OFFICE
    # ==========================================================

    pdf.setFont(
        arial_bold_font,
        9
    )

    office = (
        "Chartered Engineer, Approved Valuer, "
        "Structural Engineer, Technical Auditor"
    )

    text_width = pdf.stringWidth(
        office,
        arial_bold_font,
        9
    )

    pdf.drawString(
        (page_width - text_width) / 2,
        y_from_top(33.5) - 9,
        office
    )

    # ==========================================================
    # OFFICE ADDRESS
    # ==========================================================

    pdf.setFont(
        arial_bold_font,
        8.25
    )

    office_address = (
        "Office: 59, Preconco Colony, Annapurna Road, "
        "Indore (M.P.) 452009"
    )

    text_width = pdf.stringWidth(
        office_address,
        arial_bold_font,
        8.25
    )

    pdf.drawString(
        (page_width - text_width) / 2,
        y_from_top(39.5) - 8.25,
        office_address
    )

    # ==========================================================
    # MOBILE / EMAIL
    # ==========================================================

    pdf.setFont(
        arial_bold_font,
        8.25
    )

    contact = (
        "Mobile: +91-9425053091, +91-9179224382, "
        "Email: shreyanshjoshiconsultants@gmail.com"
    )

    text_width = pdf.stringWidth(
        contact,
        arial_bold_font,
        8.25
    )

    pdf.drawString(
        (page_width - text_width) / 2,
        y_from_top(45) - 8.25,
        contact
    )

    # ==========================================================
    # MAIN CONTENT
    # ==========================================================

    left = 26.5 * mm

    pdf.setFillColorRGB(
        0,
        0,
        0
    )

    # ==========================================================
    # TO
    # ==========================================================

    current_y = y_from_top(71)

    # To
    pdf.setFont(
        normal_font,
        10.5
    )

    pdf.drawString(
        left,
        current_y,
        "To,"
    )

    # Name immediately below To
    current_y -= 5.5 * mm

    pdf.setFont(
        bold_font,
        10.5
    )

    pdf.drawString(
        left,
        current_y,
        name
    )

    # Address immediately below Name
    current_y -= 5.5 * mm

    pdf.setFont(
        normal_font,
        10.5
    )

    pdf.drawString(
        left,
        current_y,
        address
    )

    # ==========================================================
    # SUBJECT
    # ==========================================================

    current_y -= 8 * mm

    pdf.setFont(
        bold_font,
        10.5
    )

    pdf.drawString(
        left,
        current_y,
        "Sub: Professional Fee Bill"
    )

    # ==========================================================
    # DESCRIPTION
    # ==========================================================

    current_y -= 9 * mm

    pdf.setFont(
        normal_font,
        10.5
    )

    description_text = (
        "Please find the enclosed bill of "
        + description
        + "."
    )

    pdf.drawString(
        left,
        current_y,
        description_text
    )

    # ==========================================================
    # FEES
    # ==========================================================

    current_y -= 9 * mm

    pdf.setFont(
        bold_font,
        10.5
    )

    pdf.drawString(
        left,
        current_y,
        "Fees:"
    )

    # Underline Fees
    pdf.line(
        left,
        current_y - 1,
        left + 25,
        current_y - 1
    )

    # Amount
    amount_x = left + (75 + 15) * mm

    pdf.setFont(
        normal_font,
        10.5
    )

    pdf.drawString(
        amount_x,
        current_y,
        "Rs. " + fees + ".00"
    )

    # ==========================================================
    # TOTAL
    # ==========================================================

    # Small gap between Fees and Total
    current_y -= 5 * mm

    pdf.setFont(
        bold_font,
        10.5
    )

    pdf.drawString(
        left,
        current_y,
        "Total:"
    )

    pdf.drawString(
        amount_x,
        current_y,
        "Rs. " + fees + ".00"
    )

    # ==========================================================
    # AMOUNT IN WORDS
    # ==========================================================

    current_y -= 9 * mm

    pdf.setFont(
        bold_font,
        10.5
    )

    pdf.drawString(
        left,
        current_y,
        "(Rs. " + fees_words + " Only)"
    )

    # ==========================================================
    # DATE
    # ==========================================================

    current_y -= 6 * mm

    pdf.setFont(
        normal_font,
        10.5
    )

    pdf.drawString(
        left,
        current_y,
        "Date: " + date
    )

    # ==========================================================
    # PLACE
    # ==========================================================

    # Proper gap below Date
    current_y -= 5 * mm

    pdf.setFont(
        normal_font,
        10.5
    )

    pdf.drawString(
        left,
        current_y,
        "Place: " + place
    )

    # ==========================================================
    # SIGNATURE
    # ==========================================================

    signature_y = y_from_top(187)

    pdf.setFont(
        bold_font,
        10.5
    )

    pdf.drawString(
        left,
        signature_y,
        "Er. Shreyansh Pradeep Joshi"
    )

    # ==========================================================
    # BANK DETAILS
    # ==========================================================

    bank_y = y_from_top(197.5)

    bank_lines = [
        "Bank Details:",
        "Account Name: Shreyansh Joshi",
        "A/c. No.: 63034604541",
        "Bank Name: State Bank of India",
        "Branch: Bank Colony, Indore (M.P.)",
        "IFSC Code: SBIN0030458",
        "BHIM: 9425053091@upi",
        "PAN: AVUPJ3233H",
    ]

    line_height = 5.8 * mm

    for i, line in enumerate(bank_lines):

        if i == 0:
            pdf.setFont(
                bold_font,
                10.5
            )
        else:
            pdf.setFont(
                normal_font,
                10.5
            )

        pdf.drawString(
            left,
            bank_y - (i * line_height),
            line
        )

    # ==========================================================
    # FOOTER
    # ==========================================================

    footer_y = 15.5 * mm

    pdf.setStrokeColorRGB(
        0,
        0,
        0
    )

    pdf.setLineWidth(0.7)

    pdf.line(
        0,
        footer_y,
        page_width,
        footer_y
    )

    pdf.setFont(
        arial_bold_font,
        8.25
    )

    footer_text = (
        "Deals in: Topographical Surveying, Building Planning, "
        "Structural Design, Map Approval, Estimate and Valuation"
    )

    text_width = pdf.stringWidth(
        footer_text,
        arial_bold_font,
        8.25
    )

    pdf.drawString(
        (page_width - text_width) / 2,
        footer_y - (3 * mm) - 8.25,
        footer_text
    )

    # ==========================================================
    # FINISH — ONE PAGE ONLY
    # ==========================================================

    pdf.showPage()
    pdf.save()

    return response


