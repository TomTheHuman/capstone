import React from "react";
import "./styles/Descriptive.css";
import Plotly from "plotly.js-basic-dist";
import createPlotlyComponent from "react-plotly.js/factory";
const Plot = createPlotlyComponent(Plotly);

export default class Descriptive extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      description: "Historical Market Demand by Brand",
      currentGraph: "pie"
    };

    this.handleChangeGraph = this.handleChangeGraph.bind(this)
  }

  handleChangeGraph(e) {
    let description = ""

    if (e.target.value === "pie") {
      description = "Historical Market Demand by Brand"
    } else {
      description = "Relation Between Sales and Month By Brand"
    }

    this.setState({
      description: description,
      currentGraph: e.target.value,
    })
  }

  render() {
    return (
      <div className="Descriptive">
        <h1 className="content-header">📊 Graphs</h1>
        <p className="content-description">{this.state.description}</p>
        <select
            className="graphs-select"
            name="graphs"
            onChange={this.handleChangeGraph}
          >
            <option key="1" value="pie">Pie Chart</option>
            <option key="2" value="bar">Bar Graph</option>
          </select>
        <div className="chart">
          {this.state.currentGraph === "pie" ? <PieChart /> : <ScatterPlot />}
        </div>
      </div>
    );
  }
}

class PieChart extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      dataset: {},
      data: [
        {
          values: [25, 30, 45],
          labels: ["Loading...", "Loading...", "Loading..."],
          type: "pie",
        },
      ],
      layout: {
        height: 420,
        width: 600,
      },
    };
    this.sortData = this.sortData.bind(this);
  }

  componentDidMount() {
    fetch("/api/brand-totals")
      .then((res) => res.json())
      .then((data) => {
        this.setState({ dataset: data.data }, () => {
          this.sortData();
        });
      });
  }

  sortData() {
    const brands = this.state.dataset.map((item) => {
      return item.brand;
    });

    const totals = this.state.dataset.map((item) => {
      return item.total_cases;
    });

    console.log(brands);
    console.log(totals);

    this.setState({
      data: [
        {
          values: totals,
          labels: brands,
          type: "pie",
        },
      ],
    });
  }

  render() {
    return (
      <div style={{ width: "100%", height: "100%" }}>
        <Plot
          data={this.state.data}
          layout={this.state.layout}
          onInitialized={(figure) => this.setState(figure)}
          onUpdate={(figure) => this.setState(figure)}
        />
      </div>
    );
  }
}

class ScatterPlot extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      dataset: {},
      brands: [
        "BUD CHELADA",
        "BUD LIGHT",
        "BUD LIGHT LIME",
        "BUD LIGHT PLATINUM",
        "BUD LIGHT RITA",
        "BUDWEISER",
      ],
      data: [],
      layout: {
        xaxis: {
          tickformat: "%b",
        },
        yaxis: {
          range: [],
        },
        height: 420,
        width: 600,
      },
    };
    this.sortData = this.sortData.bind(this);
  }

  componentDidMount() {
    fetch("/api/month-totals")
      .then((res) => res.json())
      .then((data) => {
        this.setState({ dataset: data.data }, () => {
          this.sortData();
        });
      });
  }

  sortData() {
    const data = this.state.brands.map((brand) => {
      var dates = [];
      for (var i in this.state.dataset) {
        if (this.state.dataset[i].brand === brand) {
          dates.push(new Date(this.state.dataset[i].invoice_date));
        }
      }
      var cases_sold = [];
      for (i in this.state.dataset) {
        if (this.state.dataset[i].brand === brand) {
          cases_sold.push(this.state.dataset[i].cases_sold);
        }
      }

      const object = {
        x: dates,
        y: cases_sold,
        mode: "markers",
        type: "scatter",
        name: brand,
      };
      return object;
    });

    this.setState({ data: data }, () => {
      console.log(this.state);
    });
  }

  render() {
    return (
      <div style={{ width: "100%", height: "100%" }}>
        <Plot
          data={this.state.data}
          layout={this.state.layout}
          onInitialized={(figure) => this.setState(figure)}
          onUpdate={(figure) => this.setState(figure)}
        />
      </div>
    );
  }
}
