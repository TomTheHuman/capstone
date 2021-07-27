import React from "react";
import { Route, Routes } from "react-router-dom";
import Form from "./Form";
import Nav from "./Nav";
import Graph from "./Graph";
import Descriptive from "./Descriptive";
import "./styles/App.css";
import "./styles/Styles.css";

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      prediction: {},
      status: "Select your options and click 'Predict' to see data.",
      isFormView: true,
    };

    this.cbPrediction = this.cbPrediction.bind(this);
    this.cbStatus = this.cbStatus.bind(this);
    this.cbFormView = this.cbFormView.bind(this);
  }

  // cb = callback
  // Get prediction data
  cbPrediction = (predData) => {
    this.setState({ prediction: predData });
  };

  // Update status
  cbStatus = (statusData) => {
    this.setState({ status: statusData });
  };

  // Change whether form/graph is in view
  cbFormView = (formView) => {
    this.setState({ isFormView: formView });
  };

  render() {
    return (
      <div className="App">
        <Nav />
        <Routes>
          <Route path="/">
            <div className="flex-container">
              <div className="content-container">
                <h1 className="content-header">🍺 Beer Predictor</h1>
                <p className="content-description">Select a brand, package size, and month to predict inventory data.</p>
              {(this.state.isFormView ? <Form
                prediction={this.state.prediction}
                cbStatus={this.cbStatus}
                cbPrediction={this.cbPrediction}
                cbFormView={this.cbFormView}
              /> :
              <Graph
                status={this.state.status}
                prediction={this.state.prediction}
                cbFormView={this.cbFormView}
              />)}
              </div>
            </div>
          </Route>
          <Route path="/info">
            <div className="flex-container">
              <div className="content-container">
                <Descriptive />
              </div>
            </div>
          </Route>
        </Routes>
      </div>
    );
  }
}

export default App;
