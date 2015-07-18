// This example displays an address form, using the autocomplete feature
// of the Google Places API to help users fill in the information.

var placeSearch, autocomplete;

function initialize() {
  // Create the autocomplete object, restricting the search
  // to geographical location types.
  console.log("hereeeee1")
  autocomplete = new google.maps.places.Autocomplete((document.getElementById('autocomplete')));
  console.log(autocomplete);
}

