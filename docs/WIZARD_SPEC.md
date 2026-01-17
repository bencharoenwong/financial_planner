# Financial Planning Guide - Design Spec

## Philosophy

**One tool, optional guidance.**

| User Type | Experience |
|-----------|------------|
| Expert | Jump straight into the calculator, ignore the guide |
| New user | Open the guide panel, follow prompts to fill in the same form |

The calculator stays front and center. The guide is a **collapsible sidebar/panel** that helps users figure out what numbers to enter.

**Design principle:** Don't create a separate flow. Enhance the existing tool with contextual help.

---

## Layout: Guide Panel + Calculator

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Financial Goal Analyzer                          [📖 Planning Guide ▼] │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─── Guide Panel (collapsible) ───┐  ┌─── Calculator (always) ────┐   │
│  │                                 │  │                            │   │
│  │  Step 1 of 5: Foundation ✓      │  │  [Goal Mode] [FIRE Mode]   │   │
│  │  ─────────────────────────      │  │                            │   │
│  │  ☑ Emergency fund (3-6 mo)      │  │  Current Savings: [____]   │   │
│  │  ☑ High-interest debt paid      │  │                            │   │
│  │                                 │  │  Target Amount:   [____]   │   │
│  │  Step 2 of 5: Current State     │  │                            │   │
│  │  ─────────────────────────      │  │  Years:           [____]   │   │
│  │  What do you have today?        │  │                            │   │
│  │                                 │  │  Monthly Savings: [____]   │   │
│  │  → Fill in "Current Savings"    │  │                            │   │
│  │    in the calculator            │  │  Risk Profile:    [____]   │   │
│  │                                 │  │                            │   │
│  │  [Continue →]                   │  │  [Analyze Goal]            │   │
│  │                                 │  │                            │   │
│  └─────────────────────────────────┘  └────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Key behaviors:**
- Guide panel is **collapsed by default** (expert users see just the calculator)
- Button to expand: "Need help? Open Guide" in header area
- Guide steps highlight which form field to fill (subtle border, no auto-focus)
- Calculator works independently—guide is purely supplementary

---

## Accessibility & Responsive Spec

### Accessibility Requirements

**Toggle button:**
```html
<button
  aria-expanded="false"
  aria-controls="guidePanel"
  class="...">
  Need help? Open Guide
</button>
```

**Guide panel:**
```html
<aside
  id="guidePanel"
  role="complementary"
  aria-label="Planning Guide"
  hidden>
  ...
</aside>
```

**Keyboard navigation:**
- Tab order: Header → Guide toggle → Calculator form (guide panel is AFTER toggle, before form)
- When guide expanded: Tab through guide content, then into calculator form
- "Continue" buttons in guide are focusable
- NO automatic focus changes when highlighting fields
- Skip link: "Skip to calculator" at top of guide panel

**Field highlighting:**
- Visual only: `border: 2px solid #3b82f6; background: rgba(59, 130, 246, 0.1);`
- NO auto-scroll to field
- NO auto-focus changes
- User controls their own viewport and focus
- Highlight applied via CSS class `.guide-highlight`

**Contrast requirements:**
- All text: minimum 4.5:1 against background
- UI components (buttons, borders): minimum 3:1
- Use existing Tailwind color classes which meet WCAG AA

### Responsive Behavior

**Desktop (1024px+):**
- Side-by-side layout: guide (350px fixed) + calculator (flex)
- Container expands to `max-w-6xl` when guide is open
- CSS Grid: `grid-template-columns: 350px 1fr`

**Tablet (768px - 1024px):**
- Guide becomes overlay/drawer from left
- Calculator remains full-width underneath
- Guide has close button and slight backdrop

**Mobile (< 768px):**
- Guide is modal overlay (full-width drawer from bottom or left)
- Calculator unchanged when guide closed
- Guide has explicit close button

