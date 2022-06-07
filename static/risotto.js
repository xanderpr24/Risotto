$(document).ready(function() {
    let entries = ['path', 'title', 'x-label'];
    let filled = [];
    for (entry in entries) {filled.push(0);}

    // when the value of an input field is changed
    $('input').on('input change', function() {
        // if new value is not empty
        if($(this).val() != '')
        {
          // set corresponding index of input field list to 1 (true)
          filled[entries.indexOf($(this).attr('id'))] = 1;
        } else {
          // set corresponding index of input field list to 0 (false)
          filled[entries.indexOf($(this).attr('id'))] = 0;
        }

        // find the number of filled input fields
        sum = 0;
        for (let i = 0; i < filled.length; i++)
        {
          sum += filled[i];
        }

        /// if 3 fields are filled, enable button
        if (sum == 3)
        {
          $('#submit').prop('disabled', false);
        } else {
          $('#submit').prop('disabled', true);
        }
    });

});
