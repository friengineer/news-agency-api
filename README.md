# News Agency API
An API for creating, viewing and deleting news stories.

Supported story categories are below.
- `pol`: politics
- `art`: art
- `tech`: technology
- `trivia`: trivial

Supported story regions are below.
- `uk`: United Kingdom
- `eu`: European
- `w`: world

## Usage
### Login
Log in to an account.

Accepts HTTP POST requests containing a JSON payload with the following fields: `username`, `password`.

#### Path
`/Login`

### Logout
Log out of the current session.

Accepts HTTP POST requests.

#### Path
`/Logout`

### Create Story
Create a news story. Requires being logged in.

Accepts HTTP POST requests containing a JSON payload with the following fields: `headline`, `category`, `region`, `details`.

#### Path
`/CreateStory`

### List Stories
List all stories.

Accepts HTTP GET requests containing a JSON payload with the following fields: `story_cat`, `story_region`, `story_date`. `story_date` must be supplied in the format dd/mm/yyyy.

Returns a HTTP response containing a JSON payload with the field `stories` containing a JSON array of stories.

#### Path
`/ListStories`

### Delete Story
Delete the specified news story. Requires being logged in.

Accepts HTTP POST requests containing a JSON payload with the following field: `story_key`.

#### Path
`/DeleteStory`

## Running the API development server
Create a Python virtual environment (venv) with your desired name. Start the virtual environment and install the requirements by running the following commands remembering to substitute the name of your venv.
```shell
$ source <venv name>/bin/activate
$ pip install -r requirements.txt
```

To execute the program in development mode, start the virtual environment and run the following command.
```shell
$ python manage.py runserver
```

If you would like to access the admin web portal, navigate to where the server is being hosted and append `/admin` to the URL.
