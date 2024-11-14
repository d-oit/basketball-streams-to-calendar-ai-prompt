import { test, expect } from '@playwright/test';

test.describe('New Button Functionality', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3000');
  });

  test('New button clears the input livestream textarea', async ({ page }) => {
    const textarea = page.locator('textarea');
    const newButton = page.locator('button:has-text("New")');

    // Enter text into the textarea
    await textarea.fill('Test content');
    await expect(textarea).toHaveValue('Test content');

    // Click the New button
    await newButton.click();

    // Check if the textarea content is cleared
    await expect(textarea).toHaveValue('');
  });
});