```css
/* Desktop: side-by-side */
@media (min-width: 1024px) {
  .layout-with-guide {
    display: grid;
    grid-template-columns: 350px 1fr;
    gap: 1.5rem;
    max-width: 1280px;
  }
}

/* Tablet/Mobile: guide is overlay */
@media (max-width: 1023px) {
  .guide-panel {
    position: fixed;
    left: 0;
    top: 0;
    bottom: 0;
    width: min(350px, 90vw);
    z-index: 50;
    transform: translateX(-100%);
    transition: transform 300ms ease;
  }
  .guide-panel.open {
    transform: translateX(0);
  }
  .guide-backdrop {
    /* Semi-transparent backdrop when guide open */
  }
}
```

### Layout Shift Mitigation

- Smooth CSS transition: `transition: all 300ms ease`
- Form values preserved during layout changes (no re-render)
- Guide slides in from left; calculator content reflows smoothly
- No jarring jumps or content disappearing

---

## Guide Steps

The guide walks users through filling in the existing calculator fields.

### Step 1: Foundation Check (Pre-Flight)

**Note:** This step is a pre-flight checklist. The checkboxes don't affect the calculator—they're reminders for the user.

```
┌─────────────────────────────────────┐
│  Before You Plan                    │
│  ─────────────────────────────────  │
│                                     │
│  Pre-flight check (for your        │
│  reference—doesn't affect calc):    │
│                                     │
│  ☐ I have 3-6 months emergency fund │
│  ☐ I've paid off high-interest debt │
│    (above 7%)                       │
│                                     │
│  [If unchecked, show gentle note:]  │
│  "Consider addressing these first.  │
│   The calculator still works, but   │
│   these are higher priority."       │
│                                     │
│  [Continue →]                       │
└─────────────────────────────────────┘
```

### Step 2: Current State

```
┌─────────────────────────────────────┐
│  What Do You Have Today?            │
│  ─────────────────────────────────  │
│                                     │
│  Think about:                       │
│  • Retirement accounts              │
│  • Brokerage accounts               │
│  • Savings allocated to this goal   │
│                                     │
│  Don't include emergency fund.      │
│                                     │
│  → Fill in "Current Savings" ←      │
│    [field highlights in calculator] │
│                                     │
│  [Continue →]                       │
└─────────────────────────────────────┘
```

### Step 3: Define Your Goal

```
┌─────────────────────────────────────┐
│  What Are You Saving For?           │
│  ─────────────────────────────────  │
│                                     │
│  Common goals:                      │
│  • Home down payment (5-10 yrs)     │
│  • Retirement (20-40 yrs)           │
│  • Children's education (10-20 yrs) │
│  • Financial independence           │
│                                     │
│  Tip: If "today's buying power,"    │
│  the tool adjusts for inflation.    │
│                                     │
│  → Fill in target amount & years ←  │
│                                     │
│  [Continue →]                       │
└─────────────────────────────────────┘
```

### Step 4: Contribution

```
┌─────────────────────────────────────┐
│  How Much Can You Save?             │
│  ─────────────────────────────────  │
│                                     │
│  Consider:                          │
│  • What you can commit monthly      │
│  • Employer matching (free money!)  │
│  • Don't forget other goals         │
│                                     │
│  Guideline: 15-20% savings rate     │
│  is a common target.                │
│                                     │
│  → Fill in monthly contribution ←   │
│                                     │
│  [Continue →]                       │
└─────────────────────────────────────┘
```

### Step 5: Risk Level

```
┌─────────────────────────────────────┐
│  How Much Risk?                     │
│  ─────────────────────────────────  │
│                                     │
│  General guideline:                 │
│                                     │
│  Near-term (< 5 yrs):               │
│    → Conservative                   │
│    (Need certainty, can't wait)     │
│                                     │
│  Medium-term (5-15 yrs):            │
│    → Moderate                       │
│    (Some flexibility)               │
│                                     │
│  Long-term (15+ yrs):               │
│    → Aggressive                     │
│    (Time to recover from dips)      │
│                                     │
│  → Select risk profile ←            │
│                                     │
│  [Analyze Goal]                     │
└─────────────────────────────────────┘
```

### Step 6: Review Results

