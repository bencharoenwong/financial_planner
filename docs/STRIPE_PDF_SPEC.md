# Technical Spec: Pay-Per-Report Integration

## Overview

Enable users to purchase PDF reports of their financial analysis. No accounts required - each purchase is a standalone transaction.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend                                 │
│                                                                  │
│  1. User completes analysis                                      │
│  2. Clicks "Download Report - $5"                               │
│  3. Redirected to Stripe Checkout                               │
│  4. After payment → redirected to success page with download    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         Backend                                  │
│                                                                  │
│  POST /api/checkout                                              │
│    - Receives analysis data (encrypted/signed)                  │
│    - Creates Stripe Checkout Session                            │
│    - Stores analysis data temporarily (Redis, 1hr TTL)          │
│    - Returns checkout URL                                        │
│                                                                  │
│  POST /api/webhook (Stripe)                                      │
│    - Receives payment confirmation                               │
│    - Generates PDF                                               │
│    - Sends email with PDF attached                               │
│    - Cleans up temp data                                         │
│                                                                  │
│  GET /api/report/{session_id}                                    │
│    - Validates session                                           │
│    - Returns PDF download                                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    External Services                             │
│                                                                  │
│  Stripe: Payment processing, customer records                   │
│  Email: SendGrid / Resend / SES for receipt + PDF               │
│  PDF: WeasyPrint / Puppeteer / html-pdf                         │
│  Cache: Redis / Vercel KV for temp storage                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## API Endpoints

### 1. Create Checkout Session

```
POST /api/checkout
```

**Request:**
```json
{
  "report_type": "single",  // "single" | "comparison"
  "analysis_data": {
    "mode": "goal",
    "currentWealth": 50000,
    "targetWealth": 500000,
    "yearsToGoal": 20,
    "monthlyContribution": 1000,
    "riskProfile": "moderate",
    "inflationRate": 3,
    // ... full analysis inputs
  },
  "results": {
    "successProbability": 0.78,
    "percentile10": 320000,
    "percentile50": 480000,
    "percentile90": 720000,
    // ... full results
  },
  "scenarios": []  // For comparison reports
}
```

**Response:**
```json
{
  "checkout_url": "https://checkout.stripe.com/c/pay/cs_xxx",
  "session_id": "cs_xxx"
}
```

**Implementation:**
```python
@app.post("/api/checkout")
async def create_checkout(request: CheckoutRequest):
    # 1. Validate analysis data
    if not validate_analysis(request.analysis_data):
        raise HTTPException(400, "Invalid analysis data")

    # 2. Store analysis data temporarily
    session_id = str(uuid.uuid4())
    await redis.setex(
        f"report:{session_id}",
        3600,  # 1 hour TTL
        json.dumps({
            "analysis_data": request.analysis_data,
            "results": request.results,
            "report_type": request.report_type
        })
    )

    # 3. Create Stripe Checkout Session
    price = 500 if request.report_type == "single" else 1000  # cents

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "unit_amount": price,
                "product_data": {
                    "name": f"Growth Graph {request.report_type.title()} Report",
                    "description": "Professional PDF analysis of your financial plan"
                }
            },
            "quantity": 1
        }],
        mode="payment",
        success_url=f"{BASE_URL}/report/success?session_id={session_id}",
        cancel_url=f"{BASE_URL}/?cancelled=true",
        metadata={
            "report_session_id": session_id
        }
    )

    return {"checkout_url": checkout_session.url, "session_id": session_id}
```

### 2. Stripe Webhook

```
POST /api/webhook
```

**Implementation:**
```python
@app.post("/api/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise HTTPException(400, "Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(400, "Invalid signature")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        report_session_id = session["metadata"]["report_session_id"]
        customer_email = session["customer_details"]["email"]

        # Get stored analysis data
        report_data = await redis.get(f"report:{report_session_id}")
        if not report_data:
            # Log error, but don't fail - Stripe will retry
            return {"status": "data_expired"}

        report_data = json.loads(report_data)

        # Generate PDF
        pdf_bytes = await generate_report_pdf(
            report_data["analysis_data"],
            report_data["results"],
            report_data["report_type"]
        )

        # Store PDF for download (24hr TTL)
        await redis.setex(
            f"pdf:{report_session_id}",
            86400,
            pdf_bytes
        )

        # Send email with PDF
        await send_report_email(customer_email, pdf_bytes, report_data)

        # Clean up analysis data
        await redis.delete(f"report:{report_session_id}")

    return {"status": "success"}
```

