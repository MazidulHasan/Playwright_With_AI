const { test, expect } = require('@playwright/test');
const { DatepickerPage } = require('../pages/DatepickerPage');

test.describe('Datepicker page load', () => {
  test('loads the datepicker page with correct URL', async ({ page }) => {
    const datepicker = new DatepickerPage(page);
    await datepicker.goto();
    await expect(page).toHaveURL(/.*\/pages\/forms\/datepicker/);
  });

  test('renders all three datepicker inputs', async ({ page }) => {
    const datepicker = new DatepickerPage(page);
    await datepicker.goto();
    await expect(datepicker.formPickerInput).toBeVisible();
    await expect(datepicker.rangePickerInput).toBeVisible();
    await expect(datepicker.minMaxPickerInput).toBeVisible();
  });

  test('all datepicker inputs are empty by default', async ({ page }) => {
    const datepicker = new DatepickerPage(page);
    await datepicker.goto();
    await expect(datepicker.formPickerInput).toHaveValue('');
    await expect(datepicker.rangePickerInput).toHaveValue('');
    await expect(datepicker.minMaxPickerInput).toHaveValue('');
  });
});