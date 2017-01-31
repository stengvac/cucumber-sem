function hideRuns(elem) {

    var passed = $('div.bs-callout-success');
    // passed.each(function () {
    //    alert(this.text());
    // });
    // alert(passed);
    if(elem.checked) {
        passed.addClass('hide');
    } else {
        passed.removeClass('hide');
    }
}