### 3. Download Report

```
GET /api/report/{session_id}
```

**Implementation:**
```python
@app.get("/api/report/{session_id}")
async def download_report(session_id: str):
    pdf_bytes = await redis.get(f"pdf:{session_id}")

    if not pdf_bytes:
        raise HTTPException(404, "Report expired or not found")

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=growth-graph-report.pdf"
        }
    )
```

---

## PDF Report Template

### Single Goal Report Structure

```
┌─────────────────────────────────────────────────────────────┐
│                     [Growth Graph Logo]                      │
│                                                              │
│              FINANCIAL GOAL ANALYSIS REPORT                  │
│                   Generated: Jan 17, 2026                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  EXECUTIVE SUMMARY                                           │
│  ─────────────────                                           │
│  Goal: Accumulate $500,000 in 20 years                      │
│  Current Savings: $50,000                                    │
│  Monthly Contribution: $1,000                                │
│  Risk Profile: Moderate (8% return, 13% volatility)          │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │           SUCCESS PROBABILITY: 78%                   │    │
│  │              ████████████████░░░░░ [GREEN]           │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  Interpretation: Your plan has a good chance of success.    │
│  In 78% of simulated scenarios, you reached your goal.      │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  PROJECTED OUTCOMES                                          │
│  ─────────────────                                           │
│                                                              │
│  [Chart: Wealth trajectory percentiles over time]            │
│                                                              │
│  After 20 years:                                             │
│  • Pessimistic (10th %ile): $320,000                        │
│  • Median (50th %ile): $480,000                             │
│  • Optimistic (90th %ile): $720,000                         │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  SENSITIVITY ANALYSIS                                        │
│  ────────────────────                                        │
│                                                              │
│  If you increased monthly contribution by $200:              │
│  → Success probability: 85% (+7%)                            │
│                                                              │
│  If you extended timeline by 3 years:                        │
│  → Success probability: 88% (+10%)                           │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  METHODOLOGY                                                 │
│  ───────────                                                 │
│  • Monte Carlo simulation with 10,000 iterations            │
│  • Log-normal return distribution                            │
│  • Assumptions: 8% arithmetic return, 13% volatility        │
│  • Inflation not modeled (all figures in today's dollars)   │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  DISCLAIMER                                                  │
│  This report is for educational purposes only. Past         │
│  performance does not guarantee future results. Consult     │
│  a qualified financial advisor before making decisions.     │
│                                                              │
│  Generated by Growth Graph • chicagoglobal.com/growth-graph │
└─────────────────────────────────────────────────────────────┘
```

### PDF Generation Options

**Option A: WeasyPrint (Python, HTML→PDF)**
```python
from weasyprint import HTML, CSS

async def generate_report_pdf(analysis_data, results, report_type):
    html_content = render_template("report.html", {
        "analysis": analysis_data,
        "results": results,
        "generated_at": datetime.now().isoformat()
    })

    pdf_bytes = HTML(string=html_content).write_pdf(
        stylesheets=[CSS(string=REPORT_CSS)]
    )

    return pdf_bytes
```

**Option B: Puppeteer (Node.js, best for charts)**
```javascript
const puppeteer = require('puppeteer');

async function generatePDF(analysisData, results) {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    // Render HTML with Chart.js
    await page.setContent(renderReportHTML(analysisData, results));
    await page.waitForSelector('#chart-rendered');  // Wait for chart

    const pdf = await page.pdf({
        format: 'Letter',
        margin: { top: '1in', bottom: '1in', left: '1in', right: '1in' }
    });

    await browser.close();
    return pdf;
}
```

**Recommendation:** Start with WeasyPrint for simplicity. Move to Puppeteer if charts in PDF are critical.

---

## Frontend Integration

### Add to index.html

```html
<!-- After results section -->
<div id="reportPurchase" class="mt-6 p-4 bg-gray-800 rounded-lg border border-gray-700 hidden">
    <div class="flex items-center justify-between">
        <div>
            <h3 class="font-medium text-white">Save Your Analysis</h3>
            <p class="text-sm text-gray-400">Download a professional PDF report</p>
        </div>
        <button onclick="purchaseReport()"
                class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition">
            Download Report - $5
        </button>
    </div>
</div>
```

