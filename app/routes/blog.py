"""Blog/Essay route handlers."""
from flask import Blueprint, render_template, abort, request, redirect, url_for, flash, session
import os
import markdown
import yaml
from datetime import datetime
import re

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
    html_content = markdown.markdown(
        md_content, 
        extensions=[
            'fenced_code', 
            'codehilite', 
            'tables',
            'nl2br',  # Convert newlines to <br> tags
            'sane_lists'  # Better list handling
        ]
    )
    
    # Normalize date to datetime object
    date_value = frontmatter.get('date', datetime.now())
    if isinstance(date_value, str):
        try:
            # Try parsing common date formats
            date_value = datetime.strptime(date_value, '%Y-%m-%d')
        except ValueError:
            try:
                date_value = datetime.strptime(date_value, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                date_value = datetime.now()
    elif not isinstance(date_value, datetime):
        # If it's a date object, convert to datetime
        try:
            date_value = datetime.combine(date_value, datetime.min.time())
        except:
            date_value = datetime.now()
    
    return {
        'filename': filename,
        'slug': filename.replace('.md', ''),
        'title': frontmatter.get('title', 'Untitled'),
        'date': date_value,
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


@blog.route('/blog/new', methods=['GET', 'POST'])
def new_post():
    """Create a new blog post (admin only)."""
    if 'logged_in' not in session or not session['logged_in']:
        flash('Please login first to create blog posts.', 'error')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        tags = request.form.get('tags', '').strip()
        published = request.form.get('published') == 'on'
        
        if not title or not content:
            flash('Title and content are required.', 'error')
            return redirect(request.url)
        
        # Create slug from title
        slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
        date_str = datetime.now().strftime('%Y-%m-%d')
        filename = f"{date_str}-{slug}.md"
        
        # Parse tags
        tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
        
        # Create frontmatter
        frontmatter = {
            'title': title,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'author': session.get('username', 'BirdyPhillips'),
            'tags': tag_list,
            'published': published
        }
        
        # Create file content
        file_content = f"---\n{yaml.dump(frontmatter, default_flow_style=False)}---\n\n{content}"
        
        # Save file
        os.makedirs(CONTENT_DIR, exist_ok=True)
        filepath = os.path.join(CONTENT_DIR, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(file_content)
        
        flash(f'✓ Blog post "{title}" created successfully!', 'success')
        return redirect(url_for('blog.blog_index'))
    
    return render_template('blog/new.html')


@blog.route('/blog/edit/<slug>', methods=['GET', 'POST'])
def edit_post(slug):
    """Edit an existing blog post (admin only)."""
    if 'logged_in' not in session or not session['logged_in']:
        flash('Please login first to edit blog posts.', 'error')
        return redirect(url_for('auth.login'))
    
    # Find the markdown file
    filename = slug if slug.endswith('.md') else f"{slug}.md"
    
    # Try to find the file (may have date prefix)
    essay_file = None
    for file in os.listdir(CONTENT_DIR):
        if file.endswith(filename) or file == filename:
            essay_file = file
            break
    
    if not essay_file:
        flash(f'Blog post "{slug}" not found.', 'error')
        return redirect(url_for('blog.blog_index'))
    
    filepath = os.path.join(CONTENT_DIR, essay_file)
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        tags = request.form.get('tags', '').strip()
        published = request.form.get('published') == 'on'
        
        if not title or not content:
            flash('Title and content are required.', 'error')
            return redirect(request.url)
        
        # Parse tags
        tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
        
        # Parse existing file to get original date
        essay = parse_essay(essay_file)
        original_date = essay['date'].strftime('%Y-%m-%d') if essay else datetime.now().strftime('%Y-%m-%d')
        
        # Create frontmatter
        frontmatter = {
            'title': title,
            'date': original_date,
            'author': session.get('username', 'BirdyPhillips'),
            'tags': tag_list,
            'published': published
        }
        
        # Create file content
        file_content = f"---\n{yaml.dump(frontmatter, default_flow_style=False)}---\n\n{content}"
        
        # Save file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(file_content)
        
        flash(f'✓ Blog post "{title}" updated successfully!', 'success')
        return redirect(url_for('blog.blog_index'))
    
    # GET request - load existing content
    essay = parse_essay(essay_file)
    if not essay:
        flash(f'Error reading blog post "{slug}".', 'error')
        return redirect(url_for('blog.blog_index'))
    
    # Get raw content (without HTML conversion)
    with open(filepath, 'r', encoding='utf-8') as f:
        file_content = f.read()
    
    # Split frontmatter and content
    parts = file_content.split('---', 2)
    raw_content = parts[2].strip() if len(parts) > 2 else ''
    
    return render_template('blog/edit.html', 
                         essay=essay, 
                         raw_content=raw_content,
                         tags_str=', '.join(essay['tags']))
