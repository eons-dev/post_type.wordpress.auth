# Wordpress Post Type Authenticator for APIE

Use the Wordpress json api to check if a user has access to a particular post type.

Built for use with the [Application Program Interface with Eons](https://github.com/eons-dev/bin_apie)


## Arguments

`post_ids` is required, see [below](#Identify-post-id-in-json-api) for how to set.

In addition to `post_ids`, you must also set:
 * `wp_url` - the url to query (e.g. "http://localhost:8080/wp-json/wp/v2")

You may additionally set:
 * `allow_public` - will cause this to return true if the requested posts are of the "publish" status (use this)

## Prerequisites

This Authenticator does require some setup to use properly.


### Required URLs

This Authenticator must be given a valid Wordpress post type url in `this.request.url`. The `request` should be populated by APIE or an Endpoint, so all you need to ensure is that this is positioned such that only calls to a Wordpress api are made.

This is best used as an argument (i.e. `authenticator`) to the `api_external` Endpoint included with apie. 


### Create Custom User Fields

This Authenticator requires [Advanced Custom Fields](https://www.advancedcustomfields.com/), [Pods](https://pods.io/), or some other user-extending field addition.

You must extend the default Wordpress user and add a list-compatible field which contains references the ids of the post type you would like to check. It is also required that you keep this custom field up to date.


### Identify Post Id in JSON API

For example, an authenticated query to https://infrastructure.tech/wp-json/wp/v2/users/me might yield the following:

```json
{
    "avatar_urls": {
    },
    "_links": {
        "collection": [
            {
                "href": "https://infrastructure.tech/wp-json/wp/v2/users"
            }
        ],
        "acf:post": [
            {
                "embeddable": true,
                "href": "https://infrastructure.tech/wp-json/wp/v2/api_endpoint/900"
            },
            {
                "embeddable": true,
                "href": "https://infrastructure.tech/wp-json/wp/v2/package/842"
            }
        ],
        "self": [
            {
                "href": "https://infrastructure.tech/wp-json/wp/v2/users/1"
            }
        ]
    },
    "description": "",
    "acf": {
        "packages": [
            842
        ],
        "api_endpoints": [
            900
        ]
    },
    "id": 1,
    "link": "https://infrastructure.tech/author/nope/",
    "meta": [],
    "slug": "nope",
    "name": "NO",
    "url": ""
}
```

Note that the `['acf']['packages']` and `['acf']['api_endpoints']` both yield post ids. This is true, even though the acf relationship field is set to return the post object.

Once you've identified the json key(s) which produce the list of post ids you'd like to compare against, simply set that string, exactly as is, as `'post_ids'`. For example, in your apie.json, you could add:
```json
"post_ids": "['acf']['packages']"
```

### User Permissions

If you would like users to be able to create, read, and share private posts in addition to published ones, they must have the following Wordpress capabilities:
* `edit_posts`
* `edit_others_posts` (for sharing)
* `edit_published_posts`
* `publish_posts`
* `read`
* `delete_posts`
* `delete_published_posts`
* `delete_private_posts` (for private)
* `edit_private_posts` (for private)
* `read_private_posts`(for private)
