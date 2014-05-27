import os

def populate():
    book_cat = add_cat('Books')

    add_page(cat=book_cat,
        title="Coding Bat",
        url="http://codingbat.com/")

    add_page(cat=book_cat,
        title="How to Think like a Computer Scientist",
        url="http://www.greenteapress.com/thinkpython/")

    add_page(cat=book_cat,
        title="Learn Python in 10 Minutes",
        url="http://www.korokithakis.net/tutorials/python/")

    compsci = add_cat("Computer Science")

    add_page(cat=compsci,
        title="Official Django Tutorial",
        url="https://docs.djangoproject.com/en/1.5/intro/tutorial01/")

    add_page(cat=compsci,
        title="Django Rocks",
        url="http://www.djangorocks.com/")

    add_page(cat=compsci,
        title="How to Tango with Django",
        url="http://www.tangowithdjango.com/")

    other_cat = add_cat("Other")

    add_page(cat=other_cat,
        title="View DNS",
        url="http://viewdns.info/")

    add_page(cat=other_cat,
        title="Unicode Table",
        url="http://unicode-table.com/")

    # Print out what we have added to the user.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print "- {0} - {1}".format(str(c), str(p))

def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title, url=url,
            views=views)[0]
    return p

def add_cat(name):
    c = Category.objects.get_or_create(name=name)[0]
    return c

# Start execution here!
if __name__ == '__main__':
    print "Starting Knowvi population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 
        'knowvi_project.settings')
    from knowvi.models import Category, Page
    populate()
