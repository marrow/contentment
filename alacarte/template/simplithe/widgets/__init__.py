# encoding: utf-8

from base import *
from layout import *
from field import *



if __name__ == '__main__':
    from alacarte.template.simplithe import html5 as tag
    
    def test1():
        search = Form('site-search', action='/search', method='get', children=[
                SearchField('q', autofocus=True, autocomplete="on", placeholder="Site-wide search.")
            ])
    
        login = Form('sign-in', class_="tabbed", action='/users/action:authenticate', children=[
                HiddenField('referrer'),
                FieldSet('local', "Local Users", TableLayout, [
                        TextField('identity', "User Name"),
                        PasswordField('password', "Password")
                    ]),
                FieldSet('openid', "OpenID Users", TableLayout, [
                        URLField('url', "OpenID URL")
                    ])
            ], footer=SubmitFooter('form', "Sign In"))
    
    
        contact = Form('contact', action="/contact", children=[
                FieldSet('contact', "Send us a Message", DefinitionListLayout, [
                        TextField('name', "Your Name", required=True, autofocus=True),
                        EmailField('email', "Your E-Mail Address", required=True),
                        PhoneField('phone', "Your Phone Number"),
                        TextArea('details', "Details")
                    ])
            ], footer=SubmitFooter('form', "Send Message"))
    
        select = SelectField('myselect', values=[
                (None, 'Default Template'),
                ("Custom Templates", [
                        ('home', "Homepage"),
                        ('contact', "Contact Form")
                    ])
            ])
    
        select2 = SelectField('select2', size=10, values=[
                (None, 'Default Template'),
                ("Custom Templates", [
                        ('home', "Homepage"),
                        ('contact', "Contact Form")
                    ])
            ])
    
        page = tag.html [
                tag.head [
                        tag.meta ( charset = "utf-8" ),
                        tag.title [ "Example Widgets" ]
                    ],
            
                tag.body [
                        tag.h1 [ "Example Widgets" ],
                    
                        tag.h2 [ "Search" ],
                        search(),
                    
                        tag.h2 [ "Login" ],
                        login(),
                    
                        tag.h2 [ "Contact" ],
                        contact(),
                    
                        tag.h2 [ "Select Fields" ],
                    
                        tag.h3 [ "Raw Select" ],
                        select(),
                    
                        tag.h3 [ "Raw Select w/ Data" ],
                        select({'myselect': 'home'}),
                    
                        tag.h3 [ "Raw Select, Large" ],
                        select2()
                    ]
            ]
    
        print unicode(page)
    
    test1()
