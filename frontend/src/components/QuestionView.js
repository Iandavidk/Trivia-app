import React, { Component } from 'react';
import '../stylesheets/QuestionView.css';

import Question from './Question';
import Search from './Search';

import $ from 'jquery';
import { HOST } from '../App';
import Modal from './Modal';

class QuestionView extends Component {
  constructor() {
    super();

    this.questionsRef = React.createRef();

    this.state = {
      questions: [],
      page: 1,
      totalQuestions: 0,
      categories: [],
      currentCategory: '',
      currentQuestion: null
    };
  }

  componentDidMount() {
    this.getQuestions();
  }

  componentDidUpdate() {
    const cards = document.querySelectorAll('.question-card');
    cards.forEach((card, index) => {
      window.setTimeout(() => {
        card.classList.add('show');
      }, 100 * index);
    });
  }

  getQuestions = () => {
    $.ajax({
      url: `${HOST}/questions?page=${this.state.page}`,
      type: 'GET',
      success: result => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          categories: result.categories,
          currentCategory: result.current_category
        });
        return;
      },
      error: error => {
        alert('Unable to load questions. Please try your request again');
        return;
      }
    });
  };

  selectPage(num) {
    this.setState({ page: num }, () => this.getQuestions());
  }

  createPagination() {
    let pageNumbers = [];
    let maxPage = Math.ceil(this.state.totalQuestions / 10);
    for (let i = 1; i <= maxPage; i++) {
      pageNumbers.push(
        <span
          key={i}
          className={`page-num ${i === this.state.page ? 'active' : ''}`}
          onClick={() => {
            this.questionsRef.current.scrollIntoView({ behavior: 'smooth' });
            this.selectPage(i);
          }}
        >
          {i}
        </span>
      );
    }
    return pageNumbers;
  }

  getByCategory = id => {
    !id
      ? this.getQuestions()
      : $.ajax({
          url: `${HOST}/categories/${id}/questions`,
          type: 'GET',
          success: result => {
            this.setState({
              questions: result.questions,
              totalQuestions: result.total_results,
              currentCategory: result.current_category
            });
            return;
          },
          error: error => {
            alert('Unable to load questions. Please try your request again');
            return;
          }
        });
  };

  submitSearch = searchTerm => {
    $.ajax({
      url: `${HOST}/questions/search`,
      type: 'POST',
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({ search_term: searchTerm }),
      crossDomain: true,
      success: result => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_results
        });
        return;
      },
      error: error => {
        if (error.status === 404) {
          this.setState({
            questions: [],
            totalQuestions: 0,
            currentCategory: ''
          });
        }
      }
    });
  };

  onQuestionChange = id => this.setState({ currentQuestion: id });

  questionAction = id => action => {
    if (action === 'DELETE')
      $.ajax({
        url: `${HOST}/questions/${id}`,
        type: 'DELETE',
        success: () => this.getQuestions(),
        error: () =>
          alert('Unable to load questions. Please try your request again.')
      });
  };

  handleCategoryChange = e => {
    e.preventDefault();
    this.setState({ currentCategory: e.target.value }, () => {
      this.getByCategory(this.state.currentCategory);
    });
  };

  render() {
    return (
      <div className="questions-view container">
        <section className="view-header">
          <div className="categories-list">
            <label htmlFor="categories" onClick={this.getQuestions}>
              Categories
            </label>
            <select
              id="categories"
              onChange={this.handleCategoryChange}
              value={this.state.currentCategory || 'all'}
            >
              <option value="">All</option>
              {this.state.categories.map(category => (
                <option
                  key={Object.keys(category)}
                  value={Object.keys(category)}
                >
                  {category[Object.keys(category)]}
                </option>
              ))}
            </select>
          </div>

          <Search submitSearch={this.submitSearch} />
        </section>

        <div className="questions-container" ref={this.questionsRef}>
          <h2>Questions</h2>
          {this.state.totalQuestions ? (
            <div className="questions-list">
              {this.state.questions.map(q => (
                <Question
                  key={q.id}
                  id={q.id}
                  question={q.question}
                  answer={q.answer}
                  category={this.state.categories[q.category - 1][q.category]}
                  difficulty={q.difficulty}
                  onQuestionChange={this.onQuestionChange}
                />
              ))}

              <Modal
                questionAction={this.questionAction(this.state.currentQuestion)}
              />
            </div>
          ) : (
            <h3>No Questions were found!</h3>
          )}
          <div className="pagination-menu">{this.createPagination()}</div>
        </div>
      </div>
    );
  }
}

export default QuestionView;