# Phase 2 Roadmap: Personalization Enhancements

## Completed in Phase 1

- [x] Removed auto-popup onboarding modal (no longer interrupts first-time users)
- [x] Added "Personalize with AI" card in both Goal Mode and FIRE Mode results
- [x] Single combined prompt generator (replaces 5-step wizard for most users)
- [x] Profile persists to localStorage and triggers prompt generation on save
- [x] Copy-to-clipboard functionality for generated prompts

---

## Phase 2A: UX Polish (Quick Wins)

### 1. Identity Badge in Header
**Status:** Not started
**Effort:** Small

Show persistent location indicator when profile is set:
```
┌─────────────────────────────────────────────────┐
│ Growth Graph                   🇮🇳 → 🇸🇬 [Edit] │
└─────────────────────────────────────────────────┘
```

**Implementation:**
- Show profile badge in header (already partially implemented)
- Make it always visible when profile exists (currently hidden by default)
- Add "Edit" link that opens onboarding modal

### 2. Pre-populate Cards on Page Load
**Status:** Not started
**Effort:** Small

If user has existing profile, automatically show "Location Set" state when results appear.

**Implementation:**
- On `initOnboarding()`, check if profile exists
- If yes, update card HTML to completed state (but keep prompt hidden until clicked)
- Show "Generate Prompt" button instead of "Set Location"

### 3. Mobile Responsive Refinement
**Status:** Not started
**Effort:** Small

Test and fix any layout issues on mobile viewports (320px, 375px, 768px).

**Implementation:**
- Test personalization card on small screens
- Ensure buttons are touch-friendly (min 44px tap target)
- Verify prompt display scrolls properly on mobile

---

## Phase 2B: Enhanced Personalization

### 4. Country-Specific Tips in Guide Panel
**Status:** Partially implemented
**Effort:** Medium

Show relevant tips based on citizenship/residence (already started with `showExpatTips()`).

**Enhancements:**
- Add more country combinations (currently: US abroad, Singapore, relocate)
- Show CPF/EPF/ISA specific guidance based on residence
- Add tax treaty warnings for common combinations

### 5. FIRE Mode Specific Prompt
**Status:** Not started
**Effort:** Medium

Generate FIRE-specific prompt that includes:
- Early access strategies (Roth conversion ladder, 72(t), etc.)
- Sequence of returns risk in user's tax jurisdiction
- Geographic arbitrage opportunities from their residence
- Healthcare gap considerations (especially for US)

**Implementation:**
```javascript
function generateFIREPrompt(profile) {
    // Include FIRE-specific content + country context
}
```

### 6. "Other" Country Handling
**Status:** Not started
**Effort:** Small

When user selects "Other" for country:
- Show text input field for custom country name
- Use that name in generated prompts

---

## Phase 2C: Advanced Features

### 7. Multi-Goal Tracking
**Status:** Not started
**Effort:** Large

Allow users to save multiple goals and see combined view.

**Implementation:**
- Save goals to localStorage array
- Show "Save This Goal" button after calculation
- Display saved goals in a collapsible panel
- Allow editing/deleting saved goals

### 8. Export Enhancement
**Status:** Partially implemented (Excel export exists)
**Effort:** Medium

Add personalization context to exports:
- Include citizenship/residence in Excel export
- Add prompt text to a "Research Prompts" sheet
- Export all saved goals with combined summary

### 9. Direct LLM Integration (Optional)
**Status:** Not started
**Effort:** Large
**Risk:** API costs, complexity

Instead of copy-paste, offer "Ask AI" button that calls Claude/GPT API directly.

**Considerations:**
- Would require API key (user's own or subsidized)
- Privacy implications (sending profile data to API)
- Cost management
- May be better to defer to Phase 3+

---

## Phase 2D: Framework Wizard Improvements

### 10. Keep 5-Step Wizard as "Advanced" Option
**Status:** Done (wizard still exists)
**Effort:** None

The existing 5-step wizard remains accessible via "Full Planning Framework" link in Guide panel for users who want structured templates.

### 11. Link Combined Prompt to Wizard
**Status:** Not started
**Effort:** Small

After showing combined prompt, add: "Want more detail? Try the full framework →"

**Implementation:**
- Add link below combined prompt display
- Opens framework wizard modal

---

## Technical Debt (Phase 2)

### 12. Consolidate localStorage Keys
**Status:** Not started
**Effort:** Small

Create centralized constants for localStorage keys:
```javascript
const LS_KEYS = {
    EXPAT_PROFILE: 'expatProfile',
    ONBOARDING_COMPLETED: 'onboardingCompleted',
    ONBOARDING_SKIPPED: 'onboardingSkipped',
    SAVED_GOALS: 'savedGoals'
};
```

### 13. Add Versioning to Profile Schema
**Status:** Done (version: 1 exists)
**Effort:** None

Profile already has version field for future migrations.

### 14. Error Handling for Corrupted localStorage
**Status:** Partially done
**Effort:** Small

`getExpatProfile()` has try/catch but could be more robust:
- Validate schema on read
- Auto-migrate old versions
- Reset gracefully if corrupted

---

## Testing Requirements (Phase 2)

### Manual Test Checklist
- [ ] First-time user: lands → calculator works → personalization card appears
- [ ] Profile set: location shows in header badge
- [ ] Profile update: changing location regenerates prompt
- [ ] FIRE mode: personalization card appears in FIRE results
- [ ] Mobile: all UI elements accessible and readable
- [ ] Copy button: works on all browsers
- [ ] localStorage: persists across page refreshes

### Automated Tests (If Investing in Infrastructure)
- Playwright E2E tests for:
  - Goal calculation flow
  - FIRE calculation flow
  - Personalization flow (set → generate → copy)
  - localStorage persistence

---

## Priority Matrix

| Item | Impact | Effort | Priority |
|------|--------|--------|----------|
| Identity badge in header | Medium | Small | P1 |
| Pre-populate cards on load | Medium | Small | P1 |
| Mobile responsive fixes | High | Small | P1 |
| FIRE-specific prompt | High | Medium | P2 |
| "Other" country handling | Low | Small | P2 |
| Multi-goal tracking | High | Large | P3 |
| Export enhancement | Medium | Medium | P3 |
| Direct LLM integration | Low | Large | P4 (defer) |

---

## Implementation Order (Recommended)

1. **Week 1:** Phase 2A (Quick Wins) - identity badge, pre-populate, mobile fixes
2. **Week 2:** Phase 2B items 5-6 - FIRE prompt, "Other" country
3. **Week 3:** Phase 2C item 7 - Multi-goal tracking
4. **Week 4:** Testing, polish, Phase 2D

---

## Questions for Future Consideration

1. **Pairwise Country Rules:** Should we add specific guidance for common combinations (US→SG, IN→US, UK→EU)? Or rely entirely on LLM prompts?

2. **Account-Specific Recommendations:** Could we show which accounts to use based on residence (e.g., "Max CPF OA/SA before taxable brokerage" for Singapore)?

3. **Tax Treaty Database:** Would a structured database of tax treaties add value, or is LLM research sufficient?

4. **Financial Planner "Council":** The original request mentioned checking with financial planners for best practices. This could inform:
   - Which country combinations to prioritize
   - Common mistakes to warn about
   - Key questions to include in prompts
