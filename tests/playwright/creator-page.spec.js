import { test, expect } from '@playwright/test';

test.describe('Textarea Content Persistence', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3000');
  });

  test('Textarea content is saved and loaded correctly', async ({ page }) => {
    const textarea = page.locator('textarea');

    // Enter text into the textarea
    await textarea.fill('Test content');
    await expect(textarea).toHaveValue('Test content');

    // Reload the page
    await page.reload();

    // Check if the textarea content is still there
    await expect(textarea).toHaveValue('Test content');
  });
});
