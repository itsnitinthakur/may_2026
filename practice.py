from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, PageBreak, HRFlowable)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import KeepTogether

# ── Colour palette ──────────────────────────────────────────────────────────
BLUE_DARK   = colors.HexColor('#1F4E79')
BLUE_MID    = colors.HexColor('#2E75B6')
BLUE_LIGHT  = colors.HexColor('#E6F1FB')
PURPLE_DARK = colors.HexColor('#26215C')
PURPLE_MID  = colors.HexColor('#7F77DD')
PURPLE_LIGHT= colors.HexColor('#EEEDFE')
GREEN_DARK  = colors.HexColor('#173404')
GREEN_MID   = colors.HexColor('#639922')
GREEN_LIGHT = colors.HexColor('#EAF3DE')
TEAL_DARK   = colors.HexColor('#085041')
TEAL_MID    = colors.HexColor('#1D9E75')
TEAL_LIGHT  = colors.HexColor('#E1F5EE')
AMBER_DARK  = colors.HexColor('#633806')
AMBER_MID   = colors.HexColor('#EF9F27')
AMBER_LIGHT = colors.HexColor('#FAEEDA')
PINK_DARK   = colors.HexColor('#4B1528')
PINK_MID    = colors.HexColor('#D4537E')
PINK_LIGHT  = colors.HexColor('#FBEAF0')
GRAY_DARK   = colors.HexColor('#2C2C2A')
GRAY_MID    = colors.HexColor('#888780')
GRAY_LIGHT  = colors.HexColor('#F1EFE8')
WHITE       = colors.white
OFF_WHITE   = colors.HexColor('#F8F8F8')

W, H = letter
MARGIN = 0.65 * inch
CW = W - 2 * MARGIN   # content width

# ── Styles ───────────────────────────────────────────────────────────────────
def make_styles():
    base = getSampleStyleSheet()
    def s(name, **kw):
        return ParagraphStyle(name, **kw)

    return {
        'page_title': s('pt', fontName='Helvetica-Bold', fontSize=26,
                        textColor=BLUE_DARK, spaceAfter=4, alignment=TA_CENTER),
        'page_sub':   s('ps', fontName='Helvetica', fontSize=11,
                        textColor=GRAY_MID, spaceAfter=14, alignment=TA_CENTER),
        'section':    s('sec', fontName='Helvetica-Bold', fontSize=13,
                        textColor=BLUE_DARK, spaceBefore=18, spaceAfter=6),
        'phase':      s('ph', fontName='Helvetica-Bold', fontSize=10,
                        textColor=GRAY_MID, spaceBefore=14, spaceAfter=4,
                        leading=14),
        'body':       s('bd', fontName='Helvetica', fontSize=9,
                        textColor=GRAY_DARK, leading=13),
        'body_bold':  s('bb', fontName='Helvetica-Bold', fontSize=9,
                        textColor=GRAY_DARK, leading=13),
        'small':      s('sm', fontName='Helvetica', fontSize=8,
                        textColor=GRAY_MID, leading=11),
        'tag':        s('tg', fontName='Helvetica-Bold', fontSize=8,
                        textColor=WHITE, leading=10),
        'time':       s('tm', fontName='Helvetica-Bold', fontSize=8,
                        textColor=BLUE_MID, alignment=TA_RIGHT, leading=11),
        'slot_title': s('st', fontName='Helvetica-Bold', fontSize=9,
                        textColor=GRAY_DARK, leading=12),
        'slot_body':  s('sb', fontName='Helvetica', fontSize=8,
                        textColor=GRAY_MID, leading=11),
        'num_big':    s('nb', fontName='Helvetica-Bold', fontSize=28,
                        textColor=BLUE_DARK, alignment=TA_CENTER, leading=32),
        'num_label':  s('nl', fontName='Helvetica', fontSize=8,
                        textColor=GRAY_MID, alignment=TA_CENTER, leading=11),
        'milestone':  s('ms', fontName='Helvetica', fontSize=8.5,
                        textColor=GRAY_DARK, leading=13),
        'footer':     s('ft', fontName='Helvetica', fontSize=7.5,
                        textColor=GRAY_MID, alignment=TA_CENTER),
    }

