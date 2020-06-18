// from data.js
var tableData = data;
console.log(tableData);

// Get reference to the table body
var tbody = d3.select("tbody");

// UFO values for each column
tableData.forEach(function(ufoSighting) {
    console.log(ufoSighting);

    // Append table row for UFO Sighting
    var row = tbody.append("tr");

    Object.entries(ufoSighting).forEach(function([key, value]) {
      console.log(key, value);

      // Append cell to the row for each value
      var cell = row.append("td");
      cell.text(value);
    });
  });


// Select the button
var button = d3.select("#filter-btn");
button.on("click", function() {
    tbody.html("");

    // Select the input date 
    var inputElement = d3.select("#datetime");

    // Get the values of input
    var inputValue = inputElement.property("value");

    console.log(inputValue);

    // Filter Data with datetime equal to input value
    var filteredData = tableData.filter(sighting => sighting.datetime === inputValue);
   
    console.log(filteredData);

    filteredData.forEach(function(selections) {
    console.log(selections);

    // Append table row for UFO Sighting
    var row = tbody.append("tr");

    Object.entries(selections).forEach(function([key, value]) {
        console.log(key, value);

        // Append cell to the row 
        var cell = row.append("td");
        cell.text(value);
    });
});
});