```
┌─────────────────────────────────────┐
│  Understanding Your Results         │
│  ─────────────────────────────────  │
│                                     │
│  🟢 Green (80%+): On track          │
│  🟡 Yellow (50-79%): Stretch goal   │
│  🔴 Red (<50%): Needs adjustment    │
│                                     │
│  If yellow/red, you can:            │
│  • Increase contribution            │
│  • Extend timeline                  │
│  • Reduce target                    │
│  • Accept more risk (if time allows)│
│                                     │
│  Keep your results and review       │
│  quarterly or when life changes.    │
└─────────────────────────────────────┘
```

---

## FIRE Mode Handling

The guide adapts when user selects FIRE Mode:

| Goal Mode Step | FIRE Mode Equivalent |
|----------------|---------------------|
| Step 2: Current State | "Current Portfolio" field |
| Step 3: Define Goal | FIRE number (auto-calculated from expenses × 25) |
| Step 4: Contribution | "Monthly Investment" field |
| Step 5: Risk Level | Same |
| Step 6: Results | Years to FIRE instead of probability |

**FIRE-specific guidance in Step 3:**
```
┌─────────────────────────────────────┐
│  Your FIRE Number                   │
│  ─────────────────────────────────  │
│                                     │
│  Based on your monthly expenses     │
│  and safe withdrawal rate (SWR),    │
│  your FIRE number is calculated.    │
│                                     │
│  Monthly expenses × 12 ÷ SWR% =     │
│  Amount needed to retire            │
│                                     │
│  → Fill in monthly expenses ←       │
│  → Adjust SWR if needed (4% default)│
└─────────────────────────────────────┘
```

---

## Phase 1 Scope (What We're Building Now)

To avoid over-building, Phase 1 includes ONLY:
- Collapsible guide panel (6 steps)
- Field highlighting (visual only)
- Link to framework document

**Deferred to Phase 2:**
- Multi-goal tracking
- Export enhancements
- Contextual tips based on inputs

---

## Link to Framework Document

The guide panel includes a link to deeper guidance:

```
┌─────────────────────────────────────┐
│  Want More Guidance?                │
│  ─────────────────────────────────  │
│                                     │
│  This tool tests your numbers.      │
│  For comprehensive planning:        │
│                                     │
│  📄 Financial Planning Framework    │
│     • Situation assessment prompts  │
│     • Deep research prompts for     │
│       your country's tax rules      │
│     • Plan evaluation checklist     │
│                                     │
│  [Open Framework Guide →]           │
│                                     │
│  No personal info required.         │
└─────────────────────────────────────┘
```

---

## What We're NOT Building

To stay parsimonious:

- ❌ Separate wizard flow (guide enhances existing tool)
- ❌ User accounts / login
- ❌ Cloud storage
- ❌ Bank linking
- ❌ Notifications
- ❌ Gamification

The guide helps fill in the calculator. The spreadsheet IS the plan.

---

## Link to Framework Document

The guide panel should link to the full framework for users who want deeper guidance:

```
┌─────────────────────────────────────┐
│  Want More Guidance?                │
│  ─────────────────────────────────  │
│                                     │
│  This tool helps you test numbers.  │
│  For comprehensive planning:        │
│                                     │
│  📄 Financial Planning Framework    │
│     • Situation assessment prompts  │
│     • Deep research prompts for     │
│       your country's tax rules      │
│     • Plan evaluation checklist     │
│     • Portability considerations    │
│       (if you may relocate)         │
│                                     │
│  [Open Framework Guide →]           │
│                                     │
│  No personal info required.         │
└─────────────────────────────────────┘
```

This keeps the tool simple while offering depth for those who want it.

---

## Implementation

### Phase 1: Guide Panel
- Add collapsible panel to index.html
- 6 steps with contextual prompts
- Highlight which form field to fill
- Link to FINANCIAL_PLANNING_FRAMEWORK.md for deep research prompts

### Phase 2: Multi-Goal Export
- Allow saving multiple goal results
- Export combined spreadsheet with tracker template

### Phase 3: Contextual Tips
- Show tips based on inputs (e.g., "Your savings rate is 8%—consider increasing if possible")
- Link to relevant sections of the framework doc
