"""Views for pages app"""
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, Http404
from django.core.mail import EmailMessage
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
import os
from pathlib import Path


def index_redirect(request):
    """Redirect root to US homepage"""
    return redirect('/US/index.do?lang=en&country=US')


def us_index(request):
    """US Homepage"""
    return render(request, 'pages/US/index.html')


def programs_math(request):
    """Math program page"""
    return render(request, 'pages/US/programs/math.html')


def programs_english(request):
    """English program page"""
    return render(request, 'pages/US/programs/english.html')


def programs_intro(request):
    """Programs intro page"""
    return render(request, 'pages/US/programs/intro.html')


def programs_summit_of_math(request):
    """Summit of Math program page"""
    return render(request, 'pages/US/programs/summit_of_math.html')


def why_intro(request):
    """Why Eye Level intro page"""
    return render(request, 'pages/US/why-eye-level/intro.html')


def about_brand(request):
    """About Eye Level brand story"""
    return render(request, 'pages/US/about-eye-level/brand-story.html')


def contact_us(request):
    """Contact us page - handles both GET and POST"""
    if request.method == 'POST':
        # Get form data - matching actual HTML field names
        center_no = request.POST.get('center_no', '')
        center_name = request.POST.get('center_name', '')
        if not center_name:
            center_name = request.POST.get('centerInfo', '')

        first_name = request.POST.get('first_name', '')
        if not first_name:
            first_name = request.POST.get('p_fName', '')

        last_name = request.POST.get('last_name', '')
        if not last_name:
            last_name = request.POST.get('p_lName', '')

        student_first = request.POST.get('student_first_name', '')
        if not student_first:
            student_first = request.POST.get('fName', '')

        student_last = request.POST.get('student_last_name', '')
        if not student_last:
            student_last = request.POST.get('lName', '')

        grade = request.POST.get('grade', '')
        email_local = request.POST.get('email_local', '')
        if not email_local:
            email_local = request.POST.get('email_id', '')

        email_domain = request.POST.get('email_domain', '')
        phone = request.POST.get('phone', '')
        inquiry_type = request.POST.get('inquiry_type', '')

        programs = request.POST.getlist('program')
        if not programs:
            programs = request.POST.getlist('subject')
        
        full_email = f"{email_local}@{email_domain}" if email_local and email_domain else email_local
        full_name = f"{first_name} {last_name}".strip()
        student_name = f"{student_first} {student_last}".strip() if student_first or student_last else 'Not provided'
        programs_str = ', '.join(programs) if programs else 'None selected'
        
        # Build email message
        center_link = 'https://share.google/vpuc1tl6AtqNCd52n'
        subject = f"Eye Level Contact Form | {center_name or 'Center not provided'} | {full_name or 'Name not provided'}"
        body = f"""New contact form submission:

Name: {full_name}
Email: {full_email}
Phone: {phone}

Student Information:
- Name: {student_name}
- Grade: {grade}

Center:
- Name: {center_name or 'Not provided'}
- Link: {center_link}

Center ID: {center_no}

Inquiry Type: {inquiry_type}
Interested Programs: {programs_str}
"""
        
        # Send email
        try:
            headers = {}
            if full_email:
                headers['Reply-To'] = full_email
            email_message = EmailMessage(
                subject=subject,
                body=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.CONTACT_EMAIL_RECIPIENT],
                headers=headers,
            )
            email_message.send(fail_silently=False)
            return render(request, 'pages/US/customer/contact-us.html', {
                'success_message': 'Thank you! Your message has been sent. We will contact you soon.'
            })
        except Exception as e:
            return render(request, 'pages/US/customer/contact-us.html', {
                'error_message': f'Sorry, there was an error sending your message. Please try again later. Error: {str(e)}'
            })
    
    # GET request - just show the form
    return render(request, 'pages/US/customer/contact-us.html')


def contact_us_finish(request):
    """Contact us finish page (thank you)."""
    return render(request, 'pages/US/customer/contact-us.html', {
        'success_message': 'Thank you! Your message has been sent. We will contact you soon.',
    })


def verify_recaptcha(request):
    """Compatibility endpoint for legacy templates.

    The static template JS expects this endpoint and treats 0 as success.
    """
    if request.method != 'POST':
        return JsonResponse({'detail': 'Method not allowed'}, status=405)
    return HttpResponse('0', content_type='text/plain')


