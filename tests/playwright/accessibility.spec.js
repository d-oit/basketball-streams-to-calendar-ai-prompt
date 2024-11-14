import { test, expect } from '@playwright/test';

test.describe('Enhanced Accessibility and Keyboard Navigation', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3000');
  });

  test('ARIA attributes are correctly implemented in the accordion component', async ({ page }) => {
    const accordionTrigger = page.locator('button[aria-expanded]');
    await expect(accordionTrigger).toHaveAttribute('aria-expanded', 'false');

    await accordionTrigger.click();
    await expect(accordionTrigger).toHaveAttribute('aria-expanded', 'true');
  });

  test('Keyboard navigation works as expected', async ({ page }) => {
    const accordionTrigger = page.locator('button[aria-expanded]');

    // Focus on the accordion trigger
    await accordionTrigger.focus();
    await expect(accordionTrigger).toBeFocused();

    // Press Enter to open the accordion
    await page.keyboard.press('Enter');
    await expect(accordionTrigger).toHaveAttribute('aria-expanded', 'true');

    // Press Tab to move focus to the next element
    await page.keyboard.press('Tab');
    const textarea = page.locator('textarea');
    await expect(textarea).toBeFocused();

    // Press Shift+Tab to move focus back to the accordion trigger
    await page.keyboard.press('Shift+Tab');
    await expect(accordionTrigger).toBeFocused();

    // Press Enter to close the accordion
    await page.keyboard.press('Enter');
    await expect(accordionTrigger).toHaveAttribute('aria-expanded', 'false');
  });
});
