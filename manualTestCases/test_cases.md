### TC-001 — Open Form Picker calendar and select a valid date

**Category:** Positive

**Preconditions:** User is on `http://localhost:4200/pages/forms/datepicker` and the page has fully loaded with the "Form Picker", "Range Picker", and "Min Max Picker" inputs visible.

**Steps:**
1. Click the input field with placeholder "Form Picker".
2. Wait for the calendar overlay to appear.
3. Click any selectable day in the current month (e.g., the 15th).

**Expected Result:** The calendar closes and the selected date is populated in the "Form Picker" input field in the format displayed by the component (e.g., `MMM DD, YYYY`).

---

### TC-002 — Form Picker calendar opens with current month and today highlighted

**Category:** Positive

**Preconditions:** User is on the Datepicker page.

**Steps:**
1. Click the "Form Picker" input.
2. Observe the calendar header and grid.

**Expected Result:** The calendar opens displaying the current month and year (April 2026), and today's date (26) is visually highlighted/marked as "today".

---

### TC-003 — Navigate to next and previous month in Form Picker

**Category:** Positive

**Preconditions:** Form Picker calendar overlay is open.

**Steps:**
1. Click the "next month" chevron in the calendar header.
2. Verify the displayed month advances by one.
3. Click the "previous month" chevron twice.
4. Verify the displayed month decrements appropriately.

**Expected Result:** Calendar header text updates each time, and the day grid re-renders to match the displayed month/year.

---

### TC-004 — Switch from day view to month/year picker

**Category:** Positive

**Preconditions:** Form Picker calendar overlay is open.

**Steps:**
1. Click the month/year label in the calendar header.
2. Select a different year (e.g., 2027).
3. Select a different month (e.g., December).
4. Click any day in the grid.

**Expected Result:** The Form Picker input shows the chosen day in December 2027.

---

### TC-005 — Select a valid date range using Range Picker

**Category:** Positive

**Preconditions:** User is on the Datepicker page.

**Steps:**
1. Click the input with placeholder "Range Picker".
2. Click a start date in the calendar (e.g., April 5, 2026).
3. Click an end date later in the same month (e.g., April 20, 2026).

**Expected Result:** The Range Picker input is populated with both dates separated by a delimiter (e.g., `Apr 5, 2026 - Apr 20, 2026`), and the calendar visually shades the days between the two endpoints.

---

### TC-006 — Range Picker spanning across multiple months

**Category:** Positive

**Preconditions:** User is on the Datepicker page.

**Steps:**
1. Click the "Range Picker" input.
2. Select a start date (e.g., April 28, 2026).
3. Click the next-month chevron.
4. Select an end date in the following month (e.g., May 10, 2026).

**Expected Result:** The Range Picker input displays the multi-month range, and the highlighted band correctly spans the month boundary in the calendar UI.

---

### TC-007 — Select a date within Min Max Picker allowed range

**Category:** Positive

**Preconditions:** User is on the Datepicker page. Min Max Picker has predefined min/max bounds (per Nebular demo: typically a window around the current date).

**Steps:**
1. Click the input with placeholder "Min Max Picker".
2. Identify enabled (non-greyed) days in the calendar.
3. Click an enabled day inside the allowed range.

**Expected Result:** The selected date populates the "Min Max Picker" input, and the calendar closes.

---

### TC-008 — Min Max Picker disables out-of-range dates

**Category:** Validation

**Preconditions:** User is on the Datepicker page.

**Steps:**
1. Click the "Min Max Picker" input.
2. Hover over and attempt to click a date outside the configured min/max window.
3. Observe styling and clickability.

**Expected Result:** Out-of-range dates are visually disabled (greyed out / not selectable), clicking them has no effect, and the input remains empty.

---

### TC-009 — Min Max Picker rejects manually typed out-of-range date

**Category:** Negative

**Preconditions:** User is on the Datepicker page.

**Steps:**
1. Click into the "Min Max Picker" input field.
2. Type a date that is clearly outside the allowed window (e.g., `Jan 1, 1990`).
3. Click outside the field to blur it.

**Expected Result:** The input is flagged as invalid (red border / validation styling) or the value is rejected/cleared; no date selection is committed to the model.

