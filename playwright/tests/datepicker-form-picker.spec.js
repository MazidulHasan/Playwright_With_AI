const { test, expect } = require('@playwright/test');
const { DatepickerPage } = require('../pages/DatepickerPage');

test.describe('Form Picker datepicker', () => {
  test('opens the calendar when input is clicked', async ({ page }) => {
    const datepicker = new DatepickerPage(page);
    await datepicker.goto();
    await datepicker.openFormPicker();
    await expect(page.locator('nb-calendar')).toBeVisible();
  });

  test('selects a future date and populates the input', async ({ page }) => {
    const datepicker = new DatepickerPage(page);
    await datepicker.goto();
    await datepicker.openFormPicker();
    const expected = await datepicker.selectDateFromToday(7);
    await expect(datepicker.formPickerInput).toHaveValue(expected);
  });

  test('selects today and populates the input', async ({ page }) => {
    const datepicker = new DatepickerPage(page);
    await datepicker.goto();
    await datepicker.openFormPicker();
    const expected = await datepicker.selectDateFromToday(0);
    await expect(datepicker.formPickerInput).toHaveValue(expected);
  });
});