const { expect } = require('@playwright/test');

class NavigationPage {
  constructor(page) {
    this.page = page;
    this.formsMenu = page.getByRole('link', { name: 'Forms', exact: true });
    this.datepickerLink = page.getByRole('link', { name: 'Datepicker', exact: true });
    this.formLayoutsLink = page.getByRole('link', { name: 'Form Layouts', exact: true });
    this.iotDashboardLink = page.getByRole('link', { name: 'IoT Dashboard', exact: true });
  }

  async gotoDatepicker() {
    await this.page.goto('http://localhost:4200/pages/forms/datepicker');
  }

  async navigateViaSidebar() {
    if (await this.datepickerLink.isVisible().catch(() => false)) {
      await this.datepickerLink.click();
    } else {
      await this.formsMenu.click();
      await this.datepickerLink.click();
    }
  }
}

module.exports = { NavigationPage };