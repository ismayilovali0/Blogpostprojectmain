# Copilot Instructions for BlogPostProject2

## Architecture Overview
This is a Django 4.0.2 blog application with a single app `posts` handling blog functionality. Key components:
- **Models**: Post, Category, Tag, Author (User extension), Like/Favourite/Comment for interactions
- **Views**: Homepage (featured/latest posts), post detail with AJAX interactions, search, category/tag filtering
- **Templates**: Base template with Tailwind CSS + Alpine.js, custom markdown filter for content rendering
- **URLs**: Slug-based post URLs, AJAX endpoints for likes/favourites/comments

Data flow: Posts have many-to-many with Categories/Tags, users can like/favourite/comment via AJAX.

## Developer Workflows
- **Run server**: `python manage.py runserver`
- **Database**: `python manage.py makemigrations && python manage.py migrate`
- **Static files**: `python manage.py collectstatic` (collects to `static_cdn`)
- **Admin**: Access `/admin/` for content management
- **Debugging**: Use Django debug toolbar if installed; check `DEBUG=True` in settings

## Project Conventions
- **Slugs**: All models use SlugField for URL-friendly identifiers (e.g., Post.slug, Category.slug)
- **View counting**: Increment `post.view_count` on detail view load
- **AJAX interactions**: Use `@require_POST` decorators, return JsonResponse with status/counts
- **Markdown content**: Render post content with custom `markdown` template filter (supports fenced code)
- **Image handling**: Store in `media_cdn` (MEDIA_ROOT), serve via `/media/`
- **Authentication**: Use Django's built-in User model extended with Author profile_picture
- **Unique constraints**: Like/Favourite models have unique_together on (user, post)

## Key Files
- [posts/models.py](posts/models.py): Data models with relationships
- [posts/views.py](posts/views.py): Business logic, AJAX handlers
- [templates/base.html](templates/base.html): Layout with Tailwind/Alpine
- [posts/templatetags/markdown_extras.py](posts/templatetags/markdown_extras.py): Custom template tags
- [blogpost/settings.py](blogpost/settings.py): Config, static/media paths

## Dependencies
- Django 4.0.2, Markdown, Pillow (image handling)
- Tailwind CSS (CDN), Alpine.js (frontend interactions)

When adding features, follow existing patterns: use slugs for URLs, AJAX for dynamic updates, extend models with migrations.</content>
<parameter name="filePath">c:\Users\ali\Blogpostproject2\.github\copilot-instructions.md