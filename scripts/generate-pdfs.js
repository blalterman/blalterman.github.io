const fs = require('fs');
const path = require('path');
const { getDocument } = require('pdfjs-dist/legacy/build/pdf.js');

async function convertPdfToHtml(inputDir, outputDir) {
  // Ensure output directory exists
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
    console.log(`Created output directory: ${outputDir}`);
  }

  try {
    const files = fs.readdirSync(inputDir).filter(file => path.extname(file).toLowerCase() === '.pdf');

    for (const file of files) {
      const pdfFilePath = path.join(inputDir, file);
      const htmlFileName = file.replace('.pdf', '.html');
      const htmlFilePath = path.join(outputDir, htmlFileName);

      console.log(`Converting ${pdfFilePath} to ${htmlFilePath}...`);

      const data = new Uint8Array(fs.readFileSync(pdfFilePath));
      const loadingTask = getDocument({ data });
      const pdfDocument = await loadingTask.promise;

      let htmlContent = `<!DOCTYPE html>\n<html>\n<head>\n<meta charset="utf-8">\n<title>${path.parse(file).name}</title>\n</head>\n<body>\n`;

      for (let i = 1; i <= pdfDocument.numPages; i++) {
        const page = await pdfDocument.getPage(i);
        const textContent = await page.getTextContent();

        // Basic conversion: Extract text content and wrap in paragraphs
        // Note: This is a very basic conversion. More sophisticated HTML
        // generation would require analyzing layout, images, etc.
        textContent.items.forEach(item => {
          if (item.str) {
            htmlContent += `<p>${item.str}</p>\n`;
          }
        });

        page.cleanup(); // Release page resources
      }

      htmlContent += `</body>\n</html>`;

      fs.writeFileSync(htmlFilePath, htmlContent);

      console.log(`Successfully converted ${pdfFilePath} to ${htmlFilePath}`);
    }

    console.log('All PDF files processed.');
  } catch (error) {
    console.error('An error occurred:', error);
  }
}

// Command-line execution
const args = process.argv.slice(2);
if (args.length !== 2) {
  console.error(`Usage: node ${path.basename(__filename)} <inputDirectory> <outputDirectory>`);
  process.exit(1);
}

const inputDirectory = args[0];
const outputDirectory = args[1];

convertPdfToHtml(inputDirectory, outputDirectory).catch(error => {
  console.error('Unhandled error during PDF to HTML conversion:', error);
  process.exit(1);
});