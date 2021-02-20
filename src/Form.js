import React, { useState, useEffect } from "react";
import axios from "axios";
import "./styles/Form.css";
import "./styles/Styles.css";
import { select } from "async";

function Form(props) {
  // Select element values
  const [selectedBrand, setSelectedBrand] = useState("");
  const [selectedSize, setSelectedSize] = useState("");
  const [selectedMonth, setSelectedMonth] = useState([]);

  // Values from API
  const [brands, setBrands] = useState([]);
  const [sizes, setSizes] = useState([]);
  const [months, setMonths] = useState([]);

  useEffect(() => {
    fetch("http://143.110.239.119/data")
      .then((res) => res.json())
      .then((data) => {
        setBrands(data.brands);
        setSizes(data.sizes);
        setMonths(data.months);
      });
    setSelectedBrand("BUD CHELADA");
    setSelectedSize("15/25");
    setSelectedMonth([0, "January"]);
  }, []);

  function populateBrands(brands) {
    if (brands.length === 0) {
      return (
        <option key={0} value={"none"}>
          Loading brands...
        </option>
      );
    } else {
      return brands.map((brand, index) => (
        <option key={index} value={brand[0]}>
          {brand[1]}
        </option>
      ));
    }
  }

  function populateSizes(sizes, brand) {
    if (sizes.length === 0) {
      return (
        <option key={0} value={"none"}>
          Loading sizes...
        </option>
      );
    } else {
      const items = sizes.filter((size) => {
        return size[0] === brand;
      });
      return items.map((item, index) => (
        <option key={index} value={item[1]}>
          {item[1]}
        </option>
      ));
    }
  }

  function populateMonths(months) {
    return months.map((month, index) => (
      <option key={index} value={month[1]}>
        {month[1]}
      </option>
    ));
  }

  function handleChangeBrand(e) {
    setSelectedBrand(e.target.value);
  }

  function handleChangeSize(e) {
    setSelectedSize(e.target.value);
  }

  function handleChangeMonth(e) {
    let month = months.filter((item) => {
      return item[1] === e.target.value;
    });
    setSelectedMonth(month[0]);
    console.log(selectedMonth[0]);
  }

  function handleSubmit(e) {
    e.preventDefault();

    const request_data = {
      brand: selectedBrand,
      size: selectedSize,
    };

    props.cbStatus("Fetching prediction...");
    if (props.prediction !== null) {
      if (Object.keys(props.prediction).length !== 0) {
        props.cbPrediction({});
      }
    }

    axios.post("/query", request_data).then((response) => {
      props.cbPrediction(filterData(response.data));
    });
  }

  function filterData(predData) {
    const monthPredictions = predData.predict.filter((item) => {
      let date = new Date(item.invoice_date);
      return date.getMonth() === selectedMonth[0];
    });
    console.log(monthPredictions);
    const data = {
      monthlyData: monthPredictions,
      brand: selectedBrand,
      size: selectedSize,
      month: selectedMonth,
    };
    return data;
  }

  return (
    <div className="Form flex-item-left flex-item">
      <head>
        <meta charset="UTF-8" />
        <title>Beer Predictor</title>
      </head>
      <body>
        <form onSubmit={handleSubmit} action="/query" method="PUT">
          <div className="form-field">
            <label className="form-label" for="brand">
              Brand{" "}
            </label>
            <select
              className="form-input"
              name="brand"
              onChange={handleChangeBrand}
            >
              {populateBrands(brands)}
            </select>
          </div>
          <div className="form-field">
            <label className="form-label" for="size">
              Package Size{" "}
            </label>
            <select
              className="form-input"
              name="size"
              onChange={handleChangeSize}
            >
              {populateSizes(sizes, selectedBrand)}
            </select>
          </div>
          <div className="form-field">
            <label className="form-label" for="months">
              Month{" "}
            </label>
            <select
              className="form-input"
              name="months"
              onChange={handleChangeMonth}
            >
              {populateMonths(months)}
            </select>
          </div>
          <div className="form-field">
            <input
              className="form-submit"
              type="submit"
              value="Predict"
            ></input>
          </div>
        </form>
      </body>
    </div>
  );
}

export default Form;
