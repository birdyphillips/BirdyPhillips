"""Blog/Essay route handlers."""
from flask import Blueprint, render_template, abort
import os
import markdown
import yaml
from datetime import datetime

blog = Blueprint('blog', __name__)

# Path to essays
CONTENT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'content', 'essays')


def parse_essay(filename):
    """Parse essay markdown file with frontmatter."""
    filepath = os.path.join(CONTENT_DIR, filename)
    
    if not os.path.exists(filepath):
        return None
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split frontmatter and content
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = yaml.safe_load(parts[1])
            md_content = parts[2].strip()
        else:
            frontmatter = {}
            md_content = content
    else:
        frontmatter = {}
        md_content = content
    
    # Convert markdown to HTML
    html_content = markdown.markdown(md_content, extensions=['fenced_code', 'codehilite', 'tables'])
    
    return {
        'filename': filename,
        'slug': filename.replace('.md', ''),
        'title': frontmatter.get('title', 'Untitled'),
        'date': frontmatter.get('date', datetime.now()),
        'author': frontmatter.get('author', 'BirdyPhillips'),
        'tags': frontmatter.get('tags', []),
        'published': frontmatter.get('published', True),
        'content': html_content
    }


def get_all_essays():
    """Get all published essays sorted by date."""
    if not os.path.exists(CONTENT_DIR):
        return []
    
    essays = []
    for filename in os.listdir(CONTENT_DIR):
        if filename.endswith('.md'):
            essay = parse_essay(filename)
            if essay and essay['published']:
                essays.append(essay)
    
    # Sort by date, newest first
    essays.sort(key=lambda x: x['date'], reverse=True)
    return essays


@blog.route('/blog')
def blog_index():
    """Blog listing page."""
    essays = get_all_essays()
    return render_template('blog/index.html', essays=essays)


@blog.route('/blog/<slug>')
def blog_post(slug):
    """Individual blog post page."""
    filename = slug if slug.endswith('.md') else f"{slug}.md"
    essay = parse_essay(filename)
    
    if not essay or not essay['published']:
        abort(404)
    
    return render_template('blog/post.html', essay=essay)
