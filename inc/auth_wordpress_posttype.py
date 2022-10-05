import os
import logging
import apie
import requests
import json
import re
from urllib.parse import urlparse

# Use the Eons Infrastructure Technologies website to authenticate api requests.
class wordpress_posttype(apie.Authenticator):
    def __init__(this, name="EIT Internal Authenticator"):
        super().__init__(name)

        this.staticKWArgs.append('wp_url')
        this.requiredKWArgs.append('post_ids')
        this.optionalKWArgs['allow_public'] = False

    def UserFunction(this):
        this.request['method'] = 'GET'
        this.request['data'] = {}
        del this.request['files']

        posts = requests.request(**this.request)
        if (posts.status_code != 200):
            logging.debug(f"Failed to get {this.request['url']} with {this.request['headers']}.")
            return False

        postsJson = json.loads(posts.text)

        if (this.allow_public and len(postsJson)):
            allow_public_access = True
            for post in postsJson:
                if (post['status'] != "publish"):
                    allow_public_access = False
                    break
            if (allow_public_access):
                logging.debug(f"Allowing anonymous access to the public posts at {this.request['url']}.")
                return True

        if (not len(postsJson)):
            logging.debug(f"No content retrieved from {this.request['url']}; trying again with private posts")
            this.request['url'] += "&status=private"
            posts = requests.request(**this.request)
            postsJson = json.loads(posts.text)

            if (posts.status_code != 200):
                logging.debug(f"Failed to get {this.request['url']} with {this.request['headers']}.")
                return False

            # Wordpress will simply not reply if a post is private, so this is as valid a 401 as a 404.
            if (not len(postsJson)):
                logging.debug(f"Could not access content at {this.request['url']} with {this.request['headers']}")
                return False

        user = requests.request("GET", f"{this.wp_url}/users/me", headers=this.request['headers'], data={})
        if (user.status_code != 200):
            logging.debug(f"Failed to get user with {this.request['headers']}")
            return False

        userJson = json.loads(user.text)

        userPostIds = eval(f"userJson{this.post_ids}")

        for post in postsJson:
            if (post['id'] not in userPostIds):
                logging.debug(f"Access forbidden to {this.request['url']} with {this.request['headers']}")
                return False

        logging.debug(f"Allowing access to {this.request['url']} with {this.request['headers']}")
        return True