### JavaScript

```javascript
async function purchaseReport() {
    const analysisData = getCurrentAnalysisData();  // Collect form inputs
    const results = getCurrentResults();  // From last analysis

    try {
        const response = await fetch('/api/checkout', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                report_type: 'single',
                analysis_data: analysisData,
                results: results
            })
        });

        const { checkout_url } = await response.json();
        window.location.href = checkout_url;  // Redirect to Stripe

    } catch (error) {
        console.error('Checkout error:', error);
        alert('Unable to start checkout. Please try again.');
    }
}
```

### Success Page

```html
<!-- report-success.html -->
<div class="text-center py-12">
    <div class="text-6xl mb-4">✅</div>
    <h1 class="text-2xl font-bold text-white mb-2">Thank You!</h1>
    <p class="text-gray-400 mb-6">Your report is ready to download.</p>

    <a id="downloadLink" href="#"
       class="inline-block px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg">
        Download PDF Report
    </a>

    <p class="text-sm text-gray-500 mt-4">
        A copy has also been sent to your email.
    </p>
</div>

<script>
    const params = new URLSearchParams(window.location.search);
    const sessionId = params.get('session_id');
    document.getElementById('downloadLink').href = `/api/report/${sessionId}`;
</script>
```

---

## Stripe Configuration

### Products to Create

1. **Single Report** - $5.00
   - Product ID: `prod_single_report`
   - One-time payment

2. **Comparison Report** - $10.00
   - Product ID: `prod_comparison_report`
   - One-time payment

3. **Report Pack (5)** - $15.00 (Phase 2)
   - Product ID: `prod_report_pack_5`

4. **Annual Unlimited** - $49.00 (Phase 3)
   - Product ID: `prod_annual_unlimited`
   - Subscription

### Environment Variables

```bash
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_PUBLISHABLE_KEY=pk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
```

### Webhook Events to Handle

- `checkout.session.completed` - Payment successful
- `charge.refunded` - Handle refund (optional: revoke download)

---

## Email Templates

### Receipt + Download Email

```
Subject: Your Growth Graph Report is Ready

Hi there,

Thank you for purchasing a Growth Graph report!

Your PDF is attached to this email. You can also download it here:
[Download Report]

---

Report Summary:
• Goal: $500,000 in 20 years
• Success Probability: 78%
• Generated: January 17, 2026

---

Questions? Reply to this email or contact support@chicagoglobal.com

— The Growth Graph Team
```

---

## Security Considerations

1. **Data in Transit**
   - Analysis data should be signed/encrypted before sending to checkout
   - Prevents tampering with inputs to generate fraudulent reports

2. **Rate Limiting**
   - Limit `/api/checkout` to prevent abuse
   - 10 requests per IP per hour

3. **Webhook Verification**
   - Always verify Stripe webhook signatures
   - Replay attack prevention (check event IDs)

4. **PDF Access**
   - Session IDs should be unguessable (UUID v4)
   - PDFs expire after 24 hours
   - Consider additional token for download URL

---

## Testing Checklist

- [ ] Stripe test mode works end-to-end
- [ ] PDF generates correctly with all data
- [ ] Email delivery works
- [ ] Webhook handles payment success
- [ ] Success page shows download link
- [ ] Cancelled checkout returns to calculator
- [ ] Error handling for expired sessions
- [ ] Mobile checkout flow works

---

## Deployment Notes

### Vercel

- Use Vercel KV for Redis-like temp storage
- Set environment variables in Vercel dashboard
- Webhook URL: `https://your-domain.vercel.app/api/webhook`

### Self-Hosted

- Use Redis for temp storage
- Set up HTTPS (required for Stripe)
- Configure webhook endpoint in Stripe dashboard

---

## Cost Estimates

| Service | Cost |
|---------|------|
| Stripe | 2.9% + $0.30 per transaction |
| Email (Resend) | Free up to 3k/month, then $20/month |
| Vercel KV | Free up to 30k requests/month |
| PDF Gen | CPU time only (included in Vercel) |

**Per $5 report:**
- Stripe fee: $0.45
- Net revenue: $4.55
- Margin: 91%
