// Let the fun begin

  let svgWidth = 960;
  let svgHeight = 500;
  
  let margin = {
  top: 20,
  right: 40,
  bottom: 80,
  left:100
  };
  
  let width = svgWidth - margin.left - margin.right;
  let height = svgHeight - margin.top - margin.bottom;
  
  //SVG with scatter id
  let svg = d3.select("#scatter")
      .append("svg")
      .attr("width", svgWidth)
      .attr("height", svgHeight);
  
  let chart = svg.append("g")
      .attr("transform", `translate(${margin.left}, ${margin.top})`);
  
  //import CSV file
  d3.csv("assets/data/data.csv")
      .then(function(riskData){
  
  //Get data and make integers
      riskData.forEach(function(data) {
          data.age = +data.age;
          data.smokes = +data.smokes;
          data.healthcare = +data.healthcare;
          data.poverty = +data.poverty;
          data.abbr = data.abbr;
          data.income = +data.income;
      });
  //Create scales
      let xLinearScale = d3.scaleLinear()
          .domain([8.5, d3.max(riskData, d => d.poverty)])
          .range([0, width]);
  
      let yLinearScale = d3.scaleLinear()
          .domain([3.5, d3.max(riskData, d => d.healthcare)])
          .range([height, 0]);
  
  //Create X and Y axis
      let xAxis = d3.axisBottom(xLinearScale);
      let yAxis = d3.axisLeft(yLinearScale);
  
  //Append to chart
      chart.append("g")
      .attr("transform", `translate(0, ${height})`)
      .call(xAxis);
  
      chart.append("g")
      .call(yAxis);
      
  //Circles
      let circles = chart.selectAll("circle")
          .data(riskData)
          .enter()
          .append("circle")
          .attr("cx", d => xLinearScale(d.poverty))
          .attr("cy", d => yLinearScale(d.healthcare))
          .attr("r", 10)
          .attr("fill", "lightblue")
          .attr("opacity", ".5")
          .attr("stroke-width", "1")
          .attr("stroke", "black");
  
          chart.select("g")
          .selectAll("circle")
          .data(riskData)
          .enter()
          .append("text")
          .text(d => d.abbr)
          .attr("x", d => xLinearScale(d.poverty))
          .attr("y", d => yLinearScale(d.healthcare))
          .attr("dy",-395)
          .attr("text-anchor", "middle")
          .attr("font-size", "12px")
          .attr("fill", "black");
       
          console.log(riskData);
        
        //   Labels for graph
      chart.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - 50)
        .attr("x", 0 -250)
        .attr("dy", "1em")
        .attr("class", "axisText")
        .text("Lacks Healthcare (%)");
  
      chart.append("text")
        .attr("transform", `translate(${width / 2.5}, ${height + margin.top + 25})`)
        .attr("class", "axisText")
        .text("In Poverty (%)");
  });
  
  