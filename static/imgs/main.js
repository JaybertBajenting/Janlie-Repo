$('.studentlife-btn').click(function() {
    $('.side-nav ul .studentlife').toggleClass("show"); 
    $('.side-nav ul .first').toggleClass("rotate");
});
$('.scholar-btn').click(function() {
    $('.side-nav ul .scholar-show').toggleClass("show2"); 
    $('.side-nav ul .second').toggleClass("rotate");
});
$('.jobplace-btn').click(function() {
    $('.side-nav ul .jobplace-show').toggleClass("show3"); 
    $('.side-nav ul .third').toggleClass("rotate");
});
$('.student_disc-btn').click(function() {
    $('.side-nav ul .student_disc-show').toggleClass("show4"); 
    $('.side-nav ul .fourth').toggleClass("rotate");
});
$('.guide-btn').click(function() {
    $('.side-nav ul .guide-show').toggleClass("show5"); 
    $('.side-nav ul .fifth').toggleClass("rotate");
});
$('.alumni-btn').click(function() {
    $('.side-nav ul .alumni-show').toggleClass("show6"); 
    $('.side-nav ul .sixth').toggleClass("rotate");
});
$('.community-btn').click(function() {
    $('.side-nav ul .community-show').toggleClass("show7"); 
    $('.side-nav ul .seventh').toggleClass("rotate");
});
$('.student_org-btn').click(function() {
    $('.side-nav ul .student_org-show').toggleClass("show8"); 
    $('.side-nav ul .eight').toggleClass("rotate");
});
$('.medical-btn').click(function() {
    $('.side-nav ul .medical-show').toggleClass("show9"); 
    $('.side-nav ul .ninth').toggleClass("rotate");
});

//PARA SA AMOA
function printPage() {
    // Hide all elements except the form
    $('body > *:not(.case-container)').hide();
    // Print the page
    window.print();
    // Show all elements after printing
    $('body > *').show();
}

function changeText() {
    var stdId = document.getElementById('std-id').value.trim();
    var stdReason = document.getElementById('std-reason').value.trim();
    var button = document.querySelector('.myButton1');
    var message = document.getElementById('message');
    if (stdId === '' || stdReason === '') {
        message.innerText = 'Please enter both Student ID and Reason.';
        button.innerText = 'Request Good Moral'; // Reset button text
        button.classList.remove('clicked'); // Reset button style
    } else {
        message.innerText = 'Wait at-least 24 hours'; // Clear any previous message
        button.innerText = 'Pending Request...'; 
        button.classList.add('clicked');
    }

    //button.innerText = 'Pending Request...'; 
    //button.classList.add('clicked');
}