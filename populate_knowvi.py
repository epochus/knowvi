import os

def populate():

    collect_cat = add_cat('Collections')
    add_page(cat=collect_cat,
        title="Over API",
        url="http://overapi.com/")
    add_page(cat=collect_cat,
        title="Cheatography",
        url="http://www.cheatography.com/")

    compsci = add_cat("Computer Science")
    add_page(cat=compsci,
        title="Computer Science Field Guide",
        url="https://c.canterbury.ac.nz/csfieldguide/")

    dict_cat = add_cat("Dictionary")
    add_page(cat=dict_cat,
        title="OneLook Dictionary Search",
        url="http://www.onelook.com/")
    add_page(cat=dict_cat,
        title="Webopedia",
        url="http://www.webopedia.com/")

    lang_cat = add_cat("Languages")
    add_page(cat=lang_cat,
        title="Free Language Learning Resources",
        url="http://www.universitiesandcolleges.org/blog/language-learning-resources/")

    lit_cat = add_cat("Literacy")
    add_page(cat=lit_cat,
        title="Gorilla Paper",
        url="http://pages.uscd.edu/~dkjordan/resources/gorillapaper/gorilla.html/")


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
