/**
 * Utility functions for research page management
 */

/**
 * Filters research projects based on published status
 * In development: returns all projects (including unpublished)
 * In production: returns only published projects
 *
 * @param projects - Array of research projects with optional published field
 * @returns Filtered array of projects
 */
export function filterPublishedProjects<T extends { published?: boolean }>(
    projects: T[]
): T[] {
    const isDev = process.env.NODE_ENV === 'development';

    // In development, show all projects for testing
    if (isDev) {
        return projects;
    }

    // In production, only show published projects (default to true if not specified)
    return projects.filter(project => project.published !== false);
}
