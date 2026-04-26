const { test, expect } = require('@playwright/test');
const { NavigationPage } = require('../pages/NavigationPage');
const { DatepickerPage } = require('../pages/DatepickerPage');

test.describe('Datepicker page navigation', () => {
  test('navigates to datepicker page directly', async ({ page }) => {
    const nav = new NavigationPage(page);
    await nav.gotoDatepicker();
    const datepicker = new DatepickerPage(page);
    await expect(datepicker.formPickerInput).toBeVisible();
  });

  test('page title contains the application name', async ({ page }) => {
    const datepicker = new DatepickerPage(page);
    await datepicker.goto();
    await expect(page).toHaveTitle(/playwright-test-admin/);
  });
});