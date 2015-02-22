function sendData() {
    $('.search_result').css('display', 'none');
    $('#checkButton').css('display', 'none');
    
    $.ajax({
      type: "POST",
      url: "/analysis/analyze/",
      data: {
          'v1': $('#v1').val(),
          'search_word': $('#v2').val(),
          'csrfmiddlewaretoken': $("input[name='csrfmiddlewaretoken']").val() 
      },
      headers: {
        'X-CSRFToken': $("input[name='csrfmiddlewaretoken']").val()
      },
      dataType: "json",
      success: function(msg){
          $('#loadingImg').remove()
          $('#checkButton').css('display', 'block');
          drawResult(msg);
      }
    });
    $loading = $('<img src="/static/img/ajax-loader.gif" id="loadingImg" />');
    $('#searchResults').append($loading);
}

function drawResult(result) {
    var $results, results, html, r;
    $('.search_result').css('display', 'block');
    $results = $('#searchResults');
    results = result.message;   
    $fragment = document.createFragment;

    for (var i = 0, len = results.length; i < len; i++) {
            r = results[i];
            html = '' +
            '   <div class="analyze_result well">' +
            '       <span class="title">Title:' + r.title + '</span>/' +
            '       <span class="link">Link:' + r.link + '</span>/' +
            '       <span class="similarity">類似度:' + r.similarity + '</span><br />' +
            '       <span class="snippet">本文:' + r.snippet + '</span><br />' +
            '   </div>';
           // html = html.replace(/[ !"#$%&'()*+,.\/:;<=>?@\[\\\]^`{|}~]/g, '\\$&'); 
           $results.append($(html));
    }

}
