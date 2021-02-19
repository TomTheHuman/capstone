import React from "react";
import * as d3 from "d3";
import "./styles/Graph.css";
import "./styles/Styles.css";

function Graph(props) {
  function populateTitle(prediction) {
    if (Object.keys(prediction).length !== 0) {
      const title = "2021 Predicted Cases Sold in " + prediction.month[1];
      return <p className="title-text">{title}</p>;
    }
  }

  function populateGraph(prediction, status) {
    if (Object.keys(prediction).length === 0) {
      d3.selectAll("svg").remove();
      return <p className="no-data">{status}</p>;
    } else {
      // Display graph
      // Configure variables
      var graphData = formatData(prediction.monthlyData);
      console.log(graphData);

      const width = 450;
      const height = 320;
      const margin = { top: 10, right: 0, bottom: 25, left: 60 };
      const graphWidth = width - margin.left - margin.right;
      const graphHeight = height - margin.top - margin.bottom;

      // Configure graph elements
      const svg = d3
        .select(".graph")
        .append("svg")
        .attr("width", width)
        .attr("height", height);
      const graph = svg
        .append("g")
        .attr("width", graphWidth)
        .attr("height", graphHeight)
        .attr("transform", `translate(${margin.left}, ${margin.top})`);
      const gXAxis = graph
        .append("g")
        .attr("transform", `translate(0, ${graphHeight})`);
      const gYAxis = graph.append("g");

      // Graph data
      const y = d3
        .scaleLinear()
        .domain([0, d3.max(graphData, (d) => d.Cases)])
        .range([graphHeight, 0]);
      const x = d3
        .scaleBand()
        .domain(graphData.map((item) => item.Year))
        .range([0, 400])
        .paddingInner(0.2)
        .paddingOuter(0.2);
      const rects = graph.selectAll("rect").data(graphData);
      rects
        .attr("width", x.bandwidth)
        .attr("class", "bar-rect")
        .attr("height", (d) => graphHeight - y(d.Cases))
        .attr("x", (d) => x(d.Year))
        .attr("y", (d) => y(d.Cases));
      rects
        .enter()
        .append("rect")
        .attr("class", "bar-rect")
        .attr("width", x.bandwidth)
        .attr("height", (d) => graphHeight - y(d.Cases))
        .attr("x", (d) => x(d.Year))
        .attr("y", (d) => y(d.Cases));
      const xAxis = d3.axisBottom(x);
      const yAxis = d3
        .axisLeft(y)
        .ticks(8)
        .tickFormat((d) => `${d}`);
      gXAxis.call(xAxis);
      gYAxis.call(yAxis);
      gXAxis.selectAll("text").style("font-size", 14);
      gYAxis.selectAll("text").style("font-size", 14);
    }
  }

  function formatData(data) {
    const graphData = [];
    for (var i in data) {
      var item = {
        Year: new Date(data[i].invoice_date).getFullYear(),
        Cases:
          data[i].pred_value === null ? data[i].cases_sold : data[i].pred_value,
      };
      graphData.push(item);
    }
    return graphData;
  }

  function populateText(prediction) {
    if (Object.keys(prediction).length !== 0) {
      return (
        <div className="predicted-cases">
          <p>Predicted Cases to Be Sold in {prediction.month[1]}, 2021</p>
          <h2>{prediction.monthlyData[5].pred_value}</h2>
        </div>
      );
    }
  }

  return (
    <div className="Graph flex-item-right flex-item">
      <div className="graph-container">
        <div className="graph-title">
          {populateTitle(props.prediction)}
          <p>{props.prediction.brand}</p>
        </div>
        <div className="graph">
          {populateGraph(props.prediction, props.status)}
        </div>
      </div>

      <div className="graph-text">{populateText(props.prediction)}</div>
    </div>
  );
}

export default Graph;
