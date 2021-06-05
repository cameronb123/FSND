# Frontend - Full Stack Trivia API 

### Getting Setup

> _tip_: this frontend is designed to work with [Flask-based Backend](../backend). It is recommended you stand up the backend first, test using Postman or curl, update the endpoints in the frontend, and then the frontend should integrate smoothly.

### Installing Dependencies

1. **Installing Node and NPM**<br>
This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

2. **Installing project dependencies**<br>
This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:
```bash
npm install
```
>_tip_: **npm i** is shorthand for **npm install**

# Required Tasks

### Running Your Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file. 

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.<br>

```bash
npm start
```

### Request Formatting

The frontend should be fairly straightforward and disgestible. You'll primarily work within the ```components``` folder in order to understand, and if you so choose edit, the endpoints utilized by the components. While working on your backend request handling and response formatting, you can reference the frontend to view how it parses the responses. 

After you complete your endpoints, ensure you return to the frontend to confirm your API handles requests and responses appropriately: 
- Endpoints defined as expected by the frontend
- Response body provided as expected by the frontend 

### Optional: Updating Endpoints and API behavior

Would you rather the API had different behavior - different endpoints, return the response body in a different format? Go for it! Make the updates to your API and the corresponding updates to the frontend so it works with your API seamlessly. 


### Optional: Styling

In addition, you may want to customize and style the frontend by editing the CSS in the ```stylesheets``` folder. 

### Optional: Game Play Mechanics

Currently, when a user plays the game they play up to five questions of the chosen category. If there are fewer than five questions in a category, the game will end when there are no more questions in that category. 

You can optionally update this game play to increase the number of questions or whatever other game mechanics you decide. Make sure to specify the new mechanics of the game in the README of the repo you submit so the reviewers are aware that the behavior is correct. 

### Error Handling

Errors are returned as JSON objects in the following format:
```js
{
    'success': false,
    'error': 404,
    'message': 'resource not found'
}
```
The API will return five error types when requests fail:
- 400: Bad request
- 404: Resource not found
- 405: Method not allowed
- 422: Unprocessable
- 500: Internal server error

### Endpoints

```js
GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: A success message, an object with a single key, categories, that contains an object of id: category_string key:value pairs, and the total number of categories. 
{
    'success': true,
    'categories': { '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" },
    'total_categories': 6
}
```


```js
GET '/questions?page=${integer}'
- Fetches a paginated set of questions, a total number of questions, and all categories. 
- Request Arguments: page - integer
- Returns: A success message, an object with 10 paginated questions, total questions, and object including all categories
{
    'success': true,
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 2
        },
    ],
    'total_questions': 100,
    'categories': { '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" }
}
```

```js
GET '/categories/${id}/questions'
- Fetches questions for a cateogry specified by id request argument 
- Request Arguments: id - integer
- Returns: A success message, an object with questions for the specified category, total questions in that category, and current category string 
{
    'success': true,
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 4
        },
    ],
    'total_questions': 100,
    'current_category': 'History'
}
```

```js
DELETE '/questions/${id}'
- Deletes a specified question using the id of the question
- Request Arguments: id - integer
- Returns: A success message, the id of the deleted question, an object with the remaining questions paginated, and the new total number of questions
{
    'success': true,
    'deleted': 15,
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 2
        },
    ],
    'total_questions': 100
}
```

```js
POST '/quizzes'
- Sends a post request in order to get the next question 
- Request Body: 
{'previous_questions':  an array of question id's such as [1, 4, 20, 15]
'quiz_category': a string of the current category }
- Returns: a success message and a single new question object 
{
    'success': true,
    'question': {
        'id': 1,
        'question': 'This is a question',
        'answer': 'This is an answer', 
        'difficulty': 5,
        'category': 4
    }
}
```

```js
POST '/questions'
- Sends a post request in order to add a new question
- Request Body: 
{
    'question':  'Heres a new question string',
    'answer':  'Heres a new answer string',
    'difficulty': 1,
    'category': 3
}
- Returns: a success message, the id of the new question, an object with 10 paginated questions, and the new total number of questions
{
    'success': true,
    'created': 28,
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 2
        },
    ],
    'total_questions': 101
}
```

```js
POST '/questions/search'
- Sends a post request in order to search for a specific question by search term 
- Request Body: 
{
    'searchTerm': 'this is the term the user is looking for'
}
- Returns: a success message, an array of questions and the number of questions that met the search term
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 5
        },
    ],
    'total_questions': 100
}
```