ST = make_styles()

def hr(color=BLUE_MID, thickness=0.5):
    return HRFlowable(width='100%', thickness=thickness,
                      color=color, spaceAfter=8, spaceBefore=4)

def pill_table(text, bg, fg=WHITE):
    """Small pill badge as a 1-cell table."""
    cell = Paragraph(f'<b>{text}</b>',
                     ParagraphStyle('pill', fontName='Helvetica-Bold',
                                    fontSize=7.5, textColor=fg, leading=9))
    t = Table([[cell]], colWidths=[len(text)*5.5 + 12])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg),
        ('ROUNDEDCORNERS', [4]),
        ('TOPPADDING',    (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING',   (0,0), (-1,-1), 7),
        ('RIGHTPADDING',  (0,0), (-1,-1), 7),
    ]))
    return t

# ── Page 1: Daily Schedule ────────────────────────────────────────────────────
def build_daily(story):
    story.append(Paragraph("Nitin's daily plan", ST['page_title']))
    story.append(Paragraph("DevOps job-seeker · 8 hrs/day · gym 4:45–7 PM · wakes 8 AM", ST['page_sub']))
    story.append(hr(BLUE_MID, 1))
    story.append(Spacer(1, 6))

    slots = [
        ("8:00 AM",  AMBER_LIGHT,  AMBER_DARK,  AMBER_MID,
         "Wake up + morning routine",
         "Freshen up, tea, 10 min light stretch. No phone for first 15 min."),
        ("8:30 AM",  GRAY_LIGHT,   GRAY_DARK,   GRAY_MID,
         "Breakfast",
         "Proper protein-heavy meal. Sets up focus for the two study blocks ahead."),
        ("9:00 AM",  PURPLE_LIGHT, PURPLE_DARK, PURPLE_MID,
         "Study block 1 — concept video  [90 min]",
         "One focused topic: Docker / Ansible / Azure / K8s / Terraform. Written notes. Phone away."),
        ("10:30 AM", GRAY_LIGHT,   GRAY_DARK,   GRAY_MID,
         "Short break  [15 min]",
         "Walk, water. No scrolling — brain needs to consolidate what it just learned."),
        ("10:45 AM", PINK_LIGHT,   PINK_DARK,   PINK_MID,
         "Hands-on practice  [75 min]",
         "KodeKloud labs / terminal. Reproduce exactly what you watched. Write one script, playbook, or config."),
        ("12:00 PM", BLUE_LIGHT,   BLUE_DARK,   BLUE_MID,
         "Job applications block 1  [60 min]",
         "Apply to 5 jobs on Naukri: 'Ansible DevOps Delhi', 'Azure DevOps Noida', 'Python automation engineer'. Track in spreadsheet."),
        ("1:00 PM",  GRAY_LIGHT,   GRAY_DARK,   GRAY_MID,
         "Lunch + rest  [60 min]",
         "Full meal. Step away from screen for 20–25 min. Essential for afternoon focus."),
        ("2:00 PM",  PURPLE_LIGHT, PURPLE_DARK, PURPLE_MID,
         "Study block 2 — deep dive  [90 min]",
         "Same topic from morning, go deeper. Read docs, harder lab, sub-concept video. Real understanding forms here."),
        ("3:30 PM",  BLUE_LIGHT,   BLUE_DARK,   BLUE_MID,
         "Job applications block 2 + LinkedIn  [60 min]",
         "5 more jobs on LinkedIn + Instahyre. Connect with 2 recruiters. Comment on 1 DevOps post."),
        ("4:30 PM",  GRAY_LIGHT,   GRAY_DARK,   GRAY_MID,
         "Tea break  [15 min]",
         "Light snack before gym."),
        ("4:45 PM",  TEAL_LIGHT,   TEAL_DARK,   TEAL_MID,
         "Gym session  [4:45 – 7:00 PM]",
         "Full workout — commute + train + cooldown. Non-negotiable mental reset."),
        ("7:00 PM",  GRAY_LIGHT,   GRAY_DARK,   GRAY_MID,
         "Post-gym + dinner  [60 min]",
         "Shower, protein meal. No screens for 20 min."),
        ("8:00 PM",  PURPLE_LIGHT, PURPLE_DARK, PURPLE_MID,
         "Study block 3 — revision + mock test  [45 min]",
         "Recall today's topic out loud. Do 10 AZ-104 practice questions on Whizlabs. Understand every wrong answer."),
        ("8:45 PM",  BLUE_LIGHT,   BLUE_DARK,   BLUE_MID,
         "Referral outreach  [20 min]",
         "Message 1–2 contacts on LinkedIn: college batchmates, Lambton alumni, ex-colleagues. Ask about openings."),
        ("9:05 PM",  GREEN_LIGHT,  GREEN_DARK,  GREEN_MID,
         "Wind down + plan tomorrow  [25 min]",
         "Write tomorrow's study topic. Check job tracker for replies. One tech article max."),
        ("10:30 PM", GRAY_LIGHT,   GRAY_DARK,   GRAY_MID,
         "Lights out",
         "7–8 hrs sleep. Brain consolidates everything during sleep. Never cut this to study more."),
    ]

    time_w  = 0.72 * inch
    bar_w   = 0.08 * inch
    card_w  = CW - time_w - bar_w - 0.1*inch

    for time, bg, fg_dark, fg_mid, title, desc in slots:
        time_cell  = Paragraph(time, ST['time'])
        title_cell = Paragraph(title, ST['slot_title'])
        desc_cell  = Paragraph(desc,  ST['slot_body'])
        card_inner = Table(
            [[title_cell], [desc_cell]],
            colWidths=[card_w - 0.24*inch]
        )
        card_inner.setStyle(TableStyle([
            ('TOPPADDING',    (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('LEFTPADDING',   (0,0), (-1,-1), 0),
            ('RIGHTPADDING',  (0,0), (-1,-1), 0),
        ]))
        card_table = Table(
            [[card_inner]],
            colWidths=[card_w]
        )
        card_table.setStyle(TableStyle([
            ('BACKGROUND',    (0,0), (-1,-1), bg),
            ('ROUNDEDCORNERS',[5]),
            ('TOPPADDING',    (0,0), (-1,-1), 7),
            ('BOTTOMPADDING', (0,0), (-1,-1), 7),
            ('LEFTPADDING',   (0,0), (-1,-1), 10),
            ('RIGHTPADDING',  (0,0), (-1,-1), 10),
        ]))
        bar_table = Table(
            [['']], colWidths=[bar_w], rowHeights=[0.45*inch]
        )
        bar_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), fg_mid),
            ('ROUNDEDCORNERS', [3]),
            ('TOPPADDING',    (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ]))
        row = Table(
            [[time_cell, bar_table, card_table]],
            colWidths=[time_w, bar_w + 0.08*inch, card_w],
            rowHeights=[None]
        )
        row.setStyle(TableStyle([
            ('VALIGN',        (0,0), (-1,-1), 'TOP'),
            ('TOPPADDING',    (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('LEFTPADDING',   (0,0), (-1,-1), 0),
            ('RIGHTPADDING',  (0,0), (-1,-1), 0),
        ]))
        story.append(row)
        story.append(Spacer(1, 5))

    # Non-negotiables footer
    story.append(Spacer(1, 6))
    nonneg = Table(
        [[Paragraph('<b>Daily non-negotiables:</b>  10 job applications &nbsp;·&nbsp; 3.5 hrs study &nbsp;·&nbsp; 1 hands-on lab &nbsp;·&nbsp; gym 4:45 PM &nbsp;·&nbsp; lights out 10:30 PM', ST['body'])]],
        colWidths=[CW]
    )
    nonneg.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), BLUE_LIGHT),
        ('ROUNDEDCORNERS',[6]),
        ('TOPPADDING',    (0,0), (-1,-1), 9),
        ('BOTTOMPADDING', (0,0), (-1,-1), 9),
        ('LEFTPADDING',   (0,0), (-1,-1), 14),
        ('RIGHTPADDING',  (0,0), (-1,-1), 14),
    ]))
    story.append(nonneg)

