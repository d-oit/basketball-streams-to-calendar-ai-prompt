import { test, expect } from '@playwright/test';

test.describe('Accordion Functionality', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3000');
  });

  test('Accordion state is persistent across page reloads', async ({ page }) => {
    // Open the accordion
    await page.click('text=Basketball live streams Input');
    await expect(page.locator('text=Enter basketball live stream text here...')).toBeVisible();

    // Reload the page
    await page.reload();

    // Check if the accordion is still open
    await expect(page.locator('text=Enter basketball live stream text here...')).toBeVisible();
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