---

### TC-010 — Form Picker rejects malformed text input

**Category:** Validation

**Preconditions:** User is on the Datepicker page.

**Steps:**
1. Click into the "Form Picker" input.
2. Type a clearly invalid string (e.g., `not-a-date`).
3. Press Tab to blur the field.

**Expected Result:** Input is marked invalid (Nebular invalid state styling) and no date value is bound to the underlying form control.

---

### TC-011 — Range Picker with end date before start date

**Category:** Negative

**Preconditions:** User is on the Datepicker page.

**Steps:**
1. Click the "Range Picker" input.
2. Click a start date (e.g., April 20, 2026).
3. Click an earlier date (e.g., April 5, 2026) as the second click.

**Expected Result:** The component either swaps the values so the earlier date becomes the start, or it resets and treats the second click as a new start date — in no case is an inverted range displayed.

---

### TC-012 — Single-click selection in Range Picker leaves end date open

**Category:** Negative

**Preconditions:** User is on the Datepicker page.

**Steps:**
1. Click the "Range Picker" input.
2. Click a single date.
3. Click outside the calendar without selecting an end date.

**Expected Result:** Either no value is committed to the input, or the input shows only the start date with no end date — and reopening the picker requires selecting an end date to complete the range.

---

### TC-013 — Calendar overlay closes when clicking outside

**Category:** Positive

**Preconditions:** Form Picker calendar overlay is open.

**Steps:**
1. Click the "Form Picker" input to open the calendar.
2. Click on an empty area of the page outside the calendar and input.

**Expected Result:** The calendar overlay closes; the input retains any previously committed value or remains empty.

---

### TC-014 — Only one calendar overlay open at a time

**Category:** Positive

**Preconditions:** User is on the Datepicker page.

**Steps:**
1. Click the "Form Picker" input to open its calendar.
2. Without closing it, click the "Range Picker" input.

**Expected Result:** The Form Picker overlay closes and the Range Picker overlay opens; only one calendar is visible at any moment.

---

### TC-015 — Boundary: select first day of month in Form Picker

**Category:** Boundary

**Preconditions:** Form Picker calendar overlay is open.

**Steps:**
1. Navigate to any month (e.g., April 2026).
2. Click day `1`.

**Expected Result:** Input value updates to the 1st of that month (e.g., `Apr 1, 2026`); calendar closes without errors.

---

### TC-016 — Boundary: select last day of a 31-day month

**Category:** Boundary

**Preconditions:** Form Picker calendar overlay is open.

**Steps:**
1. Navigate to a 31-day month (e.g., March 2026).
2. Click day `31`.

**Expected Result:** Input correctly shows `Mar 31, 2026`; no off-by-one rollover into April.

---

### TC-017 — Boundary: select Feb 29 in a leap year

**Category:** Boundary

**Preconditions:** Form Picker calendar overlay is open.

**Steps:**
1. Navigate to February 2028 (leap year).
2. Click day `29`.

**Expected Result:** Input shows `Feb 29, 2028`. Then repeat for February 2027 (non-leap) and verify day `29` is not present in the grid.

---

### TC-018 — Boundary: Range Picker with same start and end date

**Category:** Boundary

**Preconditions:** Range Picker calendar overlay is open.

**Steps:**
1. Click a date (e.g., April 15, 2026) as the start.
2. Click the exact same date again as the end.

**Expected Result:** The component accepts a single-day range and displays `Apr 15, 2026 - Apr 15, 2026` (or equivalent), with that single day highlighted.

---

### TC-019 — Boundary: Min Max Picker — exact min boundary date

**Category:** Boundary

**Preconditions:** Min Max Picker calendar is open and the min boundary date is identifiable (first non-greyed day).

**Steps:**
1. Click on the earliest selectable date (the min boundary).

**Expected Result:** The date is accepted and populates the input; no validation error.

---

### TC-020 — Boundary: Min Max Picker — exact max boundary date

**Category:** Boundary

**Preconditions:** Min Max Picker calendar is open and the max boundary date is identifiable (last non-greyed day).

**Steps:**
1. Click on the latest selectable date (the max boundary).

