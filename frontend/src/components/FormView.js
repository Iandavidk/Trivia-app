import React, { Component } from 'react';
import $ from 'jquery';

import '../stylesheets/FormView.css';
import { HOST } from '../App';

class FormView extends Component {
  constructor(props) {
    super(props);

    this.state = {
      question: '',
      answer: '',
      difficulty: 1,
      category: 1,
      categories: []
    };
  }

  componentDidMount() {
    $.ajax({
      url: `${HOST}/categories`,
      type: 'GET',
      success: result => {
        this.setState({ categories: result.categories });
        return;
      },
      error: error => {
        alert('Unable to load categories. Please try your request again');
        return;
      }
    });
  }

  submitQuestion = e => {
    e.preventDefault();
    if (this.state.answer && this.state.question) {
      $.ajax({
        url: `${HOST}/questions`,
        type: 'POST',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify({
          question: this.state.question,
          answer: this.state.answer,
          difficulty: this.state.difficulty,
          category: this.state.category
        }),
        crossDomain: true,
        success: result => {
          document.getElementById('add-question-form').reset();
          alert("You've successfully added a new question!");
          return;
        },
        error: error => {
          alert('Unable to add question. Please try your request again');
          return;
        }
      });
    } else
      alert(
        'Some information is missing, please complete the form before submitting'
      );
  };

  handleChange = e => this.setState({ [e.target.name]: e.target.value });

  render() {
    return (
      <form onSubmit={this.submitQuestion} id="add-question-form">
        <fieldset className="form-view">
          <legend>
            <h2>Add a New Trivia Question</h2>
          </legend>
          <input
            placeholder="Enter a question"
            type="text"
            name="question"
            onChange={this.handleChange}
          />
          <input
            placeholder="Enter an answer"
            type="text"
            name="answer"
            onChange={this.handleChange}
          />

          <div className="difficulty-list">
            <label>Difficulty:</label>
            <select name="difficulty" onChange={this.handleChange}>
              <option value="1">1</option>
              <option value="2">2</option>
              <option value="3">3</option>
              <option value="4">4</option>
              <option value="5">5</option>
            </select>
          </div>

          <div className="categories-list">
            <label>Category:</label>
            <select name="category" onChange={this.handleChange}>
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

          <button type="submit">Add Question</button>
        </fieldset>
      </form>
    );
  }
}

export default FormView;