@csrf_exempt
def contact_proc(request):
    """Legacy homepage AJAX endpoint.

    The crawled homepage posts to /US/contactProc.do and expects a JSON payload
    containing a string code, where "1" means success.
    """
    if request.method != 'POST':
        return JsonResponse({'code': '0', 'message': 'Method not allowed'}, status=405)

    center_no = request.POST.get('center_no', '')
    center_name = request.POST.get('center_name', '')
    if not center_name:
        center_name = request.POST.get('centerInfo', '')

    first_name = request.POST.get('first_name', '')
    if not first_name:
        first_name = request.POST.get('p_fName', '')

    last_name = request.POST.get('last_name', '')
    if not last_name:
        last_name = request.POST.get('p_lName', '')

    student_first = request.POST.get('student_first_name', '')
    if not student_first:
        student_first = request.POST.get('fName', '')

    student_last = request.POST.get('student_last_name', '')
    if not student_last:
        student_last = request.POST.get('lName', '')

    grade = request.POST.get('grade', '')
    email_local = request.POST.get('email_local', '')
    if not email_local:
        email_local = request.POST.get('email_id', '')

    email_domain = request.POST.get('email_domain', '')
    phone = request.POST.get('phone', '')
    inquiry_type = request.POST.get('inquiry_type', '')
    inflow_type = request.POST.get('inflow_type', '')
    inflow_etc = request.POST.get('inflow_etc', '')
    contents = request.POST.get('contents', '')

    programs = request.POST.getlist('program')
    if not programs:
        programs = request.POST.getlist('subject')

    full_email = f"{email_local}@{email_domain}" if email_local and email_domain else email_local
    full_name = f"{first_name} {last_name}".strip()
    student_name = (
        f"{student_first} {student_last}".strip()
        if student_first or student_last
        else 'Not provided'
    )
    programs_str = ', '.join(programs) if programs else 'None selected'

    center_link = 'https://share.google/vpuc1tl6AtqNCd52n'

    subject = f"Eye Level Contact Form | {center_name or 'Center not provided'} | {full_name or 'Name not provided'}"
    body = f"""New contact form submission:

Name: {full_name}
Email: {full_email}
Phone: {phone}

Student Information:
- Name: {student_name}
- Grade: {grade}

Center:
- Name: {center_name or 'Not provided'}
- Link: {center_link}

Center ID: {center_no}

Inquiry Type: {inquiry_type}
Interested Programs: {programs_str}

Heard About Us from: {inflow_type or 'Not provided'}
Heard About Us (Other): {inflow_etc or 'Not provided'}

Comment/Question:
{contents or 'Not provided'}
"""

    try:
        headers = {}
        if full_email:
            headers['Reply-To'] = full_email
        email_message = EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.CONTACT_EMAIL_RECIPIENT],
            headers=headers,
        )
        email_message.send(fail_silently=False)
        return JsonResponse({'code': '1'})
    except Exception as e:
        return JsonResponse({'code': '0', 'message': str(e)}, status=500)


def find_center(request):
    """Find a center page"""
    return render(request, 'pages/US/customer/find-a-center.html')


def blog_list(request):
    """Blog articles list"""
    return render(request, 'pages/US/resources/blog/articles/list.html')


def press_list(request):
    """Press release list"""
    return render(request, 'pages/US/resources/press-release/list.html')


def testimonial_list(request):
    """Testimonial list"""
    return render(request, 'pages/US/resources/testimonial/list.html')


def faq(request):
    """FAQ page"""
    return render(request, 'pages/US/footer/faq.html')


def sitemap(request):
    """Sitemap page"""
    return render(request, 'pages/US/footer/sitemap.html')


def privacy(request):
    """Privacy policy page"""
    return render(request, 'pages/US/footer/getPrivacyPolicy_2023.html')


def cookie_policy(request):
    """Cookie policy page"""
    return render(request, 'pages/US/footer/cookie-policy.html')


def global_network(request):
    """Global network page"""
    return render(request, 'pages/US/footer/global-network/subsidiary-contacts.html')


def global_partner_contacts(request):
    """Global partner contacts page"""
    return render(request, 'pages/US/footer/global-network/global-partner-contacts.html')


def global_events_intro(request):
    """Global events intro page"""
    return render(request, 'pages/US/global-events/intro.html')


def global_events_math_olympiad_intro(request):
    """Eye Level Math Olympiad intro page"""
    return render(request, 'pages/US/global-events/math-olympiad/intro.html')


def global_events_literary_award_intro(request):
    """Eye Level Literary Award intro page"""
    return render(request, 'pages/US/global-events/literary-award/intro.html')


def global_events_mun_camp_intro(request):
    """Eye Level MUN Camp intro page"""
    return render(request, 'pages/US/global-events/mun-camp/intro.html')


def global_events_oratacular_intro(request):
    """Eye Level Oratacular intro page"""
    return render(request, 'pages/US/global-events/oratacular/intro.html')


def careers(request):
    """Careers page"""
    return render(request, 'pages/US/careers/careers.html')


def us_template_router(request, template_path: str):
    normalized = template_path.strip('/')
    if not normalized or '..' in normalized.split('/'):
        raise Http404()

    template_name = f'pages/US/{normalized}.html'
    try:
        get_template(template_name)
    except TemplateDoesNotExist as exc:
        return redirect('/US/index.do?lang=en&country=US')

    return render(request, template_name)
