const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

async function renderHtmlToPdf(inputDir, outputDir) {
  const browser = await puppeteer.launch();

  try {
    // Ensure output directory exists
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
      console.log(`Created output directory: ${outputDir}`);
    }

    const files = fs.readdirSync(inputDir);

    for (const file of files) {
      if (path.extname(file).toLowerCase() === '.html') {
        const htmlFilePath = path.join(inputDir, file);
        const pdfFileName = file.replace('.html', '.pdf');
        const pdfFilePath = path.join(outputDir, pdfFileName);

        console.log(`Rendering ${htmlFilePath} to ${pdfFilePath}...`);

        const page = await browser.newPage();
        await page.goto(`file://${htmlFilePath}`, { waitUntil: 'networkidle0' });
        await page.pdf({ path: pdfFilePath, format: 'A4' });

        console.log(`Successfully rendered ${pdfFilePath}`);
      }
    }
  } catch (error) {
    console.error('An error occurred:', error);
  } finally {
    await browser.close();
    console.log('Browser closed.');
  }
}

// Command-line execution
const args = process.argv.slice(2);
if (args.length !== 2) {
  console.error('Usage: node script.js <inputDirectory> <outputDirectory>');
  process.exit(1);
}

const inputDirectory = args[0];
const outputDirectory = args[1];

renderHtmlToPdf(inputDirectory, outputDirectory);