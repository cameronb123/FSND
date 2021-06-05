import os
from flask import Flask, json, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
  # get the desired page number from the request (default is 1)
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  # get the questions on the current page
  questions = [question.format() for question in selection]
  current_qs = questions[start:end]

  return current_qs

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources = {r'/api/*': {'origins': '*'}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET')
    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def get_categories():
    #get data
    categories = Category.query.order_by(Category.id).all()

    if len(categories) == 0:
      abort(404)
    formatted_cats = {cat.id: cat.type for cat in categories}
    
    return jsonify({
      'success': True,
      'categories': formatted_cats,
      'total_categories': len(categories)
    })


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions', methods=['GET'])
  def get_questions():
    # get questions from database
    questions = Question.query.order_by(Question.id).all()

    # select the questions for the current page
    current_questions = paginate_questions(request, questions)
    # deal with no questions case
    if len(current_questions) == 0:
      abort(404)

    #select the categories to be returned 
    categories = Category.query.order_by(Category.id).all()
    formatted_cats = {cat.id: cat.type for cat in categories}

    # return questions
    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(questions),
      'categories': formatted_cats
    })


  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods = ['DELETE'])
  def delete_question(question_id):
    # see if question exists in database
    question = Question.query.filter(Question.id == question_id).one_or_none()
    
    
    if question:
      # Case when question is returned
      try:
      # Delete the question and return the new list of questions
        question.delete()
        questions = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, questions)

        # return success message with deleted id
        return jsonify({
          'success': True,
          'deleted': question_id,
          'questions': current_questions,
          'total_questions': len(questions)
        })
      except:
        # Handle error in processing deletion
        abort(422)
    else:
      # Case when no question matches the id
      abort(404)

      
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods = ['POST'])
  def create_question():
    body = request.get_json()
    # Error handling with no data
    if body == {}:
      abort(400)
    
    #Get details of new question from the request
    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_category = body.get('category', None)
    new_difficulty = body.get('difficulty', None)

    try:
      # Create a new question from the data and insert into the db
      question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
      question.insert()

      questions = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, questions)

      # return success message with created question id
      return jsonify({
        'success': True,
        'created': question.id,
        'questions': current_questions,
        'total_questions': len(questions)
      })
    
    # Error handling
    except:
      abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    # Get the search term from the request
    body = request.get_json()
    search_term = body.get('searchTerm', '')

    try:
      # Get all questions which match the search term
      questions = Question.query.order_by(Question.id).filter(Question.question.ilike('%' + search_term + '%')).all()
      # Paginate results
      current_questions = paginate_questions(request, questions)

      # return success message with matching questions
      return jsonify({
        'success': True,
        'questions': current_questions,
        'total_questions': len(questions)
      })

    except:
      abort(422)

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def retrieve_cat_questions(category_id):


    # Get questions with category category_id
    questions = Question.query.order_by(Question.id).filter(Question.category == category_id).all()
    # Paginate results
    current_questions = paginate_questions(request, questions)
    if len(current_questions) == 0:
      abort(404)

    # Get category name
    category = Category.query.filter(Category.id == category_id).one_or_none().type
    # return success message with matching questions
    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(questions),
      'current_category': category
    })


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods = ['POST'])
  def play_quiz():
    # Get the previous questions and category
    body = request.get_json()
    try:
      previous_questions = body.get('previous_questions', None)
      quiz_category = body.get('quiz_category', None)['id']
    except:
      abort(400)

    # Error handling for wrongly formatted body
    # if (body == {}) or (previous_questions is None) or (quiz_category is None):
    #   abort(400)

    # Case when 'All' selected for category
    if quiz_category == 0:
      categories = Category.query.all()
      quiz_category = random.randint(1, len(categories))

    try:
      # Get a random question satisfying the request criteria
      # Since previous_questions is just a list of ids, we can simply filter on these ids
      questions = Question.query.order_by(Question.id).filter(Question.category == quiz_category).filter(~Question.id.in_(previous_questions)).all()
      # Handle case when all questions have been asked
      # Frontend can deal with this, just need to return a success message
      if len(questions) == 0:
        return jsonify({
          'success': True
        })
      # Select a random question
      random_id = random.randint(0, len(questions) - 1)
      random_question = questions[random_id]

      return jsonify({
        'success': True,
        'question': random_question.format()
      })
    
    except:
      abort(422)



  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success': False,
      'error': 400,
      'message': 'bad request'
    }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'resource not found'
    }), 404

  @app.errorhandler(405)
  def not_allowed(error):
    return jsonify({
      'success': False,
      'error': 405,
      'message': 'method not allowed'
    }), 405

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'unprocessable entity'
    }), 422

  @app.errorhandler(500)
  def internal_error(error):
    return jsonify({
      'success': False,
      'error': 500,
      'message': 'internal server error'
    }), 500

  return app

    