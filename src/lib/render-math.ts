import katex from 'katex';

/**
 * Renders LaTeX math expressions in text to HTML using KaTeX.
 * Processes both inline ($...$) and display ($$...$$) math.
 *
 * @param text - Text containing LaTeX expressions with quadruple-escaped backslashes
 * @returns HTML string with rendered math expressions
 */
export function renderMathInText(text: string): string {
  // Pattern matches both $...$ (inline) and $$...$$ (display) math
  // Non-greedy matching to handle multiple expressions in one string
  const mathPattern = /\$\$(.+?)\$\$|\$(.+?)\$/g;

  return text.replace(mathPattern, (match, display, inline) => {
    const latex = display || inline;
    const displayMode = !!display;

    try {
      // Convert quadruple backslashes to single for KaTeX
      // JSON storage requires \\\\mathrm -> \mathrm for LaTeX
      const normalizedLatex = latex.replace(/\\\\/g, '\\');

      return katex.renderToString(normalizedLatex, {
        displayMode,
        throwOnError: false,
        output: 'html',
        trust: false, // Security: don't allow arbitrary HTML
        strict: 'warn' // Warn on unknown commands but continue
      });
    } catch (error) {
      console.error('KaTeX rendering error for:', latex, error);
      return match; // Return original text if rendering fails
    }
  });
}