import React, { Component } from 'react';
import $ from 'jquery';

import '../stylesheets/QuizView.css';
import { icons } from './Question';
import { HOST } from '../App';

const questionsPerPlay = 5;

class QuizView extends Component {
  constructor(props) {
    super(props);

    this.state = {
      quizCategory: null,
      previousQuestions: [],
      showAnswer: false,
      categories: {},
      numCorrect: 0,
      currentQuestion: {},
      guess: '',
      forceEnd: false,
      totalQuestions: null
    };
  }

  componentDidMount() {
    $.ajax({
      url: `${HOST}/categories`,
      type: 'GET',
      success: ({ categories }) =>
        categories.map(category =>
          this.setState(prevState => ({
            categories: {
              ...prevState.categories,
              [Object.keys(category)]: {
                id: [Object.keys(category)][0][0],
                name: category[[Object.keys(category)][0][0]]
              }
            }
          }))
        ),
      error: err =>
        alert('Unable to load categories. Please try your request again')
    });
  }

  selectCategory = ({ type, id = 0 }) => {
    this.setState({ quizCategory: { type, id } }, this.getNextQuestion);
    this.getTotalQuestions(id);
  };

  handleChange = e => this.setState({ [e.target.name]: e.target.value });

  getNextQuestion = () => {
    const previousQuestions = [...this.state.previousQuestions];
    if (this.state.currentQuestion.id) {
      previousQuestions.push(this.state.currentQuestion.id);
    }

    $.ajax({
      url: `${HOST}/quiz`,
      type: 'POST',
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        previous_questions: previousQuestions,
        category: Number(this.state.quizCategory.id)
      }),
      crossDomain: true,
      success: result => {
        this.setState({
          showAnswer: false,
          previousQuestions: previousQuestions,
          currentQuestion: result.question,
          guess: '',
          forceEnd: result.question ? false : true
        });
        return;
      },
      error: error => {
        alert('Unable to load question. Please try your request again');
        alert(this.state.quizCategory.id);
        return;
      }
    });
  };

  submitGuess = e => {
    e.preventDefault();
    let evaluate = this.evaluateAnswer();
    this.setState({
      numCorrect: !evaluate ? this.state.numCorrect : this.state.numCorrect + 1,
      showAnswer: true
    });
  };

  restartGame = () => {
    this.setState({
      quizCategory: null,
      previousQuestions: [],
      showAnswer: false,
      numCorrect: 0,
      currentQuestion: {},
      guess: '',
      forceEnd: false
    });
  };

  getTotalQuestions = id =>
    id === 0
      ? $.ajax({
          url: `${HOST}/questions`,
          type: 'GET',
          dataType: 'json',
          contentType: 'application/json',
          crossDomain: true,
          success: ({ total_questions: totalQuestions }) =>
            this.setState({ totalQuestions }),
          error: error => console.log(error)
        })
      : $.ajax({
          url: `${HOST}/categories/${id}/questions`,
          type: 'GET',
          dataType: 'json',
          contentType: 'application/json',
          crossDomain: true,
          success: ({ total_results: totalQuestions }) =>
            this.setState({ totalQuestions }),
          error: error => console.log(error)
        });

  renderPrePlay() {
    return (
      <div className="quiz-play-holder">
        <div className="choose-header">Choose Category</div>
        <div className="category-holder">
          <div className="play-category" onClick={this.selectCategory}>
            ALL
          </div>
          {Object.keys(this.state.categories).map(key => (
            <div
              className="play-category"
              key={key}
              value={key}
              onClick={() =>
                this.selectCategory({
                  type: this.state.categories[key].name,
                  id: this.state.categories[key].id
                })
              }
            >
              {this.state.categories[key].name}
            </div>
          ))}
        </div>
      </div>
    );
  }

  RenderFinalScore = () => (
    <div className="quiz-play-holder final-score-view">
      Your Final Score is
      <span className="final-score">
        {this.state.numCorrect} / {this.state.previousQuestions.length}
      </span>
      <div className="play-again button" onClick={this.restartGame}>
        Play Again?
      </div>
    </div>
  );

  evaluateAnswer = () => {
    const formatGuess = this.state.guess
      .replace(/[.,/#!$%^&*;:{}=\-_`~()]/g, '')
      .toLowerCase();
    const answerArray = this.state.currentQuestion.answer.toLowerCase();
    return answerArray.includes(formatGuess);
  };

  RenderCorrectAnswer = ({ quizOver }) => (
    <>
      <div className="correct-answer">{this.state.currentQuestion.answer}</div>
      <input
        className="next-question button"
        type="button"
        onClick={this.getNextQuestion}
        value={`${quizOver ? 'End Quiz' : 'Next Question'}`}
      />
    </>
  );

  getCurrentCategoryName = () =>
    Object.keys(this.state.categories)
      .map(key => this.state.categories[key])
      .filter(
        category => Number(category.id) === this.state.currentQuestion.category
      )[0]?.name;

  renderPlay() {
    const answerView = this.state.showAnswer;
    const isCorrect = answerView ? this.evaluateAnswer() : null;
    const pastQuestions = this.state.previousQuestions.length + 1;
    const remaining =
      this.state.totalQuestions > questionsPerPlay
        ? questionsPerPlay - pastQuestions
        : this.state.totalQuestions - pastQuestions;
    const quizOver =
      pastQuestions - 1 === questionsPerPlay || this.state.forceEnd;

    return quizOver ? (
      <this.RenderFinalScore />
    ) : (
      <div
        className={`quiz-play-holder ${
          answerView ? (isCorrect ? 'correct' : 'incorrect') : ''
        }`}
      >
        <div className="quiz-header">
          <div className="quiz-info remaining">
            <span className="info-title">Remaining</span>
            <span className="info-value">{remaining}</span>
          </div>
          <div className="quiz-info category">
            <span className="info-title">Category</span>
            <span className="info-value">
              <span className="category-name">
                {this.getCurrentCategoryName()}
              </span>
              <i
                className={icons[this.getCurrentCategoryName()?.toLowerCase()]}
              ></i>
            </span>
          </div>
          <div className="quiz-info score">
            <span className="info-title">Score</span>
            <span className="info-value">{this.state.numCorrect}</span>
          </div>
        </div>

        <div className="quiz-question">
          {this.state.currentQuestion.question}
        </div>

        <form onSubmit={this.submitGuess}>
          {answerView ? (
            <this.RenderCorrectAnswer quizOver={remaining === 0} />
          ) : (
            <>
              <input
                className="answer"
                type="text"
                name="guess"
                placeholder="Your answer or guess"
                onChange={this.handleChange}
              />
              <input
                className="submit-guess button"
                type="submit"
                value="Submit Answer"
              />
            </>
          )}
        </form>
      </div>
    );
  }

  render() {
    return this.state.quizCategory ? this.renderPlay() : this.renderPrePlay();
  }
}

export default QuizView;