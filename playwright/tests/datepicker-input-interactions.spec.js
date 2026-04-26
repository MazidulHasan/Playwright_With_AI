const { test, expect } = require('@playwright/test');
const { DatepickerPage } = require('../pages/DatepickerPage');

test.describe('Datepicker input interactions', () => {
  test('opening one picker does not populate other inputs', async ({ page }) => {
    const datepicker = new DatepickerPage(page);
    await datepicker.goto();
    await datepicker.openFormPicker();
    const expected = await datepicker.selectDateFromToday(3);
    await expect(datepicker.formPickerInput).toHaveValue(expected);
    await expect(datepicker.rangePickerInput).toHaveValue('');
    await expect(datepicker.minMaxPickerInput).toHaveValue('');
  });

  test('inputs accept focus independently', async ({ page }) => {
    const datepicker = new DatepickerPage(page);
    await datepicker.goto();
    await datepicker.formPickerInput.focus();
    await expect(datepicker.formPickerInput).toBeFocused();
    await datepicker.rangePickerInput.focus();
    await expect(datepicker.rangePickerInput).toBeFocused();
  });
});