# ── Page 2: 12-Week Plan ──────────────────────────────────────────────────────
def build_weeks(story):
    story.append(PageBreak())
    story.append(Paragraph("12-week learning + job hunt plan", ST['page_title']))
    story.append(Paragraph("Study · apply · build skills · get interviews", ST['page_sub']))
    story.append(hr(BLUE_MID, 1))

    phases = [
        ("Phase 1 — weeks 1–3 · foundation", PURPLE_MID, [
            ("Week 1", "Docker basics", PURPLE_LIGHT, PURPLE_DARK,
             "Docker concepts, Dockerfile, docker run, docker-compose.\nGoal: run a Python app inside a container by Friday.\nApply to 50 jobs this week."),
            ("Week 2", "Docker + CI/CD", PURPLE_LIGHT, PURPLE_DARK,
             "Docker Hub, image tagging, GitHub Actions pipeline that builds a Docker image.\nMove Docker from 'learning' to 'skills' on resume.\n50 more applications."),
            ("Week 3", "Ansible deep dive", PURPLE_LIGHT, PURPLE_DARK,
             "Revisit and strengthen Ansible — roles, vars, handlers, vault.\nYou have production experience — make it interview-proof.\n50 applications."),
        ]),
        ("Phase 2 — weeks 4–6 · AZ-104 certification push", AMBER_MID, [
            ("Week 4", "AZ-104: identities + networking", AMBER_LIGHT, AMBER_DARK,
             "Azure AD, RBAC, VNets, NSGs, load balancers.\n2 hrs study + 30 practice questions daily.\nKeep applying — 50 this week."),
            ("Week 5", "AZ-104: storage + compute", AMBER_LIGHT, AMBER_DARK,
             "Azure VMs, scale sets, storage accounts, blob, Azure Monitor.\nDaily practice test on Whizlabs.\n50 applications."),
            ("Week 6", "AZ-104 mock exams", AMBER_LIGHT, AMBER_DARK,
             "Full 60Q mock exam daily. Score 80%+ consistently then book real exam.\nContinue 50 applications in parallel."),
        ]),
        ("Phase 3 — weeks 7–9 · expand the stack", TEAL_MID, [
            ("Week 7", "Terraform basics", TEAL_LIGHT, TEAL_DARK,
             "Providers, resources, state, plan/apply on Azure free tier.\nGoal: one real .tf file deployed end-to-end.\n50 applications."),
            ("Week 8", "Kubernetes basics", TEAL_LIGHT, TEAL_DARK,
             "Pods, deployments, services, kubectl. KodeKloud K8s for beginners.\nEnough to answer interview basics confidently.\n50 applications."),
            ("Week 9", "Jenkins + monitoring", TEAL_LIGHT, TEAL_DARK,
             "Jenkins pipeline: GitHub → Docker build. Prometheus + Grafana basics.\nThese appear in 70% of Indian DevOps JDs.\n50 applications."),
        ]),
        ("Phase 4 — weeks 10–12 · job sprint", PINK_MID, [
            ("Week 10", "Interview prep", PINK_LIGHT, PINK_DARK,
             "Practice top 30 DevOps interview questions out loud.\nMock interview with a friend or record yourself.\nUpdate resume with all new skills. 70 applications."),
            ("Week 11", "Referral push", PINK_LIGHT, PINK_DARK,
             "Message every person you know in Indian IT.\nAsk for referrals directly — one referral = 50 cold applications.\nKeep cold applying in parallel."),
            ("Week 12", "Active interview mode", GREEN_LIGHT, GREEN_DARK,
             "AZ-104 done, Docker + Ansible + Terraform on resume, 600+ sent.\nShift 50% of daily time to interview prep and follow-ups.\nYou are job ready."),
        ]),
    ]

    WK = (CW - 0.2*inch) / 3

    for phase_title, phase_color, weeks in phases:
        story.append(Paragraph(phase_title.upper(), ST['phase']))
        row_data = []
        for wnum, wtitle, bg, fg, content in weeks:
            lines = content.split('\n')
            inner = [Paragraph(f'<b>{wnum}</b>', ST['small']),
                     Paragraph(wtitle, ST['body_bold']),
                     Spacer(1, 4)]
            for line in lines:
                inner.append(Paragraph(line, ST['body']))
            cell_table = Table([[inner]], colWidths=[WK - 0.2*inch])
            cell_table.setStyle(TableStyle([
                ('BACKGROUND',    (0,0), (-1,-1), bg),
                ('ROUNDEDCORNERS',[6]),
                ('TOPPADDING',    (0,0), (-1,-1), 9),
                ('BOTTOMPADDING', (0,0), (-1,-1), 9),
                ('LEFTPADDING',   (0,0), (-1,-1), 10),
                ('RIGHTPADDING',  (0,0), (-1,-1), 10),
                ('VALIGN',        (0,0), (-1,-1), 'TOP'),
            ]))
            row_data.append(cell_table)

        grid = Table([row_data], colWidths=[WK, WK, WK])
        grid.setStyle(TableStyle([
            ('TOPPADDING',    (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('LEFTPADDING',   (0,0), (-1,-1), 3),
            ('RIGHTPADDING',  (0,0), (-1,-1), 3),
            ('VALIGN',        (0,0), (-1,-1), 'TOP'),
        ]))
        story.append(KeepTogether([grid, Spacer(1, 6)]))

    # Applications milestone banner
    story.append(Spacer(1, 8))
    banner = Table(
        [[Paragraph('<b>Total applications target:</b>  Week 1–3 = 150 &nbsp;·&nbsp; Week 4–6 = 150 &nbsp;·&nbsp; Week 7–9 = 150 &nbsp;·&nbsp; Week 10–12 = 210 &nbsp;·&nbsp; <b>Total = 660+</b>', ST['body'])]],
        colWidths=[CW]
    )
    banner.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), GREEN_LIGHT),
        ('ROUNDEDCORNERS',[6]),
        ('TOPPADDING',    (0,0), (-1,-1), 9),
        ('BOTTOMPADDING', (0,0), (-1,-1), 9),
        ('LEFTPADDING',   (0,0), (-1,-1), 14),
        ('RIGHTPADDING',  (0,0), (-1,-1), 14),
    ]))
    story.append(banner)

