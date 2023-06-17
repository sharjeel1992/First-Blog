from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


def data_loader():
    """
    This function opens the json file and returns the data in it
    """
    with open('data.json', 'r') as json_file:
        data = json.load(json_file)
    return data


@app.route('/')
def index():
    """
    This function renders the data from json file to a html file.This function also
    serves as our main route
    """
    data = data_loader()
    return render_template('index.html', post=data)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
     This function provides another route called add, and also make sure that request method
     is only post and will get user inputs at add route and will add them to our json database
      and also redirect the route to the main page.
      """
    if request.method == 'POST':
        unique_id = request.form.get('ID')
        title = request.form.get('Title')
        author = request.form.get('Author')
        content = request.form.get('Content')
        new_post = {
            'id': int(unique_id),
            'Title': title,
            'author': author,
            'content': content
        }
        data = data_loader()
        data.append(new_post)
        with open("data.json", "w") as update_file:
            json.dump(data, update_file, indent=4)
        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete_post(post_id):
    """
    This functions takes an int as argument.Removes the item from the database based on user input.
    Update the main database that is json file and redirects to the main page
    """
    data = data_loader()
    for item in data:
        if item['id'] == post_id:
            data.remove(item)
            break
    with open("data.json", "w") as update_file:
        json.dump(data, update_file, indent=4)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update_post(post_id):
    """This function also takes an int argument as unique ID set with each blog post.This function
       handles both get and post requests in different ways.update the database and redirect to the main page
       """
    blog_posts = data_loader()
    if request.method == 'GET':
        for post in blog_posts:
            if post['id'] == post_id:
                return render_template('update.html', post=post)
        return redirect('/')
    elif request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']
        for post in blog_posts:
            if post['id'] == post_id:
                post['Title'] = title
                post['author'] = author
                post['content'] = content
                break
        with open("data.json", "w") as update_file:
            json.dump(blog_posts, update_file, indent=4)
        return redirect('/')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(debug=True)
