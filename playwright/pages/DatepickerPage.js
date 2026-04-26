const { expect } = require('@playwright/test');

class DatepickerPage {
  constructor(page) {
    this.page = page;
    this.url = 'http://localhost:4200/pages/forms/datepicker';
    this.formPickerInput = page.getByPlaceholder('Form Picker');
    this.rangePickerInput = page.getByPlaceholder('Range Picker');
    this.minMaxPickerInput = page.getByPlaceholder('Min Max Picker');
    this.calendar = page.locator('nb-calendar, nb-calendar-range');
  }

  async goto() {
    await this.page.goto(this.url);
  }

  async openFormPicker() {
    await this.formPickerInput.click();
    await expect(this.page.locator('nb-calendar')).toBeVisible();
  }

  async openRangePicker() {
    await this.rangePickerInput.click();
    await expect(this.page.locator('nb-calendar-range')).toBeVisible();
  }

  async openMinMaxPicker() {
    await this.minMaxPickerInput.click();
    await expect(this.page.locator('nb-calendar')).toBeVisible();
  }

  formatDate(date) {
    const month = date.toLocaleString('en-US', { month: 'short' });
    const day = date.getDate();
    const year = date.getFullYear();
    return `${month} ${day}, ${year}`;
  }

  async selectDateFromToday(daysFromToday) {
    const date = new Date();
    date.setDate(date.getDate() + daysFromToday);
    const expectedMonthLong = date.toLocaleString('en-US', { month: 'long' });
    const expectedYear = date.getFullYear();
    const day = date.getDate().toString();

    await this.navigateToMonthYear(date);

    await this.page
      .locator('.day-cell:not(.bounding-month)')
      .getByText(day, { exact: true })
      .first()
      .click();

    return this.formatDate(date);
  }

  async selectDateRangeFromToday(startOffset, endOffset) {
    const startDate = new Date();
    startDate.setDate(startDate.getDate() + startOffset);
    const endDate = new Date();
    endDate.setDate(endDate.getDate() + endOffset);

    await this.navigateToMonthYear(startDate);
    await this.page
      .locator('.day-cell.range-cell:not(.bounding-month)')
      .getByText(startDate.getDate().toString(), { exact: true })
      .first()
      .click();

    await this.navigateToMonthYear(endDate);
    await this.page
      .locator('.day-cell.range-cell:not(.bounding-month)')
      .getByText(endDate.getDate().toString(), { exact: true })
      .first()
      .click();

    return `${this.formatDate(startDate)} - ${this.formatDate(endDate)}`;
  }

  async navigateToMonthYear(date) {
    const expectedMonthLong = date.toLocaleString('en-US', { month: 'long' });
    const expectedYear = date.getFullYear();
    const calendarHeader = this.page.locator('nb-calendar-view-mode').first();
    await expect(calendarHeader).toBeVisible();

    let headerText = (await calendarHeader.textContent()) || '';
    let safety = 0;
    while (!headerText.includes(`${expectedMonthLong} ${expectedYear}`) && safety < 24) {
      await this.page.locator('nb-calendar-pageable-navigation [data-name="chevron-right"]').click();
      headerText = (await calendarHeader.textContent()) || '';
      safety++;
    }
  }
}

module.exports = { DatepickerPage };