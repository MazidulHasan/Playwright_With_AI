const { test, expect } = require('@playwright/test');
const { DatepickerPage } = require('../pages/DatepickerPage');

test.describe('Range Picker datepicker', () => {
  test('opens the range calendar when input is clicked', async ({ page }) => {
    const datepicker = new DatepickerPage(page);
    await datepicker.goto();
    await datepicker.openRangePicker();
    await expect(page.locator('nb-calendar-range')).toBeVisible();
  });

  test('selects a date range spanning a week', async ({ page }) => {
    const datepicker = new DatepickerPage(page);
    await datepicker.goto();
    await datepicker.openRangePicker();
    const expected = await datepicker.selectDateRangeFromToday(2, 9);
    await expect(datepicker.rangePickerInput).toHaveValue(expected);
  });
});