# ── Page 3: Daily Targets ─────────────────────────────────────────────────────
def build_targets(story):
    story.append(PageBreak())
    story.append(Paragraph("Daily targets + milestones", ST['page_title']))
    story.append(Paragraph("Hit these numbers every day — the resume is ready, execution is all that's left", ST['page_sub']))
    story.append(hr(BLUE_MID, 1))
    story.append(Spacer(1, 8))

    # Big number metric cards
    metrics = [
        ("10",    "Job applications\nper day (Naukri + LinkedIn)", BLUE_LIGHT,   BLUE_DARK),
        ("3.5h",  "Focused study\nacross 3 daily blocks",          PURPLE_LIGHT, PURPLE_DARK),
        ("1",     "Hands-on lab or\nscript built per day",          PINK_LIGHT,   PINK_DARK),
        ("2",     "LinkedIn recruiter\nconnections sent daily",     TEAL_LIGHT,   TEAL_DARK),
        ("1–2",   "Referral messages\nto network contacts",         GREEN_LIGHT,  GREEN_DARK),
        ("10",    "AZ-104 practice\nquestions answered",            AMBER_LIGHT,  AMBER_DARK),
        ("660+",  "Total applications\nby end of week 12",          BLUE_LIGHT,   BLUE_DARK),
        ("10:30", "Lights out every\nnight — no exceptions",        GRAY_LIGHT,   GRAY_DARK),
    ]

    MK = (CW - 0.18*inch) / 4
    for i in range(0, 8, 4):
        row = []
        for num, label, bg, fg in metrics[i:i+4]:
            num_p   = Paragraph(num,   ParagraphStyle('mn', fontName='Helvetica-Bold',
                                fontSize=26, textColor=fg, alignment=TA_CENTER, leading=30))
            label_p = Paragraph(label, ParagraphStyle('ml', fontName='Helvetica',
                                fontSize=8, textColor=fg, alignment=TA_CENTER,
                                leading=11))
            inner = Table([[num_p], [label_p]], colWidths=[MK - 0.2*inch])
            inner.setStyle(TableStyle([
                ('TOPPADDING',    (0,0), (-1,-1), 0),
                ('BOTTOMPADDING', (0,0), (-1,-1), 0),
                ('LEFTPADDING',   (0,0), (-1,-1), 0),
                ('RIGHTPADDING',  (0,0), (-1,-1), 0),
            ]))
            card = Table([[inner]], colWidths=[MK - 0.06*inch])
            card.setStyle(TableStyle([
                ('BACKGROUND',    (0,0), (-1,-1), bg),
                ('ROUNDEDCORNERS',[8]),
                ('TOPPADDING',    (0,0), (-1,-1), 14),
                ('BOTTOMPADDING', (0,0), (-1,-1), 14),
                ('LEFTPADDING',   (0,0), (-1,-1), 10),
                ('RIGHTPADDING',  (0,0), (-1,-1), 10),
                ('ALIGN',         (0,0), (-1,-1), 'CENTER'),
            ]))
            row.append(card)
        grid = Table([row], colWidths=[MK]*4)
        grid.setStyle(TableStyle([
            ('TOPPADDING',    (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('LEFTPADDING',   (0,0), (-1,-1), 3),
            ('RIGHTPADDING',  (0,0), (-1,-1), 3),
            ('VALIGN',        (0,0), (-1,-1), 'TOP'),
        ]))
        story.append(grid)
        story.append(Spacer(1, 8))

    # Weekly milestones
    story.append(Spacer(1, 10))
    story.append(Paragraph("WEEKLY MILESTONES — track these every Sunday", ST['phase']))

    milestones = [
        (PURPLE_MID, PURPLE_LIGHT, PURPLE_DARK, "Week 1",  "Run a Python app inside Docker on your own machine"),
        (PURPLE_MID, PURPLE_LIGHT, PURPLE_DARK, "Week 2",  "Move Docker to main skills section on resume + LinkedIn"),
        (AMBER_MID,  AMBER_LIGHT,  AMBER_DARK,  "Week 6",  "Book your AZ-104 exam date"),
        (AMBER_MID,  AMBER_LIGHT,  AMBER_DARK,  "Week 7",  "AZ-104 passed — update resume and LinkedIn immediately"),
        (TEAL_MID,   TEAL_LIGHT,   TEAL_DARK,   "Week 9",  "Terraform + K8s basics added to skills section on resume"),
        (PINK_MID,   PINK_LIGHT,   PINK_DARK,   "Week 10", "Can answer top 30 DevOps interview questions confidently"),
        (GREEN_MID,  GREEN_LIGHT,  GREEN_DARK,  "Week 12", "660 applications sent, referrals active, interviews happening"),
    ]

    for dot_color, bg, fg, week, text in milestones:
        dot_cell  = Table([['']], colWidths=[0.14*inch], rowHeights=[0.14*inch])
        dot_cell.setStyle(TableStyle([
            ('BACKGROUND',    (0,0), (-1,-1), dot_color),
            ('ROUNDEDCORNERS',[7]),
        ]))
        week_p = Paragraph(f'<b>{week}</b>', ParagraphStyle('wk',
                    fontName='Helvetica-Bold', fontSize=8.5,
                    textColor=fg))
        text_p = Paragraph(text, ParagraphStyle('tx',
                    fontName='Helvetica', fontSize=8.5,
                    textColor=GRAY_DARK, leading=12))
        inner = Table([[week_p, text_p]], colWidths=[0.7*inch, CW - 1.1*inch])
        inner.setStyle(TableStyle([
            ('TOPPADDING',    (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('LEFTPADDING',   (0,0), (-1,-1), 0),
            ('RIGHTPADDING',  (0,0), (-1,-1), 0),
            ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
        ]))
        row = Table([[dot_cell, inner]], colWidths=[0.25*inch, CW - 0.25*inch])
        row.setStyle(TableStyle([
            ('TOPPADDING',    (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('LEFTPADDING',   (0,0), (-1,-1), 0),
            ('RIGHTPADDING',  (0,0), (-1,-1), 0),
            ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
        ]))
        card = Table([[row]], colWidths=[CW])
        card.setStyle(TableStyle([
            ('BACKGROUND',    (0,0), (-1,-1), bg),
            ('ROUNDEDCORNERS',[5]),
            ('TOPPADDING',    (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING',   (0,0), (-1,-1), 12),
            ('RIGHTPADDING',  (0,0), (-1,-1), 12),
        ]))
        story.append(card)
        story.append(Spacer(1, 5))

    # Sunday rule
    story.append(Spacer(1, 10))
    sunday = Table(
        [[Paragraph('<b>Sunday rule:</b>  Half day only — 1 hr revision, no new topics, no job applications. Rest is part of the plan. A burnt-out job seeker performs badly in interviews. Protect Sundays.', ST['body'])]],
        colWidths=[CW]
    )
    sunday.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), GRAY_LIGHT),
        ('ROUNDEDCORNERS',[6]),
        ('TOPPADDING',    (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING',   (0,0), (-1,-1), 14),
        ('RIGHTPADDING',  (0,0), (-1,-1), 14),
    ]))
    story.append(sunday)

    story.append(Spacer(1, 10))
    closing = Table(
        [[Paragraph('The resume is good enough. The plan is clear. The only variable left is execution — start today.', 
                    ParagraphStyle('cl', fontName='Helvetica-Bold', fontSize=9.5,
                                   textColor=BLUE_DARK, alignment=TA_CENTER, leading=13))]],
        colWidths=[CW]
    )
    closing.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), BLUE_LIGHT),
        ('ROUNDEDCORNERS',[6]),
        ('TOPPADDING',    (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('LEFTPADDING',   (0,0), (-1,-1), 14),
        ('RIGHTPADDING',  (0,0), (-1,-1), 14),
    ]))
    story.append(closing)

# ── Footer callback ───────────────────────────────────────────────────────────
def add_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 7.5)
    canvas.setFillColor(GRAY_MID)
    page_labels = {1: "Daily schedule", 2: "12-week plan", 3: "Daily targets"}
    label = page_labels.get(doc.page, "")
    canvas.drawString(MARGIN, 0.42 * inch, f"Nitin — DevOps job plan  ·  {label}")
    canvas.drawRightString(W - MARGIN, 0.42 * inch, f"Page {doc.page} of 3")
    canvas.restoreState()

# ── Build ─────────────────────────────────────────────────────────────────────
out = "Nitin_DevOps_Plan.pdf"
doc = SimpleDocTemplate(
    out, pagesize=letter,
    leftMargin=MARGIN, rightMargin=MARGIN,
    topMargin=0.6*inch, bottomMargin=0.7*inch
)

story = []
build_daily(story)
build_weeks(story)
build_targets(story)

doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)
print("Done:", out)
