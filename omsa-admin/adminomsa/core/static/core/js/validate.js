$(document).ready(function () {
  
    //validation for First Name
    $('#identificador').on('input', function () {
       var firstName = $(this).val();
       var validName = /^[a-zA-Z ]*$/;
       if (firstName.length == 0) {
          $('.first-name-msg').addClass('invalid-msg').text("First Name is required");
          $(this).addClass('invalid-input').removeClass('valid-input');
          
       }
       else if (!validName.test(firstName)) {
          $('.first-name-msg').addClass('invalid-msg').text('only characters & Whitespace are allowed');
          $(this).addClass('invalid-input').removeClass('valid-input');
          
       }
       else {
          $('.first-name-msg').empty();
          $(this).addClass('valid-input').removeClass('invalid-input');
       }
      });

    // validation to submit the form
    $('input').on('input',function(e){
       if($('#myForm').find('.valid-input').length==5){
           $('#submit-btn').removeClass('allowed-submit');
           $('#submit-btn').removeAttr('disabled');
       }
      else{
           e.preventDefault();
           $('#submit-btn').attr('disabled','disabled')
           
          }
    });
    });