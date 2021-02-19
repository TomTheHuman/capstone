import React from "react";
import { Route, Routes } from "react-router-dom";
import Form from "./Form";
import Nav from "./Nav";
import Footer from "./Footer";
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
    };

    this.cbPrediction = this.cbPrediction.bind(this);
    this.cbStatus = this.cbStatus.bind(this);
  }

  // Get prediction data
  cbPrediction = (predData) => {
    this.setState({ prediction: predData });
  };

  // Update status
  cbStatus = (statusData) => {
    this.setState({ status: statusData });
  };

  render() {
    return (
      <div className="App">
        <Nav />
        <Routes>
          <Route path="/">
            <div className="flex-container">
              <Form
                prediction={this.state.prediction}
                cbStatus={this.cbStatus}
                cbPrediction={this.cbPrediction}
              />
              <Graph
                status={this.state.status}
                prediction={this.state.prediction}
              />
            </div>
          </Route>
          <Route path="/info" element={<Descriptive />} />
        </Routes>
        <Footer />
      </div>
    );
  }
}

export default App;
