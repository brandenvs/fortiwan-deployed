// $(document).ready(function() {
//             // Show the spinner while waiting for the response
//             $('#spinner').show();
        
//             // Make the AJAX request
//             $.ajax({
//                 url: '{% url "fortiwan_dashboard:home" %}',
//                 type: 'GET',
//                 dataType: 'json',
//                 success: function(data) {
//                     // Hide the spinner and display the content
//                     $('#spinner').hide();
//                     $('#content').html(data.api_data).show();
//                 },
//                 error: function(error) {
//                     console.error('Error:', error);
//                     // Handle errors as needed
//                 }
//             });
//     // Attach a click event to the "Expiry" link
//     $('a.dropdown-item').on('click', function(e) {
//         e.preventDefault();  // Prevent the default behavior of the link


//     });
// });