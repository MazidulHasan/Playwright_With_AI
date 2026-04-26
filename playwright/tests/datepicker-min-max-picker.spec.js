const { test, expect } = require('@playwright/test');
const { DatepickerPage } = require('../pages/DatepickerPage');

test.describe('Min Max Picker datepicker', () => {
  test('opens the calendar when input is clicked', async ({ page }) => {
    const datepicker = new DatepickerPage(page);
    await datepicker.goto();
    await datepicker.openMinMaxPicker();
    await expect(page.locator('nb-calendar')).toBeVisible();
  });

  test('disables dates outside the allowed min/max range', async ({ page }) => {
    const datepicker = new DatepickerPage(page);
    await datepicker.goto();
    await datepicker.openMinMaxPicker();
    const disabledCells = page.locator('.day-cell.disabled');
    await expect(disabledCells.first()).toBeVisible();
  });

  test('only one min-max calendar is visible at a time', async ({ page }) => {
    const datepicker = new DatepickerPage(page);
    await datepicker.goto();
    await datepicker.openMinMaxPicker();
    await expect(page.locator('nb-calendar')).toHaveCount(1);
  });
});