**Expected Result:** The date is accepted and populates the input; no validation error.

---

### TC-021 — Empty submission: leave all three pickers blank

**Category:** Validation

**Preconditions:** User is on the Datepicker page; no values entered.

**Steps:**
1. Do not interact with any of the three picker inputs.
2. Inspect the page state (no submit button is present, but check for validation cues on focus/blur).
3. Click into each input then click outside without selecting.

**Expected Result:** None of the inputs show a "required" error (since `required: false` per the JSON), and all three remain empty without page errors.

---

### TC-022 — Special characters typed into Form Picker input

**Category:** Negative

**Preconditions:** User is on the Datepicker page.

**Steps:**
1. Click into the "Form Picker" input.
2. Type special characters: `!@#$%^&*()`.
3. Blur the field.

**Expected Result:** Input is marked invalid; no date is parsed; no JS errors appear in the browser console.

---

### TC-023 — Sidebar navigation: Datepicker link is highlighted as active

**Category:** Navigation

**Preconditions:** User is on the Datepicker page.

**Steps:**
1. Inspect the left-side menu under "Forms".
2. Locate the "Datepicker" link.

**Expected Result:** "Datepicker" appears as the active/selected menu item (highlighted styling).

---

### TC-024 — Navigate from Datepicker to Form Layouts and back

**Category:** Navigation

**Preconditions:** User is on the Datepicker page.

**Steps:**
1. Click the "Form Layouts" link in the left sidebar.
2. Verify navigation to `/pages/forms/layouts`.
3. Use the browser Back button.

**Expected Result:** Browser returns to `/pages/forms/datepicker`; previously selected dates (if any) may or may not persist depending on component state, but the page renders without errors.

---

### TC-025 — Deep link directly to Datepicker page

**Category:** Navigation

**Preconditions:** Browser is at any other page (e.g., IoT Dashboard).

**Steps:**
1. Manually enter `http://localhost:4200/pages/forms/datepicker` in the address bar.
2. Press Enter.

**Expected Result:** The Datepicker page loads with all three picker inputs ("Form Picker", "Range Picker", "Min Max Picker") visible and functional.

---

### TC-026 — Theme toggle (Light button) does not break datepicker

**Category:** Positive

**Preconditions:** User is on the Datepicker page.

**Steps:**
1. Click the "Light" theme button in the header.
2. Switch to a different theme (e.g., Dark).
3. Open the "Form Picker" calendar.
4. Select a date.

**Expected Result:** Theme changes apply to the calendar overlay (colors update), and date selection continues to work without errors.

---

### TC-027 — Keyboard accessibility: open Form Picker with keyboard

**Category:** Positive

**Preconditions:** User is on the Datepicker page.

**Steps:**
1. Press Tab repeatedly until focus reaches the "Form Picker" input.
2. Press Enter or Space, or click the calendar icon button.
3. Use arrow keys / Tab inside the calendar (if supported) and press Enter on a date.

**Expected Result:** Focus indicators are visible, the calendar opens via keyboard, and a date can be committed without using the mouse.

---

### TC-028 — Reopening Form Picker shows previously selected date

**Category:** Positive

**Preconditions:** User has already selected a date in the "Form Picker" input.

**Steps:**
1. Note the currently selected date in the Form Picker input.
2. Click the input again to reopen the calendar.

**Expected Result:** The calendar opens to the month of the previously selected date, and that date is visually highlighted as the current selection.

---

### TC-029 — Page refresh clears all picker values

**Category:** Negative

**Preconditions:** User has selected dates in all three pickers.

**Steps:**
1. Confirm all three inputs show selected values.
2. Press F5 to refresh the page.

**Expected Result:** Page reloads and all three inputs ("Form Picker", "Range Picker", "Min Max Picker") return to empty placeholders; no values persist (mock app, no storage).

---

### TC-030 — External link "Akveo" opens correctly

**Category:** Navigation

**Preconditions:** User is on the Datepicker page.

**Steps:**
1. Locate the "Akveo" link in the page.
2. Click it.

**Expected Result:** Navigates to `https://akveo.page.link/8V2f` (typically opens in a new tab or same tab depending on link config) without breaking the Datepicker page state.
